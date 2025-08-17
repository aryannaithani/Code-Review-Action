import os
import requests

# 1. Get environment variables set by GitHub Actions
repo = os.getenv("GITHUB_REPOSITORY")     # e.g., "username/reponame"
pr_number = os.getenv("PR_NUMBER")        # set in workflow
token = os.getenv("GITHUB_TOKEN")         # GitHub automatically provides this

# 2. GitHub API URL for the PR diff
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3.diff"  # this gives us raw diff instead of JSON
}

# 3. Fetch the diff
response = requests.get(url, headers=headers)

if response.status_code == 200:
    diff = response.text
    added_lines = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line)
    print("==== ADDED LINES ====")
    for line in added_lines:
        print(line)

    # (Later we’ll send this diff to the LLM for analysis)
else:
    print(f"Failed to fetch PR diff: {response.status_code}")
    print(response.text)
