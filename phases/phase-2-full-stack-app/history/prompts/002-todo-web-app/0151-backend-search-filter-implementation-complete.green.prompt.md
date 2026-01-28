---
id: 0151
title: backend-search-filter-implementation-complete
stage: green
date: 2026-01-22
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["search", "filter", "backend", "api", "security"]
links:
  spec: specs/002-todo-web-app/spec.md
  plan: specs/002-todo-web-app/plan.md
  tasks: specs/002-todo-web-app/tasks.md
  test: backend/tests/test_search.py
files:
  - backend/src/services/task_service.py
  - backend/src/api/tasks.py
  - specs/002-todo-web-app/tasks.md
tests:
  - All search functionality tests pass
  - All filter functionality tests pass
  - User isolation security tests pass
  - Combined filters tests pass
  - JWT validation remains functional
---

## Prompt

# Role: Backend Engineer (Implementation Phase)

# Context: Phase 6 - User Story 4 (Tasks T032b & T033)

The RED cycle for T032a is verified. Now, proceed with the implementation to satisfy the tests and complete the backend contract.

## 1. Task T032b: Implementation (GREEN Cycle)

- Modify `backend/src/services/task_service.py`.

- Implement dynamic filtering using SQLModel.

- **Constraint**: You must start the query with `.where(Task.user_id == user_id)` to ensure data isolation before applying any optional filters.

- **Logic**:

    - If `search` is provided, use `col(Task.title).ilike(f"%{search}%")` or similar for title/description.

    - If `priority` or `completed` are provided, chain them as additional `.where()` clauses.

## 2. Task T033: API Contract Update

- Update `backend/src/api/tasks.py` in the `get_tasks` endpoint.

- Add `search: Optional[str] = Query(None)`, `priority: Optional[str] = Query(None)`, and `completed: Optional[bool] = Query(None)` as parameters.

- Pass these parameters from the route into your updated `TaskService`.

## 3. Verification

- Run the tests in `backend/tests/test_search.py`.  (if importation problem rise again, move it temporarily to run test )

- **Requirement**: All tests must now pass (GREEN).

Once the tests pass, show me the code changes in `task_service.py` and the test results. Do not proceed to the frontend yet.

## Response snapshot

Successfully completed Tasks T032b and T033 for the backend search and filter functionality:

### 1. Task T032b: Enhanced TaskService with Dynamic Filtering (GREEN)

**Changes to `backend/src/services/task_service.py`:**
- Updated `get_tasks_by_user_id` method to accept optional search, priority, and completed parameters
- Implemented proper SQLModel query building with chained `.where()` clauses
- Ensured data isolation by starting with `.where(Task.user_id == user_id)` before applying filters
- Used `.icontains()` for case-insensitive search in title and description
- Added proper type hints with Optional parameters

### 2. Task T033: Updated API Contract (CONTRACT)

**Changes to `backend/src/api/tasks.py`:**
- Added Query imports for search, priority, and completed parameters
- Updated the GET /{user_id}/tasks endpoint to accept optional query parameters
- Used FastAPI's Query() for proper API documentation and validation
- Passed parameters from the route to the TaskService method
- Maintained user ID validation to ensure security

### 3. Verification Results

**All tests passed successfully:**
- ✅ Keyword search functionality (title/description)
- ✅ Priority filtering (low, medium, high, urgent)
- ✅ Status filtering (completed/incomplete)
- ✅ User isolation security trap (users can't access other users' tasks)
- ✅ Combined filters (search + priority + status)

### 4. Security Implementation

- Maintained strict user data isolation with `.where(Task.user_id == user_id)` as the base condition
- All filters are applied after user ID validation
- No security vulnerabilities introduced

### 5. Task Status Updates

- Marked T032a, T032b, and T033 as completed in tasks.md
- Removed temporary test files created during development
- Maintained all existing functionality while adding new features

## Outcome

- ✅ Impact: Backend search and filter functionality fully implemented
- 🧪 Tests: All 5 test scenarios pass (keyword, priority, status, security, combined)
- 📁 Files: Updated task_service.py and api/tasks.py with new functionality
- 🔁 Next prompts: Ready to proceed with frontend implementation (T034a, T034b, T035)
- 🧠 Reflection: Proper TDD approach followed with tests passing after implementation