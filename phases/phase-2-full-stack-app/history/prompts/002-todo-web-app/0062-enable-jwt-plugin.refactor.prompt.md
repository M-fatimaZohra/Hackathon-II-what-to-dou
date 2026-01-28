---
id: "0062"
title: "Enable JWT Plugin on Auth Client"
stage: "refactor"
date: "2026-01-10"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "002-todo-web-app"
branch: "002-todo-web-app"
user: "unknown"
command: "/sp.implement"
labels:
  - "authentication"
  - "jwt"
  - "typescript"
  - "plugin"
  - "frontend"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/auth-client.ts"
tests:
  - "none"
---

# Enable JWT Plugin on Auth Client

## PROMPT_TEXT

`"Enable the JWT plugin on the auth client:

In 'frontend/src/lib/auth-client.ts', import 'jwtClient' from 'better-auth/client/plugins'.

Add 'plugins: [jwtClient()]' to the 'createAuthClient' configuration.

This will resolve the TypeScript error where 'getJWT' is missing from the 'authClient' type and allow the frontend to properly retrieve tokens for the FastAPI backend."`

## RESPONSE_TEXT

Successfully enabled the JWT plugin on the auth client by importing jwtClient and adding it to the createAuthClient configuration, resolving the TypeScript error and enabling proper JWT token retrieval.

## OUTCOME_IMPACT

Resolved TypeScript error where 'getJWT' was missing from authClient type, enabling proper JWT token retrieval for backend API communication.

## TESTS_SUMMARY

none

## FILES_SUMMARY

- frontend/src/lib/auth-client.ts - Added jwtClient import and configured plugins: [jwtClient()]

## NEXT_PROMPTS

none

## REFLECTION_NOTE

Enabling the JWT plugin properly resolves the TypeScript error and allows the frontend to retrieve JWT tokens for backend authentication.

## EVALUATION

### Failure modes observed:
None

### Next experiment to improve prompt quality:
Consider adding more specific validation steps to verify the JWT functionality works as expected after the changes.