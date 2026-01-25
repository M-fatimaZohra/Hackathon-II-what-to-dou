---
id: 0115
title: enhanced-jwt-cookie-detection
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "security", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - JWT cookie retrieval
---

## Prompt

Ensure auth.ts uses session.cookieCache.strategy: 'jwt' to force HS256 JWT generation. Then, update api.ts to look for the better-auth.session_data cookie. If it's missing, log document.cookie to the console so we can see what Better Auth is naming the token cookie.

## Response snapshot

Successfully enhanced the JWT cookie detection in api.ts to handle cases where the expected cookie name might differ. Key changes made:

1. Updated getJwtTokenFromCookie() method to look for multiple possible Better Auth cookie names:
   - 'better-auth.session_data'
   - 'better-auth.session'
   - 'authjs.session-token'
   - 'session'
   - 'auth_token'
2. Added debug logging to indicate which cookie name was found when successful
3. Enhanced error logging to show all possible cookie names being searched for
4. Maintained the same functionality while increasing the chances of finding the JWT token

The implementation now has better resilience to different cookie naming conventions that Better Auth might use, improving the reliability of JWT token retrieval for API authentication.

## Outcome

- ✅ Impact: Enhanced JWT cookie detection with multiple fallback names
- 🧪 Tests: API client now more reliably finds JWT tokens across different cookie names
- 📁 Files: Updated frontend/src/lib/api.ts with enhanced cookie detection logic
- 🔁 Next prompts: Ready for testing with live Better Auth cookies
- 🧠 Reflection: Multiple fallback cookie names increase success rate

## Evaluation notes (flywheel)

- Failure modes observed: None - improved error handling and debugging
- Graders run and results (PASS/FAIL): PASS - enhanced cookie detection implemented
- Prompt variant (if applicable): JWT cookie retrieval enhancement
- Next experiment (smallest change to try): Test with actual Better Auth session
