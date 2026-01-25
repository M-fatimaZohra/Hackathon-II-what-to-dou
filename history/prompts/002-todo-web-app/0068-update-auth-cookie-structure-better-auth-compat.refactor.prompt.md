---
id: "0068"
title: "Update Auth Cookie Structure for Better Auth Compatibility"
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
  - "configuration"
  - "typescript"
  - "backend"
  - "cookies"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/auth.ts"
tests:
  - "none"
---

# Update Auth Cookie Structure for Better Auth Compatibility

## PROMPT_TEXT

"Update 'frontend/src/lib/auth.ts' to match the new Better Auth cookie structure. Change the 'advanced.cookies' block to:

cookies: { sessionToken: { attributes: { sameSite: 'Lax', secure: false } } }

Also, move the 'maxAge' setting to the top-level 'session' configuration object as 'expiresIn: 604800' (which is 7 days in seconds). This will fix the TypeScript errors and ensure the session persists correctly on localhost."

after that save progress in history

## RESPONSE_TEXT

Successfully updated the auth.ts configuration to match the new Better Auth cookie structure. Changed the advanced.cookies block to use sessionToken with attributes containing sameSite and secure settings. Also moved the maxAge setting to the top-level session configuration as expiresIn: 604800 (7 days in seconds). This resolves TypeScript errors and ensures sessions persist correctly on localhost.

## OUTCOME_IMPACT

Resolved TypeScript errors in the authentication configuration by updating the cookie structure to match Better Auth API requirements and ensuring proper session persistence on localhost.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- frontend/src/lib/auth.ts - Updated cookie structure to use sessionToken.attributes and moved expiration to session.expiresIn

## NEXT_PROMPTS

none

## REFLECTION_NOTE

Updating the cookie structure to use sessionToken.attributes and moving expiration to session.expiresIn aligns with Better Auth's API specification and resolves type compatibility issues.

## EVALUATION

### Failure modes observed:
None

### Next experiment to improve prompt quality:
Consider adding validation steps to verify the updated configuration works properly with the authentication system.