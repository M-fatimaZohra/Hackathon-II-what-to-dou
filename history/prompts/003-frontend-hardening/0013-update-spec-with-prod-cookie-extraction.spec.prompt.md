---
id: 0013
title: Update spec with prod cookie extraction
stage: spec
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-frontend-hardening
branch: 003-frontend-hardening
user: user
command: /sp.specify
labels: ["spec", "frontend", "security", "production", "cookies", "cors"]
links:
  spec: ../../specs/003-frontend-hardening/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ../../specs/003-frontend-hardening/spec.md
tests:
  - null
---

## Prompt

Update Spec "003-frontend-hardening" - Production Cookie Extraction and Backend CORS Alignment

## Objective

Finalize the production deployment by resolving the "Session Token Not Found" error through prefix-aware cookie parsing and backend CORS alignment.

## 1. Production Cookie Extraction (The "Secure" Prefix Fix)

- **Problem**: In production HTTPS, Better Auth prefixes cookies with `__Secure-`. The extraction logic in `api.ts` currently misses these, causing session failures.

- **Requirement**: Update the `getJwtTokenFromCookie` method in `api.ts` to be prefix-aware.

- **Implementation**:
  - Create an array of keys: `['__Secure-better-auth.session_data', 'better-auth.session_data', '__Secure-better-auth.session_token', 'better-auth.session_token']`.
  - Iterate through the document cookies and match against this array using `startsWith`.
  - Ensure the JWT validation (3-part split and `HS256` check) is applied to the found token.

## 4. Backend CORS Handshaking (Credentials Support)

- **Requirement**: Update the FastAPI `main.py` (Backend) to explicitly allow the frontend to send these secure cookies.

- **Action**:
  - In `CORSMiddleware`, ensure `allow_origins` includes your specific Vercel URL (not a wildcard).
  - Set `allow_credentials=True`.

- **Reason**: Browsers will block the `__Secure-` cookies from reaching the Hugging Face backend if `allow_credentials` is not enabled on the server side.

## Validation

- Confirm `api.ts` now successfully extracts tokens in an HTTPS environment.
- Run `npm run build` one final time to ensure no new linting errors were introduced by the logic change.

## Response snapshot

Successfully updated the specification to include production cookie extraction and backend CORS alignment requirements:

- Added User Story 4: Production Cookie Extraction & Backend CORS Alignment (Priority: P1)
- Added 7 new functional requirements (FR-010 to FR-016) covering cookie prefix awareness and CORS configuration
- Added 5 new success criteria (SC-008 to SC-012) measuring production authentication functionality
- Updated edge cases to include cookie prefix variations and CORS scenarios
- All changes integrated into the existing specification while maintaining previous functionality requirements

## Outcome

- ✅ Impact: Enhanced specification with production authentication requirements
- 🧪 Tests: No tests affected by specification update
- 📁 Files: Updated spec.md with production cookie and CORS requirements
- 🔁 Next prompts: Ready for planning phase with complete requirements
- 🧠 Reflection: Specification now covers both development and production authentication scenarios

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Specification enhancement
- Next experiment (smallest change to try): Proceed with planning phase for implementation
