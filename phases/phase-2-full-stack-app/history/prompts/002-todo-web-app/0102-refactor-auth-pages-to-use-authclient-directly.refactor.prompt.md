---
id: 0102
title: refactor-auth-pages-to-use-authclient-directly
stage: refactor
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "refactor", "security", "ui", "client"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/app/signin/page.tsx
  - frontend/src/app/signup/page.tsx
  - frontend/src/lib/auth-service.ts
tests:
  - frontend/src/lib/auth-client.ts
---

## Prompt

Task: Refactor Auth pages to use authClient directly and remove the AuthService middleman.

Success Criteria:

Sign-In Page: Replace AuthService.signIn(email, password) with:

const { data, error } = await authClient.signIn.email({
  email,
  password,
  callbackURL: "/tasks",
});

Sign-Up Page: Replace AuthService.signUp(name, email, password) with:

const { data, error } = await authClient.signUp.email({
  email,
  password,
  name,
  callbackURL: "/tasks",
});

Cleanup: Delete lib/auth-service.ts.

Navigation: Use useRouter() from next/navigation for redirects instead of window.location.href to maintain the React state.

Context: This ensures the frontend library and the backend session are "in sync." Once the library handles the login, the apiClient will immediately be able to see the session and generate the JWT for FastAPI.

## Response snapshot

Successfully refactored the auth pages to use authClient directly and removed the AuthService middleman. Key changes made:

1. Updated sign-in page to use authClient.signIn.email() method directly with proper error handling
2. Updated sign-up page to use authClient.signUp.email() method directly with proper error handling
3. Replaced window.location.href with useRouter().push() for navigation
4. Removed AuthService import and usage from both pages
5. Deleted the lib/auth-service.ts file as it's no longer needed
6. Both pages now properly handle success and error responses from authClient

The implementation now uses the direct Better Auth client methods which ensures the frontend library and backend session stay in sync, allowing the apiClient to immediately see the session and generate JWTs for FastAPI.

## Outcome

- ✅ Impact: Eliminated unnecessary abstraction layer and improved auth flow reliability
- 🧪 Tests: Both sign-in and sign-up pages use direct authClient methods with proper error handling
- 📁 Files: Updated auth pages and removed deprecated auth-service.ts file
- 🔁 Next prompts: Ready for end-to-end auth flow testing
- 🧠 Reflection: Direct authClient usage provides better integration and consistency

## Evaluation notes (flywheel)

- Failure modes observed: None - proper error handling maintained during refactoring
- Graders run and results (PASS/FAIL): PASS - code now uses direct authClient methods
- Prompt variant (if applicable): Standard auth refactoring prompt
- Next experiment (smallest change to try): Test complete auth flow with apiClient integration
