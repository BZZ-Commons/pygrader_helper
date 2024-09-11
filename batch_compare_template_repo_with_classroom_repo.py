import os
import subprocess
import shutil
from git_utils import clone_repo, checkout_branch, commit_and_push_changes
from dotenv import load_dotenv


def are_repos_identical(repo_path1, repo_path2):
    """Compare two git repositories and list the files that have changed if they are not identical."""
    result = subprocess.run(["git", "diff", "--name-only", "--no-index", repo_path1, repo_path2],
                            capture_output=True, text=True)
    if result.returncode == 0:
        return True
    else:
        print(f"Files that have changed between {repo_path1} and {repo_path2}:\n")
        print(result.stdout)
        return False


def remove_existing_repo(repo_dir):
    """Remove the existing directory if it exists and is not empty."""
    if os.path.exists(repo_dir):
        print(f"Removing existing directory: {repo_dir}")
        subprocess.run(['rm', '-rf', repo_dir])


def repo_cloned_successfully(repo_dir):
    """Check if the repository directory exists and is not empty."""
    return os.path.exists(repo_dir) and os.listdir(repo_dir)


def copy_files(source_dir, target_dir):
    """Copy all files from source to target, excluding .git folder."""
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        tgt_path = os.path.join(target_dir, item)
        if os.path.isdir(src_path) and item == '.git':
            continue  # Skip the .git directory
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, tgt_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, tgt_path)


def compare_repos(source_org, target_org, repo_names, github_token, branches):
    """Compare repositories from two organizations and update target repo if differences exist."""
    temp_dir = './TEMP_REPOS'

    # Create a temporary directory for repos if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Change to the temporary directory
    os.chdir(temp_dir)

    for repo_name in repo_names:
        source_repo = repo_name
        target_repo = f'{target_org}-{repo_name}-{repo_name}'

        # Define repo directories inside TEMP_REPOS
        source_repo_dir = source_repo
        target_repo_dir = target_repo

        # Remove existing directories if they exist to avoid conflicts
        remove_existing_repo(source_repo_dir)
        remove_existing_repo(target_repo_dir)

        # Clone the source and target repositories
        print(f"Cloning source repo: {source_org}/{source_repo}")
        clone_repo(source_org, source_repo, github_token)

        # Check if the source repo was cloned successfully
        if not repo_cloned_successfully(source_repo_dir):
            print(f"Error: Source repository {source_repo} was not cloned successfully.")
            continue

        print(f"Cloning target repo: {target_org}/{target_repo}")
        clone_repo(target_org, target_repo, github_token)

        # Check if the target repo was cloned successfully
        if not repo_cloned_successfully(target_repo_dir):
            print(f"Error: Target repository {target_repo} was not cloned successfully.")
            continue

        # For each branch, check if the branches are identical
        for branch in branches:
            print(f"Checking branch '{branch}' for {source_repo} and {target_repo}")

            # Checkout the branch in both repos
            try:
                os.chdir(source_repo_dir)
                checkout_branch(branch)
                os.chdir('../')  # Go back to TEMP_REPOS after branch checkout

                os.chdir(target_repo_dir)
                checkout_branch(branch)
                os.chdir('../')  # Go back to TEMP_REPOS after branch checkout
            except FileNotFoundError as e:
                print(f"Error checking out branch '{branch}' for {source_repo} or {target_repo}: {e}")
                continue

            # Compare the two repositories on this branch
            if are_repos_identical(source_repo_dir, target_repo_dir):
                print(f"The repositories '{source_repo}' and '{target_repo}' are identical on branch '{branch}'.")
            else:
                print(f"The repositories '{source_repo}' and '{target_repo}' differ on branch '{branch}'.")

                # Copy the files from source to target
                print(f"Updating {target_repo} with files from {source_repo}...")
                copy_files(source_repo_dir, target_repo_dir)

                # Commit and push the changes using git_utils
                commit_message = f"Update from {source_repo} on branch {branch}"
                os.chdir(target_repo_dir)
                commit_and_push_changes(branch, commit_message)
                os.chdir('../')  # Go back to TEMP_REPOS after pushing changes

        # Cleanup cloned repositories
        remove_existing_repo(source_repo_dir)
        remove_existing_repo(target_repo_dir)


def main():
    # Usage Example
    source_org_name = 'templates-python'
    target_org_name = 'm323-ix22'
    repo_names = [
        "m323-lu01-a01-imperativer-bubblesort",
        "m323-lu01-a02-imperativer-ggt",
        "m323-lu01-a03-funktionaler-bubblesort",
        "m323-lu01-a04-funktionaler-ggt",
        "m323-lu01-a05-sum",
        "m323-lu02-a01-pure1",
        "m323-lu02-a02-pure2",
        "m323-lu02-a03-pure3",
        "m323-lu02-a04-immutable1",
        "m323-lu02-a05-immutable2",
        "m323-lu02-a06-immutable3",
        "m323-lu02-a07-buchhaltung",
        "m323-lu02-a08-kochbuch",
        "m323-lu03-a01-verzeichnisbaum",
        "m323-lu03-a03-taskscheduler",
        "m323-lu03-a04-filter",
        "m323-lu03-a05-lager",
        "m323-lu03-a06-transformation",
        "m323-lu03-a02-zinseszins",
        "m323-lu03-a07-abschreibung",
        "m323-lu04-a12-sorting",
        "m323-lu03-a08-countries",
        "m323-lu03-a10-timer",
        "m323-lu03-a09-callback",
        "m323-lu04-a01-lambda",
        "m323-lu04-a02-lambda",
        "m323-lu04-a03-comprehensions",
        "m323-lu04-a04-comprehensions",
        "m323-lu04-a05-map",
        "m323-lu04-a06-map",
        "m323-lu04-a07-filter",
        "m323-lu04-a08-filter",
        "m323-lu04-a09-reduce",
        "m323-lu04-a10-reduce",
        "m323-lu04-a13-ternary",
        "m323-lu04-a14-ternary",
        "m323-lu04-a11-sorting",
        "m323-lu06-a01-routing",
        "m323-lu06-a02-routingjson",
        "m323-lu04-a15-generator",
        "m323-lu04-a16-generator",
        "m323-lu04-a17-generatorexpression",
        "m323-lu05-a01-args",
        "m323-lu05-a02-args2",
        "m323-lu05-a03-args3",
        "m323-lu05-a04-kwargs",
        "m323-lu05-a05-kwargs2",
        "m323-lu05-a06-inner",
        "m323-lu05-a07-inner2",
        "m323-lu04-a18-slicing",
        "m323-lu05-a08-closures",
        "m323-lu05-a10-decorator",
        "m323-lu05-a11-decorator2",
        "m323-lu05-a09-closures2",
        "m323-lu06-a03-dao",
        "m323-lu06-a04-restful",
        "m323-lu06-a05-authentication",
        "m323-lu06-a06-blueprints",
        "m323-lu06-a07-multiuser",
        "m323-lu06-a08-hashing",
        "m323-lu02-a09-dataclass",
        "m323-lu02-a10-dataclass1",
        "m323-lu02-a11-dataclass2",
    ]

    """

    """
    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    branches = ['main', 'solution']

    compare_repos(source_org_name, target_org_name, repo_names, github_token, branches)


if __name__ == '__main__':
    main()
