#vcs.core.py

import os

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