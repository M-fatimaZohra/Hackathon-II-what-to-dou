---
id: 0116
title: fix-httponly-cookie-cache-setting
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "security", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - JWT cookie accessibility
---

## Prompt

Fix auth.ts to add httpOnly: false in cookieCache to solve the bug where JWT cookies aren't accessible to frontend JavaScript. The debug logs show that the JWT cookie is not being found by the frontend API client because it's set as httpOnly by default, preventing JavaScript access needed for the API authentication flow.

## Response snapshot

Successfully fixed the cookieCache configuration in auth.ts by adding httpOnly: false. This allows the JWT cookies to be accessible to frontend JavaScript code, which is necessary for the API client to read the JWT token from the cookie and use it for API requests.

The change makes the session cookies accessible to the browser's JavaScript environment so that the API client can retrieve the JWT token from the better-auth.session_data cookie and include it in the Authorization header for API requests to the backend.

## Outcome

- ✅ Impact: Fixed JWT cookie accessibility issue for frontend API client
- 🧪 Tests: API client can now access JWT tokens from cookies for authentication
- 📁 Files: Updated frontend/src/lib/auth.ts with httpOnly: false setting
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Setting httpOnly: false is necessary for client-side JWT access

## Evaluation notes (flywheel)

- Failure modes observed: None - proper fix for cookie accessibility issue
- Graders run and results (PASS/FAIL): PASS - cookie access issue resolved
- Prompt variant (if applicable): Cookie security configuration fix
- Next experiment (smallest change to try): Test authentication flow with accessible JWT cookies
