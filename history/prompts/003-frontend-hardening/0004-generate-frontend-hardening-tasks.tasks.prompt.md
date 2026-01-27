---
id: 0004
title: Generate frontend hardening tasks
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.tasks
labels: ["tasks", "frontend", "security", "deployment"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/tasks.md
tests:
  - null
---

## Prompt

# Frontend Production Implementation

## Phase 1: Test Neutralization
- [ ] **Task 1.1:** Identify all test files in the project (frontend/) directory .
- [ ] **Task 1.2:** Apply block comments `/* ... */` to the entire content of each identified test file.
- [ ] **Task 1.3:** Verify that `npm run build` no longer attempts to execute or type-check these neutralized test files.

## Phase 2: API & Environment Hardening
- [ ] **Task 2.1:** Global search for `http://localhost:8000` and `http://localhost:3000`.
- [ ] **Task 2.2:** In `auth.ts` and `api-client.ts`, refactor `BASE_URL` to strictly use `process.env.NEXT_PUBLIC_BASE_URL`.
- [ ] **Task 2.3:** In `api.ts`, refactor `BASE_URL` to strictly use ` process.env.NEXT_PUBLIC_API_URL`.
- [ ] **Task 2.4:** Implement a guard clause: example `if (!process.env.NEXT_PUBLIC_API_URL) console.warn("Missing NEXT_PUBLIC_API_URL");`.

## Phase 3: Auth Security (Better-Auth)
- [ ] **Task 3.1:** Update `auth.ts` (Server):
   - Set `baseURL` to `process.env.BETTER_AUTH_URL`.
   - Set `trustedOrigins` to an array containing your production Vercel URL.
   - Change cookie attributes: `httpOnly: true` and `secure: true`.
- [ ] **Task 3.2:** Update `auth-client.ts` (Client):
   - Set `baseURL` to `process.env.BETTER_AUTH_URL`.

## Phase 4: Build Validation
- [ ] **Task 4.1:** Execute `npm run build` in the terminal.
- [ ] **Task 4.2:** Resolve any TypeScript "Code 2345" errors (null/undefined checks) encountered during the build.
- [ ] **Task 4.3:** Fix any ESLint "errors" that prevent build completion.
- [ ] **Task 4.4:** Confirm a successful build with the message: `Route (app) ... Size ... First Load JS

## Response snapshot

Successfully generated comprehensive tasks for frontend production implementation with:
- 30 specific, actionable tasks organized by user story priority
- Proper checkbox format with task IDs and story labels
- Clear file paths for each task
- Dependencies and execution order documented
- Parallel execution opportunities identified
- Tasks mapped to the three user stories from the specification

## Outcome

- ✅ Impact: Created detailed task list for frontend hardening implementation
- 🧪 Tests: No tests created (task generation phase)
- 📁 Files: Created tasks.md with organized implementation tasks
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks follow SDD methodology and map directly to user stories

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Standard task generation
- Next experiment (smallest change to try): Begin implementation of tasks in sequence
