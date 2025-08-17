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
    removed_lines = []
    file_paths = set()
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            file_paths.add(line[6:])
        elif line.startswith("--- a/"):
            file_paths.add(line[6:])
        elif line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line[1:])
    if added_lines:
        print("==== ADDED LINES ====")
        for line in added_lines:
            print(line)
    if removed_lines:
        print("==== REMOVED LINES ====")
        for line in removed_lines:
            print(line)
    print("==== ORIGINAL FILES ====")
    for file in file_paths:
        file_url = f"https://raw.githubusercontent.com/{REPO}/main/{file}"
        file_resp = requests.get(file_url, headers=headers)
        if file_resp.status_code == 200:
            print(f"\n--- {file} ---")
            print(file_resp.text[:500])  # print first 500 chars for safety
        else:
            print(f"Could not fetch original {file}")

    # (Later we’ll send this diff to the LLM for analysis)
else:
    print(f"Failed to fetch PR diff: {response.status_code}")
    print(response.text)
