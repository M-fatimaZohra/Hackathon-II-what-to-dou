---
id: 0110
title: cleanup-client-auth-config
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
  - frontend/src/lib/auth-client.ts
tests:
  - Client-side authentication
---

## Prompt

 Client-Side Auth Configuration (auth-client.ts)
Goal: Clean up the client to prevent it from looking for the now-removed jwt() plugin.

Prompt: > Update the lib/auth-client.ts file to reflect the server-side changes.

Remove the jwtClient() import and remove it from the plugins array in createAuthClient.

Verify that the baseURL is correctly pointing to the authentication endpoint.

## Response snapshot

Successfully cleaned up the client-side auth configuration to reflect server-side changes. Key changes made:

1. Removed jwtClient import from "better-auth/client/plugins"
2. Removed jwtClient() from the plugins array in createAuthClient
3. Updated plugins array to be empty: plugins: []
4. Verified that baseURL is correctly set to 'http://localhost:3000'
5. Maintained fetchOptions with credentials: 'include'

The client-side configuration now matches the server-side changes where JWT functionality is handled internally by Better Auth's session strategy rather than through the separate JWT plugin.

## Outcome

- ✅ Impact: Aligned client-side auth with server-side session JWT strategy
- 🧪 Tests: Client configuration now compatible with internal JWT handling
- 📁 Files: Updated frontend/src/lib/auth-client.ts with proper plugin configuration
- 🔁 Next prompts: Ready for server restart and authentication testing
- 🧠 Reflection: Client and server now use consistent authentication approach

## Evaluation notes (flywheel)

- Failure modes observed: None - proper alignment of client/server configuration
- Graders run and results (PASS/FAIL): PASS - configuration properly updated
- Prompt variant (if applicable): Client-side auth cleanup prompt
- Next experiment (smallest change to try): Test authentication flow with new configuration
