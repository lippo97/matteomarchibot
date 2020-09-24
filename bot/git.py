import os
from git import Repo

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
repo = Repo(root)
