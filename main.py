import argparse
from vcs.core import init_repo, add_file, commit_changes, show_log, create_branch, checkout_branch
def main():
    parser = argparse.ArgumentParser(description="Mini VCS")
    subparsers = parser.add_subparsers(dest='command')
    #'init' command
    subparsers.add_parser("init", help="Initialize a new repo")

    #'add' command with a filename argument
    add_parser = subparsers.add_parser("add", help = "Add file")
    add_parser.add_argument("filename", help= "Name of the file to add")
    ## add_argument = parser.parse_args()

    #add 'commit' command to CLI
    commit_parser = subparsers.add_parser("commit", help = "Commit changes")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

    #'log' command to show commit history 
    log_parser = subparsers.add_parser("log", help="Show commit history")

    #'branch' command to create a new branch
    branch_parser = subparsers.add_parser("branch", help="Create a new branch")
    branch_parser.add_argument("branch_name", help="Name of the new branch")
    
    #'checkout' command to switch to a branch
    checkout_parser = subparsers.add_parser("checkout", help="Switch to a branch")
    checkout_parser.add_argument("branch_name", help="Name of the branch to switch to")


    #read the user;s command and handel it
    args = parser.parse_args()
    #check if the command is 'init'
    if args.command == "init":
        init_repo()
    elif args.command == "add":
        add_file(args.filename)
    elif args.command == "commit":
        commit_changes(args.message)
    elif args.command == "log":
        show_log()
    elif args.command == "branch":
        create_branch(args.branch_name)
    elif args.command == "checkout":
        checkout_branch(args.branch_name)
    else:
        print("Invalid command. Try python main.py init")


if __name__ == "__main__":
    main()
