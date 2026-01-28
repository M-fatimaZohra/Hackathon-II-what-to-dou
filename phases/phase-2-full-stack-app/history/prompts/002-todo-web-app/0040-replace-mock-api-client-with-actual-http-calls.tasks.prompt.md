---
id: 0040
title: "Replace Mock API Client With Actual HTTP Calls"
stage: tasks
date: 2026-01-09
surface: agent
model: Haiku 4.5
feature: 002-todo-web-app
branch: 002-todo-web-app
user: user
command: /sp.implement
labels: ["api", "integration", "frontend", "backend", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
  - frontend/.env.local
tests:
  - none
---

## Prompt

  - Replace the mock API client in @frontend/src/lib/api.ts with actual HTTP calls to the backend API (BACKEND_API_URL in env)
  - The API calls should include the JWT token in the Authorization header
  - The API calls should include the user ID from the session in the URL path

## Response snapshot

Replaced the mock API client in frontend/src/lib/api.ts with actual HTTP calls to the backend API, including proper JWT token handling and user ID from session in URL path.

## Outcome

- ✅ Impact: Successfully connected frontend to backend API, replacing mock data with real HTTP requests for task management
- 🧪 Tests: none
- 📁 Files: frontend/src/lib/api.ts, frontend/.env.local
- 🔁 Next prompts: none
- 🧠 Reflection: Properly connecting frontend and backend with authentication is crucial for user data isolation

## Evaluation notes (flywheel)

- Failure modes observed: Initially saved in wrong directory (general instead of feature-specific)
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Improve directory routing for PHR creation
