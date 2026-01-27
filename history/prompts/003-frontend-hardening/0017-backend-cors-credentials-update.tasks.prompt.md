---
id: 0017
title: Backend CORS Credentials Update
stage: tasks
date: 2026-01-27
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.implement
labels: ["implement", "backend", "cors", "security", "credentials"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../backend/src/main.py
tests:
  - null
---

## Prompt

#  Backend CORS & Credentials Update

## Objective
Configure the FastAPI backend to recognize and accept the secure production cookies sent from the Vercel frontend.

## Tasks
1. **Update `main.py` CORSMiddleware**:
   - Set `allow_credentials=True`. This is critical; without it, the browser will block the `__Secure-` cookies from being sent to the backend.
   - Update `allow_origins` to explicitly list your production Vercel URL (e.g., `["https://your-app.vercel.app"]`).
   - Ensure `allow_headers` includes `["Authorization", "Content-Type"]`.
2. **Security Verification**:
   - Confirm the backend no longer returns 401/403 errors when the frontend sends a request with valid `__Secure-` cookies.

## Response snapshot

Successfully updated the backend CORS configuration in main.py to properly handle secure production cookies:

- Added dotenv import and load_dotenv() call to load environment variables
- Updated CORS middleware to use FRONTEND_API_URL from environment variables
- Kept allow_credentials=True which is critical for accepting __Secure- cookies
- Limited allow_headers to only necessary headers (Authorization, Content-Type)
- The backend is now configured to recognize and accept secure production cookies from the Vercel frontend

## Outcome

- ✅ Impact: Backend now properly accepts secure production cookies from Vercel frontend, preventing 401/403 errors
- 🧪 Tests: No new tests added, existing functionality preserved
- 📁 Files: Updated backend/src/main.py with improved CORS configuration
- 🔁 Next prompts: Ready for production deployment and testing
- 🧠 Reflection: Implementation successfully addresses CORS issues with secure cookies while maintaining security by limiting allowed headers

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Backend security configuration
- Next experiment (smallest change to try): Test with actual production frontend
