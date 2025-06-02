# Mini Version Control System (MyVCS)

A simple Git-like version control system built from scratch using Python.  
It supports basic commands such as `init`, `add`, `commit`, `log`, `branch`, `checkout`, and `merge`.

## Features

- `init` – Initialize a new repository
- `add <filename>` – Stage files for commit
- `commit -m "message"` – Save a snapshot of staged files
- `log` – View commit history
- `branch <name>` – Create a new branch
- `checkout <branch>` – Switch to a different branch
- `merge <branch>` – Merge another branch into the current one

## How to Use

```bash
# Initialize a repository
python main.py init

# Stage files
python main.py add myfile.txt

# Commit changes
python main.py commit -m "Initial commit"

# View commit history
python main.py log

# Create a new branch
python main.py branch dev

# Switch to a branch
python main.py checkout dev

# Merge a branch
python main.py merge dev
```

## How It Works

- All metadata is stored in a hidden `.vcs/` folder
- Commits are saved as JSON files in `.vcs/commits/`
- Branches are stored as text files in `.vcs/branches/`
- Uses SHA-1 hashes to generate unique commit IDs
- Tracks files by saving their full content in each commit

## Folder Structure

```
.vcs/
├── HEAD                  ← Current branch name
├── branches/             ← One file per branch (points to commit)
├── commits/              ← One JSON file per commit
└── staging_area.json     ← List of files staged for commit
```

## Requirements

- Python 3.x
- No third-party packages required
- Uses only: `os`, `json`, `argparse`, `hashlib`, `time`, `datetime`

## License

MIT License – free to use, modify, and share.

## Credits

Built with ❤️ by a student learning data structures through real-world projects.
