import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from batch_requirements_manager import update_requirements_file  # Importing the function


def clone_repo(org_name, repo_name, github_token):
    """Clone the GitHub repository using the provided organization name and repository name."""
    repo_url = f"https://{github_token}@github.com/{org_name}/{repo_name}.git"
    subprocess.run(["git", "clone", repo_url])


def checkout_branch(branch_name):
    """Checkout the specified branch."""
    subprocess.run(["git", "checkout", branch_name])


def commit_and_push_changes(branch_name):
    """Commit the changes and push to the specified branch."""
    subprocess.run(["git", "add", "."])
    subprocess.run(
        ["git", "commit", "-m", f"Add configurations and update requirements.txt for {branch_name} branch"])
    subprocess.run(["git", "push", "origin", branch_name])


def replace_run_pylint(repo_root, template_dir):
    """Replace _run_pylint.py in the repository with the one from the template if it exists."""
    repo_pylint_path = repo_root / "_run_pylint.py"
    template_pylint_path = Path(template_dir) / "_run_pylint.py"

    if repo_pylint_path.exists() and template_pylint_path.exists():
        shutil.copy2(template_pylint_path, repo_pylint_path)
        print(f"Replaced _run_pylint.py in {repo_root} with the template version.")
    elif template_pylint_path.exists():
        shutil.copy2(template_pylint_path, repo_pylint_path)
        print(f"Copied _run_pylint.py from template to {repo_root}.")


def process_repository(org_name, repo_name, github_token, template_dir, packages):
    """Process a single repository by cloning, making changes, and pushing updates."""
    # Clone the repository
    clone_repo(org_name, repo_name, github_token)

    # Change directory to the cloned repository
    os.chdir(repo_name)

    # Branches to update
    branches = ['main', 'solution']

    for branch in branches:
        # Checkout the branch
        checkout_branch(branch)

        # Paths
        repo_root = Path(os.getcwd())

        # Replace _run_pylint.py if it exists
        replace_run_pylint(repo_root, template_dir)

        # Copy all files from the template directory to the repo
        for item in Path(template_dir).iterdir():
            if item.is_dir():
                shutil.copytree(item, repo_root / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, repo_root / item.name)

        # Update requirements.txt using the new module
        update_requirements_file(repo_root, packages)

        # Commit and push the changes to the current branch
        commit_and_push_changes(branch)

    # Go back to the parent directory before processing the next repository
    os.chdir('..')

    # Optionally, remove the cloned repository folder after processing
    shutil.rmtree(repo_name)


def main():
    ##############################
    #START TODO
    ##############################

    # GitHub organization name
    org_name = "m323-ix22"

    # List of repositories to process
    repo_names = [
        "m323-ix22-m323-lu01-a01-imperativer-bubblesort-m323-lu01-a01-imperativer-bubblesort",
        "m323-ix22-m323-lu01-a02-imperativer-ggt-m323-lu01-a02-imperativer-ggt",
        "m323-ix22-m323-lu01-a03-funktionaler-bubblesort-m323-lu01-a03-funktionaler-bubblesort",
        "m323-ix22-m323-lu01-a04-funktionaler-ggt-m323-lu01-a04-funktionaler-ggt",
        "m323-ix22-m323-lu01-a05-sum-m323-lu01-a05-sum",
    ]

    # Specify the packages and versions to use
    packages = {
        "pylint": "3.2.6",
    }

    ##############################
    #END TODO
    ##############################

    # Capture the original working directory
    original_working_dir = os.getcwd()

    # Directory containing the templates
    template_dir = os.path.join(original_working_dir, 'templates_for_add_run_pylint')


    # Load GitHub token from .env file
    load_dotenv()
    github_token = os.environ['GITHUB_TOKEN']



    # Process each repository
    for repo_name in repo_names:
        process_repository(org_name, repo_name, github_token, template_dir, packages)

    print('Operation completed successfully for all repositories.')


if __name__ == '__main__':
    main()