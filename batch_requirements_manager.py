import os
import shutil
from pathlib import Path
import subprocess
from dotenv import load_dotenv


def update_requirements_file(repo_path, packages):
    """
    Update the requirements.txt file to include specified packages and versions.

    Args:
        repo_path (Path): The path to the repository.
        packages (dict): A dictionary of packages and their versions to add/update.
                         e.g., {"pylint": "3.2.6", "requests": "2.25.1"}
    """
    requirements_path = Path(repo_path) / "requirements.txt"

    # Create the requirements.txt file if it doesn't exist
    if not requirements_path.exists():
        with open(requirements_path, 'w', encoding='utf-8') as req_file:
            for pkg, version in packages.items():
                req_file.write(f"{pkg}=={version}\n")
    else:
        with open(requirements_path, 'r', encoding='utf-8') as req_file:
            lines = req_file.readlines()

        # Check each package in the current requirements file and update if needed
        for pkg, version in packages.items():
            pkg_exists = False
            for i, line in enumerate(lines):
                if pkg in line:
                    pkg_exists = True
                    # Update the version if it doesn't match
                    if f"{pkg}==" not in line or line.strip() != f"{pkg}=={version}":
                        lines[i] = f"{pkg}=={version}\n"
                    break

            # Add the package if it's not already listed
            if not pkg_exists:
                lines.append(f"{pkg}=={version}\n")

        # Write the updated content back to requirements.txt
        with open(requirements_path, 'w', encoding='utf-8') as req_file:
            req_file.writelines(lines)


def clone_repo(org_name, repo_name, github_token):
    """Clone the GitHub repository using the provided organization name and repository name."""
    repo_url = f"https://{github_token}@github.com/{org_name}/{repo_name}.git"
    subprocess.run(["git", "clone", repo_url])


def process_repos(org_name, repo_names, packages, github_token):
    """Process the list of repositories and update their requirements.txt."""
    # Load GitHub token
    load_dotenv()

    for repo_name in repo_names:
        # Clone the repository
        clone_repo(org_name, repo_name, github_token)

        # Change directory to the cloned repository
        os.chdir(repo_name)

        # Update requirements.txt using the new module
        update_requirements_file(Path(os.getcwd()), packages)

        # Commit and push changes
        subprocess.run(["git", "add", "."])
        subprocess.run(
            ["git", "commit", "-m", "Updated requirements.txt with specified package versions"]
        )
        subprocess.run(["git", "push", "origin", "main"])

        # Return to the parent directory
        os.chdir('..')

        # Optionally, remove the cloned repository folder after processing
        shutil.rmtree(repo_name)

    print(f"Repositories processed successfully in {org_name}")


def main():
    # List of repositories to process
    repo_names = [
        "m323-ix22-m323-lu01-a01-imperativer-bubblesort-m323-lu01-a01-imperativer-bubblesort",
        "m323-ix22-m323-lu01-a02-imperativer-ggt-m323-lu01-a02-imperativer-ggt",
        "m323-ix22-m323-lu01-a03-funktionaler-bubblesort-m323-lu01-a03-funktionaler-bubblesort",
        "m323-ix22-m323-lu01-a04-funktionaler-ggt-m323-lu01-a04-funktionaler-ggt",
        "m323-ix22-m323-lu01-a05-sum-m323-lu01-a05-sum",
    ]

    # GitHub organization name
    org_name = "m323-ix22"

    # Specify the packages and versions to use
    packages = {
        "pylint": "3.2.6",
        "requests": "2.25.1"  # Example of adding another package
    }

    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    # Process the repositories
    process_repos(org_name, repo_names, packages, github_token)


if __name__ == '__main__':
    main()
