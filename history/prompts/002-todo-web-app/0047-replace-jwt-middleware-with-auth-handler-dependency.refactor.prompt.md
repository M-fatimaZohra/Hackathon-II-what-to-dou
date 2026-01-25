---
id: 0047
title: Replace JWT middleware with auth handler dependency
stage: refactor
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.implement
labels: ["backend", "auth", "jwt", "middleware", "dependency", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/auth_handler.py
 - backend/main.py
 - backend/routes/tasks.py
tests:
 - none
---

## Prompt

"Create backend/middleware/auth_handler.py. Move the JWT decoding logic from jwt_middleware.py into a function 'get_current_user'. It should take 'token: str = Depends(HTTPBearer())' and return the user_id. Remove the global app.middleware('http')(jwt_middleware) from main.py."

## Response snapshot

Successfully implemented the refactoring to replace JWT middleware with FastAPI dependency injection.

## Outcome

- ✅ Impact: Replaced global JWT middleware with reusable auth dependency using FastAPI's Depends() pattern
- 🧪 Tests: none
- 📁 Files: Created backend/auth_handler.py, updated backend/main.py and backend/routes/tasks.py
- 🔁 Next prompts: none
- 🧠 Reflection: Moving from global middleware to dependency injection makes auth handling more explicit and maintainable.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
