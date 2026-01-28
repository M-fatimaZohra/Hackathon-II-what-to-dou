---
id: 0150
title: refactor-phase6-tdd-compliance
stage: tasks
date: 2026-01-22
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.tasks"
labels: ["tdd", "refactor", "test-first", "compliance", "us4"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-todo-web-app/tasks.md
tests:
  - Phase 6 tasks updated to follow TDD approach
  - RED-GREEN-REFACTOR cycle implemented
  - Security constraint added to tasks
  - Task T052 added to Phase 9 for deployment prep
---

## Prompt

# Role: SDD-RI Compliance Officer

# Action: Refactor Phase 6 for TDD Alignment

Please use the `/sp.tasks` tool to update `tasks.md`. You must observe the existing state of the codebase and the current completion status (Phases 1-5 are marked complete) while refactoring Phase 6 to be 100% compliant with our Test-First mandate.

## 1. Refactor Phase 6 (User Story 4)

Replace the current sequential implementation tasks (T032-T035) with the following RED-GREEN-REFACTOR atomic units:

- [ ] **T032a [US4] [RED]**: Create backend integration tests in `backend/tests/test_search.py` verifying keyword matching, priority filtering, and strict User ID isolation (User A cannot search User B's tasks).
- [ ] **T032b [US4] [GREEN]**: Enhance `TaskService` with dynamic SQLModel query building in `backend/src/services/task_service.py` to satisfy T032a.
- [ ] **T033 [US4] [CONTRACT]**: Update `GET /api/{user_id}/tasks` in `backend/src/api/tasks.py` to accept and pass optional `Query` parameters for search, priority, and completed status.
- [ ] **T034a [US4] [RED]**: Create frontend unit tests for `SearchFilter.tsx` to verify state management and URL parameter generation.
- [ ] **T034b [US4] [GREEN]**: Implement `SearchFilter.tsx` in `frontend/src/components/` using `URLSearchParams` for safe URL construction and a 300ms debounce.
- [ ] **T035 [US4]**: Integrate `SearchFilter` into `TaskList.tsx` and update the API client in `frontend/src/lib/api.ts` to support optional query params.

## 2. Integrity Maintenance

- Do not modify any tasks marked as [x] (completed).
- Maintain all existing path conventions and monorepo structure rules.
- Ensure the "Security Implementation" section in Phase 6 explicitly mentions the **Primary Filter Constraint** (`.where(Task.user_id == user_id)`).

## 3. Deployment Prep

- Add a new task: **T052 [Phase 9]**: Perform a final end-to-end dry run of the search/filter feature in a production-like environment before GitHub push.

Please output the updated `tasks.md` content following these constitutional requirements.

## Response snapshot

Successfully refactored Phase 6 (User Story 4) in tasks.md to be 100% compliant with the Test-First Development mandate:

### 1. Implemented RED-GREEN-REFACTOR Cycle:
- **T032a [RED]**: Created backend integration tests for search functionality with keyword matching, priority filtering, and user ID isolation
- **T032b [GREEN]**: Enhanced TaskService with dynamic SQLModel query building to satisfy the tests
- **T033 [CONTRACT]**: Updated API endpoint to accept optional Query parameters
- **T034a [RED]**: Created frontend unit tests for SearchFilter component
- **T034b [GREEN]**: Implemented SearchFilter component with safe URL construction
- **T035**: Integrated SearchFilter into TaskList and updated API client

### 2. Added Security Implementation:
- Included Primary Filter Constraint requiring `.where(Task.user_id == user_id)` as base condition
- Ensured user data isolation is maintained in all filtered queries

### 3. Deployment Preparation:
- Added T052 task to Phase 9 for end-to-end dry run in production-like environment
- Maintained all existing completed tasks (marked [x]) unchanged
- Preserved existing path conventions and monorepo structure

### 4. Constitutional Compliance:
- Aligned with Principle VI: Test-First Development (TDD mandatory)
- Ensured all requirements follow the red-green-refactor cycle
- Maintained security requirements for user data isolation
- Added proper test coverage for all functionality

The tasks.md file now fully complies with the constitution requirements for Test-First Development and includes proper architectural safeguards for security and maintainability.

## Outcome

- ✅ Impact: Phase 6 tasks now follow constitutional requirements
- 🧪 Tests: TDD approach integrated into task breakdown
- 📁 Files: Updated tasks.md with TDD-compliant task structure
- 🔁 Next prompts: Ready for implementation following constitutional guidelines
- 🧠 Reflection: Proper adherence to Test-First principle ensures quality