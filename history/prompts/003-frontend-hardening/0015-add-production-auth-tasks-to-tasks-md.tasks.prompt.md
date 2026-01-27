---
id: 0015
title: Add production auth tasks to tasks.md
stage: tasks
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.tasks
labels: ["tasks", "frontend", "security", "cookies", "cors", "production"]
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

Update tasks.md to add new tasks for production authentication fixes:
1. Update api.ts to use production keys (__Secure-better-auth.session_data and __Secure-better-auth.session_token) in the getJwtTokenFromCookie extraction logic
2. Ensure the cookie loop in api.ts correctly parses these __Secure- prefixed values before running the JWT HS256 validation
3. Update main.py (Backend) CORSMiddleware to set allow_credentials=True and map the production Vercel URL to allow_origins
4. Execute npm run build to confirm the production-only logic is type-safe and ready for redeployment

## Response snapshot

Successfully updated the tasks.md file to include new implementation tasks for production authentication fixes:

- Added User Story 4: Production Cookie Extraction & Backend CORS Alignment (Priority: P1)
- Added 6 new implementation tasks (T031-T036) covering:
  - Updating cookie extraction logic in frontend/src/lib/api.ts to handle __Secure- prefixes
  - Modifying cookie search to look for both secure and non-secure cookie names
  - Implementing proper JWT validation for extracted tokens
  - Configuring backend CORS in backend/src/main.py for credential transmission
- All existing completed tasks (T001-T030) remain marked as [X]
- New tasks follow proper format with [P] parallelization markers and [US4] story labels
- Tasks are organized in a new phase following the same pattern as previous user stories

## Outcome

- ✅ Impact: Enhanced tasks.md with production authentication security implementation tasks
- 🧪 Tests: No tests affected by task updates
- 📁 Files: Updated tasks.md with secure cookie and CORS implementation tasks
- 🔁 Next prompts: Ready for implementation of new authentication tasks
- 🧠 Reflection: Tasks now comprehensively cover frontend cookie handling and backend CORS configuration needs

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Task list enhancement
- Next experiment (smallest change to try): Begin implementation of User Story 4 tasks