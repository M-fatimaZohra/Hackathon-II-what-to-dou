---
id: 0056
title: Refactor API client to use env vars and optimize session
stage: refactor
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.implement
labels: ["frontend", "api", "env-vars", "session", "optimization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/lib/api.ts
 - frontend/.env
tests:
 - none
---

## Prompt

"Refactor frontend/src/lib/api.ts to use environment variables and optimize session handling.

In 'frontend/.env', add 'NEXT_PUBLIC_API_URL=http://localhost:8000/api'.

In 'api.ts', replace the hardcoded 'BASE_URL' with 'process.env.NEXT_PUBLIC_API_URL'.

Refactor the methods to stop calling 'authClient.getSession()' twice.

Modify 'getAuthHeaders' to return BOTH the headers AND the session data (including userId) in a single call to save processing time.

Ensure all fetch calls use the new 'process.env' variable."
## Response snapshot

Successfully refactored API client to use environment variables and optimize session handling.

## Outcome

- ✅ Impact: Refactored API client to use env vars and optimized session handling with single call
- 🧪 Tests: none
- 📁 Files: Updated frontend/src/lib/api.ts and frontend/.env with proper environment configuration
- 🔁 Next prompts: none
- 🧠 Reflection: Single session call optimization reduces redundant API requests and improves performance.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
