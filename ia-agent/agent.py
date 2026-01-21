import os
import re
import subprocess
from github import Github
from hf_client import analyze

# Environment variables
repo_name = os.getenv("GITHUB_REPOSITORY")
issue_number = int(os.getenv("ISSUE_NUMBER"))
gh_token = os.getenv("GITHUB_TOKEN")

# GitHub client
g = Github(gh_token)
repo = g.get_repo(repo_name)
issue = repo.get_issue(number=issue_number)

# Extract multiple files from issue body
files_section = re.search(r"files:\s*((?:- .+\n?)*)", issue.body)
if not files_section:
    raise Exception("No files specified. Use:\nfiles:\n- path/to/file.py")

files = [
    line.replace("-", "").strip()
    for line in files_section.group(1).splitlines()
    if line.strip()
]

# Read all files
files_content = ""
for path in files:
    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    with open(path, "r") as f:
        files_content += f"\nFILE: {path}\n"
        files_content += f.read()
        files_content += "\n"

# Prompt for IA
prompt = f"""
You are a senior Python developer.

The following files contain a bug.

{files_content}

Bug description:
{issue.body}

Return TWO sections in this EXACT format:

=== FIXED FILES ===
FILE: path/to/file.py
<code>

FILE: path/to/other.py
<code>

=== TECHNICAL EXPLANATION ===
<markdown explanation>
"""

response = analyze(prompt)

# Split response
parts = response.split("=== TECHNICAL EXPLANATION ===")
if len(parts) != 2:
    raise Exception("IA response missing technical explanation")

files_part = parts[0].replace("=== FIXED FILES ===", "").strip()
explanation = parts[1].strip()

# Parse fixed files
pattern = r"FILE:\s*(.+?)\n([\s\S]*?)(?=FILE:|$)"
matches = re.findall(pattern, files_part)

if not matches:
    raise Exception("IA did not return files in expected format")

written_files = []

for path, content in matches:
    path = path.strip()
    content = content.replace("```python", "").replace("```", "").strip()

    with open(path, "w") as f:
        f.write(content)

    written_files.append(path)

# Write technical report
os.makedirs("ia-report", exist_ok=True)
report_path = f"ia-report/bug-{issue_number}.md"

with open(report_path, "w") as f:
    f.write(explanation)

# Git operations
branch = f"bugfix/ia-{issue_number}"
subprocess.run(["git", "checkout", "-b", branch], check=True)
subprocess.run(["git", "add"] + written_files + [report_path], check=True)
subprocess.run(
    ["git", "commit", "-m", f"fix: ia fix with technical report for bug #{issue_number}"],
    check=True
)
subprocess.run(
    ["git", "push", "--force-with-lease", "origin", branch],
    check=True
)
# Create Pull Request
pr = repo.create_pull(
    title=f"IA fix for bug #{issue_number}",
    body=f"Auto-generated fix for files:\n" + "\n".join(written_files),
    head=branch,
    base="main"
)

print("PR CREATED:", pr.html_url)
