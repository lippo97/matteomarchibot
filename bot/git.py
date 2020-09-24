import os
from git import Repo

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
repo = Repo(root)
version = repo.git.describe()
branch_name = repo.active_branch.name
remote_repo = next(repo.remote().urls).replace(':', '/').replace('git@', 'https://').replace('.git', '')
