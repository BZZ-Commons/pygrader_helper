import subprocess

def delete_repos(repo_list, current_owner):
    """
    Deletes a list of repositories for a specific owner using the GitHub CLI.

    Parameters:
    repo_list (list): List of repository names to be deleted.
    current_owner (str): Current owner of the repositories.

    Returns:
    None
    """
    for repo in repo_list:
        command = f'gh repo delete {current_owner}/{repo} --yes'
        try:
            print(f'Deleting repo {repo} owned by {current_owner}')
            subprocess.run(command, shell=True, check=True)
            print(f'Successfully deleted {repo}')
        except subprocess.CalledProcessError as e:
            print(f'Failed to delete {repo}: {e}')

if __name__ == '__main__':
    # List of repositories to delete
    repos_to_delete = [
        "m319-ix24-m319-lu04-a03-story-m319_lu04_a03_story",
        "m319-ix24-m319-lu04-a04-multiplicator-m319_lu04_a04_multiplicator",
        "m319-ix24-m319-lu04-a01-classroom-m319_lu04_a00_classroom",
    ]

    # Current owner of the repositories
    current_owner = "m319-ix24"

    # Delete the repositories
    delete_repos(repos_to_delete, current_owner)