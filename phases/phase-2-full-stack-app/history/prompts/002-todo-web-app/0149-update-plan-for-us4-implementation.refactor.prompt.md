---
id: 0149
title: update-plan-for-us4-implementation
stage: refactor
date: 2026-01-22
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.plan"
labels: ["spec", "plan", "architecture", "us4", "search-filter"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-todo-web-app/plan.md
tests:
  - Phase 4 tasks updated to follow TDD approach
  - ADR-004 added for server-side query building
  - Security constraint added for user data isolation
  - Task breakdown follows red-green-refactor cycle
---

## Prompt

# Role: Lead Architect (SDD-RI Governance)
# Action: Update plan.md for US4 Implementation

Please use the `/sp.plan` tool to refactor the `plan.md` for the current phase. The objective is to bring Phase 4 (Search and Filter) into 100% compliance with our Ratified Constitution (v1.0.0).

## 1. Architectural Strategy Update
In the "Architecture Summary" or "Implementation Strategy" section, add a new **ADR (Architecture Decision Record)**:
- **ADR-004: Server-Side Dynamic Query Building**.
- **Rationale**: To maintain user data isolation and prevent 422 errors, we will use FastAPI `Query` parameters and SQLModel conditional `.where()` chaining. This ensures a stable API contract without modifying path parameters.

## 2. Phase 4 Refactoring (Principle VI: Test-First)
Refactor the "Tasks" list under **Phase 4: Search and Filter Functionality** to strictly follow the RED-GREEN-REFACTOR cycle:
- **Task 4.1 (RED)**: Implement Backend Integration Tests in `backend/tests/test_search.py` specifically for cross-user isolation and partial-match logic.
- **Task 4.2 (GREEN)**: Implement dynamic filtering in `task_service.py` to satisfy the tests.
- **Task 4.3 (CONTRACT)**: Update the GET route in `tasks.py` to accept and pass optional query parameters.
- **Task 4.4 (FRONTEND)**: Implement `SearchFilter.tsx` using `URLSearchParams` for safe URL construction and a 300ms debounce.

## 3. Safety Guardrails
Update the "Security Implementation" section to include:
- **Primary Filter Constraint**: Every filtered query MUST have `.where(Task.user_id == user_id)` as the base condition before any search or priority filters are appended.

Please output the updated `plan.md` content following these constitutional requirements.

## Response snapshot

Successfully updated the plan.md file to bring Phase 4 (Search and Filter functionality) into compliance with the Ratified Constitution (v1.0.0):

### 1. Added ADR-004 (Architecture Decision Record):
- Created new ADR section in the Architecture Summary
- Documented the decision to use FastAPI `Query` parameters and SQLModel conditional `.where()` chaining
- Explained rationale for maintaining user data isolation and preventing 422 errors
- Maintained stable API contract without modifying path parameters

### 2. Refactored Phase 4 to Follow Test-First Principle:
- Restructured tasks to follow the RED-GREEN-REFACTOR cycle:
  - **Task 4.1 (RED)**: Backend Integration Tests for cross-user isolation and partial-match logic
  - **Task 4.2 (GREEN)**: Dynamic filtering implementation in task_service.py
  - **Task 4.3 (CONTRACT)**: GET route update to accept optional query parameters
  - **Task 4.4 (FRONTEND)**: SearchFilter component implementation with safe URL construction
- Updated acceptance criteria to include user data isolation verification

### 3. Added Safety Guardrails:
- Included primary filter constraint requiring `.where(Task.user_id == user_id)` as base condition
- Emphasized that user data isolation must be maintained in all filtered queries

### 4. Constitution Compliance:
- Aligned with Principle VI: Test-First Development (TDD mandatory)
- Ensured Red-Green-Refactor cycle is explicitly followed
- Maintained security requirements for user data isolation
- Added proper architecture decision documentation

The plan now fully complies with the constitution requirements for Test-First Development and includes proper architectural safeguards for security and maintainability.

## Outcome

- ✅ Impact: Phase 4 plan now follows constitutional requirements
- 🧪 Tests: TDD approach integrated into task breakdown
- 📁 Files: Updated plan.md with ADR and refactored Phase 4
- 🔁 Next prompts: Ready for implementation following constitutional guidelines
- 🧠 Reflection: Proper adherence to Test-First principle ensures quality