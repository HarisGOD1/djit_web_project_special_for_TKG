import subprocess
import os
import crypt

from . import repository_manager

# acceptedSymbols = 'abcdefghijklmnopqrstuvwxyz0123456789-_'

allowed_symbols = 'abcdefghijklmnopqrstuvwxyz0123456789-'
max_len = 29
min_len = 4
# print(len(      'abcdefghijklmnopqrstuvwxyz'))


def check_username(username):
    problem = 'server problem'
    if not is_username_correct(username):
        problem = "USERNAME_CONTAINS_UNACCEPTABLE_SYMBOLS"
        return False, problem

    if len(username) > max_len or len(username) < min_len:
        problem = "USERNAME_INCORRECT_LENGTH([4,29]-supported)"
        return False, problem

    if is_user_registered(username):
        return False, "USER_YET_CREATED"


    return True, problem

def create_user(username):
    try:
        # Create the user with a home directory
        check_flag, problem = check_username(username)
        if not check_flag:
            return problem
        else:
            # print(username+" "+passwd)
            # we are not need to use crypt.crypt
            # we need only hash, provided by django app, and
            # need specify salt in our system to work with it,
            # or maybe overwrite django app to work with our salt
            # sudo useradd --home /srv/git/UR/username1 --shell /usr/bin/git-shell username1
            print('trying to create user')
            repository_manager.create_directory__(f'/srv/git/UR/{username}')
            os.system(f"useradd --home /srv/git/UR/{username} --shell /user/bin/git-shell {username}")
            return f"USER_{username}_CREATED"
    except subprocess.CalledProcessError as e:
        print(e.output)
        return f"Error creating user: {e}"

#TO-DO maybe need to rewrite
def set_user_password(username, password):
    try:
        # echo 'username:password' | chpasswd
        cmd = f"echo '{username}:{password}' | sudo chpasswd"
        subprocess.run(cmd, shell=True, check=True)
        return f"Password set for user '{username}'."
    except subprocess.CalledProcessError as e:
        return f"Error setting password: {e}"

def delete_user(username):
    try:
        # Create the user with a home directory
        subprocess.run(['sudo', 'userdel', username], check=True)
        return f"User '{username}' deleted successfully."
    except subprocess.CalledProcessError as e:
        return f"Error creating user: {e}"

def get_user_list():
    try:
        cmd = 'getent passwd'
        # perform list of "...thegod:x:1000:1000:msigf66thegod,,,:/home/thegod:/bin/bash"
        # to list..."...thegod..."
        user_list = [substr[0:(substr.find(':'))] for substr in subprocess.check_output(cmd , shell = True).decode('ascii').split('\n')]
        return user_list
    except subprocess.CalledProcessError as e:
        return f"Error setting password: {e}"

def is_user_registered(name:str):
    for username in get_user_list():
        if name==username:
            return True
    return False

# TO-DO add injections-check, verify data
def set_user_rights(username,rights,path):
    try:
        subprocess.run(['sudo','setfacl','-m',f'u:{username}:{rights}',f'/srv/git/UR/{path}'])
        return f'USER RIGHTS SET'
    except subprocess.CalledProcessError as e:
        return f'Error setting rights: {e}'

# TO-DO add injections-check, verify data
def clear_user_rights(username,path):
    try:
        subprocess.run(['sudo','setfacl','-x',f'u:{username}',path])
        return f'USER RIGHTS CLEARED'
    except subprocess.CalledProcessError as e:
        return f'Error clearing rights: {e}'

def get_file_ACL(path):
    try:
        subprocess.run(['sudo','getfacl',path])
        return f'USER RIGHTS CLEARED'
    except subprocess.CalledProcessError as e:
        return f'Error clearing rights: {e}'

def is_username_correct(username):
    #a-zA-Z0-9_-
    for c in username:
        if c not in allowed_symbols:
            print(username,c)
            return False
    if username[0]=='-' or username[0] =='_':
        return False
    return True

def verify_repo_name(reponame):
    return is_username_correct(reponame)
# TO-DO
# make CRUD user
# make edit user rights
#
def main():
    get_user_list()

if __name__ == "__main__":
    main()
