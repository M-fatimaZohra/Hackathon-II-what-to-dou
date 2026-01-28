---
id: 0001
title: Create frontend hardening spec
stage: spec
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.specify "Frontend Production & Security Hardening"
labels: ["spec", "frontend", "security", "deployment"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/spec.md
  - ../../specs/003-frontend-hardening/checklists/requirements.md
tests:
  - null
---

## Prompt

Create new specs for frontend deployment updates

# Specification: Frontend Production & Security Hardening

## 1. Environment & API Realignment

Goal: Eliminate local fallbacks and point to the production Hugging Face backend.

- **Files:** `api.ts`, `api-client.ts`, and any network utility files.

- **Actions:**
  - Replace any hardcoded `http://localhost:8000` with `process.env.NEXT_PUBLIC_API_URL`.
  - Ensure the app throws a clear console error if `NEXT_PUBLIC_API_URL` is undefined.

## 2. Better-Auth Production Hardening

Goal: Update `auth.ts` and `auth-client.ts` to support HTTPS and production domains.

- **File:** `src/lib/auth.ts` (or equivalent server auth file)
  - Change `baseURL` from `http://localhost:3000` to `process.env.NEXT_PUBLIC_BASE_URL` .
  - Update `trustedOrigins`: Remove `http://localhost:3000` and use an environment variable for the production domain.
  - **Security Update:**
    - Set `httpOnly: true` (Prevents XSS access to tokens).
    - Set `secure: true` (Ensures cookies are only sent over HTTPS).
    - Set `sameSite: "lax"` or `"strict"`.

- **File:** `src/lib/auth-client.ts`
  - Change `baseURL` from `http://localhost:3000` to `process.env.NEXT_PUBLIC_BASE_URL`.

## 3. Build Error Mitigation (Test Neutralization)

Goal: Prevent `npm run build` failures from legacy or incomplete tests.

- **Action:** Identify all test related files in /frontend and /frontend/src
- **Implementation:** Comment out the entire contents of these test files using block comments `/* ... */`.

## 4. Build Validation & Linting

Goal: Ensure the project is ready for Vercel deployment.

- **Action:** Run `npm run build` in the terminal.
- **Requirement:** Resolve any TypeScript or Linting errors that appear.
- **Focus:** Pay specific attention to "Code 2345" (null/undefined checks) in components and ensure all `<img>` or `<Image />` tags have `alt` attributes.

## 5. Deployment Baseline

- **Verification:** Confirm that a `.next` folder is successfully generated.
- use NEXT_PUBLIC_BASE_URL belongs to frontend app, NEXT_PUBLIC_API_URL belongs to (deployed) backend

## Response snapshot

A complete specification for "Frontend Production & Security Hardening" has been created with:
- Three user stories covering environment/API realignment, auth hardening, and build validation
- Nine functional requirements addressing all aspects of the security hardening
- Seven measurable success criteria
- Two key entities defined
- Proper edge cases identified

## Outcome

- ✅ Impact: Created complete specification for frontend security hardening and production readiness
- 🧪 Tests: No tests created (specification phase)
- 📁 Files: Created spec.md and requirements checklist in specs/003-frontend-hardening/
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification follows SDD methodology and covers all requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Standard spec creation
- Next experiment (smallest change to try): Proceed with /sp.plan to generate implementation plan
