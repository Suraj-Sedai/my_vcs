import argparse
def main():
    parser = argparse.ArgumentParser(description="Mini VCS")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser("init", help="Initialize a new repo")

    #read the user;s command and handel it
    args = parser.parse_args()
    #check if the command is 'init'
    if args.command == "init":
        pass
    else:
        print("Invalid command. Try python main.py init")


if __name__ == "__main__":
    main()
