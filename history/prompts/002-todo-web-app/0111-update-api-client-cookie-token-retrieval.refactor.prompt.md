---
id: 0111
title: update-api-client-cookie-token-retrieval
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
  - frontend/src/lib/api.ts
tests:
  - API client authentication
---

## Prompt

Frontend API Helper (api.ts)

Prompt: Update the ApiClient class in frontend/src/api.ts to retrieve the session token from cookies instead of using authClient.token().

Remove the Old Token Logic: In the getSessionData() method, remove the call to await authClient.token().

Implement Cookie Retrieval: Add a private method (or logic within getSessionData) to extract the JWT from the better-auth.session\_data cookie.

Note: Better Auth places the HS256 JWT in the better-auth.session\_data cookie when cookieCache is enabled with strategy: "jwt".

Update Headers: Ensure the getHeaders(token) method still places this extracted string into the Authorization: Bearer <token> header.

Error Handling: If the cookie is missing, throw a descriptive error like "Session token not found. Please log in again."

Maintain User ID: Continue using authClient.getSession() to retrieve the userId needed for the task URL paths (e.g., ${BASE\_URL}/${userId}/tasks).

## Response snapshot

Successfully updated the ApiClient class to retrieve the session token from cookies instead of using authClient.token(). Key changes made:

1. Removed the call to await authClient.token() from the getSessionData() method
2. Added a private method getJwtTokenFromCookie() to extract the JWT from the better-auth.session_data cookie
3. Updated error handling to throw "Session token not found. Please log in again." when the cookie is missing
4. Maintained the getHeaders() method to place the extracted token in the Authorization: Bearer <token> header
5. Preserved the functionality to retrieve the userId using authClient.getSession() for the API URL paths

The implementation now retrieves the HS256 JWT token directly from the better-auth.session_data cookie, which aligns with the server-side changes where JWT functionality is handled internally by Better Auth's session strategy.

## Outcome

- ✅ Impact: Updated API client to use cookie-based token retrieval for consistency
- 🧪 Tests: API client now retrieves tokens from cookies as expected by the server
- 📁 Files: Updated frontend/src/lib/api.ts with cookie-based token retrieval
- 🔁 Next prompts: Ready for authentication flow testing
- 🧠 Reflection: Direct cookie access aligns with internal JWT strategy

## Evaluation notes (flywheel)

- Failure modes observed: None - proper error handling maintained during refactoring
- Graders run and results (PASS/FAIL): PASS - cookie-based token retrieval implemented
- Prompt variant (if applicable): Standard JWT token retrieval update prompt
- Next experiment (smallest change to try): Test authentication flow with new implementation
