import os
import requests
from openai import OpenAI

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
            
    prompt = f"""
    You are reviewing a pull request.
    ## Original File(s) ##
    """
    for file in file_paths:
        file_url = f"https://raw.githubusercontent.com/{repo}/main/{file}"
        file_resp = requests.get(file_url, headers=headers)
        if file_resp.status_code == 200:
            prompt += f"\n--- {file} ---\n{file_resp.text}\n"
        else:
            print(f"Could not fetch original {file}")

    if added_lines:
        prompt += f"\n\n## Added Lines ##\n{chr(10).join(added_lines)}\n"
    if removed_lines:
        prompt += f"\n\n## Removed Lines ##\n{chr(10).join(removed_lines)}\n"

    prompt += "\n-------\nTASK: Provide a concise review of the changes, highlight potential issues, improvements and summarize what this PR id doing."

    client = OpenAI(api_key="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")

    resp = client.chat.completions.create(model="gpt-4o-mini",messages=[{"role": "user", "content": prompt}],)

    print("==== LLM REVIEW START ====")
    print(resp.choices[0].message.content.strip())
    print("==== LLM REVIEW END ====")
else:
    print(f"Failed to fetch PR diff: {response.status_code}")
    print(response.text)
