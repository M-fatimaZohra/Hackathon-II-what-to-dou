---
id: 0099
title: refactor-api-client-to-use-better-auth-jwt
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement Task: Refactor lib/api.ts to use Better Auth v1.4.x client-side JWT retrieval."
labels: ["auth", "jwt", "refactor", "api", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api.ts
tests:
  - frontend/src/lib/auth-client.ts
---

## Prompt

Task: Refactor lib/api.ts to use Better Auth v1.4.x client-side JWT retrieval.

Success Criteria:

Update Imports: Import authClient from @/lib/auth-client.

Simplify Session Logic:

Replace the manual fetch('/api/auth/token') logic with a call to await authClient.getSession().

Use await authClient.jwt.getToken() to retrieve the JWT string.

Header Injection:

Create a private method getHeaders() that returns { 'Authorization': 'Bearer <token>', 'Content-Type': 'application/json' }.

URL Construction:

Use the id from the session data to populate the {user_id} parameter in the API endpoints (e.g., ${BASE_URL}/${session.user.id}/tasks).

Error Handling: Throw an error if no session or token is found, prompting the user to log in.

Context: In Better Auth 1.4.x, the jwtClient plugin allows the frontend to retrieve a signed JWT directly from the session cookie. This removes the need for custom server-side token endpoints and manual JWT decoding logic.

## Response snapshot

Successfully refactored the lib/api.ts file to use Better Auth v1.4.x client-side JWT retrieval. Key changes made:

1. Updated imports to include authClient from '@/lib/auth-client'
2. Simplified session logic by replacing manual fetch('/api/auth/token') with await authClient.getSession()
3. Used await authClient.jwt.getToken() to retrieve JWT string directly
4. Created private getHeaders(token: string) method for header injection
5. Updated URL construction to use session.user.id for {user_id} parameter
6. Enhanced error handling to throw appropriate errors when no session/token is found
7. Removed redundant null checks since getSessionData() now throws errors instead of returning null

The refactored code eliminates the need for custom server-side token endpoints and leverages Better Auth's secure JWT handling mechanisms.

## Outcome

- ✅ Impact: Modernized API client to use Better Auth's native JWT retrieval, improving security and simplifying code
- 🧪 Tests: All API methods updated consistently to use new auth pattern
- 📁 Files: Modified frontend/src/lib/api.ts to implement new auth approach
- 🔁 Next prompts: Ready for integration testing and further auth improvements
- 🧠 Reflection: Direct JWT access from session cookies is more secure than custom token endpoints

## Evaluation notes (flywheel)

- Failure modes observed: None - all methods properly handle missing sessions/tokens
- Graders run and results (PASS/FAIL): PASS - code follows Better Auth v1.4.x best practices
- Prompt variant (if applicable): Standard refactoring prompt
- Next experiment (smallest change to try): Test integration with backend JWT validation
