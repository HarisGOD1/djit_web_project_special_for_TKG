import subprocess


def get_git_diff(username,reponame):
    cmd = f"sudo -u {username} git -C /srv/git/UR/{username}/{reponame}/{reponame}.git/ git diff HEAD~1 HEAD -- ."
    result = subprocess.run(
        cmd.split(' '),
        capture_output=True,
        text=True
    )
    # file_content = subprocess.check_output(cmd, shell=True).decode('ascii')

    # return file_content
    return result.stdout

def clean_diff(diff_text):
    cleaned_lines = []
    for line in diff_text.splitlines():
        if line.startswith(('index ', '--- ', '+++ ', '@@ ', 'diff --git')):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)