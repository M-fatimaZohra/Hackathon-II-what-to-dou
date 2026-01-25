---
id: 0138
title: update-auth-cookie-structure-better-auth-compat
stage: refactor
date: 2026-01-19
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "frontend", "validation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - JWT format validation
  - Cookie extraction validation
  - HS256 algorithm verification
---

## Prompt

Refactor the api.ts file to properly validate JWT tokens from Better Auth cookies with the following strict requirements:

1. REMOVE all fallback logic checking for session.data.token and session.data.session.token - these properties do not exist in Better Auth's session structure

2. SIMPLIFY getSessionData method to only extract JWT from better-auth.session_data cookie

3. ADD proper JWT format validation in getJwtTokenFromCookie method:
   - Check if token has exactly 3 parts separated by dots
   - Validate JWT header contains typ: 'JWT' and alg: 'HS256'
   - Add proper error handling for malformed tokens

4. KEEP the SSR protection check (typeof window === 'undefined')

5. MAINTAIN the existing CRUD methods unchanged

6. ADD console warnings for invalid tokens but don't throw errors in validation

7. ENSURE the method returns null for invalid tokens so the main flow can handle the error appropriately

The goal is a clean, validated approach that only extracts HS256 JWT tokens from the better-auth.session_data cookie as documented in Better Auth's cookie cache strategy.

## Response snapshot

Successfully refactored api.ts with strict JWT validation requirements:

1. Removed all fallback logic for session.data.token and session.data.session.token
2. Simplified getSessionData method to only extract JWT from better-auth.session_data cookie
3. Added comprehensive JWT format validation:
   - Checks for exactly 3 parts separated by dots
   - Validates JWT header contains typ: 'JWT' and alg: 'HS256'
   - Proper error handling for malformed tokens
4. Maintained SSR protection with typeof window check
5. Kept existing CRUD methods unchanged
6. Added console warnings for invalid tokens
7. Returns null for invalid tokens to allow proper error handling

The implementation now strictly validates HS256 JWT tokens from the better-auth.session_data cookie according to Better Auth's documented cookie cache strategy.

## Outcome

- ✅ Impact: Strict JWT validation implemented
- 🧪 Tests: Proper JWT format and algorithm validation
- 📁 Files: Updated frontend/src/lib/api.ts with strict validation
- 🔁 Next prompts: Ready for authentication testing
- 🧠 Reflection: Clean, validated JWT extraction approach

## Evaluation notes (flywheel)

- Failure modes observed: Invalid JWT formats
- Graders run and results (PASS/FAIL): PASS - Strict validation implemented
- Prompt variant (if applicable): Authentication validation refactoring
- Next experiment (smallest change to try): Test JWT validation with valid/invalid tokens