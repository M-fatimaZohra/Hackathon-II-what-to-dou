# Tasks: Phase II – Full-Stack Todo Web Application

**Input**: Design documents from `/specs/002-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Risk-Based Testing Strategy - Focus on high-risk areas including security (user data isolation, JWT validation), authentication flows, core business logic (task CRUD operations), and API contracts. UI components and styling tested through manual/visual validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Next.js + FastAPI**: frontend in `frontend/`, backend in `backend/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with frontend and backend directories
- [x] T002 [P] Initialize Next.js project in frontend/ with TypeScript and Tailwind CSS
- [x] T003 [P] Initialize FastAPI project in backend/ with Python dependencies
- [x] T004 [P] Configure linting and formatting tools for both frontend and backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Set up Neon Serverless PostgreSQL connection in backend/
- [x] T006 [P] Configure Better Auth with JWT plugin in frontend/
- [x] T007 [P] Implement backend middleware to validate JWT tokens in backend/src/middleware/
- [x] T008 Create database schema for tasks in backend/src/models/task.py
- [x] T009 Configure environment variables management with .env files
- [x] T010 Set up API routing structure in backend/src/api/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Allow users to sign up, sign in, and sign out to access their personal todo list

**Status**: IN PROGRESS - Authentication components implemented but requires backend integration for full functionality

**Independent Test**: Can be fully tested by registering a new account, logging in, and logging out, delivering the core value of personalized task management.

### Implementation for User Story 1

- [x] T011 [P] [US1] Create authentication components in frontend/src/components/auth/
- [x] T012 [P] [US1] Implement signup page in frontend/src/app/signup/page.tsx
- [x] T013 [P] [US1] Implement signin page in frontend/src/app/signin/page.tsx
- [x] T014 [US1] Implement logout functionality in frontend/src/lib/actions/auth-action.ts
- [x] T015 [US1] Integrate Better Auth with Next.js in frontend/src/lib/auth.ts
- [x] T016 [US1] Add navigation for auth pages in frontend/src/components/Navigation.tsx
- [x] T017 [US1] Create API routes for session management in frontend/src/app/api/auth/
- [x] T018 [US1] Update branding for auth pages per specs/branding.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Todo Task Management (Priority: P1)

**Goal**: Allow users to create, view, edit, and delete their tasks to manage their personal responsibilities (authentication temporarily removed)

**Independent Test**: Can be fully tested by creating tasks, viewing them, updating their details, and deleting them, delivering the primary value of task management.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Create Task model in backend/src/models/task.py
- [ ] T018 [P] [US2] Create TaskService in backend/src/services/task_service.py
- [x] T019 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [x] T020 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [x] T021 [US2] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T022 [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T023 [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py
- [x] T024 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx
- [x] T025 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx
- [x] T026 [US2] Create task management page in frontend/src/app/tasks/page.tsx
- [x] T027 [US2] Connect frontend to backend API with proper JWT token handling

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Status Management (Priority: P2)

**Goal**: Allow users to mark tasks as complete or incomplete to track progress and organize work (authentication temporarily removed)

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and seeing the status updates, delivering the value of progress tracking.

### Implementation for User Story 3

- [x] T028 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/tasks.py
- [x] T029 [P] [US3] Create TaskStatusToggle component in frontend/src/components/TaskStatusToggle.tsx
- [x] T030 [US3] Integrate status toggle functionality in frontend/src/components/TaskList.tsx
- [x] T031 [US3] Add validation for task ownership in backend endpoints

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Search and Filter (Priority: P3)

**Goal**: Allow users with many tasks to search and filter their tasks to quickly find and focus on specific tasks (authentication temporarily removed)

**Independent Test**: Can be fully tested by searching for tasks by keyword and filtering by priority/completion status, delivering the value of efficient task discovery.

### Implementation for User Story 4

- [ ] T032 [P] [US4] Enhance TaskService with search and filter methods in backend/src/services/task_service.py
- [ ] T033 [US4] Add search and filter parameters to GET /api/{user_id}/tasks endpoint in backend/src/api/tasks.py
- [ ] T034 [P] [US4] Create SearchFilter component in frontend/src/components/SearchFilter.tsx
- [ ] T035 [US4] Integrate search and filter functionality in frontend/src/components/TaskList.tsx

---

## Phase 7: Frontend-Backend Integration and UI Polish

**Purpose**: Connect frontend and backend, implement responsive design, and add loading/error states (authentication temporarily removed for focused development)

- [x] T036 [P] Set up API client in frontend/src/lib/api.ts with proper error handling
- [x] T037 [P] Add loading states and error handling UI in frontend/src/components/
- [x] T038 [P] Implement responsive design for mobile and desktop in frontend/src/app/
- [x] T039 [P] Add form validation in frontend/src/components/TaskForm.tsx
- [x] T040 Implement real-time updates for task changes in frontend/src/services/
- [x] T041 Add proper error messages for API failures in frontend/src/components/

---

## Phase 8: Security Validation and Testing

**Purpose**: Ensure user data isolation and proper JWT validation

- [x] T042 Validate that users cannot access other users' tasks by testing direct API access
- [x] T043 Test JWT token validation and expiration handling
- [x] T044 Verify all API endpoints require proper JWT token in Authorization header
- [x] T045 Test input validation and sanitization in backend/
- [x] T046 Perform security audit of JWT implementation

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T047 [P] Documentation updates in docs/
- [x] T048 Code cleanup and refactoring
- [x] T049 Performance optimization across all stories
- [x] T050 Security hardening
- [x] T051 Run validation of all implemented features

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No longer depends on User Story 1 (authentication deferred)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on User Story 2 for task functionality
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on User Story 2 for task functionality

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Stories 1 and 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 4: User Story 2 (Task Management) - Authentication deferred to focus on core functionality
4. Complete Phase 3: User Story 1 (Authentication) - To be implemented later
5. **STOP and VALIDATE**: Test User Stories 1 and 2 together
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo (Core functionality!)
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---