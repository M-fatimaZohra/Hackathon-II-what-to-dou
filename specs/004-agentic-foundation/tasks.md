---
description: "Task list for backend agentic foundation implementation"
---

# Tasks: Backend Agentic Foundation

**Input**: Design documents from `/specs/004-agentic-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Create project structure per implementation plan in backend/
- [x] T002 [P] Initialize Python 3.12 project with FastAPI, SQLModel, uv dependencies
- [ ] T003 [P] Configure linting and formatting tools in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup database schema and migrations framework in backend/src/database/db.py
- [x] T004a Setup database initialization framework in backend/src/database/init_db.py
- [x] T005 [P] Create middleware to verify authentication/authorization requests in backend/src/middleware/auth_handler.py
- [x] T005a Create MCP server implementation in backend/src/my_mcp_server/server.py
- [x] T006 [P] Setup API routing and middleware structure in backend/src/api/
- [x] T007 Create base models/entities that all stories depend on in backend/src/schema/models.py
- [x] T007a Create chat-specific models in backend/src/schema/chat_models.py
- [x] T008 Configure error handling and logging infrastructure in backend/src/main.py
- [x] T009 Setup environment configuration management in backend/src/main.py (loading .env file)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - AI-Powered Task Management (Priority: P1) 🎯 MVP

**Goal**: Provide natural language interaction for task management

**Independent Test**: Can be fully tested by engaging with the chatbot using natural language commands to manage tasks, delivering the primary value of AI-assisted task management.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Contract test for chat endpoint in backend/tests/contract/test_chat.py
- [x] T011 [P] [US1] Integration test for natural language task operations in backend/tests/integration/test_natural_language_tasks.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Update main.py with PROD/DEV toggle and update backend/CLAUDE.md per plan
- [x] T013 [P] [US1] Install openai-agents, mcp, psycopg2-binary dependencies in backend using uv
- [x] T014 [US1] Create config files for both Gemini (GEMINI) and Groq (GORQ) model parameters in backend/src/configs/
  - gemini_config.py for Gemini model parameters (reads GEMINI_API_KEY from env)
  - groq_config.py for Groq model configuration (reads GORQ_API_KEY from env)
- [x] T015 [US1] Configure OpenAI Agents SDK to pull settings from both gemini_config.py (GEMINI) and groq_config.py (GORQ) in backend/src/services/chat_service.py
  - Add configuration for Gemini model parameters
  - Add configuration for Groq model configuration
- [x] T016 [US1] Create 5 Task CRUD tools using FastMCP with user-isolation logic in backend/src/mcp/tools/
- [x] T017 [US1] Create stateless Agent initialization in backend/src/services/chat_service.py that can pull settings from both gemini_config.py (GEMINI) and groq_config.py (GORQ)
  - Support for Gemini model parameters
  - Support for Groq model configuration
- [x] T018 [US1] Implement chatbot runner using Runner() in backend/src/services/chat_service.py (chatbot engine that initializes Agent and handles Runner() logic)
- [x] T018a [US1] Integrate agent with MCP server in backend/src/services/chat_service.py
- [x] T018b [US1] Connect MCP server to agent in backend/src/services/chat_service.py
- [x] T019 [US1] Create POST API endpoint at /api/{user_id}/chat in backend/src/api/chat.py (loads history via conversation_service, gets AI response via chat_service, saves new messages via conversation_service)
- [x] T020 [US1] Add validation and error handling for chat endpoint in backend/src/api/chat.py
- [x] T021 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation Management (Priority: P2)

**Goal**: Maintain conversation context for meaningful ongoing interactions

**Independent Test**: Can be fully tested by having multi-turn conversations with the chatbot, ensuring it remembers context and references previous exchanges appropriately.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T022 [P] [US2] Contract test for conversation persistence in backend/tests/contract/test_conversation.py
- [x] T023 [P] [US2] Integration test for multi-turn conversations in backend/tests/integration/test_conversation_context.py

### Implementation for User Story 2

- [x] T024 [P] [US2] Define Pydantic models for conversation in backend/src/schema/chat_models.py
- [x] T025 [P] [US2] Define SQLModel tables for Conversation and Message in backend/src/schema/models.py (user_id as VARCHAR)
- [x] T026 [US2] Implement conversation history fetching from database in backend/src/services/conversation_service.py (CRUD for Conversation/Message tables)
- [x] T027 [US2] Implement storing and managing new messages in database after processing in backend/src/services/conversation_service.py (CRUD for Conversation/Message tables)
- [x] T028 [US2] Integrate conversation context with chatbot service in backend/src/services/chat_service.py (depends on T017)
- [x] T029 [US2] Add conversation management logic to chat endpoint in backend/src/api/chat.py (loads history via conversation_service, gets AI response via chat_service, saves new messages via conversation_service) (depends on T019)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Production/Development Mode Toggle (Priority: P3)

**Goal**: Safely toggle between production and development modes for testing

**Independent Test**: Can be fully tested by switching between modes and verifying different behaviors and configurations are applied appropriately.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T030 [P] [US3] Contract test for environment mode toggle in backend/tests/contract/test_env_toggle.py
- [x] T031 [P] [US3] Integration test for different environment configurations in backend/tests/integration/test_env_configs.py

### Implementation for User Story 3

- [x] T032 [P] [US3] Create environment configuration in backend/src/main.py (loading .env file for environment toggle)
- [x] T033 [US3] Implement production/development mode toggle logic
- [x] T034 [US3] Apply different security configurations based on environment mode
- [x] T035 [US3] Apply different logging configurations based on environment mode

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - MCP Tool Authentication & Context Fix (Priority: P1) 🎯 Critical Security Fix

**Goal**: Secure authentication context propagation from API layer through service layer to MCP tools to ensure user data isolation

**Independent Test**: Can be fully tested by verifying that all MCP tool calls include auth_user_id in context and that operations without valid auth are rejected, while maintaining user data isolation.

### Tests for User Story 4 (REQUIRED for security)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T042 [P] [US4] Integration test for auth_user_id propagation to MCP tools in backend/tests/integration/test_auth_propagation.py
- [x] T043 [P] [US4] Test user isolation with invalid auth_user_id in backend/tests/unit/test_user_isolation.py
- [x] T044 [P] [US4] Test MCP tool rejection of requests without valid auth_user_id in backend/tests/unit/test_mcp_auth_validation.py

### Implementation for User Story 4

- [x] T045 [P] [US4] Update task_create_tool to accept ctx parameter and validate auth_user_id in backend/src/my_mcp_server/tools/task_create_tool.py
- [x] T046 [P] [US4] Update task_list_tool to accept ctx parameter and validate auth_user_id in backend/src/my_mcp_server/tools/task_list_tool.py
- [x] T047 [P] [US4] Update task_update_tool to accept ctx parameter and validate auth_user_id in backend/src/my_mcp_server/tools/task_update_tool.py
- [x] T048 [P] [US4] Update task_delete_tool to accept ctx parameter and validate auth_user_id in backend/src/my_mcp_server/tools/task_delete_tool.py
- [x] T049 [P] [US4] Update task_complete_tool to accept ctx parameter and validate auth_user_id in backend/src/my_mcp_server/tools/task_complete_tool.py
- [x] T050 [US4] Refactor chat_service run_agent_workflow to pass proper auth context in backend/src/services/chat_service.py
- [x] T051 [US4] Add error handling for missing auth_user_id in MCP tools in backend/src/my_mcp_server/tools/
- [ ] T052 [US4] Update server.py to properly initialize MCP tools with context support in backend/src/my_mcp_server/server.py
- [ ] T053 [US4] Update API contract documentation to reflect string return format changes in specs/api/mcp-tools.md
- [x] T054 [US4] Update MCP integration tests to verify auth context propagation in backend/tests/test_mcp_integration.py

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently - all MCP tools properly validate auth context

---

## Phase 6: User Story 4 - MCP Tool Return Value Fix (Priority: P1) 🎯 Critical UX Fix

**Goal**: Update MCP tool return values to use the "Secret String Receipt" pattern where tools return descriptive strings that contain IDs for AI memory but hide these from users in the final UI response, to prevent agent fallback errors and improve reliability.

**Independent Test**: Can be fully tested by verifying that all MCP tool calls return descriptive strings with SUCCESS/ERROR prefixes instead of JSON objects, ensuring the agent processes responses without triggering fallback errors.

### Tests for User Story 4 (REQUIRED for reliability)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T042 [P] [US4] Integration test for string-based MCP tool responses in backend/tests/integration/test_mcp_string_responses.py
- [x] T043 [P] [US4] Test user isolation with string-formatted error responses in backend/tests/unit/test_user_isolation_strings.py
- [x] T044 [P] [US4] Test MCP tool rejection returns error strings instead of JSON in backend/tests/unit/test_mcp_error_responses.py

### Implementation for User Story 4

- [x] T045 [P] [US4] Update task_create_tool to return descriptive string receipts in format "SUCCESS: Created task '[title]' (ID: [id])" in backend/src/my_mcp_server/tools/task_create_tool.py
- [x] T046 [P] [US4] Update task_list_tool to return descriptive string receipts in format "SUCCESS: Found [n] task(s) for user (ID: [id]): '[title]' ([status])" in backend/src/my_mcp_server/tools/task_list_tool.py
- [x] T047 [P] [US4] Update task_update_tool to return descriptive string receipts in format "SUCCESS: Updated task to '[title]' (ID: [id])" in backend/src/my_mcp_server/tools/task_update_tool.py
- [x] T048 [P] [US4] Update task_delete_tool to return descriptive string receipts in format "SUCCESS: Deleted task '[title]' (ID: [id])" in backend/src/my_mcp_server/tools/task_delete_tool.py
- [x] T049 [P] [US4] Update task_complete_tool to return descriptive string receipts in format "SUCCESS: Completed task '[title]' (ID: [id])" in backend/src/my_mcp_server/tools/task_complete_tool.py
- [x] T050 [US4] Refactor chat_service run_agent_workflow to handle string responses from tools in backend/src/services/chat_service.py
- [x] T051 [US4] Update error handling in MCP tools to return "ERROR: [reason]" strings instead of JSON objects in backend/src/my_mcp_server/tools/
- [x] T052 [US4] Update server.py to properly initialize MCP tools for string response format in backend/src/my_mcp_server/server.py
- [x] T053 [US4] Update API contract documentation to reflect string response changes in specs/api/mcp-tools.md
- [x] T054 [US4] Update MCP integration tests to verify string response format in backend/tests/test_mcp_integration.py

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently - all MCP tools return descriptive string receipts for improved agent reliability

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 [P] Documentation updates in backend/docs/
- [ ] T037 Code cleanup and refactoring
- [ ] T038 Performance optimization across all stories
- [ ] T039 [P] Additional unit tests (if requested) in backend/tests/unit/
- [x] T040 Security hardening
- [ ] T041 Run quickstart.md validation

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
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Addresses MCP tool return value reliability

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
5. Add User Story 4 → Test independently → Deploy/Demo (Reliability improvement!)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4 (MCP reliability)
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