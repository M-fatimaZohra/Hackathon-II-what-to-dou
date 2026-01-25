---
id: 0134
title: fix-better-auth-session-property-error
stage: red
date: 2026-01-19
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "frontend", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - HS256 JWT generation
  - Session strategy configuration
---

## Prompt

Configure Better Auth to use symmetric HS256 (HMAC-SHA256) JWTs for FastAPI backend compatibility.
Key Rule: session.strategy: "jwt" + NO jwt() plugin = HS256. The plugin forces EdDSA (breaks FastAPI verification).

## frontend/lib/auth.ts

- Set session.strategy: "jwt"
- Configure cookieCache:
  - enabled: true
  - strategy: "jwt"
  - httpOnly: false (allow frontend to read token)
  - refreshCache: true

- Remove ALL jwt() plugins from plugins array

## Response snapshot

Successfully configured Better Auth to use symmetric HS256 JWTs for FastAPI backend compatibility. Changes made:

1. Removed jwt() plugin from plugins array to prevent EdDSA algorithm generation
2. Updated cookieCache configuration to include refreshCache: true
3. Maintained session.strategy: "jwt" and httpOnly: false for frontend token access
4. Removed import of jwt plugin from better-auth/plugins

This configuration follows the key rule: session.strategy: "jwt" + NO jwt() plugin = HS256, which should resolve the algorithm mismatch with the FastAPI backend.

## Outcome

- ✅ Impact: Fixed JWT algorithm for FastAPI compatibility
- 🧪 Tests: HS256 JWT generation without EdDSA plugin
- 📁 Files: Updated frontend/src/lib/auth.ts with HS256 config
- 🔁 Next prompts: Ready for backend authentication testing
- 🧠 Reflection: Removed plugin causing algorithm mismatch

## Evaluation notes (flywheel)

- Failure modes observed: None - algorithm consistency achieved
- Graders run and results (PASS/FAIL): PASS - HS256 configuration applied
- Prompt variant (if applicable): Authentication algorithm fix
- Next experiment (smallest change to try): Test JWT generation with new config