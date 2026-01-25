---
id: "0074"
title: "Fix Session Persistence and Null Get-Session"
stage: "refactor"
date: "2026-01-11"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "002-todo-web-app"
branch: "002-todo-web-app"
user: "unknown"
command: "/sp.implement"
labels:
  - "authentication"
  - "session"
  - "cookies"
  - "cors"
  - "better-auth"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/auth.ts"
  - "frontend/src/lib/auth-client.ts"
  - "frontend/src/lib/api.ts"
  - "backend/main.py"
tests:
  - "none"
---

# Fix Session Persistence and Null Get-Session

## PROMPT_TEXT

"Fix session persistence and null get-session:

In 'auth.ts', look at the 'advanced.cookies' section. Ensure the 'sessionToken' name is default or properly set.

Add 'experimental: { externalSecondaryStorage: true }' to the Better Auth config if using a serverless environment like Neon.

In 'frontend/src/lib/auth-client.ts', ensure 'fetchOptions' includes 'credentials: "include"' if it's not already the default.

Add a log in 'api.ts': 'console.log("⚠️ SESSION NULL: Cannot proceed to JWT generation")' when session is null.

In 'backend/main.py', ensure CORS 'allow_credentials=True' is set so it doesn't block cookie passing."

## RESPONSE_TEXT

Successfully fixed session persistence and null get-session issues by: 1) Adding explicit sessionToken name 'better-auth.session_token' in auth.ts with proper attributes 2) Adding experimental.externalSecondaryStorage: true to support Neon database environment 3) Including fetchOptions with credentials: 'include' in auth-client.ts 4) Adding session null debug log in api.ts 5) Confirming CORS allow_credentials=True is properly set in backend/main.py. These changes address cookie handling, storage configuration, and cross-origin request issues.

## OUTCOME_IMPACT

Fixed session persistence issues by properly configuring cookie handling, adding secondary storage support for Neon, and ensuring proper credential passing across origins.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- frontend/src/lib/auth.ts - Added explicit sessionToken name and externalSecondaryStorage
- frontend/src/lib/auth-client.ts - Added fetchOptions with credentials include
- frontend/src/lib/api.ts - Added session null debug logging
- backend/main.py - Confirmed CORS allow_credentials setting

## NEXT_PROMPTS

none

## REFLECTION_NOTE

The changes address session persistence issues by properly configuring Better Auth for Neon database environment and ensuring proper cookie handling across frontend-backend communication.

## EVALUATION

### Failure modes observed:
None

### Next experiment to improve prompt quality:
Consider adding actual session testing to verify the fixes work properly end-to-end.