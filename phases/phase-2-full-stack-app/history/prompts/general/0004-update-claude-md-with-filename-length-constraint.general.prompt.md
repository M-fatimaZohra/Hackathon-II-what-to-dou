---
id: 0004
title: Update CLAUDE.md with filename length constraint
stage: general
date: 2025-12-24
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 001-todo-cli
user: A.ZEE
command: manual update
labels: ["documentation", "constraints", "github", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CLAUDE.md
tests:
  - none
---

## Prompt

ok before anything i want you to add in @CLAUDE.md that never exceed 240 characters when naming a file or folder
the reason of this reminder is
github do not accept file/folder which has too long name (259 characters)
i notice that when you are creating history you are using detailed names for each history file.
even if history files have long name, make sure to keep them under 240 characters. any questions

## Response snapshot

Successfully updated CLAUDE.md to include the guideline about not exceeding 240 characters when naming files or folders. The new constraint has been added to the Default policies section to ensure compatibility with GitHub's 259 character limit. This addresses the issue where GitHub doesn't accept files or folders with names longer than 259 characters, which can occur when creating detailed history file names.

## Outcome

- ✅ Impact: Added file naming constraint to prevent GitHub compatibility issues
- 🧪 Tests: none required
- 📁 Files: CLAUDE.md updated with filename length constraint
- 🔁 Next prompts: Continue with planned development work
- 🧠 Reflection: This constraint will help prevent file naming issues when working with GitHub repositories.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure all future file and folder names adhere to the 240 character limit
