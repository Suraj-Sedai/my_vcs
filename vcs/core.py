#vcs.core.py

import os
import json

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
    
    