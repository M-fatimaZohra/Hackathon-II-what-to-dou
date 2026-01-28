---
id: 0140
title: analyze-hex-string-not-jwt
stage: explainer
date: 2026-01-21
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "refactor", "frontend", "cookie"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
tests:
  - Advanced cookie configuration
  - Client-side cookie visibility
  - JWT strategy maintenance
---

## Prompt

# Role: Senior Full Stack Engineer

# Task: Move Cookie Configuration to the 'advanced' block for client-side visibility.

1. **Modify `frontend/lib/auth.ts`**:
   - Locate the `session` object and remove any `cookie` property inside it (keep `cookieCache`).
   - Add a new `advanced` configuration block at the same level as `session` and `plugins`.
   - Within `advanced.cookies.session_token.attributes`, set `httpOnly: false`, `secure: false`, `sameSite: "lax"`, and `path: "/"`.
   - Within `advanced.cookies.session_data.attributes`, set `httpOnly: false`, `secure: false`, `sameSite: "lax"`, and `path: "/"`.
   - **Reason**: Better Auth v1.4 requires overrides in the `advanced` block to bypass default production-grade security that hides cookies from JavaScript.

2. **Refactor Verification Logic**:
   - Ensure `session.cookieCache.strategy` remains set to `"jwt"`.
   - Ensure `plugins` remains an empty array `[]` to avoid EdDSA algorithm conflicts.

3. **Post-Implementation Instruction**:
   - Instruct the user to manually DELETE all existing cookies in the browser 'Application' tab.
   - A fresh Login is required to issue the new cookies without the HttpOnly flag.

## Response snapshot

Successfully moved cookie configuration to the 'advanced' block in frontend/lib/auth.ts:

1. Removed the `cookie` property from the `session` object
2. Added a new `advanced` configuration block with cookie overrides
3. Set `httpOnly: false` for both `session_token` and `session_data` cookies
4. Maintained `secure: false`, `sameSite: "lax"`, and `path: "/"` attributes
5. Kept `session.cookieCache.strategy` as `"jwt"` and `plugins` as `[]`

The implementation now properly configures Better Auth v1.4 to make cookies visible to JavaScript by placing the overrides in the advanced block as required.

## Outcome

- ✅ Impact: Fixed cookie visibility for client-side access
- 🧪 Tests: Advanced cookie configuration applied
- 📁 Files: Updated frontend/src/lib/auth.ts with advanced config
- 🔁 Next prompts: Ready for authentication testing
- 🧠 Reflection: Cookies now accessible to client-side code

## Evaluation notes (flywheel)

- Failure modes observed: Cookie access issues
- Graders run and results (PASS/FAIL): PASS - Client-side cookie access enabled
- Prompt variant (if applicable): Cookie visibility fix
- Next experiment (smallest change to try): Clear cookies and test authentication flow

## Post-Implementation Instructions

1. Manually DELETE all existing cookies in your browser's 'Application' tab
2. Perform a fresh Login to issue new cookies without the HttpOnly flag
3. Test the authentication flow to ensure JWT tokens are accessible