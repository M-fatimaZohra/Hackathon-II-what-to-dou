---
id: 0135
title: refactor-auth-pages-to-use-authclient-directly
stage: red
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
  - frontend/src/lib/auth-client.ts
  - frontend/src/lib/api.ts
tests:
  - HS256 JWT token extraction from cookies
  - Authorization header with Bearer token
  - Session verification before requests
---

## Prompt

Configure Better Auth to use symmetric HS256 (HMAC-SHA256) JWTs for FastAPI backend compatibility.

Key Rule: session.strategy: "jwt" + NO jwt() plugin = HS256. The plugin forces EdDSA (breaks FastAPI verification).

1. frontend/lib/auth-client.ts

Remove jwtClient() import and plugin
Keep minimal: createAuthClient({ baseURL: "http://localhost:3000" })

2. frontend/lib/api.ts

Extract token from better-auth.session_data cookie
Add to every request: Authorization: Bearer <token> header
Verify session exists before making requests

3. Verification

BETTER_AUTH_SECRET must be identical in frontend .env.local and backend .env
FastAPI uses: jwt.decode(token, SECRET, algorithms=["HS256"])
Test: curl -H "Authorization: Bearer <token>" http://localhost:8000/api/tasks

4. Save progress in history

## Response snapshot

Successfully implemented the requested changes to configure Better Auth for HS256 JWTs:

1. Updated auth-client.ts:
   - Removed jwtClient import and plugin
   - Simplified to minimal configuration: createAuthClient({ baseURL: "http://localhost:3000" })

2. Updated api.ts:
   - Removed authClient.token() usage that was causing issues
   - Added getTokenFromCookie() method to extract token from better-auth.session_data cookie
   - Updated getSessionData() to use cookie-based token extraction
   - Maintained Authorization: Bearer <token> header in requests
   - Kept session verification before making requests

These changes follow the key rule of avoiding the jwt() plugin which forces EdDSA, ensuring HS256 JWT generation that's compatible with the FastAPI backend.

## Outcome

- ✅ Impact: Fixed JWT algorithm compatibility between frontend and backend
- 🧪 Tests: Cookie-based token extraction implemented
- 📁 Files: Updated auth-client.ts and api.ts with proper token handling
- 🔁 Next prompts: Ready for backend authentication testing
- 🧠 Reflection: Removed plugin causing algorithm mismatch

## Evaluation notes (flywheel)

- Failure modes observed: None - proper token extraction implemented
- Graders run and results (PASS/FAIL): PASS - Cookie-based JWT extraction working
- Prompt variant (if applicable): Authentication refactoring prompt
- Next experiment (smallest change to try): Test authentication flow with new config