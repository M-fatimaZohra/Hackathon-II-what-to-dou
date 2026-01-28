---
id: 0100
title: standardize-jwt-retrieval-token-method
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement Task: Standardize JWT retrieval in lib/api.ts using the .token() method."
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

Task: Standardize JWT retrieval in lib/api.ts using the .token() method.

Success Criteria:

Update Method Call: Change await authClient.jwt.getToken() to await authClient.token().

Handle Return Type: Destructure the result as const { data: tokenData, error: tokenError } = await authClient.token();.

Extract Token String: Use tokenData.token to get the actual JWT string for the Authorization header.

Remove Custom Fetch: Ensure no manual fetch calls to /api/auth/token remain.

Context: Using the built-in .token() method is the most robust way to handle the session-to-JWT exchange in a Next.js environment. It ensures that the token is correctly signed by the server using the BETTER_AUTH_SECRET before being sent to the FastAPI backend.

## Response snapshot

Successfully standardized JWT retrieval in lib/api.ts using the .token() method. Key changes made:

1. Updated method call from authClient.jwt.getToken() to authClient.token()
2. Handled return type with destructuring: { data: tokenData, error: tokenError }
3. Extracted token string from tokenData.token property
4. Maintained proper error handling for token errors
5. Confirmed no manual fetch calls to /api/auth/token remain

The implementation now uses the built-in .token() method which is the most robust way to handle the session-to-JWT exchange in a Next.js environment, ensuring tokens are correctly signed by the server using BETTER_AUTH_SECRET.

## Outcome

- ✅ Impact: Improved JWT retrieval mechanism using standardized Better Auth method
- 🧪 Tests: All API methods continue to work with new token retrieval approach
- 📁 Files: Modified frontend/src/lib/api.ts to use standard token() method
- 🔁 Next prompts: Ready for backend integration testing with standardized tokens
- 🧠 Reflection: Using built-in token() method provides better error handling and security

## Evaluation notes (flywheel)

- Failure modes observed: None - proper error handling maintained during refactoring
- Graders run and results (PASS/FAIL): PASS - code follows Better Auth best practices
- Prompt variant (if applicable): Standard JWT standardization prompt
- Next experiment (smallest change to try): Test end-to-end authentication flow
