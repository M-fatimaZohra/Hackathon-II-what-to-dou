---
id: 2
title: Execute Git Workflow Commit and PR Push Code on Main Branch
stage: general
date_iso: 2025-12-27
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: user
command: sp.git.commit_pr push code on main branch
labels: ["git", "workflow", "commit", "push"]
spec: null
ticket: null
adr: null
pr: null
---

# Files Modified
 - history/prompts/general/0001-execute-git-workflow-commit-and-pr.general.prompt.md
 - phases/

# Tests Run
 - Git status, diff, and log verification
 - Commit and push operations

# Prompt Text
```
/sp.git.commit_pr push code on main branch
```

# Response Text
Successfully executed git workflow:
- Added new PHR record and project phases structure
- Committed 66 new files with message "chore: add PHR record and project phases structure"
- Pushed all changes to remote main branch
- Repository is now up-to-date

# Outcome
Git workflow completed successfully with all changes pushed to main branch as requested.