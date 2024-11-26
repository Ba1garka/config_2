import subprocess

def get_commits(repo_path):

    cmd = ['git', '-C', repo_path, 'log', '--all', '--pretty=format:%H|%s|%P']
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception("Ошибка получения коммитов!")

    commits = []
    for line in result.stdout.splitlines():
        if line:
            parts = line.split('|')
            commit_data = {
                "hash": parts[0],
                "massage": parts[1],
                "dependencies": parts[2].split() if len(parts) > 2 and parts[2] else []
            }
            commits.append(commit_data)
    return commits