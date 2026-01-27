---
id: 0002
title: Create frontend hardening plan
stage: plan
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.plan
labels: ["plan", "frontend", "security", "deployment"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/plan.md
  - ../../specs/003-frontend-hardening/research.md
  - ../../specs/003-frontend-hardening/data-model.md
  - ../../specs/003-frontend-hardening/quickstart.md
  - ../../specs/003-frontend-hardening/contracts/
tests:
  - null
---

## Prompt

# Frontend Production Readiness & Security Sweep

## Goal
Prepare the Next.js frontend for Vercel deployment by neutralizing test interference, hardening authentication security, and removing all localhost references.

## 1. Test Neutralization
- **Task:** Search for all test files in the frontend and frontend/srd directory.
- **Action:** Comment out the entire content of these files using block comments (`/* ... */`).
- **Objective:** Prevent `npm run build` from failing due to outdated or incomplete tests.

## 2. API & Logic Hardening
- **Files:** `api.ts`, `api-client.ts`, and all network utility files.
- **Action:** - Remove hardcoded `http://localhost:8000`.
    - Refactor to: `const BASE_URL = process.env.NEXT_PUBLIC_API_URL;`.
    - Add a runtime check: `if (!BASE_URL) throw new Error("API URL missing");`.

## 3. Auth Production Configuration (Better-Auth)
- **File:** `auth.ts` (Server Configuration)
    - Update `baseURL` and `trustedOrigins` to use environment variables (`process.env.NEXT_PUBLIC_BASE_URL`) instead of `http://localhost:3000`.
    - **Security Sweep:** - Change `httpOnly: false` to `httpOnly: true`.
        - Change `secure: false` to `secure: true`.
        - Ensure `sameSite` is set to `"lax"`.
- **File:** `auth-client.ts` (Client Configuration)
    - Change `baseURL` to `process.env.NEXT_PUBLIC_BASE_URL`.

## 4. Build & Validation
- **Action:** Run `npm run build` locally.
- **Iteration:** Resolve every TypeScript (e.g., Code 2345) and Lint error that arises.
- **Requirement:** The process is only complete when the build finishes successfully with a generated `.next` folder.

## Response snapshot

Successfully created an implementation plan for frontend production readiness and security hardening with:
- Complete plan.md with technical context and constitution check
- research.md with security and configuration decisions
- data-model.md with environment and auth configuration
- quickstart.md with setup instructions
- contracts/ directory created
- All files placed in specs/003-frontend-hardening/

## Outcome

- ✅ Impact: Created comprehensive implementation plan for frontend security hardening
- 🧪 Tests: No tests created (planning phase)
- 📁 Files: Created plan, research, data model, quickstart, and contracts directory
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan addresses all requirements from user input and follows SDD methodology

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Standard plan creation
- Next experiment (smallest change to try): Proceed with /sp.tasks to generate implementation tasks
