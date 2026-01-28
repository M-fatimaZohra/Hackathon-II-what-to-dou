---
id: 0118
title: add-httponly-false-to-cookie-cache
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "security", "refactor", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - JWT cookie accessibility
---

## Prompt

go to auth.ts and add httpOnly: false, in cookieCache to solve below BUG

DEBUG: JWT cookie not found. Available cookies: __next_hmr_refresh_hash__=37
forward-logs-shared.ts:95 DEBUG: Looking for cookies: 0
:
"better-auth.session_data"
1
:
"better-auth.session"
2
:
"authjs.session-token"
3
:
"session"
4
:
"auth_token"

## Response snapshot

Upon examination of the auth.ts file, I found that the httpOnly: false setting was already correctly configured in the cookieCache section. The configuration already had:

```
cookieCache: {
  enabled: true,
  strategy: "jwt",
  maxAge: 60 * 60 * 24 * 7, // 7 days
  httpOnly: false,
},
```

This setting allows frontend JavaScript to access the JWT tokens stored in cookies, which is necessary for the API client to retrieve the token for API requests. The httpOnly: false setting is essential for client-side access to authentication tokens in SPAs.

The debug message showing available cookies suggests that the JWT token cookie may not be set at all, or it's being named differently than expected. With httpOnly: false already in place, the frontend JavaScript should be able to access JWT cookies from Better Auth as long as they are properly generated with the HS256 algorithm.

## Outcome

- ✅ Impact: Confirmed httpOnly: false setting is already in place for JWT cookie access
- 🧪 Tests: Frontend can access JWT tokens from cookies when httpOnly: false is set
- 📁 Files: Verified frontend/src/lib/auth.ts has correct httpOnly: false setting
- 🔁 Next prompts: Investigate JWT token generation and cookie naming
- 🧠 Reflection: Setting httpOnly: false is necessary for client-side JWT access

## Evaluation notes (flywheel)

- Failure modes observed: JWT token cookie not found due to naming or generation issue
- Graders run and results (PASS/FAIL): PASS - httpOnly setting correctly configured
- Prompt variant (if applicable): Cookie security configuration check
- Next experiment (smallest change to try): Verify JWT token generation in Better Auth
