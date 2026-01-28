---
id: 0021
title: Update Tasks for Production Auth Visibility Fix
stage: tasks
date: 2026-01-27
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.tasks
labels: ["tasks", "authentication", "security", "production"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/tasks.md
tests:
  - null
---

## Prompt

update task.md
Locate the current task list and refactor it to include a new priority group: 'Production Auth Visibility Fix'.

Ensure the following specific sub-tasks are integrated:

[ ] Change session_data attribute httpOnly to false in frontend/src/lib/auth.ts.

[ ] Verify session_token remains httpOnly: true for core session security.

## Response snapshot

Successfully updated the tasks.md file to include the new "Production Auth Visibility Fix" priority group with the specified sub-tasks:

- Updated T020 task to indicate selective httpOnly settings will be applied separately
- Changed T020 status from [X] to [ ] since the task is not yet complete with the new requirements
- Added new Priority Group: "Production Auth Visibility Fix"
- Added task T037: Change session_data attribute httpOnly to false in frontend/src/lib/auth.ts
- Added task T038: Verify session_token remains httpOnly: true for core session security in frontend/src/lib/auth.ts
- Ensured "Phase N: Polish & Cross-Cutting Concerns" stays at the end as requested

The updates implement the "Surgical Fix" approach where session_data has httpOnly: false to allow JWT extraction while session_token maintains httpOnly: true for security.

## Outcome

- ✅ Impact: Tasks now properly reflect the selective httpOnly configuration approach for production authentication
- 🧪 Tests: No new tests added, existing functionality preserved
- 📁 Files: Updated tasks.md with new priority group and tasks
- 🔁 Next prompts: Ready for implementation of the selective httpOnly configuration
- 🧠 Reflection: Successfully balanced security requirements with functional needs for cross-domain JWT transmission

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Task list update
- Next experiment (smallest change to try): Implement the new authentication visibility tasks
