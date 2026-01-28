---
id: 0020
title: Update Documentation for Surgical Auth Fix
stage: spec
date: 2026-01-27
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.plan
labels: ["plan", "documentation", "authentication", "security"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/plan.md
  - ../../specs/003-frontend-hardening/data-model.md
  - ../../specs/003-frontend-hardening/research.md
  - ../../specs/003-frontend-hardening/quickstart.md
tests:
  - null
---

## Prompt

Update the following project documentation to align with the 'Surgical Auth' production fix:

1. Update specs/003-frontend-hardening/plan.md:

   Explicitly state the requirement to modify frontend/src/lib/auth.ts by
   setting session_data.attributes.httpOnly = false.
   Detail that session_token must remain httpOnly = true for security.

2. use data of updated plan.md and update data-model.md research.md and
   quickstart.md

## Response snapshot

Successfully updated all project documentation to align with the 'Surgical Auth' production fix:

- Updated plan.md to reflect the selective httpOnly strategy where session_token maintains httpOnly: true for security while session_data has httpOnly: false to allow JWT extraction
- Added detailed Authentication Security Configuration section explaining the dual-cookie approach
- Updated data-model.md to specify different httpOnly values for session_token vs session_data cookies
- Updated research.md to document the selective httpOnly decision with rationale and alternatives considered
- Updated quickstart.md with the specific code configuration needed for the selective httpOnly approach

All documentation now accurately reflects the "Surgical Fix" approach that balances security requirements with functional needs for cross-domain JWT transmission.

## Outcome

- ✅ Impact: All project documentation now aligns with the surgical auth fix approach
- 🧪 Tests: No new tests added, existing functionality preserved
- 📁 Files: Updated plan.md, data-model.md, research.md, and quickstart.md with selective httpOnly configuration
- 🔁 Next prompts: Ready for implementation based on updated documentation
- 🧠 Reflection: Successfully aligned all documentation with the pragmatic balance between security and functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Documentation alignment
- Next experiment (smallest change to try): Proceed with implementation based on updated docs
