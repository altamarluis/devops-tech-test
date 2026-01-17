import os
from github import Github
from hf_client import analyze

# Leer variables de GitHub
repo_name = os.getenv("GITHUB_REPOSITORY")
issue_number = int(os.getenv("ISSUE_NUMBER"))

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(repo_name)
issue = repo.get_issue(number=issue_number)

prompt = f"""
You are a senior Python developer.

Bug title:
{issue.title}

Bug description:
{issue.body}

Explain the root cause and propose a fix.
"""

response = analyze(prompt)

print("=== IA RESPONSE ===")
print(response)
