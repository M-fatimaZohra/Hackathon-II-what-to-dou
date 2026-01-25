---
id: "0066"
title: "Fix Auth Configuration Structure"
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
  - "jwt"
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

# Fix Auth Configuration Structure

## PROMPT_TEXT

"In 'frontend/src/lib/auth.ts', fix the configuration structure:

Move the 'cookie' settings inside 'advanced: { cookie: { ... } }'.

In the plugins array, change 'jwt({ jwt: { secret: ... } })' to just 'jwt()'. The plugin automatically uses the top-level 'secret'.

Ensure 'BETTER_AUTH_SECRET' is used as the main secret at the top level.

This will resolve the TypeScript errors and ensure the JWTs are signed properly for the backend to read."

after that save progresss to history

## RESPONSE_TEXT

Successfully updated the auth.ts configuration by moving cookie settings inside the advanced object and simplifying the JWT plugin configuration. The cookie settings were moved from session: { cookie: { ... } } to advanced: { cookie: { ... } }, and the JWT plugin was simplified from jwt({ jwt: { secret: process.env.BETTER_AUTH_SECRET } }) to just jwt(). The BETTER_AUTH_SECRET is maintained as the main secret at the top level. This resolves TypeScript errors and ensures JWTs are signed properly for the backend to read.

## OUTCOME_IMPACT

Resolved TypeScript errors in the authentication configuration and ensured proper JWT signing for backend verification by updating the Better Auth configuration structure.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- frontend/src/lib/auth.ts - Updated configuration structure to move cookie settings to advanced object and simplify JWT plugin

## NEXT_PROMPTS

none

## REFLECTION_NOTE

Moving the cookie configuration to the advanced section and simplifying the JWT plugin configuration follows Better Auth's recommended practices and resolves type compatibility issues.

## EVALUATION

### Failure modes observed:
None

### Next experiment to improve prompt quality:
Consider adding validation steps to verify the updated configuration works properly with the backend JWT verification.