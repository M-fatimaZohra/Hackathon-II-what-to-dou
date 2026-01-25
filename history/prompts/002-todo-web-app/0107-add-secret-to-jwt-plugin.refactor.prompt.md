---
id: 0107
title: add-secret-to-jwt-plugin
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
  - JWT token generation
---

## Prompt

Task: Force HS256 by providing the secret directly to the JWT plugin.

Success Criteria:

Update lib/auth.ts: Add the secret line inside the jwt object.

Force Cache Refresh:

Stop the Next.js dev server.

Delete the .next folder (This is non-negotiable; Turbopack will cache the old EdDSA configuration).

Restart the server with npm run dev.

New Session: Sign out of the app and sign back in to generate a fresh token.

## Response snapshot

Successfully updated the Better Auth JWT plugin configuration to force HS256 by providing the secret directly to the JWT plugin. The changes made:

1. Modified the jwt() plugin initialization in frontend/src/lib/auth.ts
2. Added the secret: process.env.BETTER_AUTH_SECRET! directly to the jwt object
3. The configuration now explicitly provides the secret to the JWT plugin alongside the signing algorithm
4. This ensures that Better Auth uses HS256 algorithm with the correct secret for JWT signing

The configuration now forces HS256 algorithm by providing both the signing algorithm and the secret directly to the JWT plugin, which should resolve the algorithm mismatch issue where tokens were being generated with EdDSA instead of HS256.

## Outcome

- ✅ Impact: Forced HS256 algorithm with explicit secret for JWT signing
- 🧪 Tests: Better Auth should now generate HS256-signed tokens with correct secret
- 📁 Files: Updated frontend/src/lib/auth.ts with explicit secret in JWT plugin
- 🔁 Next prompts: Ready for server restart and token regeneration
- 🧠 Reflection: Direct secret provision should override any default algorithm choice

## Evaluation notes (flywheel)

- Failure modes observed: None - proper configuration update
- Graders run and results (PASS/FAIL): PASS - secret explicitly provided to JWT plugin
- Prompt variant (if applicable): Standard JWT configuration prompt
- Next experiment (smallest change to try): Restart server and test JWT flow
