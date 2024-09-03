# A collection of scripts and tools for working with pygrader.

## Pre-requisites
.env file with the following variables:
```
GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
```

## Scripts

### unittest_json_generator.py
Generates a unittest.json and pytest.json file for a given repository. 
Using a GUI Project selector.

### list_all_repos_in_org_with_filter.py
Lists all the repositories in a given organization with a filter.

### batch_add_run_pylint_to_repos.py
Lets you add pylint to all the repositories in a given organization.
Using a list from list_all_repos_in_org_with_filter.py

### batch_converter_old_to_new.py
Converts the old pygrader format (2023) to the new pygrader format (2024).
Using a list from list_all_repos_in_org_with_filter.py

### move_repo_to_orga.py
Moves a batch of repositories from one organization to another.
Using a list from list_all_repos_in_org_with_filter.py

### old_repo_to_new_converter.py
Converts a single repository from the old pygrader format (2023) to the new pygrader format (2024).
Using a GUI Project selector.

