---
id: 0005
title: Correct frontend hardening tasks with proper env vars
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.tasks
labels: ["tasks", "frontend", "security", "correction"]
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

mistake!

the frontend base url is in NEXT_PUBLIC_BASE_URL not in BETTER_AUTH_URL
in api.ts the only updates are: update BASE_URL = process.env.NEXT_PUBLIC_API_URL


in auth.ts the updates for env are:

baseURL: "process.env.NEXT_PUBLIC_BASE_URL",
trustedOrigins: ["process.env.NEXT_PUBLIC_BASE_URL"],



in auth-client.ts the updates are:
baseURL: "process.env.NEXT_PUBLIC_BASE_URL",

## Response snapshot

Successfully corrected the tasks for frontend production implementation with:
- Updated environment variable references to use NEXT_PUBLIC_BASE_URL consistently for frontend base URLs
- Corrected auth.ts updates to use process.env.NEXT_PUBLIC_BASE_URL for both baseURL and trustedOrigins
- Corrected auth-client.ts updates to use process.env.NEXT_PUBLIC_BASE_URL
- Maintained api.ts updates to use process.env.NEXT_PUBLIC_API_URL
- All 30 tasks updated with correct environment variable references

## Outcome

- ✅ Impact: Corrected environment variable references in implementation tasks
- 🧪 Tests: No tests created (task correction phase)
- 📁 Files: Updated tasks.md with correct environment variable usage
- 🔁 Next prompts: Ready for implementation phase with correct configuration
- 🧠 Reflection: Tasks now properly reflect the correct environment variable usage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Correction of existing tasks
- Next experiment (smallest change to try): Begin implementation with corrected tasks
