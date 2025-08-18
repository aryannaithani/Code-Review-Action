import os
import requests
import google.generativeai as genai


repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")
token = os.getenv("GITHUB_TOKEN") 


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"


headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3.diff"}


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

    prompt += "\n-------\nTASK: Provide a concise review of the changes, highlight potential issues, improvements and summarize what this PR id doing.\nFormat your response in Markdown with headings, bullet points, and code blocks where relevant.\nMake use of colorful emojis to convey the goodness or badness of a change.\nIMPORTANT: at the end include a mandatory bold check if the PR should be merged or not."

    response = model.generate_content(prompt)

    with open("gemini_output.txt", "w") as f:
        f.write(response.text)
else:
    print(f"Failed to fetch PR diff: {response.status_code}")
    print(response.text)
