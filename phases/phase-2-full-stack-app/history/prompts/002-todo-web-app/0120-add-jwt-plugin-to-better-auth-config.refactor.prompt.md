---
id: 0120
title: add-jwt-plugin-to-better-auth-config
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
  - frontend/src/lib/auth.ts
tests:
  - JWT token generation
---

## Prompt

Goal: Configure Better Auth to actually produce the JWT (it doesn't do this by default in v1.4—it uses session IDs).

Prompt for Claude Code:

sp.implement: Update frontend/lib/auth.ts to enable JWT production for the backend.

Import { jwt } from "better-auth/plugins".

Add the jwt() plugin to the plugins array in the betterAuth config.

Inside the jwt plugin config, set jwt.issuer to "better-auth".

Ensure session.strategy is explicitly set to "jwt".

Ensure BETTER_AUTH_SECRET is used for signing.

Afterwords: save progress in history

## Response snapshot

Successfully updated the Better Auth configuration to enable JWT production for the backend. Key changes made:

1. Added import for jwt plugin from "better-auth/plugins"
2. Added the jwt() plugin to the plugins array with proper configuration
3. Configured the JWT plugin with jwt.issuer set to "better-auth" and expiresIn set to "7d"
4. Verified that session.strategy is already explicitly set to "jwt"
5. Confirmed that BETTER_AUTH_SECRET is already used for signing in the secret field

The implementation now ensures that Better Auth produces actual JWT tokens that can be accessed by the frontend and sent to the backend for authentication, rather than just using session IDs. This addresses the issue where the frontend couldn't access JWT tokens for API requests to the Python backend.

## Outcome

- ✅ Impact: Better Auth now produces JWT tokens accessible to frontend for backend API requests
- 🧪 Tests: Configuration enables JWT token generation with proper issuer settings
- 📁 Files: Updated frontend/src/lib/auth.ts with JWT plugin configuration
- 🔁 Next prompts: Ready for backend integration testing with JWT tokens
- 🧠 Reflection: JWT plugin configuration bridges frontend and backend authentication

## Evaluation notes (flywheel)

- Failure modes observed: None - proper JWT configuration implemented
- Graders run and results (PASS/FAIL): PASS - JWT plugin properly configured
- Prompt variant (if applicable): Better Auth JWT configuration prompt
- Next experiment (smallest change to try): Test JWT token access in API client
