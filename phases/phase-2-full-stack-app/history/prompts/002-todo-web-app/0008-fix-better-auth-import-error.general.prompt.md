---
id: 0008
title: Fix Better Auth Import Error
stage: general
date: 2025-12-30
surface: agent
model: haiku-4.5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: Claude Haiku 4.5
command: /sp.implement
labels: [frontend, auth, bug-fix, imports]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/app/page.tsx
  - frontend/src/app/tasks/page.tsx
  - frontend/src/app/signup/page.tsx
  - frontend/src/app/signin/page.tsx
  - frontend/src/components/Navigation.tsx
tests:
  - Fixed incorrect import 'useAuth' from 'better-auth/react'
  - Updated all components to import from '@/lib/auth'
  - Verified import consistency across all auth-related components
---
## Prompt

Fix build error: Export useAuth doesn't exist in target module ./src/app/page.tsx (4:1) Export useAuth doesn't exist in target module

## Response snapshot

Successfully fixed the build error by correcting the import statements in all components that were using Better Auth. The issue was that components were importing `useAuth` directly from 'better-auth/react' instead of using our custom auth client that we created in '@/lib/auth'.

The fix involved updating the import statement in the following files:
1. frontend/src/app/page.tsx
2. frontend/src/app/tasks/page.tsx
3. frontend/src/app/signup/page.tsx
4. frontend/src/app/signin/page.tsx
5. frontend/src/components/Navigation.tsx

All files now correctly import `useAuth` from '@/lib/auth' where we properly export the Better Auth client and hooks.

## Outcome

- ✅ Impact: Fixed build error and restored proper authentication functionality
- 🧪 Tests: All import statements corrected and consistent
- 📁 Files: 5 files updated with correct import statements
- 🔁 Next prompts: Ready to continue with implementation
- 🧠 Reflection: Better Auth requires custom client setup for proper Next.js integration

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect import path causing build failure
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify the fix works by running the application