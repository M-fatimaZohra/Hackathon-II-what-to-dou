---
id: 0083
title: update-api-client-jwt
stage: green
date: 2026-01-14
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE COMPUTERS
command: /sp.implement
labels: ["api-client", "jwt", "authentication", "better-auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/lib/api.ts
tests:
 - none
---

## Prompt

/sp.implement
Task: Update frontend API client to attach JWT to all backend requests
File: frontend/src/lib/api.ts
Requirements:
- Remove old authClient.token() calls
- Fetch JWT from /api/auth/token using credentials: include
- Attach JWT in Authorization: Bearer <token> header
- Ensure GET, POST, PUT, DELETE, PATCH all include JWT
- Maintain existing TaskRead, TaskCreate, TaskUpdate logic
Output: Updated api.ts code fully integrated with JWT
Afterwords: save progress in history

## Response snapshot

Updated frontend API client to fetch JWT from /api/auth/token endpoint and attach it to all backend requests with proper Authorization header.

## Outcome

- ✅ Impact: API client now properly fetches JWT from dedicated endpoint and includes it in all requests
- 🧪 Tests: none
- 📁 Files: frontend/src/lib/api.ts
- 🔁 Next prompts: Test API client functionality with JWT authentication
- 🧠 Reflection: Successfully replaced authClient.token() with direct fetch to token endpoint

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test authentication flow end-to-end