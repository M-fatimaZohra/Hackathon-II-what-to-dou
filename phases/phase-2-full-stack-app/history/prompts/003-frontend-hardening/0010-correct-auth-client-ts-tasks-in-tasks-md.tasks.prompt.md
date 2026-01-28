---
id: 0010
title: Correct auth-client.ts tasks in tasks.md
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.tasks
labels: ["tasks", "frontend", "security", "auth-client", "correction"]
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

solve mistakes:
Mistake 1: auth_client.ts (which was mistakenly named api-client.ts) only needs conversion from   http://localhost:3000 to process.env.NEXT_PUBLIC_BASE_URL!

so update the following tasks to refine tasks.md
[ ] T014
[ ] T015
[ ] T016

## Response snapshot

Successfully updated the tasks in tasks.md to correct the auth-client.ts file reference and environment variable conversion:

- Updated T014: Changed from searching in api-client.ts to auth-client.ts for http://localhost:3000
- Updated T015: Changed from updating api-client.ts to auth-client.ts with process.env.NEXT_PUBLIC_BASE_URL
- Updated T016: Changed from updating api-client.ts to auth-client.ts with NEXT_PUBLIC_BASE_URL guard clause
- All tasks now correctly reference auth-client.ts instead of api-client.ts
- Environment variable changed from NEXT_PUBLIC_API_URL to NEXT_PUBLIC_BASE_URL as required

## Outcome

- ✅ Impact: Corrected file references in implementation tasks for auth-client.ts
- 🧪 Tests: No tests affected by this task correction
- 📁 Files: Updated tasks.md with correct file and environment variable references
- 🔁 Next prompts: Ready to proceed with implementation tasks
- 🧠 Reflection: Tasks now correctly represent the actual project structure and requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Task correction
- Next experiment (smallest change to try): Proceed with implementation of corrected tasks
