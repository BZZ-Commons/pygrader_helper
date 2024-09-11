import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from git_utils import clone_repo, checkout_branch, commit_and_push_changes

def manage_files_in_repo(repo_path, template_dir, files_to_remove=None):
    """
    Manage files (copy and replace) from the template directory to the repository, maintaining the folder structure.
    Optionally remove files and folders specified in files_to_remove.

    Args:
        repo_path (Path): The path to the repository.
        template_dir (Path): The path to the template directory containing files and folders to add or update.
        files_to_remove (list): List of file/folder paths to remove from the repository.
    """
    repo_path = Path(repo_path)
    template_dir = Path(template_dir)

    # Remove specified files and folders
    if files_to_remove:
        for file_name in files_to_remove:
            file_path = repo_path / file_name
            if file_path.exists():
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"Removed directory {file_name} from {repo_path}")
                else:
                    file_path.unlink()
                    print(f"Removed file {file_name} from {repo_path}")
            else:
                print(f"Warning: {file_name} not found in {repo_path}")

    # Ensure the template directory exists
    if not template_dir.exists():
        print(f"Error: Template directory {template_dir} does not exist.")
        return False  # Exit early if the template directory doesn't exist

    # Copy all files and folders from the template directory to the repository
    for item in template_dir.rglob('*'):
        relative_path = item.relative_to(template_dir)
        destination_path = repo_path / relative_path

        if item.is_dir():
            # Create directory if it doesn't exist
            destination_path.mkdir(parents=True, exist_ok=True)
        else:
            # Copy file and replace if it already exists
            shutil.copy2(item, destination_path)
            print(f"Copied {item} to {destination_path}")
    return True




def process_repos(org_name, repo_names, template_dir, branches, github_token, files_to_remove=None):
    """Process the list of repositories to manage files and update branches, with optional file/folder removal."""
    original_working_dir = os.getcwd()

    for repo_name in repo_names:
        # Clone the repository
        clone_repo(org_name, repo_name, github_token)

        # Change directory to the cloned repository
        os.chdir(repo_name)

        for branch in branches:
            # Checkout the branch
            checkout_branch(branch)

            # Manage files (copy and replace from template directory) and remove specified files
            if manage_files_in_repo(Path(os.getcwd()), template_dir, files_to_remove):
                # Commit and push changes to the current branch only if the template directory exists
                commit_and_push_changes(branch,f"Managed files and pushed updates to {branch} branch")

        # Return to the original working directory
        os.chdir(original_working_dir)

        # Optionally, remove the cloned repository folder after processing
        shutil.rmtree(repo_name)

    print(f"Repositories processed successfully in {org_name}")


def main():
    # List of repositories to process
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


    # GitHub organization name
    org_name = "templates-python"

    # Optional list of files and directories to remove from the repositories
    files_to_remove = []

    # Get the path of the current script
    script_dir = Path(__file__).resolve().parent

    # Directory containing the templates (configurable) in the same path as the script
    template_dir = script_dir / 'templates_for_file_manager'

    # Branches to update
    branches = ['main', 'solution']

    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    # Process the repositories
    process_repos(org_name, repo_names, template_dir, branches, github_token, files_to_remove)


if __name__ == '__main__':
    main()