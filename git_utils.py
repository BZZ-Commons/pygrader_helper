import subprocess


def clone_repo(org_name, repo_name, github_token):
    """Clone the GitHub repository using the provided organization name and repository name."""
    repo_url = f"https://{github_token}@github.com/{org_name}/{repo_name}.git"
    subprocess.run(["git", "clone", repo_url])


def checkout_branch(branch_name):
    """Checkout the specified branch. Print a message if the branch doesn't exist."""
    subprocess.run(["git", "checkout", branch_name])


def commit_and_push_changes(branch_name, commit_message):
    """Commit the changes and attempt to push to the specified branch. Print a message if the branch doesn't exist remotely."""
    # Check if there are any changes to commit
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"No changes to commit on branch {branch_name}.")
        return

    # Commit changes if there are any
    subprocess.run(["git", "add", "."])
    subprocess.run(
        ["git", "commit", "-m", commit_message],
        check=True
    )

    # Check if the branch exists on remote before pushing
    result = subprocess.run(["git", "ls-remote", "--heads", "origin", branch_name], capture_output=True, text=True)
    if branch_name in result.stdout:
        subprocess.run(["git", "push", "origin", branch_name])
    else:
        print(f"Branch {branch_name} does not exist on remote. No push was made.")
