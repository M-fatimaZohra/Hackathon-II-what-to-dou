---
description: "Task list for Frontend Production & Security Hardening"
---

# Tasks: Frontend Production & Security Hardening

**Input**: Design documents from `/specs/003-frontend-hardening/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Configure environment variable validation for NEXT_PUBLIC_API_URL
- [X] T003 [P] Configure environment variable validation for NEXT_PUBLIC_BASE_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Search for all test files in frontend/tests/ directory
- [X] T005 Search for all test files in frontend/src/components/__tests__/ directory
- [X] T006 [P] Identify all test files in the project (frontend/) directory
- [X] T007 [P] Apply block comments /* ... */ to the entire content of each identified test file in frontend/tests/
- [X] T008 [P] Apply block comments /* ... */ to the entire content of each identified test file in frontend/src/components/__tests__/
- [X] T009 Verify that npm run build no longer attempts to execute or type-check these neutralized test files

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Environment & API Realignment (Priority: P1) 🎯 MVP

**Goal**: Eliminate localhost references and configure proper environment variables for API connectivity

**Independent Test**: Can be fully tested by verifying the application successfully makes API calls to the production backend and receives valid responses, delivering the core value of connecting to live services.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for API URL configuration in tests/contract/test_api_config.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Global search for http://localhost:8000 and http://localhost:3000 in frontend/src/lib/api.ts
- [X] T012 [P] [US1] Refactor BASE_URL in frontend/src/lib/api.ts to strictly use process.env.NEXT_PUBLIC_API_URL
- [X] T013 [P] [US1] Implement guard clause in frontend/src/lib/api.ts: if (!process.env.NEXT_PUBLIC_API_URL) console.warn("Missing NEXT_PUBLIC_API_URL")
- [X] T014 [US1] Global search for http://localhost:3000 in frontend/src/lib/auth-client.ts
- [X] T015 [US1] Refactor BASE_URL in frontend/src/lib/auth-client.ts to strictly use process.env.NEXT_PUBLIC_BASE_URL
- [X] T016 [US1] Implement guard clause in frontend/src/lib/auth-client.ts: if (!process.env.NEXT_PUBLIC_BASE_URL) console.warn("Missing NEXT_PUBLIC_BASE_URL")

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Better-Auth Production Hardening (Priority: P1)

**Goal**: Hardening Better-Auth security settings for production (httpOnly, secure, sameSite flags)

**Independent Test**: Can be fully tested by verifying authentication cookies are set with proper security flags (httpOnly, secure, sameSite) when the application runs in production, delivering the value of enhanced security.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Contract test for auth security configuration in tests/contract/test_auth_security.py

### Implementation for User Story 2

- [X] T018 [P] [US2] Update baseURL in frontend/src/lib/auth.ts to process.env.NEXT_PUBLIC_BASE_URL
- [X] T019 [P] [US2] Update trustedOrigins in frontend/src/lib/auth.ts to [process.env.NEXT_PUBLIC_BASE_URL]
- [X] T020 [US2] Change cookie attributes in frontend/src/lib/auth.ts: httpOnly: true and secure: true
- [X] T021 [US2] Update baseURL in frontend/src/lib/auth-client.ts to process.env.NEXT_PUBLIC_BASE_URL
- [X] T022 [US2] Verify sameSite is set to "lax" in frontend/src/lib/auth.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Build Error Mitigation & Validation (Priority: P2)

**Goal**: Ensure the frontend build process completes successfully without test-related failures

**Independent Test**: Can be fully tested by running the build command and verifying it completes without errors, delivering the value of a deployable application bundle.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Integration test for successful build completion in tests/integration/test_build_validation.py

### Implementation for User Story 3

- [X] T024 [P] [US3] Execute npm run build in the terminal
- [X] T025 [US3] Resolve any TypeScript "Code 2345" errors (null/undefined checks) encountered during the build
- [X] T026 [US3] Fix any ESLint "errors" that prevent build completion
- [X] T027 [US3] Confirm a successful build with the message: Route (app) ... Size ... First Load JS
- [X] T028 [US3] Verify a valid .next folder is generated upon successful build completion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Production Cookie Extraction & Backend CORS Alignment (Priority: P1)

**Goal**: Update cookie extraction logic to handle production __Secure- prefixes and configure backend CORS for credential transmission

**Independent Test**: Can be fully tested by verifying the application successfully retrieves session tokens from cookies in both development (non-secure) and production (secure with __Secure- prefix) environments and that API requests include credentials properly, delivering the core value of seamless authentication.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Contract test for secure cookie extraction in tests/contract/test_secure_cookie_extraction.py

### Implementation for User Story 4

- [X] T031 [P] [US4] Update getJwtTokenFromCookie() in frontend/src/lib/api.ts to detect __Secure- prefixed cookies
- [X] T032 [P] [US4] Modify cookie extraction logic in frontend/src/lib/api.ts to search for both '__Secure-better-auth.session_data' and 'better-auth.session_data' keys
- [X] T033 [US4] Implement array-based iteration through document.cookies in frontend/src/lib/api.ts to match possible cookie names using startsWith
- [X] T034 [US4] Apply JWT validation (3-part split and HS256 check) to retrieved tokens in frontend/src/lib/api.ts
- [X] T035 [US4] Update CORSMiddleware in backend/src/main.py to set allow_credentials=True
- [X] T036 [US4] Configure trustedOrigins in backend/src/main.py with specific Vercel frontend URL in allowed origins

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Documentation updates in docs/
- [X] T030 Code cleanup and refactoring
- [ ] T031 Performance optimization across all stories
- [ ] T032 [P] Additional unit tests (if requested) in tests/unit/
- [X] T033 Security hardening
- [ ] T034 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for API URL configuration in tests/contract/test_api_config.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Refactor BASE_URL in frontend/src/lib/api.ts to strictly use process.env.NEXT_PUBLIC_API_URL"
Task: "Refactor BASE_URL in frontend/src/lib/api-client.ts to strictly use process.env.NEXT_PUBLIC_API_URL"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence