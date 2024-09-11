import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from git_utils import clone_repo, checkout_branch, commit_and_push_changes


def manage_requirements_file(repo_path, packages_to_add=None, packages_to_remove=None):
    """
    Manage the requirements.txt file to add, update, or remove specified packages.

    Args:
        repo_path (Path): The path to the repository.
        packages_to_add (dict): A dictionary of packages to add or update with versions.
                                e.g., {"pylint": "3.2.6", "requests": "2.25.1"}
        packages_to_remove (list): A list of packages to remove.
                                e.g., ["unused_package"]
    """
    requirements_path = Path(repo_path) / "requirements.txt"

    # If the file doesn't exist, create it and add the packages_to_add
    if not requirements_path.exists():
        with open(requirements_path, 'w', encoding='utf-8') as req_file:
            if packages_to_add:
                for pkg, version in packages_to_add.items():
                    req_file.write(f"{pkg}=={version}\n")
        return

    # Read the existing requirements file
    with open(requirements_path, 'r', encoding='utf-8') as req_file:
        lines = req_file.readlines()

    updated_lines = []

    # Check for each package in the current requirements file and update or remove if needed
    for line in lines:
        pkg_name = line.split('==')[0].strip()

        # Remove package if it's in the remove list
        if packages_to_remove and pkg_name in packages_to_remove:
            continue

        # Update package version if it's in the add/update list
        if packages_to_add and pkg_name in packages_to_add:
            updated_lines.append(f"{pkg_name}=={packages_to_add[pkg_name]}\n")
            packages_to_add.pop(pkg_name)  # Remove from the dict to avoid adding it again later
        else:
            updated_lines.append(line)

    # Add any remaining packages that are in packages_to_add
    if packages_to_add:
        for pkg, version in packages_to_add.items():
            updated_lines.append(f"{pkg}=={version}\n")

    # Write the updated content back to requirements.txt
    with open(requirements_path, 'w', encoding='utf-8') as req_file:
        req_file.writelines(updated_lines)


def process_repos(org_name, repo_names, packages_to_add, packages_to_remove, branches, github_token):
    """Process the list of repositories and update their requirements.txt across multiple branches."""
    for repo_name in repo_names:
        # Clone the repository
        clone_repo(org_name, repo_name, github_token)

        # Change directory to the cloned repository
        os.chdir(repo_name)

        # Iterate through the branches
        for branch in branches:
            # Checkout the branch
            checkout_branch(branch)

            # Update requirements.txt
            manage_requirements_file(
                Path(os.getcwd()), packages_to_add=packages_to_add, packages_to_remove=packages_to_remove
            )

            # Commit and push changes
            commit_and_push_changes(branch,f"Updated requirements.txt with specified package versions on {branch} branch")

        # Return to the parent directory
        os.chdir('..')

        # Optionally, remove the cloned repository folder after processing
        shutil.rmtree(repo_name)

    print(f"Repositories processed successfully in {org_name}")


def main():
    # List of repositories to process
    repo_names = [
        "m323-lu01-a01-imperativer-bubblesort-graphics80",
    ]

    # GitHub organization name
    org_name = "m323-ix22"

    # Specify the packages to add or update
    packages_to_add = {
        #"pylint": "3.2.6",
    }

    # Specify packages to remove (if any)
    packages_to_remove = ["hello"]  # "pylint", "requests" Example of removing the added packages

    # Specify branches to process
    branches = ['main']  # List the branches you want to process

    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    # Process the repositories
    process_repos(org_name, repo_names, packages_to_add, packages_to_remove, branches, github_token)


if __name__ == '__main__':
    main()