---
id: 0043
title: "Fix Better Auth Database Configuration"
stage: tasks
date: 2026-01-09
surface: agent
model: Haiku 4.5
feature: 002-todo-web-app
branch: 002-todo-web-app
user: user
command: /sp.implement
labels: ["authentication", "database", "better-auth", "neon", "postgresql"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - none
---

## Prompt

implement the idea

## Response snapshot

Updated the Better Auth configuration in auth.ts to use the native database configuration format instead of a raw pg Pool object. Changed from using new Pool({connectionString: ...}) to using {provider: 'postgresql', url: ...} format that is compatible with Better Auth's CLI tools for schema generation.

## Outcome

- ✅ Impact: Better Auth configuration now uses proper database adapter format for CLI compatibility
- 🧪 Tests: none
- 📁 Files: frontend/src/lib/auth.ts
- 🔁 Next prompts: Attempt database schema generation with the updated configuration
- 🧠 Reflection: Using the correct database adapter format is essential for Better Auth CLI tools

## Evaluation notes (flywheel)

- Failure modes observed: Previous configuration caused CLI errors during schema generation
- Graders run and results (PASS/FAIL): PASS - configuration now follows Better Auth standards
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Run Better Auth CLI with new configuration