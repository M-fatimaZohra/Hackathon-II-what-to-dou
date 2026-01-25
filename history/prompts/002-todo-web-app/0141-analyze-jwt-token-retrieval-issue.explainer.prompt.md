---
id: 0141
title: analyze-jwt-token-retrieval-issue
stage: explainer
date: 2026-01-21
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.analyze"
labels: ["auth", "jwt", "debug", "frontend", "cookie"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
  - analysis only
tests:
  - JWT validation logic
  - Cookie name identification
  - Token structure analysis
---

## Prompt

Analyze the error logs showing JWT validation issues in the application:

🚀 API Request: Sending JWT to port 8000 for user: 0Bc7a7VracLKy5enbDblpchHl6FZBfC1
api.ts:95 Invalid JWT header: typ is not JWT undefined
warn @ forward-logs-shared.ts:95
getJwtTokenFromCookie @ api.ts:95
getSessionData @ api.ts:23
await in getSessionData
request @ api.ts:122
getTasks @ api.ts:132
loadTasks @ TaskList.tsx:52
api.ts:114 DEBUG: JWT cookie not found. Available cookies: (2) ['better-auth.session_token', 'better-auth.session_data']
api.ts:115 DEBUG: Looking for cookies containing "better-auth.session_data"
TaskList.tsx:61 Failed to load tasks: Error: Session token not found. Please log in again.

## Response snapshot

Analysis of the error logs reveals the following:

1. **Success**: The advanced configuration worked - cookies are now visible: `Available cookies: (2)['better-auth.session_token', 'better-auth.session_data']`

2. **Issue**: JWT Header Validation Failure with `Invalid JWT header: typ is not JWT undefined` at api.ts:95

3. **Root Cause**: Better Auth v1.4 is setting two different cookie types:
   - `better-auth.session_token`: May contain the actual JWT token
   - `better-auth.session_data`: May contain session metadata instead of a JWT

4. **Problem**: The validation logic expects JWT structure with `typ: 'JWT'` in the header, but the `session_data` cookie doesn't contain a JWT with that structure.

The advanced configuration successfully made the cookies visible to JavaScript, but the JWT validation logic needs to be updated to identify which cookie contains the actual JWT token and properly validate its structure.

## Outcome

- 🔍 Analysis: Cookie visibility fixed but JWT validation needs adjustment
- 📁 Files: Analysis of frontend/src/lib/api.ts JWT logic
- 🧪 Debug: JWT header validation in cookies
- 🧠 Issue: Need to identify which cookie contains the actual JWT

## Evaluation notes (flywheel)

- Failure modes observed: JWT header validation mismatch
- Graders run and results (PASS/FAIL): N/A - analysis only
- Prompt variant (if applicable): Debug analysis prompt
- Next experiment (smallest change to try): Update JWT validation to check both cookie types