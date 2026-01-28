---
id: 0109
title: switch-to-session-jwt-strategy
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

Goal: Switch from the jwt() plugin to the internal session JWT strategy.

Prompt: > Update the lib/auth.ts file to use the symmetric Session JWT strategy.

Set session.strategy to "jwt".

Ensure session.cookieCache is enabled and set its strategy to "jwt".

CRITICAL: Remove the jwt() plugin from the plugins array.

Ensure secret: process.env.BETTER_AUTH_SECRET is correctly passed to the betterAuth constructor.

Afterwards: save implementation phr

## Response snapshot

Successfully switched from the jwt() plugin to the internal session JWT strategy. Key changes made:

1. Updated session configuration to use JWT strategy: set session.strategy to "jwt"
2. Enabled cookieCache with JWT strategy: configured session.cookieCache with enabled: true and strategy: "jwt"
3. Removed the jwt() plugin from the plugins array completely
4. Verified that secret: process.env.BETTER_AUTH_SECRET is correctly passed to the betterAuth constructor
5. Removed unused jwt import since the plugin is no longer used

The implementation now uses Better Auth's internal session JWT strategy instead of the standalone JWT plugin, which should generate tokens with HS256 algorithm as expected by the backend.

## Outcome

- ✅ Impact: Switched from jwt() plugin to internal session JWT strategy for consistency
- 🧪 Tests: Configuration now aligned with backend expectations for HS256 tokens
- 📁 Files: Updated frontend/src/lib/auth.ts with new session JWT configuration
- 🔁 Next prompts: Ready for server restart and token verification
- 🧠 Reflection: Internal JWT strategy should resolve algorithm mismatch issues

## Evaluation notes (flywheel)

- Failure modes observed: None - proper migration from plugin to internal strategy
- Graders run and results (PASS/FAIL): PASS - configuration properly updated
- Prompt variant (if applicable): JWT strategy migration prompt
- Next experiment (smallest change to try): Test token generation with new strategy
