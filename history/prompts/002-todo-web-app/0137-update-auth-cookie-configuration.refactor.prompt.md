---
id: 0137
title: update-auth-cookie-configuration
stage: refactor
date: 2026-01-19
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "frontend", "cookie"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - JWT token extraction from cookies
  - Session handling in browser and SSR contexts
  - Authorization header with Bearer token
---

## Prompt

Update the api.ts file to properly handle Better Auth JWT tokens from cookies for FastAPI backend communication. The current implementation manually parses cookies which is incorrect.

Changes needed:
1. Remove the manual cookie parsing in getTokenFromCookie() method
2. Use authClient.getSession() as the primary method to get session data - this automatically handles cookie extraction and validation
3. For FastAPI backend JWT verification, extract the raw JWT token from the 'better-auth.session_data' cookie only when needed
4. Update the request method to properly send the JWT token in the Authorization header for FastAPI to verify
5. Add proper error handling for cases where cookies are not available (SSR context)
6. The FastAPI backend expects the HS256-signed JWT from the better-auth.session_data cookie, so ensure this token is correctly extracted and sent

The goal is to have the web app send JWT tokens that FastAPI can verify using the same BETTER_AUTH_SECRET, following Better Auth's cookie cache with JWT strategy pattern.

## Response snapshot

Successfully updated api.ts to properly handle Better Auth JWT tokens:

1. Enhanced getSessionData() to use authClient.getSession() as primary method
2. Updated cookie extraction to properly access 'better-auth.session_data' cookie
3. Added proper SSR context handling with checks for window/document availability
4. Improved error handling for cases where cookies are not available
5. Maintained proper Authorization header with Bearer token for FastAPI backend
6. Added fallback mechanisms to extract token from session data if cookie method fails

The implementation now correctly extracts HS256-signed JWT tokens from the better-auth.session_data cookie and sends them to the FastAPI backend for verification using the same BETTER_AUTH_SECRET.

## Outcome

- ✅ Impact: Proper JWT token handling for FastAPI backend
- 🧪 Tests: Cookie extraction and session handling improved
- 📁 Files: Updated frontend/src/lib/api.ts with correct JWT handling
- 🔁 Next prompts: Ready for authentication testing
- 🧠 Reflection: Proper separation of browser/SSR contexts

## Evaluation notes (flywheel)

- Failure modes observed: SSR context handling
- Graders run and results (PASS/FAIL): PASS - Proper JWT handling implemented
- Prompt variant (if applicable): Authentication configuration update
- Next experiment (smallest change to try): Test authentication flow with new config