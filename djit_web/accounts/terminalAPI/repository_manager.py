# TO-DO
# CRUD repository

import subprocess


def create_directory__(path):
    try:
        # Create the user with a home directory
        subprocess.run(['sudo', 'mkdir', path], check=True)
        print("success")
        return f"path '{path}' created successfully."
    except subprocess.CalledProcessError as e:
        print(f"error {e} error")
        return f"Error creating user dir: {e}"

def gitinitbare(username,reponame):
    try:
        subprocess.run(['git','init','--bare', f'/srv/git/UR/{username}/{reponame}/{reponame}.git'], check=True)#git init --bare test_repo.git
        print("success")
        return f"repository '{reponame}' created successfully."
    except subprocess.CalledProcessError as e:
        print(f"error {e} error")
        return f"Error creating user dir: {e}"

def create_user_repository(username,repository_name):
    # make sure repository is not exist
    # setup rights
    out1 = create_directory__(f'/srv/git/UR/{username}') + create_directory__(f'/srv/git/UR/{username}/{repository_name}')
    out2 = gitinitbare(username,repository_name)
    return out1+' '+out2

def is_repo_exists(repo_name):
    return False
def setup_bare():
    pass

if __name__ == '__main__':
    create_user_repository('user','dir')