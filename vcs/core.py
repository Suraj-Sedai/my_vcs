#vcs.core.py

import os
import json
import hashlib
import time


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

    