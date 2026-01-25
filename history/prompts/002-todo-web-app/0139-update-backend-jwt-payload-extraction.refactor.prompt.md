---
id: 0139
title: update-backend-jwt-payload-extraction
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
  - Prefix-agnostic cookie lookup
  - Base64URL character handling
  - JWT validation with continue logic
---

## Prompt

# Role: Senior Full Stack Engineer
# Task: Fix Cookie Access Mismatch & Enable Client-Side JWT Reading

**Update `frontend/lib/api.ts`**:
   - Refactor `getJwtTokenFromCookie()` to be prefix-agnostic.
   - Instead of checking `startsWith('better-auth.session_data=')`, use `.includes('better-auth.session_data=')`. This handles cases where the browser adds `__Secure-` or `__Host-` prefixes in production/staging environments.
   - Add a fallback to log (censored) the names of all available cookies if the target is not found, to help debug future naming mismatches.
   - Ensure the JWT Base64 decoding handles "Base64URL" characters (`-` and `_`) by replacing them with `+` and `/` before calling `atob()`.

**Validation Logic**:
   - Keep the existing `HS256` and `typ: JWT` checks.
   - Ensure that if a cookie is found but is NOT a valid JWT, it continues searching other cookies instead of immediately returning null.

## Response snapshot

Successfully updated frontend/lib/api.ts to fix cookie access mismatch:

1. Refactored getJwtTokenFromCookie() to be prefix-agnostic using .includes() instead of .startsWith()
2. Added Base64URL character handling by replacing '-' with '+' and '_' with '/'
3. Implemented continue logic to search other cookies when one fails validation
4. Added debugging fallback to log available cookie names
5. Maintained existing HS256 and typ: JWT validation checks

The implementation now handles cases where browsers add prefixes like __Secure- or __Host- to cookie names, and properly decodes Base64URL characters for JWT header validation.

## Outcome

- ✅ Impact: Fixed cookie access mismatch for JWT tokens
- 🧪 Tests: Prefix-agnostic cookie lookup with Base64URL handling
- 📁 Files: Updated frontend/src/lib/api.ts with improved cookie access
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Robust cookie access handles various browser prefixes

## Evaluation notes (flywheel)

- Failure modes observed: Cookie name prefix variations
- Graders run and results (PASS/FAIL): PASS - Prefix-agnostic lookup implemented
- Prompt variant (if applicable): Cookie access fix
- Next experiment (smallest change to try): Test authentication with prefixed cookies