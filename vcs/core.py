#vcs.core.py
import os,json,hashlib,time
from datetime import datetime

def init_repo():
    #create the .vcs folder and subfoulders
    os.makedirs(".vcs/commits", exist_ok=True)
    os.makedirs(".vcs/branches", exist_ok=True)

    #create the HEAD file
    with open(".vcs/HEAD", "w") as head_file:
        head_file.write("main")

    #create an empty main branch file
    with open(".vcs/branches/main", "w") as branch_file:
        branch_file.write("")

    print("Initalized empty VCS repository in .vcs/")


def add_file(filename):

    #check if repo exist:
    if not os.path.exists(".vcs"):
        print("Error: Repository not initalized. Run 'init' first.")
        return
    
    #check if the file to add actually exists
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' not found.")
        return
    
    #set the path to staging file and lost it(or create it)
    staging_path = ".vcs/staging_area.json"

    #try to load existing staged files
    if os.path.exists(staging_path):
        with open(staging_path, "r") as f:
            staged_files = json.load(f)
    else:
        staged_files = []

    if filename not in staged_files:
        staged_files.append(filename)
        print(f"Added '{filename}' to staging area.")
    else:
        print(f"'{filename}' is already staged.")

    with open(staging_path, "w") as f:
        json.dump(staged_files,f, indent=2)


def commit_changes(message):
    #check if repo exist:
    if not os.path.exists(".vcs"):
        print("Error: Repository not initalized. Run 'init' first.")
        return
    
    #Check if there are any staged files
    staging_path = ".vcs/staging_area.json"
    if not os.path.exists(staging_path):
        print("Nothing to commit. Staging area is empty.")
        return
    
    #Read the staging area file
    with open(staging_path, "r") as f:
        staged_files = json.load(f)
    if not staged_files:
        print("Nothing to commit. Staging area is empty.")
        return
    
    # Read the content of each staged file
    file_snapshots = {}
    for filename in staged_files:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                file_snapshots[filename] = f.read()
        else:
            print(f"Warning: '{filename}' was deleted ot moved, Skipping.")

    # Generate a unique commit ID
    timestamp = time.time()
    commit_id = hashlib.sha1(f"{message}{timestamp}".encode()).hexdigest()[:7]

    #get parent commit
    with open(".vcs/HEAD","r") as f:
        current_branch = f.read().strip()
    
    branch_path = f".vcs/branches/{current_branch}"
    parent_commit = ""

    if os.path.exists(branch_path):
        with open(branch_path, "r") as f:
            parent_commit = f.read().strip()

    # Create a commit dictionary with message, timestamp, files, and parent
    commit_data = {
        "commit_id": commit_id,
        "message": message,
        "timestamp": timestamp,
        "files": file_snapshots,
        "parent": parent_commit or None
    }

    # Save this as a .json file in .vcs/commits/
    commit_path = f".vcs/commits/{commit_id}.json"
    with open(commit_path, "w") as f:
        json.dump(commit_data, f, indent=2)
    
    # Update branch pointer to this commit
    with open(branch_path, "w") as f:
        f.write(commit_id)

    # Clear the staging area
    with open(staging_path, "w") as f:
        json.dump([], f)

    #print a confirmation message
    print(f"[{commit_id}] {message}")

def show_log():
    # Read the current branch from .vcs/HEAD
    if not os.path.exists(".vcs/HEAD"):
        print("No repository found. Run 'init' first.")
        return
    with open(".vcs/HEAD", "r") as f:
        current_branch = f.read().strip()
    
    # Get the latest commit ID for that branch from .vcs/branches/<branch>
    branch_path = f".vcs/branches/{current_branch}"
    if not os.path.exists(branch_path):
        print(f"No commits found on this branch.")
        return
    with open(branch_path, "r") as f:
        commit_id = f.read().strip()
    if not commit_id:
        print("Branch has no commits yet.")
    
    # Follow the parent chain backward through commit files
    while commit_id:
        commit_path = f".vcs/commits/{commit_id}.json"
        if not os.path.exists(commit_path):
            break

        with open(commit_path, "r") as f:
            commit = json.load(f)
        
        # Print commit details
        date_str = datetime.fromtimestamp(commit["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

        print(f"Commit: {commit['commit_id']}")
        print(f"Message: {commit['message']}")
        print(f"Date: {date_str}\n")

        commit_id = commit["parent"]

def create_branch(branch_name):
    # Read the current branch name from .vcs/HEAD
    head_path = ".vcs/HEAD"
    if not os.path.exists(head_path):
        print("No repository found. Run 'init' first.")
        return
    with open(head_path, "r") as f:
        current_branch = f.read().strip()

    # Get that branch’s latest commit ID from .vcs/branches/<current_branch>
    branch_path = f".vcs/branches/{current_branch}"
    if not os.path.exists(branch_path):
        print("Error: Current branch not found.")
        return
    with open(branch_path, "r") as f:
        current_commit_id = f.read().strip()
    
    # Create a new file: .vcs/branches/<new_branch>
    new_branch_path = f".vcs/branches/{branch_name}"
    if os.path.exists(new_branch_path):
        print(f"Branch '{branch_name}' already exists.")
        return

    # Write the current commit ID into that file
    with open(new_branch_path, "w") as f:
        f.write(current_commit_id)

    # Show a success message
    print(f"Created branch '{branch_name}' at commit {current_commit_id or '(no commits yet)'}")

def checkout_branch(name):
   
    # Check if the branch exists
    branch_path = f".vcs/branches/{name}"
    if not os.path.exists(branch_path):
        print(f"Error: Branch '{name}' does not exist.")
        return
    
    # Get the commit ID it points to
    with open(branch_path, "r") as f:
        commit_id = f.read().strip()

    if not commit_id:
        print(f"Branch '{name}' has no commits yet.")
        return

    # Load the commit file
    commit_path = f".vcs/commits/{commit_id}.json"
    if not os.path.exists(commit_path):
        print(f"Error: Commit '{commit_id}' does not exist.")
        return
    with open(commit_path, "r") as f:
        commit_data = json.load(f)

    # For each file in the commit, overwrite the current version
    for filename, content in commit_data['files'].items():
        with open(filename, "w") as f:
            f.write(content)
    # Update .vcs/HEAD to point to the new branch
    with open(".vcs/HEAD", "w") as f:
        f.write(name)
        
    # Print a success message
    print(f"Switched to branch '{name}' at commit {commit_id}")


def merge_branch(branch_name):
    # Read both commits
    head_path = ".vcs/HEAD"
    if not os.path.exists(head_path):
        print("No repository found. Run 'init' first.")
        return
    
    with open(head_path, "r") as f:
        current_branch = f.read().strip()

    current_branch_path = f".vcs/branches/{current_branch}"
    merge_branch_path = f".vcs/branches/{branch_name}"
    
    if not os.path.exists(merge_branch_path):
        print(f"Error: Branch '{branch_name}' does not exist.")
        return
    
    with open(current_branch_path, "r") as f:
        current_commit= f.read().strip()

    with open(merge_branch_path, "r") as f:
        merge_commit= f.read().strip()
    
    '''load both commit files'''
    with open(f".vcs/commits/{current_commit}.json", "r") as f:
        current_data = json.load(f)
    with open(f".vcs/commits/{merge_commit}.json", "r") as f:
        merge_data = json.load(f)

    # Merge their files (prefer current branch if conflicts)
    merged_files = merge_data['files'].copy()
    merged_files.update(current_data['files'])   #this way current wins if conflicts


    # Create a new commit with two parents
    message = f"Merged branch '{branch_name}' into '{current_branch}'"
    timestamp = time.time()
    commit_id = hashlib.sha1(f"{message}{timestamp}".encode()).hexdigest()[:7]

    merged_commit = {
        "commit_id": commit_id,
        "message": message,
        "timestamp": timestamp,
        "files": merged_files,
        "parent": [current_commit, merge_commit]
    }

    with open(f".vcs/commits/{commit_id}.json", "w") as f:
        json.dump(merged_commit, f, indent=2)

    # Point the current branch to that new commit
    with open(current_branch_path, "w") as f:
        f.write(commit_id)

    # Print a success message
    print(f"Merge complete. Created commit {commit_id}")
