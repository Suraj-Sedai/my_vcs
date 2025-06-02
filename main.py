import argparse
from vcs.core import init_repo, add_file
def main():
    parser = argparse.ArgumentParser(description="Mini VCS")
    subparsers = parser.add_subparsers(dest='command')
    #'init' command
    subparsers.add_parser("init", help="Initialize a new repo")

    #'add' command with a filename argument
    add_parser = subparsers.add_parser("add", help = "Add file")
    add_parser.add_argument("filename", help= "Name of the file to add")
    ## add_argument = parser.parse_args()

    #'add' commint command to CLI
    commit_parser = subparsers.commit_parser("commit", help = "Commit changes")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")

    #read the user;s command and handel it
    args = parser.parse_args()
    #check if the command is 'init'
    if args.command == "init":
        init_repo()
    elif args.command == "add":
        add_file(args.filename)
    elif args.command == "commit":
        commit_changes(args.message)
    else:
        print("Invalid command. Try python main.py init")


if __name__ == "__main__":
    main()
