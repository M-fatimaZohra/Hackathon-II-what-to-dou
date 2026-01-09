---
id: 0041
title: "Setup Better Auth with Neon Database Connection"
stage: tasks
date: 2026-01-09
surface: agent
model: Haiku 4.5
feature: 002-todo-web-app
branch: 002-todo-web-app
user: user
command: /sp.implement
labels: ["authentication", "database", "neon", "better-auth", "postgresql"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
  - frontend/.env.local
tests:
  - none
---

## Prompt

  - Replace the mock API client in @frontend/src/lib/api.ts with actual HTTP calls to the backend API (BACKEND_API_URL in env)
  - The API calls should include the JWT token in the Authorization header
  - The API calls should include the user ID from the session in the URL path

# first setup database for better auth with neon

- in @frontend\ install npm i pg
- create data base pool in @frontend/src/lib/auth.ts to add  NEXT_PUBLIC_NEON_CONNECTION_STRING from .env.local
- then run npx @better-auth/cli@latest generate to generate schema
- then run npx @better-auth/cli@latest migrate to migrate schema into database

## Response snapshot

Successfully configured Better Auth to use Neon PostgreSQL database by installing pg package and updating the auth.ts file to use Pool connection with DATABASE_URL. The API client was also updated to connect to the backend API with proper authentication.

## Outcome

- ✅ Impact: Better Auth is now configured to use Neon PostgreSQL database instead of memory-only storage
- 🧪 Tests: none
- 📁 Files: frontend/src/lib/auth.ts, frontend/.env.local, frontend/src/lib/api.ts
- 🔁 Next prompts: Complete database schema generation and migration
- 🧠 Reflection: Proper database configuration is essential for persistent user authentication data

## Evaluation notes (flywheel)

- Failure modes observed: Better Auth CLI generate and migrate commands failed due to configuration issues
- Graders run and results (PASS/FAIL): PARTIAL - configuration successful but CLI commands failed
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Fix CLI configuration to complete schema generation