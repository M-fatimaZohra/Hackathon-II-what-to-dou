---
id: 0053
title: Prepare for full-stack test with backend and frontend
stage: misc
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.implement
labels: ["full-stack", "test", "backend", "frontend", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - none
tests:
 - none
---

## Prompt

"Everything is ready for a full-stack test.

Ensure the FastAPI backend is running (port 8000) and Next.js is running (port 3000).

Open the browser to the /signup page.

Create a test account.

Verify that the redirect to /tasks works.

Create a task and confirm it doesn't disappear on refresh (which proves it hit Neon!).

If anything fails, check the FastAPI logs for '401 Unauthorized' and the browser console for CORS errors."

## Response snapshot

Prepared instructions for full-stack testing, including commands to start backend and frontend servers.

## Outcome

- ✅ Impact: Provided clear instructions for full-stack testing of the integrated application
- 🧪 Tests: none
- 📁 Files: none
- 🔁 Next prompts: none
- 🧠 Reflection: Full-stack testing requires coordinated startup of both backend and frontend services.

## Evaluation notes (flywheel)

- Failure modes observed: Cannot start long-running processes directly in this environment
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
