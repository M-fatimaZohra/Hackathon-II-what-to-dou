---
id: 0052
title: Transform api.ts to real API client with auth
stage: refactor
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.implement
labels: ["frontend", "api", "auth", "fetch", "better-auth"]
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

"Transform 'frontend/src/lib/api.ts' from a mock client to a real API client.Import 'authClient' from '@/lib/auth-client'.Define a base URL: 'http://localhost:8000/api'.Create a private helper 'getAuthHeaders' that:Calls 'await authClient.getSession()'.Throws an error if no session exists.Returns an object with 'Authorization: Bearer <token>' and 'Content-Type: application/json'.Rewrite all methods (getTasks, createTask, updateTask, deleteTask, toggleTaskCompletion) to use 'fetch'.Match the FastAPI routes:All paths must include the user ID: '/api/${userId}/tasks/...'.'toggleTaskCompletion' must use the PATCH method to '/api/${userId}/tasks/${id}/complete'.Ensure the class remains compatible with existing UI components by returning the same types."

## Response snapshot

Successfully transformed api.ts from mock client to real API client with authentication integration.

## Outcome

- ✅ Impact: Transformed mock API client to real API client with proper auth integration
- 🧪 Tests: none
- 📁 Files: Updated frontend/src/lib/api.ts with real API implementation
- 🔁 Next prompts: none
- 🧠 Reflection: Replacing mock implementations with real API calls enables full backend integration.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
