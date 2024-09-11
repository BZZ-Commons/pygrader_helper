import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from batch_file_manager import manage_files_in_repo
from git_utils import clone_repo, checkout_branch, commit_and_push_changes

from batch_requirements_manager import manage_requirements_file


def process_repos(org_name, repo_names, github_token, template_dir, branches):
    """Process the list of repositories, manage files, and update their requirements.txt across multiple branches."""

    for repo_name in repo_names:
        # Clone the repository
        clone_repo(org_name, repo_name, github_token)

        # Change directory to the cloned repository
        os.chdir(repo_name)

        for branch in branches:
            # Checkout the branch
            checkout_branch(branch)

            # Manage files (copy _run_pylint.py from the template_dir)
            manage_files_in_repo(Path(os.getcwd()), template_dir)

            # Add pylint to requirements.txt
            manage_requirements_file(Path(os.getcwd()), packages_to_add={"pylint": "3.2.7"})

            # Commit and push changes to the current branch
            commit_and_push_changes(branch,f"Added _run_pylint and requirements and pushed updates to {branch} branch")

        # Return to the parent directory
        os.chdir('..')

        # Optionally, remove the cloned repository folder after processing
        shutil.rmtree(repo_name)

    print(f"Repositories processed successfully in {org_name}")


def main():
    # List of repositories to process
    repo_names = [
        "m319-lu04-a01-classroom",
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
    ]

    # GitHub organization name
    org_name = "templates-python"

    # Directory containing the template (configurable)
    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir / 'templates_for_add_run_pylint'

    # Branches to update
    branches = ['main', 'solution']

    # Load GitHub token from the environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return

    # Process the repositories
    process_repos(
        org_name,
        repo_names,
        github_token,
        template_dir,
        branches
    )


if __name__ == '__main__':
    main()
