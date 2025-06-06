# to-do generate username-associated ssh key
from . import repository_manager
from . import user_manager
import subprocess

# A-Z a-z 0-9 + / = <- ssh allowed symbols
allowed_ssh_symbols = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+/=-@ '
def save_ssh(username,sshkey_string):

    # if not user_manager.is_user_registered(username):
    #     user_manager.create_user(username)

    b,p = user_manager.check_username(username)
    print(b, p)

    if (not b) and (p == 'USER_YET_CREATED'):
        # check ssh
        for e in sshkey_string:
            if e not in allowed_ssh_symbols:
                return 'ssh looks not valid'

        repository_manager.create_directory__(f'/srv/git/UR/{username}/.ssh')
        try:
            subprocess.run(['sudo','chown',username,f'/srv/git/UR/{username}/.ssh'],check=True)
            subprocess.run(['sudo','chown',username,f'/srv/git/UR/{username}/.ssh/authorized_keys'],check=True)
            subprocess.run(['sudo','chmod','700',f'/srv/git/UR/{username}/.ssh'],check=True)
            subprocess.run(['sudo','chmod','600',f'/srv/git/UR/{username}/.ssh/authorized_keys'],check=True)
            subprocess.run(['sudo','chmod','744',f'/srv/git/UR/{username}'],check=True)

        except subprocess.CalledProcessError as e:
            print(f'error {e} error')

        with open(f'/srv/git/UR/{username}/.ssh/authorized_keys','w') as f:
            f.write(sshkey_string)
            print('AAAA')
            return 'ssh add/edit success'


    else:
        return p


