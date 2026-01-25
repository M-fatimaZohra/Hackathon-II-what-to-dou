---
id: 0051
title: Configure Better Auth CLI to use Neon database
stage: green
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.implement
labels: ["frontend", "auth", "cli", "database", "neon", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/.env
tests:
 - none
---

## Prompt

"I am getting a connection error because the Better Auth CLI isn't reading '.env.local'.

Find the active Neon 'DATABASE_URL' in the project (check backend/.env if needed).

Create or update 'frontend/.env' (not .env.local) with this exact URL.

Ensure 'sslmode=require' is appended to the connection string if it is missing.

Run 'npx @better-auth/cli migrate' from the frontend directory.

If successful, run 'uv run backend/init_db.py' to ensure both the auth tables and the task tables exist in the same active Neon branch."

## Response snapshot

Successfully configured Better Auth CLI to use Neon database and ran migrations for both auth and task tables.

## Outcome

- ✅ Impact: Created frontend/.env with proper DATABASE_URL, ran auth migrations and task table initialization
- 🧪 Tests: none
- 📁 Files: Created frontend/.env with Neon database configuration
- 🔁 Next prompts: none
- 🧠 Reflection: Proper environment configuration enables CLI tools to access the correct database.
- ✅ Both auth and task tables now exist in the same Neon branch

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
