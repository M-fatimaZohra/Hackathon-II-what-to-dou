---

description: "Advanced Integration implementation for ChatKit Frontend with self-hosted backend"
---

# Tasks: ChatKit Frontend Integration (Advanced Integration)

**Input**: Design documents from `/specs/005-specification-phase-iii/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contract.md, quickstart.md

**Scope**: Full implementation of ChatKit-based AI chat functionality using @openai/chatkit-react SDK with self-hosted FastAPI backend. Focus on SDK-first approach with SSE streaming, sidebar overlay UI, and ChatKitServer backend implementation.

**Tests**: Included in Phase 5 for TTFT and MCP tool rendering validation.

**Organization**: Tasks are grouped by implementation phase following the Advanced Integration strategy.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/` for source code
- **Backend**: `backend/src/` for Python code
- **Configuration**: `frontend/src/lib/` for configuration files
- **Components**: `frontend/src/components/` for UI components
- **Types**: `frontend/src/types/` for TypeScript interfaces
- **Pages**: `frontend/src/app/` for Next.js App Router pages

---

## Phase 1: Environment & Config

**Purpose**: Apply dev-prod-toggle-config skill and configure environment variables

**⚠️ CRITICAL**: This phase establishes the foundation for all environment-specific behavior

- [ ] T001 Install @openai/chatkit-react SDK in frontend/package.json
- [ ] T002 Apply dev-prod-toggle-config skill to create frontend/src/lib/config.ts with NEXT_PUBLIC_MOD toggle
- [ ] T003 Implement CONFIG object in frontend/src/lib/config.ts with API_BASE_URL, AUTH_BASE_URL, COOKIE_SECURE, HTTP_ONLY_TOKEN, REFRESH_CACHE
- [ ] T004 Create frontend/.env.local.example with NEXT_PUBLIC_MOD, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BASE_URL, NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- [ ] T005 Update frontend/src/lib/api.ts to use CONFIG.API_BASE_URL instead of hardcoded URLs
- [ ] T006 Verify Better Auth 1.4.10 configuration in frontend/src/lib/auth-client.ts respects CONFIG settings

**Checkpoint**: Environment toggle working, CONFIG object accessible throughout frontend

---

## Phase 2: Authentication Bridge

**Purpose**: Implement useChatKit hook with custom fetch function to inject JWT from Better Auth

**⚠️ CRITICAL**: This phase enables authenticated communication between frontend and backend

- [X] T007 Create frontend/src/types/chat.ts with ChatKitConfig, ChatProviderProps, and ChatError interfaces
- [X] T008 Create frontend/src/components/ChatProvider.tsx component using useChatKit hook (import: ChatKit, useChatKit from '@openai/chatkit-react')
- [X] T009 Implement JWT fetching from authClient.getSession() in custom fetch function
- [X] T010 Implement custom fetch function to add Authorization: Bearer <jwt_token> header to all ChatKit requests
- [X] T011 Configure useChatKit api.url to CONFIG.API_BASE_URL + '/api/{user_id}/chat' with user_id from JWT
- [X] T012 Implement error handling for expired tokens and authentication failures in custom fetch function
- [X] T013 Add onError callback to useChatKit for SSE connection errors and reconnection handling

**Checkpoint**: useChatKit hook successfully injects JWT via custom fetch, handles auth errors

---

## Phase 3: The Copilot UI

**Purpose**: Implement persistent, collapsible sidebar with ChatKit SDK's <ChatKit /> component

- [X] T014 Create frontend/src/components/chat/ChatAssistant.tsx wrapper component
- [X] T015 Integrate @openai/chatkit-react SDK's <ChatKit /> component (not ChatView) in ChatAssistant.tsx with control prop from useChatKit
- [X] T016 Implement sidebar overlay UI with collapsible functionality in ChatAssistant.tsx
- [X] T017 Add toggle button to frontend/src/app/tasks/page.tsx for opening/closing chat sidebar
- [X] T018 Update frontend/src/app/tasks/page.tsx to use ChatProvider component that wraps useChatKit hook
- [X] T019 Implement sidebar positioning (right side, fixed, z-index management) with Tailwind CSS
- [X] T020 Add slide-in/slide-out animations for sidebar (< 300ms transition)
- [X] T021 Implement responsive design for sidebar (mobile: full screen, desktop: 400px width)
- [X] T022 Add close button and keyboard shortcut (Escape key) to close sidebar

**Checkpoint**: Sidebar overlay functional on tasks page, <ChatKit /> renders correctly with control object, animations smooth

---

## Phase 4: Backend Protocol Alignment

**Purpose**: Implement OpenAI model configuration and Runner.run_streamed() for SSE streaming

**⚠️ CRITICAL**: This phase enables SSE streaming and proper ChatKit protocol support

### Backend Dependencies

- [X] T023 Verify OpenAI SDK (openai>=1.59.5) is installed in backend
- [X] T024 Verify OpenAI Agents SDK (openai-agents>=0.7.0) and MCP SDK are installed in backend

### OpenAI Model Configuration

- [X] T025 Configure OPENAI_API_KEY environment variable in backend/.env
- [X] T026 Update backend/src/configs/ to add openai_config.py with OpenAI model configuration
- [X] T027 Create OPENAI_MODEL constant using model="gpt-4.1-nano" for Agent() constructor
- [X] T028 Add ModelSettings configuration with temperature=0.7 for chat responses

### Streaming Implementation with Runner.run_streamed()

- [X] T029 Create run_agent_workflow_streamed() function in backend/src/services/chat_service.py
- [X] T030 Implement Agent initialization with OpenAI model (gpt-4.1-nano) and ModelSettings
- [X] T031 Implement Runner.run_streamed() call with conversation history
- [X] T032 Implement event filtering for ResponseTextDeltaEvent (token-by-token streaming)
- [X] T033 Implement event filtering for tool_start and tool_end events
- [X] T034 Accumulate full_response from text deltas for database persistence
- [X] T035 Save user message and assistant response to database after streaming completes

### Session Endpoint Implementation

- [X] T036 Create POST /api/{user_id}/chat/session endpoint in backend/src/api/chat.py
- [X] T037 Implement client.beta.chatkit.sessions.create() with correct parameters (user, workflow)
- [X] T038 Return SessionResponse with client_secret for frontend
- [X] T039 Add JWT validation and user_id matching in session endpoint

### Streaming Endpoint Refactoring

- [X] T040 Update backend/src/api/chat.py POST /api/{user_id}/chat to return StreamingResponse
- [X] T041 Create stream_chat_response() generator function for SSE events
- [X] T042 Update stream_chat_response() to call run_agent_workflow_streamed()
- [X] T043 Implement SSE event formatting: data: {"type": "chunk", "content": "..."}\n\n
- [X] T044 Add Content-Type: text/event-stream header to streaming response
- [X] T045 Add Cache-Control and Connection headers for SSE protocol

### Authentication & User Isolation

- [X] T046 Verify backend/src/middleware/auth_handler.py validates JWT before processing
- [X] T047 Verify user_id extraction from JWT in auth_handler.py
- [X] T048 Verify user_id path parameter validation (must match JWT user_id)
- [X] T049 Verify 403 Forbidden returned if user_id mismatch detected

**Checkpoint**: Backend streams SSE responses using Runner.run_streamed(), OpenAI model configured, JWT validation enforced

---

## Phase 5: Real-time Validation

**Purpose**: Test TTFT performance and verify MCP tool rendering in stream

### TTFT Testing

- [ ] T040 Create test script to measure Time to First Token (TTFT) for chat requests
- [ ] T041 Send 10 test messages and record TTFT for each request
- [ ] T042 Verify 90% of requests achieve TTFT < 500ms
- [ ] T043 Identify and document any requests exceeding 500ms TTFT
- [ ] T044 Optimize backend processing if TTFT target not met

### MCP Tool Rendering Validation

- [ ] T045 Test task creation via chat: "Create a task to buy groceries"
- [ ] T046 Verify MCP tool response appears in SSE stream (event: mcp_tool)
- [ ] T047 Verify task appears in task list after creation via chat
- [ ] T048 Test task update via chat: "Mark the groceries task as complete"
- [ ] T049 Verify task status updates in database and UI
- [ ] T050 Test task deletion via chat: "Delete the groceries task"
- [ ] T051 Verify task is removed from database and UI

### Error Handling Validation

- [ ] T052 Test expired JWT token handling (should prompt re-authentication)
- [ ] T053 Test network error handling (should retry with exponential backoff)
- [ ] T054 Test backend unavailable scenario (should show error with retry option)
- [ ] T055 Test SSE connection loss (should automatically reconnect)
- [ ] T056 Test user_id mismatch (should return 403 Forbidden)

### End-to-End Integration

- [ ] T057 Test complete user flow: open sidebar → send message → receive streamed response → MCP tool executes → task list updates
- [ ] T058 Test multi-turn conversation: send 5 messages in sequence, verify context maintained
- [ ] T059 Test conversation history loading: refresh page, verify previous messages load correctly
- [ ] T060 Test concurrent chat sessions: open multiple browser tabs, verify user isolation

**Checkpoint**: TTFT < 500ms for 90% of requests, MCP tools render correctly, all error scenarios handled

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Environment & Config)**: No dependencies - can start immediately
- **Phase 2 (Authentication Bridge)**: Depends on Phase 1 completion (needs CONFIG object)
- **Phase 3 (Copilot UI)**: Depends on Phase 2 completion (needs ChatProvider)
- **Phase 4 (Backend Protocol)**: Can run in parallel with Phase 3 (different codebases)
- **Phase 5 (Real-time Validation)**: Depends on Phase 3 AND Phase 4 completion

### Parallel Opportunities

- **Phase 1**: T002, T003 can run in parallel after T001
- **Phase 2**: T007 can run in parallel with T008-T013
- **Phase 3**: T014-T016 can run in parallel, T017-T022 sequential
- **Phase 4**: T023-T024 can run in parallel, T025-T030 sequential, T031-T035 sequential, T036-T039 can run in parallel
- **Phase 5**: T040-T044 sequential, T045-T051 can run in parallel, T052-T056 can run in parallel, T057-T060 sequential

---

## Implementation Strategy

### MVP First (Phase 1-3)

1. Complete Phase 1: Environment & Config
2. Complete Phase 2: Authentication Bridge
3. Complete Phase 3: Copilot UI
4. **STOP and VALIDATE**: Test sidebar opens, ChatKit SDK initializes, JWT injection works
5. Proceed to Phase 4 only after frontend validation

### Full Integration (Phase 4-5)

1. Complete Phase 4: Backend Protocol Alignment
2. **STOP and VALIDATE**: Test SSE streaming works, MCP tools execute
3. Complete Phase 5: Real-time Validation
4. **FINAL VALIDATION**: All success criteria met, TTFT < 500ms, MCP tools render correctly

### Parallel Team Strategy

With multiple developers:

1. **Team A**: Phase 1-3 (Frontend)
2. **Team B**: Phase 4 (Backend) - can start after Phase 1 completes
3. **Team C**: Phase 5 (Testing) - starts after Phase 3 and 4 complete

---

## Notes

- [P] tasks = different files, no dependencies
- Focus on SDK-first approach: leverage @openai/chatkit-react built-in components
- Backend must use ChatKitServer class from openai-chatkit Python SDK
- All requests must include JWT verification via auth_handler middleware
- TTFT < 500ms is a critical performance target
- Commit after each phase completion
- Stop at any checkpoint to validate independently

---

## Success Criteria

The implementation is complete when:

- ✅ Environment toggle works (dev/prod switching via NEXT_PUBLIC_MOD)
- ✅ useChatKit hook with custom fetch injects JWT into all ChatKit SDK requests
- ✅ Sidebar overlay renders on tasks page with <ChatKit /> component
- ✅ Backend uses ChatKitServer with SSE streaming
- ✅ TTFT < 500ms for 90% of chat requests
- ✅ MCP tool responses render correctly in chat stream
- ✅ Task list updates automatically after chat operations
- ✅ All error scenarios handled gracefully
- ✅ User isolation enforced (403 on user_id mismatch)
- ✅ Multi-turn conversations maintain context
