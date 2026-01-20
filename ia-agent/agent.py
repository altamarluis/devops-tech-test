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

# Extract target file from issue body
match = re.search(r"file:\s*(.+)", issue.body)
if not match:
    raise Exception("No file specified in issue. Use: file: path/to/file.py")

target_file = match.group(1).strip()

if not os.path.exists(target_file):
    raise Exception(f"File not found: {target_file}")

# Read current file content
with open(target_file, "r") as f:
    current_code = f.read()

# Prompt for IA
prompt = f"""
You are a senior Python developer.

The following file contains a bug.

File path:
{target_file}

Current code:
{current_code}

Bug description:
{issue.body}

Return ONLY the full corrected content of the file.
Do not add explanations.
"""

fixed_code = analyze(prompt)

# Clean markdown if present
fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

# Minimal validation
if len(fixed_code.strip()) < 20:
    raise Exception("IA returned empty or invalid code")

# Write corrected file
with open(target_file, "w") as f:
    f.write(fixed_code)

# Git operations
branch = f"bugfix/ia-{issue_number}"
subprocess.run(["git", "checkout", "-b", branch], check=True)
subprocess.run(["git", "add", target_file], check=True)
subprocess.run(
    ["git", "commit", "-m", f"fix: ia fix for bug #{issue_number}"],
    check=True
)
subprocess.run(
    ["git", "push", "--force-with-lease", "origin", branch],
    check=True
)
# Create Pull Request
pr = repo.create_pull(
    title=f"IA fix for bug #{issue_number}",
    body=f"Auto-generated fix for `{target_file}`",
    head=branch,
    base="main"
)

print("PR CREATED:", pr.html_url)
