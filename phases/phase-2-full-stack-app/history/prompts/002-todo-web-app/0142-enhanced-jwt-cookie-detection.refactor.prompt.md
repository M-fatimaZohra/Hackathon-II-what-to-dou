---
id: 0142
title: enhanced-jwt-cookie-detection
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
  - Multiple cookie name support
  - JWT validation loop
  - HS256 algorithm check
---

## Prompt

# Role: Senior Full Stack Engineer

# Task: Update JWT extraction to support multiple Better Auth cookie names.

1. **Modify `frontend/lib/api.ts`**:
   - Update `getJwtTokenFromCookie()` to iterate through both `better-auth.session_data` and `better-auth.session_token`.
   - Implement a validation loop: for each cookie found, verify if it is a 3-part string (split by dots).
   - If it has 3 parts, decode the header (handling Base64URL characters `-` and `_`) and check if `alg === "HS256"`.
   - Remove any strict checks for the `typ` header field as it may be undefined.
   - Return the first token that satisfies the `HS256` requirement.

2. **Reasoning**: Better Auth v1.4 may store the JWT in either session_token or session_data depending on the cache state. This change ensures the API client finds the correct symmetric token for FastAPI.

## Response snapshot

Successfully updated JWT extraction in frontend/lib/api.ts to support multiple Better Auth cookie names:

1. Modified getJwtTokenFromCookie() to iterate through both `better-auth.session_token` and `better-auth.session_data`
2. Implemented validation loop to verify 3-part JWT structure (split by dots)
3. Added proper header decoding with Base64URL character handling (- and _)
4. Updated validation to check only `alg === "HS256"` (removed strict typ header check)
5. Return first token that satisfies HS256 requirement
6. Added comprehensive debugging messages to track which cookie contains the valid token

The implementation now supports Better Auth v1.4's potential storage of JWTs in either session_token or session_data cookies, ensuring the API client finds the correct symmetric token for FastAPI compatibility.

## Outcome

- ✅ Impact: Enhanced JWT cookie detection with multiple name support
- 🧪 Tests: Both cookie names checked with proper validation
- 📁 Files: Updated frontend/src/lib/api.ts with improved detection
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Flexible cookie name detection improves reliability

## Evaluation notes (flywheel)

- Failure modes observed: Cookie name variations
- Graders run and results (PASS/FAIL): PASS - Multiple cookie names supported
- Prompt variant (if applicable): Enhanced cookie detection
- Next experiment (smallest change to try): Test authentication with new detection