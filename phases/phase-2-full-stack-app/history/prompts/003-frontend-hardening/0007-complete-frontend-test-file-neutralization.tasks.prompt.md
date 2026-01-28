---
id: 0007
title: Complete frontend test file neutralization
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.implement
labels: ["tasks", "frontend", "security", "build", "test-neutralization"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/tasks.md
  - ../../frontend/test/account-jwt-test.ts
  - ../../frontend/test/auth-jwt-experiment.ts
  - ../../frontend/test/check-data.ts
  - ../../frontend/test/check-tables.ts
  - ../../frontend/test/check-user-table.ts
  - ../../frontend/test/jwt-flow-test.ts
  - ../../frontend/test/jwt-init-test.ts
  - ../../frontend/test/jwt-test.ts
  - ../../frontend/test/mock-auth-test.ts
  - ../../frontend/test/simple-check.ts
  - ../../frontend/test/trigger-jwt-init.ts
  - ../../frontend/src/components/__tests__/SearchFilter.test.tsx
tests:
  - null
---

## Prompt

Secure Test Neutralization & Build

## Objective

Comment out all test files using a "clean wrap" method to ensure no syntax errors occur during the build process.

## Step 1: Test File Neutralization

For every file matching inside frontend/tests/ and frontend/src/components/__tests___  :

1. **Clean Existing Comments:** Search for and remove all existing multi-line comment tags (`/*` and `*/`) within the file content.

2. **Clean JSDoc:** Ensure no JSDoc or block comments remain that could interfere with the parent wrap.

3. **Apply Parent Wrap:** - Add `/*` as the absolute first line of the file.

   - Add `*/` as the absolute last line of the file.

4. **Logic Check:** Ensure the resulting file has exactly one opening `/*` and one closing `*/`.

## Step 2: Production Build

1. After commenting, run `npm run build`.

2. If the build fails due to "unclosed comments" or "unexpected tokens" in test files, re-verify the "Clean Existing Comments" step.

3. Fix any unrelated TypeScript/Lint errors to ensure the build succeeds.

## Step 3: Confirmation

- Provide a list of the files that were successfully neutralized.

- Confirm that `npm run build` finished without errors.

## Response snapshot

Successfully completed the test file neutralization and build validation for frontend production readiness:

- Identified and processed 11 test files in frontend/test/ directory:
  * account-jwt-test.ts
  * auth-jwt-experiment.ts
  * check-data.ts
  * check-tables.ts
  * check-user-table.ts
  * jwt-flow-test.ts
  * jwt-init-test.ts
  * jwt-test.ts
  * mock-auth-test.ts
  * simple-check.ts
  * trigger-jwt-init.ts
- Identified and processed 1 test file in frontend/src/components/__tests__/ directory:
  * SearchFilter.test.tsx
- Applied proper comment wrapping to all test files to neutralize them
- Confirmed that all test files are now wrapped with /* at the beginning and */ at the end
- Successfully ran npm run build with no errors
- Updated tasks.md to mark foundational tasks (T004-T009) and build validation tasks (T024-T028) as completed

## Outcome

- ✅ Impact: All test files neutralized to prevent build failures during production build
- 🧪 Tests: Test files neutralized but preserved for future use
- 📁 Files: Updated 12 test files with proper comment wrapping, updated tasks.md
- 🔁 Next prompts: Ready to proceed with remaining tasks for environment and auth configuration
- 🧠 Reflection: Build process now completes successfully without test interference

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Build completed successfully
- Prompt variant (if applicable): Test neutralization implementation
- Next experiment (smallest change to try): Proceed with remaining tasks in tasks.md for API and auth configuration