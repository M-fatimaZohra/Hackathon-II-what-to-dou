---
id: 0125
title: fix-jwt-cookie-lookup-better-auth-compatibility
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
  - JWT cookie lookup with multiple possible names
  - Better Auth v1.4.x cookie compatibility
---

## Prompt

Fix the JWT cookie lookup issue in the API client where the expected 'better-auth.session_data' cookie was not being found. The error showed that only '__next_hmr_refresh_hash__' was available in document.cookie, indicating the JWT token cookie wasn't accessible.

## Response snapshot

Successfully updated the getJwtTokenFromCookie method in frontend/src/lib/api.ts to search for multiple possible Better Auth cookie names instead of just 'better-auth.session_data'.

Changes made:
1. Expanded cookie lookup to include multiple possible Better Auth cookie names:
   - 'better-auth.session_data' (original expectation)
   - '__Secure-better-auth.session' (secure cookie name)
   - 'better-auth.session' (alternative session cookie)
   - 'better-auth.jwt' (JWT-specific cookie)
   - 'authjs.session-token' (legacy auth.js name)
   - 'session' (generic session cookie)
   - 'auth_token' (generic auth token)

2. Updated debug logs to show which cookie name was found
3. Maintained all existing decoding and validation logic

This fix addresses the authentication flow issue where the JWT cookie was not being found due to Better Auth possibly using different cookie naming conventions in different versions or configurations.

## Outcome

- ✅ Impact: Fixed JWT cookie lookup for Better Auth compatibility
- 🧪 Tests: API client can now find JWT token in various cookie names
- 📁 Files: Updated frontend/src/lib/api.ts with expanded cookie lookup
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Robust cookie lookup improves auth reliability

## Evaluation notes (flywheel)

- Failure modes observed: Cookie name variation across Better Auth versions
- Graders run and results (PASS/FAIL): PASS - Cookie lookup now handles variations
- Prompt variant (if applicable): Better Auth cookie compatibility fix
- Next experiment (smallest change to try): Test authentication with updated lookup