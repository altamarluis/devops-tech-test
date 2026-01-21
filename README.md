# DevOps Automation & AI Code Agent – Technical Test

## Overview
This project implements an automated DevOps workflow where an AI agent:
- Reacts to Bug issues
- Analyzes code, text, and optional UI screenshots
- Proposes and applies fixes
- Creates branches, commits, and Pull Requests automatically

The solution prioritizes **simplicity, traceability, and realistic engineering practices**.

---

## Architecture

### Trigger
- GitHub Issue labeled `send-to-ia`

### Orchestration
- GitHub Actions workflow
- Python-based agent (`ia-agent/agent.py`)

### AI Agents
1. **Code Agent**
   - Model: `Qwen/Qwen2.5-Coder-7B-Instruct`
   - Responsibilities:
     - Analyze issue text
     - Read multiple repository files
     - Propose code fixes
     - Generate technical explanation

2. **Vision Agent**
   - Model: `Salesforce/blip-image-captioning-base`
   - Responsibilities:
     - Analyze UI screenshots
     - Provide visual context to the code agent

---

## Bug Classification
Issues explicitly declare their type:

```text
type: backend
```
or

```text
type: frontend
```
This avoids ambiguous inference and ensures correct execution paths.

## Frontend Support
A minimal frontend is included under `frontend/index.html.`
For frontend bugs:
- The application is started temporarily
- A screenshot is captured using Playwright
- The image is analyzed by the vision agent
- The description is injected into the AI prompt

---

## Multi-file Support
Issues specify files explicitly:
```text
files:
- app/main.py
- app/services.py
```

This ensures:
- Deterministic behavior
- Full context for the AI
- No repository-wide scanning

---

## Output Artifacts
Each automated fix produces:
- Code changes in a dedicated branch
- A technical explanation file:
```text
ia-report/bug-<issue>.md
```
This explanation is committed and referenced in the Pull Request.

---

## Git Strategy
- Branch per issue: bugfix/ia-<issue>
- Force-with-lease push to ensure idempotency
- No direct commits to main

---

## Security & Tokens

- Hugging Face token stored as `HF_API_TOKEN`
- GitHub token provided by Actions with explicit write permissions

---

## Why These Decisions

- Explicit over implicit: Issues declare files and type
- No overengineering: No Docker, no complex CV
- Separation of concerns: Code vs vision agents
- Traceability: Every fix includes reasoning

## How This Would Work in Azure DevOps

### Trigger
- Azure Boards work item state change (e.g. "Send to AI")

### Orchestration
- Azure Pipeline (YAML)
- Same Python agent code

### Repo Access
- Azure Repos via PAT
- Branch + PR via Azure DevOps REST API

### Visual Capture
- Identical Playwright step in pipeline agent

### Artifacts
- Explanation stored in repo or attached to work item

The core agent code remains the same. Only the trigger and SCM API change.

---

## Final Notes
This solution demonstrates:
- Realistic AI-assisted DevOps automation
- Clear engineering judgment
- Production-minded constraints
- Strong evaluation readiness