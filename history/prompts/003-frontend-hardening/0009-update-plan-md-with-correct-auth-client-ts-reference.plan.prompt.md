---
id: 0009
title: Update plan.md with correct auth-client.ts reference
stage: plan
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.plan
labels: ["plan", "frontend", "security", "auth-client", "file-structure"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/plan.md
  - ../../specs/003-frontend-hardening/research.md
  - ../../specs/003-frontend-hardening/quickstart.md
tests:
  - null
---

## Prompt

fix mini error in plan.md

change file name from api-client.ts to auth-client.ts

after that re write quickstart.md and auth-client.ts will have conversion from   http://localhost:3000 to process.env.NEXT_PUBLIC_BASE_URL!

then update any other md(s) (except tasks.md and spec.md) which have same mistake

## Response snapshot

Successfully updated the implementation plan and related documentation files to correct the file name reference from api-client.ts to auth-client.ts:

- Updated plan.md with correct file structure showing auth.ts, auth-client.ts, and api.ts (removed api-client.ts)
- Updated research.md with correct file locations mentioning auth-client.ts
- Verified quickstart.md already had correct information about auth-client.ts with environment variable conversion
- All documentation now accurately reflects the actual project structure with auth-client.ts instead of incorrectly referencing api-client.ts

## Outcome

- ✅ Impact: Fixed incorrect file reference in documentation improving accuracy
- 🧪 Tests: No tests affected by this documentation update
- 📁 Files: Updated plan.md, research.md with correct file structure information
- 🔁 Next prompts: Ready to proceed with implementation tasks
- 🧠 Reflection: Documentation now correctly represents the actual project structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Documentation correction
- Next experiment (smallest change to try): Proceed with implementation tasks based on corrected documentation
