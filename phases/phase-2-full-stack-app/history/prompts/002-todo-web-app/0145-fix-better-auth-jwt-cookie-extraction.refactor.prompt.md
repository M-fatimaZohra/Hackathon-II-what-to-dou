---
id: 0145
title: fix-better-auth-jwt-cookie-extraction
stage: refactor
date: 2026-01-21
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
  - JWT cookie extraction with startsWith
  - Proper substring calculation
  - HS256 token validation
---

## Prompt

Fix Better Auth JWT cookie extraction: getJwtTokenFromCookie() method fails to parse better-auth.session_data cookie. Issue is using cookie.includes() instead of cookie.startsWith() and incorrect substring calculation. Need to properly extract JWT from Better Auth cookieCache with JWT strategy.

## Response snapshot

Successfully fixed the JWT cookie extraction in getJwtTokenFromCookie():

1. Changed from using cookie.includes() to cookie.startsWith() for more precise cookie name matching
2. Corrected the substring calculation to properly extract token value after the equals sign
3. Used proper index calculation with cookie.substring('better-auth.session_data='.length) instead of indexOf + 1 approach
4. Maintained both session_data and session_token cookie checks for comprehensive coverage
5. Preserved all JWT validation logic including 3-part structure check, Base64URL character handling, and HS256 algorithm verification

The fix addresses the root cause where the previous implementation was using includes() which could match substrings incorrectly, and the substring calculation was not properly extracting the cookie value. Now the method properly extracts JWT tokens from Better Auth's cookieCache with JWT strategy.

## Outcome

- ✅ Impact: Fixed JWT cookie extraction from Better Auth
- 🧪 Tests: Proper startsWith matching and substring calculation
- 📁 Files: Updated frontend/src/lib/api.ts with correct extraction
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Precise cookie name matching improves reliability

## Evaluation notes (flywheel)

- Failure modes observed: Cookie name matching and substring calculation
- Graders run and results (PASS/FAIL): PASS - Proper cookie extraction implemented
- Prompt variant (if applicable): Cookie extraction fix
- Next experiment (smallest change to try): Test JWT extraction with fixed method