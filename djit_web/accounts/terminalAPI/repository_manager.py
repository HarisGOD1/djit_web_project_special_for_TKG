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

def gitinitbare(username,reponame,repogroupname):
    try:
        pathtorepo = f'/srv/git/UR/{username}/{reponame}/{reponame}.git'
        # subprocess.run(['git', 'init', f'/srv/git/UR/{username}/{reponame}/{reponame}.git'], check=True)
        # /\ this will create repo with root root access
        # 'gr'+repo.uid = repogroupname
        # inition a group for spec repo
        # print('1')
        subprocess.run(['sudo', 'groupadd', repogroupname], check=True)
        subprocess.run(['sudo', 'usermod','-aG', repogroupname, username], check=True)
        subprocess.run(['sudo', 'usermod', '-aG', repogroupname, 'root'], check=True)
        # print('1')
        # owe repo to gr
        subprocess.run(['sudo', 'mkdir', '-p', pathtorepo], check=True)
        subprocess.run(
            ['sudo', 'git', 'init', '--bare', '--shared=group', pathtorepo],
            check=True)  # git init --bare test_repo.git
        # print('1')
        # setup the spermissions
        subprocess.run(['sudo', 'chgrp', '-R', repogroupname, pathtorepo], check=True)
        subprocess.run(['sudo', 'chmod', '-R','g+ws', pathtorepo], check=True)
        subprocess.run(['sudo', 'chmod', '-R','g+rs', pathtorepo], check=True)
        subprocess.run(['sudo', 'chmod', '-R','g+xs', pathtorepo], check=True)
        print('1')

        subprocess.run(['sudo', 'chown', '-R', username, f'/srv/git/UR/{username}/{reponame}'], check=True)
        subprocess.run(['sudo', 'git', 'config', '--global', '--add', 'safe.directory', pathtorepo], check=True)
        print('1')

        print("success", username, reponame)
        return f"repository '{reponame}' created successfully."
    except subprocess.CalledProcessError as e:
        print(f"error {e} error")
        return f"Error creating user dir: {e}"

def create_user_repository(username,repository_name,repogroupname):
    # make sure repository is not exist
    # setup rights
    out1 = create_directory__(f'/srv/git/UR/{username}') + create_directory__(f'/srv/git/UR/{username}/{repository_name}')
    out2 = gitinitbare(username,repository_name,repogroupname)
    return out1+' '+out2

def get_content_from_path(username,reponame,path):
    try:
        # print(username,reponame,path)
        path = 'master' if path=='/'or path=='' else f'master:{path}'
        cmd = f'sudo -u {username} git -C /srv/git/UR/{username}/{reponame}/{reponame}.git ls-tree {path} -l'
        # perform list of "...thegod:x:1000:1000:msigf66thegod,,,:/home/thegod:/bin/bash"
        # to list..."...thegod..."
        # for st in (subprocess.check_output(cmd, shell=True).decode('ascii')).split('\n'):
        #     print(repr(st))

        subs_list = [(substr.split(' ')[1],substr.split(' ')[-1].split('\t')[1]) for substr in
                     subprocess.check_output(cmd, shell=True).decode('ascii').split('\n')[:-1]]
        return subs_list
    except subprocess.CalledProcessError as e:
        # print(f"error {e} error")
        return False

def get_file_from_path(username,reponame,path):
    try:
        # print(username,reponame,path)
        path = f'master:{path}'
        cmd = f'sudo -u {username} git -C /srv/git/UR/{username}/{reponame}/{reponame}.git cat-file blob {path}'
        # perform list of "...thegod:x:1000:1000:msigf66thegod,,,:/home/thegod:/bin/bash"
        # to list..."...thegod..."
        # for st in (subprocess.check_output(cmd, shell=True).decode('ascii')).split('\n'):
        #     print(repr(st))

        file_content = subprocess.check_output(cmd, shell=True).decode('ascii')
        return file_content
    except subprocess.CalledProcessError as e:
        print(f"error {e} error")
        return f"Error creating user dir: {e}"


def is_repo_exists(username,repo_name):
    path = f'/srv/git/UR/{username}/{repo_name}'
    cmd = f'ls {path}'
    # perform list of "...thegod:x:1000:1000:msigf66thegod,,,:/home/thegod:/bin/bash"
    # to list..."...thegod..."
    # for st in (subprocess.check_output(cmd, shell=True).decode('ascii')).split('\n'):
    #     print(repr(st))

    file_content = subprocess.check_output(cmd, shell=True).decode('ascii')
    # print(file_content)
    return f'{repo_name}.git' in file_content

def setup_bare():
    pass

def sudormrf_user_dir(username,dirname):
    path = f'/srv/git/UR/{username}/{dirname}'
    cmd = f'sudo rm -rf {path}'

    output = subprocess.check_output(cmd, shell=True).decode('ascii')

def delete_group(repogroupname):
    cmd = f'sudo groupdel {repogroupname}'

    output = subprocess.check_output(cmd, shell=True).decode('ascii')

def add_user_in_group(groupname,membername):
    # sanitize inputs
    subprocess.run(['sudo', 'usermod', '-aG', groupname, membername], check=True)

def delete_user_from_group(groupname,membername):
    # sanitize inputs
    # gpasswd - -delete
    # user
    # group
    subprocess.run(['sudo', 'gpasswd', '--delete', membername,groupname], check=True)

def setup_dir_rights(path:str,rights:int):
    subprocess.run(['sudo', 'chmod', '-R', str(rights), path], check=True)


def make_dir_private(username,reponame):
    setup_dir_rights(f'/srv/git/UR/{username}/{reponame}',770)


def make_dir_public(username,reponame):
    setup_dir_rights(f'/srv/git/UR/{username}/{reponame}',775)

if __name__ == '__main__':
    # create_user_repository('user','dir')
    pass