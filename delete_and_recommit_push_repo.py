import os
import subprocess
from git_utils import clone_repo
from dotenv import load_dotenv


def clone_repo_with_branches(org_name, repo_name, github_token, branches):
    """Clone the repository and fetch specified branches."""
    clone_repo(org_name, repo_name, github_token)

    os.chdir(repo_name)
    for branch in branches:
        # Fetch and checkout each branch
        subprocess.run(['git', 'checkout', branch])
        subprocess.run(['git', 'pull', 'origin', branch])
    os.chdir('../')


def delete_repo(org_name, repo_name):
    """Delete the repository on GitHub using the GitHub CLI."""
    repo_full_name = f'{org_name}/{repo_name}'
    print(f"Deleting repo: {repo_full_name}")
    subprocess.run(['gh', 'repo', 'delete', repo_full_name, '--yes'])


def create_repo(org_name, repo_name):
    """Create the repository again on GitHub using the GitHub CLI."""
    #print(f"Creating repo: {repo_name} under {org_name}")
    subprocess.run(['gh', 'repo', 'create', f'{org_name}/{repo_name}', '--public'])


def push_branches(repo_name, branches):
    """Push the specified branches to the remote repository."""
    os.chdir(repo_name)

    for branch in branches:
        #print(f"Pushing branch: {branch} to {repo_name}")
        subprocess.run(['git', 'checkout', branch])
        subprocess.run(['git', 'push', '--set-upstream', 'origin', branch])

    os.chdir('../')


def manage_repos(org_name, repo_names, github_token):
    """Clone, delete, recreate, and push repositories with 'main' and 'solution' branches."""
    branches = ['main', 'solution']  # The two typical branches

    for repo_name in repo_names:
        print(f"Processing repo: {repo_name}")

        # Step 1: Clone the repository with the specified branches
        clone_repo_with_branches(org_name, repo_name, github_token, branches)

        # Step 2: Delete the repository on GitHub using gh CLI
        delete_repo(org_name, repo_name)

        # Step 3: Recreate the repository
        create_repo(org_name, repo_name)

        # Step 4: Push the main and solution branches to the new remote repository
        push_branches(repo_name, branches)


def main():
    # Example input
    org_name = 'templates-python'
    repo_names = [
        "m319-lu05-a02-larger",
        "m319-lu06-a03-lists",
        "m319-lu06-a01-simplelist",
        "m319-lu05-a01-positivity",
        "m319-lu05-a03-grades",
        "m319-lu05-a04-oddeven",
        "m319-lu05-a05-age",
        "m319-lu05-a06-leapyear",
        "m319-lu05-a07-tax",
        "m319-lu05-a08-carryon",
        "m319-lu05-a09-positives",
        "m319-lu05-a11-factorial",
        "m319-lu05-a12-pieces",
        "m319-lu05-a13-bankloan",
        "m319-lu06-a04-minmax",
        "m319-lu06-a05-converter",
        "m319-lu06-a06-cheese",
        "m319-lu06-a07-roman",
        "m319-lu06-a02-names",
        "m319-lu07-a01-conditional",
        "m319-lu07-a02-listadd",
        "m319-lu07-a03-counting",
        "m319-lu04-a02-conversation",
        "m319-lu04-a03-story",
        "m319-lu04-a04-multiplicator",
        "m319-lu08-a01-syntaxfehler-1",
        "m319-lu08-a02-syntaxfehler-2",
        "m319-lu08-a03-logikfehler",
        "m319-lu09-a01-first-functions",
        "m319-lu09-a02-define-functions",
        "m319-lu09-a03-advanced-functions",
        "m319-lu09-a04-digit-sum",
        "m319-lu09-a05-distance-two-points",
        "m319-lu09-a06-triangle",
        "m319-lu09-a07-breaking",
        "m319-lu10-a01-calculator",
        "m319-lu10-a02-reader-module",
        "m319-lu10-a03-reader-module-extended",
        "m319-lu11-a01-dict",
        "m319-lu11-a02-numerals",
        "m319-lu12-a01-car",
        "m319-lu12-a02-farmshop",
        "m319-lu12-a03-lottery",
        "m319-lu13-a01-boat",
        "m319-lu13-a02-farmshop-extended",
        "m319-lu14-a01-timeuntil",
        "m319-lu14-a02-chessclock",
        "m319-lu20-a01-library",
        "m319-lu20-a02-library-extended",
        "m319-lu20-a03-library-json-read-write",
        "m319-lu04-a01-classroom",
    ]

    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    # Manage the repositories
    manage_repos(org_name, repo_names, github_token)


if __name__ == '__main__':
    main()
