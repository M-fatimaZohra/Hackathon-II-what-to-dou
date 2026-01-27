---
id: 0011
title: Update auth-client.ts and api.ts with env vars
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.implement
labels: ["tasks", "frontend", "security", "auth-client", "api", "environment-variables"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../frontend/src/lib/auth-client.ts
  - ../../frontend/src/lib/api.ts
  - ../../specs/003-frontend-hardening/tasks.md
tests:
  - null
---

## Prompt

go to auth\_client.ts and update   baseURL: 'http://localhost:3000', to   baseURL: process.env.NEXT\_PUBLIC\_BASE\_URL,

go to api.ts and update const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'; to const BASE_URL = process.env.NEXT_PUBLIC_API_URL!

then update task.md acording to the updates

## Response snapshot

Successfully implemented the requested changes:

- Updated auth-client.ts: Changed baseURL from 'http://localhost:3000' to process.env.NEXT_PUBLIC_BASE_URL!
- Updated api.ts: Changed BASE_URL from process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api' to process.env.NEXT_PUBLIC_API_URL!
- Updated tasks.md: Marked tasks T011-T016 as completed [X] since they have been implemented
- Both files now properly use environment variables instead of hardcoded localhost URLs for production readiness
- Strict null assertion operator (!) added to ensure environment variables are defined

## Outcome

- ✅ Impact: Improved security and production readiness by removing hardcoded URLs
- 🧪 Tests: No tests affected by these changes
- 📁 Files: Updated auth-client.ts, api.ts, and tasks.md with environment variable configuration
- 🔁 Next prompts: Ready to proceed with remaining implementation tasks
- 🧠 Reflection: Implementation completed successfully with proper environment variable usage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Implementation of environment variable configuration
- Next experiment (smallest change to try): Proceed with remaining tasks in the task list
