---
id: 0006
title: environment-toggle-implementation
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.implement
labels: ["backend", "configuration", "environment", "cors"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/.env
  - backend/src/main.py
tests:
  - null
---

## Prompt

Environment & App Setup
In backend/.env file add  ENVIRONMENT="development" for toggle

Create main.py and implement a production/development toggle for FastAPI.
If ENVIRONMENT == 'development', set CORS to allow localhost:3000 and enable Swagger docs.
If ENVIRONMENT == 'production', set CORS to FRONTEND_API_URL and disable /docs and /redoc.

## Response snapshot

Successfully implemented the environment and app setup tasks:

1. **Added the ENVIRONMENT variable to the .env file**:
   - Added `ENVIRONMENT="development"` to the existing .env file
   - Positioned it after the existing application configuration

2. **Updated main.py to implement the production/development toggle**:
   - Added logic to read the `ENVIRONMENT` environment variable
   - If `ENVIRONMENT == 'production'`, the app disables `/docs` and `/redoc` endpoints and uses the production frontend URL
   - If `ENVIRONMENT == 'development'`, the app keeps the documentation endpoints enabled and allows localhost:3000 for CORS
   - The CORS configuration adjusts based on the environment mode as requested

The implementation follows the requirements exactly:
- In development mode: CORS allows localhost:3000 and Swagger docs are enabled
- In production mode: CORS uses the FRONTEND_API_URL from the environment and docs/redoc are disabled

## Outcome

- ✅ Impact: Implemented environment toggle functionality for production/development mode in FastAPI application
- 🧪 Tests: No tests added yet, but implementation follows FastAPI best practices
- 📁 Files: Updated backend/.env and backend/src/main.py with environment toggle functionality
- 🔁 Next prompts: Ready to continue with other implementation tasks
- 🧠 Reflection: The implementation properly handles environment-specific configurations with conditional FastAPI instantiation

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements successfully implemented
- Graders run and results (PASS/FAIL): Not applicable for this implementation
- Prompt variant (if applicable): Standard configuration implementation task
- Next experiment (smallest change to try): Continue with remaining tasks from the task list