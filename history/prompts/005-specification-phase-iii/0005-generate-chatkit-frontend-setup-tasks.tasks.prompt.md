---
id: 0005
title: Generate ChatKit frontend setup tasks
stage: tasks
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: A.ZEE COMPUTERS
command: /sp.tasks
labels: [task-generation, chatkit, frontend-setup, mvp, environment-toggle]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/tasks.md
tests:
 -
---

## Prompt

/sp.tasks

You are a senior frontend engineer implementing tasks from a Spec-Driven Development plan. Follow the existing specs and plan exactly. Do not introduce new architecture or abstractions unless explicitly required.

## Objective

Implement frontend setup and integration tasks required to support ChatKit-based AI chat functionality in a Next.js App Router project, using an existing monorepo spec structure.

## Task Scope

### 1. Dependency Installation

Add the required ChatKit dependency to the frontend project.

- Install @openai/chatkit-react
- Do not add unrelated SDKs or experimental packages

This task only verifies installation and readiness for usage in later steps.

---

### 2. Environment-Based Dev / Production Toggle

Implement a simple and explicit dev/production toggle system.

Requirements:
- Use a public environment variable (NEXT_PUBLIC_MOD)
- Treat "developer" as dev mode
- All environment switching logic must live inside src/lib/
- Do not scatter conditionals across components

Behavior:
- Resolve base URLs using a single toggle condition
- Support both localhost (dev) and production base URLs
- This toggle must be reusable by auth, API routing, and ChatKit config

Avoid:
- Feature flags
- Config factories
- Runtime detection beyond env variables

---

### 3. Update `/lib` Configuration Files

Update or create files inside `src/lib/` to support:

- Centralized environment detection (dev vs production)
- Shared configuration values (base URLs, API roots, ChatKit config placeholders)

Rules:
- No business logic
- No network calls
- No auth redesign
- Configuration only

The auth client is not modified in this task.

---

### 4. Project Structure Enforcement

Create and organize files strictly according to the plan.

Rules:
- Routing and API handlers live in src/app/
- Chat and UI components live in src/components/
- Configuration and clients live in src/lib/
- Type schemas and interfaces live in src/types/

Do not:
- Introduce new root folders
- Duplicate configuration logic
- Move responsibilities across layers

---

### 5. ChatKit Setup Preparation (No Full Chat Logic)

Prepare the project for ChatKit usage without implementing full chat behavior.

Allowed:
- Typed ChatKit configuration objects
- Placeholder provider setup if required by plan.md
- Environment-aware configuration wiring

Not allowed:
- Streaming optimizations
- Presence systems
- Reconnection logic
- Performance tuning
- Stateful frontend logic

This step is setup-only.

---

### 6. Specs and Monorepo Consistency

All implementation must reflect existing specs under the specs/ directory.

Rules:
- Do not rewrite specs
- Do not add new spec files
- Implementation must follow plan.md and existing specs only

---

## Constraints

- MVP-level implementation only
- No overengineering
- No speculative features
- Prefer clarity over flexibility

## Completion Criteria

The task is complete when:
- ChatKit dependency is installed
- Dev/prod toggle works and is centralized
- Auth client respects environment switching
- File structure matches the plan
- Codebase is ready for next ChatKit task

## Response snapshot

Successfully generated tasks.md with 42 implementation tasks for ChatKit frontend setup, organized by user story and following strict checklist format.

**Task Organization:**

1. **Phase 1: Setup (3 tasks)** - Dependency installation (@openai/chatkit-react) and verification
2. **Phase 2: Foundational (6 tasks)** - Environment toggle implementation with NEXT_PUBLIC_MOD variable, centralized in src/lib/config.ts
3. **Phase 3: User Story 1 (8 tasks)** - Chat interface type definitions and configuration (Message, Conversation, ChatKitConfig)
4. **Phase 4: User Story 2 (7 tasks)** - Advanced integration error types and environment-aware configuration (ChatError, ChatErrorCode, LoggingConfig)
5. **Phase 5: User Story 3 (8 tasks)** - Multi-turn conversation types and API structure (ChatState, SendMessageRequest, Pagination)
6. **Phase 6: Project Structure (5 tasks)** - Enforce plan.md structure (src/app/, src/components/, src/lib/, src/types/)
7. **Phase 7: Polish (5 tasks)** - Documentation and validation

**Key Features:**
- All tasks follow strict format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- 18 tasks marked [P] for parallel execution
- Each user story independently completable and validatable
- Scope limited to setup only (no full chat logic, no UI implementation, no business logic)
- MVP-first approach with clear checkpoints
- Dependency graph showing execution order
- Parallel execution examples provided

**Alignment with Requirements:**
- ✅ Dependency installation (T001)
- ✅ Environment toggle with NEXT_PUBLIC_MOD (T004-T009)
- ✅ Centralized configuration in src/lib/ (T004-T006, T015, T023, T032)
- ✅ Project structure enforcement (T033-T037)
- ✅ ChatKit setup preparation without full logic (T010-T032)
- ✅ Specs consistency maintained (no spec rewrites)
- ✅ MVP-level implementation only

## Outcome

- ✅ Impact: Generated 42 implementation tasks organized by user story for ChatKit frontend setup phase, enabling systematic preparation for full chat implementation
- 🧪 Tests: No tests in this phase - setup and configuration only, tests will be added in future implementation phases
- 📁 Files: Created specs/005-specification-phase-iii/tasks.md with complete task breakdown
- 🔁 Next prompts: Ready for `/sp.implement` to execute setup tasks, or manual implementation following task order
- 🧠 Reflection: Task organization by user story enables independent validation of each setup phase, MVP-first approach focuses on essential setup without overengineering

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation followed template structure and user requirements correctly
- Graders run and results (PASS/FAIL): Task format validation: PASS (all tasks follow `- [ ] [TaskID] [P?] [Story?] Description with file path` format), Scope validation: PASS (setup only, no full implementation), Organization validation: PASS (grouped by user story with clear checkpoints)
- Prompt variant (if applicable): Standard /sp.tasks workflow with specific scope constraints for setup phase only
- Next experiment (smallest change to try): Execute Phase 1-3 tasks (Setup + Foundational + User Story 1) to validate MVP setup approach
