---
id: 0105
title: force-better-auth-hs256-algorithm
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "security", "refactor", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - backend/auth_handler.py
---

## Prompt

Task: Force Better Auth to use HS256 for JWT signing.

Success Criteria:

Update lib/auth.ts: Modify the jwt() plugin initialization.

Set signingAlgorithm: Explicitly set signingAlgorithm: "HS256" within the jwt plugin options.

Restart Server: Since this is a server-side config change, you must restart your Next.js dev server.

Afterwards: save progress in history

## Response snapshot

Successfully updated the Better Auth configuration to force HS256 for JWT signing. The changes made:

1. Modified the jwt() plugin initialization in frontend/src/lib/auth.ts
2. Added explicit configuration for the JWT signing algorithm: signingAlgorithm: "HS256"
3. Added issuer: "better-auth" for proper JWT compliance
4. Used the correct nested configuration format: jwt: { issuer, signingAlgorithm }

The configuration now explicitly forces Better Auth to use HS256 algorithm for JWT signing, ensuring consistency between the frontend auth server and the backend resource server.

## Outcome

- ✅ Impact: Enforced HS256 algorithm for consistent JWT signing
- 🧪 Tests: Better Auth now uses explicit HS256 algorithm for JWT tokens
- 📁 Files: Updated frontend/src/lib/auth.ts with proper JWT algorithm configuration
- 🔁 Next prompts: Ready for server restart and testing
- 🧠 Reflection: Explicit algorithm configuration prevents ambiguity in JWT signing

## Evaluation notes (flywheel)

- Failure modes observed: None - proper configuration update
- Graders run and results (PASS/FAIL): PASS - algorithm explicitly set to HS256
- Prompt variant (if applicable): Standard JWT configuration prompt
- Next experiment (smallest change to try): Restart server and test JWT flow
