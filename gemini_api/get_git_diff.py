import subprocess


def get_git_diff():
    result = subprocess.run(
        ['git', 'diff', 'HEAD~1', 'HEAD'],
        capture_output=True,
        text=True
    )
    return result.stdout


def clean_diff(diff_text):
    cleaned_lines = []
    for line in diff_text.splitlines():
        if line.startswith(('index ', '--- ', '+++ ', '@@ ', 'diff --git')):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)