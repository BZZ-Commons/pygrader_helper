import subprocess

def transfer_repos(repo_list, current_owner, new_owner):
    """
    Transfers a list of repositories from one owner to another using the GitHub CLI.

    Parameters:
    repo_list (list): List of repository names to be transferred.
    current_owner (str): Current owner of the repositories.
    new_owner (str): New owner of the repositories.

    Returns:
    None
    """
    for repo in repo_list:
        command = f'gh api repos/{current_owner}/{repo}/transfer -f new_owner={new_owner}'
        try:
            print(f'Transferring repo {repo} from {current_owner} to {new_owner}')
            subprocess.run(command, shell=True, check=True)
            print(f'Successfully transferred {repo}')
        except subprocess.CalledProcessError as e:
            print(f'Failed to transfer {repo}: {e}')

if __name__ == '__main__':
    # List of repositories to transfer
    repos_to_transfer = [
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
        "m319-lu04-a00-first",
        "m319-lu08-a01-syntaxfehler-1",
        "m319-lu08-a02-syntaxfehler-2",
        "m319-lu08-a03-logikfehler",
        "m319-lb01-primes",
        "m319-lb01-words",
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
        "m319-lb02-echarge",
        "m319-lb02a-efuel",

        # Add more repositories here
    ]

    # Current owner of the repositories
    current_owner = "BZZ-M319"

    # New owner of the repositories
    new_owner = "templates-python"

    # Transfer the repositories
    transfer_repos(repos_to_transfer, current_owner, new_owner)