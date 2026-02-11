---
id: 0032
title: Specification Alignment Analysis - ChatKit Protocol Bridge
stage: misc
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.analyze
labels: [specification-alignment, protocol-bridge, chatkit-sdk, architecture-analysis]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/spec.md (analyzed)
 - specs/005-specification-phase-iii/plan.md (analyzed)
 - specs/005-specification-phase-iii/research.md (analyzed)
 - specs/005-specification-phase-iii/tasks.md (analyzed)
 - specs/architecture.md (analyzed)
 - specs/api/rest-endpoints.md (analyzed)
 - specs/features/agentic_chat.md (analyzed)
 - backend/src/api/chat.py (analyzed)
 - frontend/src/components/ChatProvider.tsx (analyzed)
tests:
 - none
---

## Prompt

/sp.analyze what changes do we need to make in our specs/005-specification-phase-iii/, specs/api/, specs/features/agentic_chat.md, specs/architecture.md and other important monorepo .md to match our Docs requirement (the image i share you)

## Response

### Executive Summary

**Problem**: Specifications were written assuming ChatKit SDK would accept custom SSE format, but ChatKit SDK requires its own protocol (ThreadStreamEvent objects). This creates a gap between documented architecture and ChatKit SDK reality.

**Solution**: Implement a **Protocol Bridge Layer** that translates between:
- **Backend Format** (custom SSE): `{type: "response.output_text.delta", delta: "..."}`
- **ChatKit Protocol** (expected): ThreadStreamEvent objects with specific structure

**Impact**: 5 specification files need updates to document this bridge layer and align with ChatKit SDK requirements.

---

## Root Cause Analysis

### What Specs Currently Document

| File | Current State | Problem |
|------|---------------|---------|
| **research.md** | Shows correct CustomApiConfig pattern (lines 34-56) | Doesn't explain ChatKit protocol requirements or why bridge is needed |
| **plan.md** | References ChatKitServer integration | ChatKitServer class not implemented; specs assume it exists |
| **tasks.md** | Lists T036-T039 for ChatKitServer session endpoint | Session endpoint removed in actual implementation; tasks outdated |
| **spec.md** | Defines functional requirements | Silent on protocol translation; assumes ChatKit will "just work" |
| **architecture.md** | Shows ChatKitServer integration | Doesn't match actual implementation (custom streaming instead) |
| **api/rest-endpoints.md** | Documents custom SSE format | Doesn't document ChatKit protocol or bridge layer |
| **features/agentic_chat.md** | Defines custom API contract | Doesn't mention ChatKit protocol requirements |

### What Actually Happens

```
Frontend (ChatKit SDK)
  ↓ expects ThreadStreamEvent objects
Backend (FastAPI)
  ↓ sends custom format: {type: "response.output_text.delta", delta: "..."}
  ✗ MISMATCH - ChatKit SDK rejects or misinterprets
```

### Why This Matters

1. **Frontend Configuration Error**: ChatProvider.tsx mixes incompatible config types because specs don't clarify which config type to use
2. **Backend Implementation Confusion**: Tasks reference ChatKitServer that was never implemented
3. **Protocol Incompatibility**: Custom SSE format doesn't match ChatKit SDK's expected protocol
4. **Missing Bridge Documentation**: No specs document how to translate between formats

---

## Specification Changes Required

### 1. **research.md** - Add ChatKit Protocol Documentation

**Current State** (lines 34-56):
- Shows correct CustomApiConfig pattern
- Missing: ChatKit protocol requirements

**Required Changes**:

Add new section after line 56:

```markdown
### ChatKit Protocol Requirements

**ChatKit SDK Protocol**: The @openai/chatkit-react SDK expects responses in ChatKit protocol format, NOT custom JSON.

**ChatKit Protocol Structure**:
```typescript
// ThreadStreamEvent - Base event type
interface ThreadStreamEvent {
  type: "thread.stream.start" | "thread.stream.end" | "thread.item.created" | "thread.item.delta";
  event_id: string;
  created_at: number;
}

// AssistantMessageItem - For assistant responses
interface AssistantMessageItem {
  id: string;
  type: "message";
  role: "assistant";
  content: Array<{
    type: "text";
    text: string;
  }>;
}

// ThreadItemDoneEvent - Signals message completion
interface ThreadItemDoneEvent extends ThreadStreamEvent {
  type: "thread.item.done";
  item: AssistantMessageItem;
}
```

**Backend Custom Format vs ChatKit Protocol**:

| Aspect | Backend Custom Format | ChatKit Protocol |
|--------|----------------------|------------------|
| Message Type | `{type: "response.output_text.delta", delta: "..."}` | `ThreadItemDoneEvent` with `AssistantMessageItem` |
| Tool Calls | `{type: "tool_start", tool_name: "..."}` | `ThreadItemDoneEvent` with tool call metadata |
| Streaming | Token-by-token deltas | Complete message objects |
| Protocol | Custom SSE | ChatKit-specific event structure |

**Protocol Bridge Requirement**: Backend must translate custom format to ChatKit protocol before sending to frontend, OR frontend must translate ChatKit protocol to custom format on receive.

**Recommended Approach**: Implement bridge in backend (translate before sending) to keep frontend simple and ChatKit SDK unaware of custom backend format.
```

**Location**: Insert after line 56 (after the integration pattern code block)

---

### 2. **plan.md** - Add Protocol Bridge Architecture

**Current State** (lines 59-120):
- Documents ChatKitServer integration
- Missing: Protocol bridge layer details

**Required Changes**:

Add new section after line 120 (after "Backend Integration" section):

```markdown
## Protocol Bridge Architecture

**Problem**: Backend uses custom SSE format for flexibility with MCP tools, but ChatKit SDK expects ChatKit protocol.

**Solution**: Implement protocol bridge layer in backend that translates custom format → ChatKit protocol.

**Bridge Responsibilities**:
1. Receive custom SSE events from `run_agent_workflow_streamed()`
2. Translate to ChatKit protocol (ThreadStreamEvent objects)
3. Send ChatKit protocol to frontend
4. Maintain message context and metadata

**Bridge Implementation Location**: `backend/src/services/protocol_bridge.py`

**Translation Logic**:

```python
# Custom format (from agent)
{
  "type": "response.output_text.delta",
  "delta": "Hello"
}

# Translates to ChatKit protocol
{
  "type": "thread.item.delta",
  "event_id": "evt_123",
  "created_at": 1707000000,
  "delta": {
    "type": "content_block_delta",
    "content_block": {
      "type": "text",
      "text": "Hello"
    }
  }
}
```

**Bridge Integration Points**:
- Input: `run_agent_workflow_streamed()` yields custom events
- Processing: `ProtocolBridge.translate()` converts to ChatKit protocol
- Output: `stream_chat_response()` yields ChatKit protocol events

**Key Design Decision**: Bridge is transparent to frontend - ChatKit SDK receives expected protocol format without modification.
```

**Location**: Insert after line 120 (after Backend Integration section, before Authentication Flow)

---

### 3. **tasks.md** - Update Implementation Tasks

**Current State** (lines 86-139):
- Phase 4 references ChatKitServer (not implemented)
- Tasks T036-T039 are outdated

**Required Changes**:

**Replace Phase 4 section (lines 86-139)** with:

```markdown
## Phase 4: Backend Protocol Alignment & Bridge Implementation

**Purpose**: Implement OpenAI model configuration, Runner.run_streamed() for SSE streaming, AND protocol bridge layer

**⚠️ CRITICAL**: This phase enables SSE streaming with ChatKit protocol compatibility

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

### Protocol Bridge Implementation (NEW)

**Purpose**: Translate backend custom format to ChatKit protocol

- [ ] T036 Create backend/src/services/protocol_bridge.py with ProtocolBridge class
- [ ] T037 Implement ProtocolBridge.translate_text_delta() to convert custom text events to ChatKit ThreadItemDeltaEvent
- [ ] T038 Implement ProtocolBridge.translate_tool_call() to convert tool events to ChatKit protocol
- [ ] T039 Implement ProtocolBridge.translate_message_complete() to create ThreadItemDoneEvent with AssistantMessageItem
- [ ] T040 Update stream_chat_response() in backend/src/api/chat.py to use ProtocolBridge for all events
- [ ] T041 Add event_id generation and timestamp tracking in ProtocolBridge
- [ ] T042 Implement message context preservation (role, content, metadata) in bridge

### Streaming Endpoint Implementation

- [ ] T043 Update backend/src/api/chat.py POST /api/{user_id}/chat to return StreamingResponse
- [ ] T044 Create stream_chat_response() generator function for SSE events
- [ ] T045 Update stream_chat_response() to call run_agent_workflow_streamed()
- [ ] T046 Update stream_chat_response() to use ProtocolBridge.translate() for all events
- [ ] T047 Implement SSE event formatting: data: <json>\n\n
- [ ] T048 Add Content-Type: text/event-stream header to streaming response
- [ ] T049 Add Cache-Control and Connection headers for SSE protocol

### Authentication & User Isolation

- [X] T050 Verify backend/src/middleware/auth_handler.py validates JWT before processing
- [X] T051 Verify user_id extraction from JWT in auth_handler.py
- [X] T052 Verify user_id path parameter validation (must match JWT user_id)
- [X] T053 Verify 403 Forbidden returned if user_id mismatch detected

**Checkpoint**: Backend streams SSE responses using Runner.run_streamed(), protocol bridge translates to ChatKit format, OpenAI model configured, JWT validation enforced
```

**Location**: Replace lines 86-139 (entire Phase 4 section)

---

### 4. **spec.md** - Add Protocol Requirements

**Current State** (lines 73-93):
- Defines functional requirements
- Missing: Protocol specification

**Required Changes**:

Add new requirement after FR-016:

```markdown
- **FR-017**: Backend MUST implement protocol bridge layer that translates custom SSE format to ChatKit protocol (ThreadStreamEvent objects) before sending to frontend
- **FR-018**: Backend MUST preserve message context (role, content, metadata) during protocol translation
- **FR-019**: Backend MUST generate unique event_id and timestamp for each ChatKit protocol event
```

**Location**: Insert after line 93 (after FR-016)

---

### 5. **architecture.md** - Update Integration Diagram

**Current State**:
- Shows ChatKitServer integration
- Doesn't match actual implementation

**Required Changes**:

Replace the architecture diagram with:

```markdown
## Architecture: ChatKit Frontend + Custom Backend with Protocol Bridge

### Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Frontend (Next.js 16 + ChatKit React SDK)                       │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ChatProvider (useChatKit hook)                              │ │
│ │ - CustomApiConfig: {domainKey, url, fetch}                 │ │
│ │ - Custom fetch injects JWT Authorization header            │ │
│ │ - Sends: POST /api/{user_id}/chat with message             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP POST + JWT
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend (FastAPI + OpenAI Agents SDK)                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 1. JWT Validation (auth_handler middleware)                │ │
│ │    - Verify JWT signature                                  │ │
│ │    - Extract user_id from JWT                              │ │
│ │    - Verify path user_id matches JWT user_id               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 2. Conversation Service                                    │ │
│ │    - Fetch conversation history from Neon DB               │ │
│ │    - Build message context for agent                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 3. Agent Execution (OpenAI Agents SDK)                     │ │
│ │    - Initialize Agent with gpt-4.1-nano model              │ │
│ │    - Run with Runner.run_streamed()                        │ │
│ │    - Yields: ResponseTextDeltaEvent, tool_start, tool_end  │ │
│ │    - Custom format: {type: "response.output_text.delta"...}│ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 4. Protocol Bridge (NEW)                                   │ │
│ │    - Receives: Custom SSE format from agent                │ │
│ │    - Translates: Custom → ChatKit protocol                 │ │
│ │    - Outputs: ThreadStreamEvent objects                    │ │
│ │    - Preserves: Message context, metadata, event_id        │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 5. SSE Response Stream                                     │ │
│ │    - Format: data: <ChatKit protocol JSON>\n\n             │ │
│ │    - Headers: Content-Type: text/event-stream              │ │
│ │    - Streaming: Token-by-token via ChatKit protocol        │ │
│ └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │ SSE Stream (ChatKit Protocol)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Frontend (ChatKit React SDK)                                    │
│ - Receives: ThreadStreamEvent objects                           │ │
│ - Renders: Real-time chat messages                              │ │
│ - Displays: MCP tool responses                                  │ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Protocol Bridge in Backend**: Translates custom format to ChatKit protocol before sending to frontend
   - Keeps frontend simple (ChatKit SDK unaware of custom backend)
   - Centralizes protocol logic in one place
   - Easier to maintain and test

2. **Custom Backend Format Preserved**: Backend continues using custom format internally
   - Flexibility for MCP tool integration
   - Easier to extend with new event types
   - Decouples backend from ChatKit SDK changes

3. **Stateless Frontend**: Frontend does not persist conversation state
   - Each request includes JWT + userId
   - Backend manages conversation history in Neon DB
   - Enables user isolation and scalability
```

**Location**: Replace existing architecture diagram section

---

### 6. **api/rest-endpoints.md** - Document Protocol Bridge

**Current State**:
- Documents custom SSE format
- Missing: ChatKit protocol documentation

**Required Changes**:

Add new section:

```markdown
## Protocol Bridge: Custom Format → ChatKit Protocol

### Why Bridge is Needed

Backend uses custom SSE format for flexibility with MCP tools, but ChatKit SDK expects ChatKit protocol. The bridge translates between formats transparently.

### Custom Backend Format (Internal)

```json
// Text delta event
{
  "type": "response.output_text.delta",
  "delta": "Hello, "
}

// Tool start event
{
  "type": "tool_start",
  "tool_name": "create_task"
}

// Tool end event
{
  "type": "tool_end",
  "tool_name": "create_task",
  "output": "Task created successfully"
}
```

### ChatKit Protocol Format (Sent to Frontend)

```json
// Text delta event (translated)
{
  "type": "thread.item.delta",
  "event_id": "evt_20260209_001",
  "created_at": 1707000000,
  "delta": {
    "type": "content_block_delta",
    "content_block": {
      "type": "text",
      "text": "Hello, "
    }
  }
}

// Message complete event
{
  "type": "thread.item.done",
  "event_id": "evt_20260209_002",
  "created_at": 1707000001,
  "item": {
    "id": "msg_123",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "Hello, how can I help?"
      }
    ]
  }
}
```

### Translation Rules

| Custom Format | ChatKit Protocol | Notes |
|---------------|------------------|-------|
| `response.output_text.delta` | `thread.item.delta` with `content_block_delta` | Token-by-token streaming |
| `tool_start` | `thread.item.delta` with tool metadata | Tool execution started |
| `tool_end` | `thread.item.delta` with tool result | Tool execution completed |
| End of stream | `thread.item.done` with `AssistantMessageItem` | Message complete |

### Bridge Implementation

Location: `backend/src/services/protocol_bridge.py`

Responsibilities:
- Translate custom events to ChatKit protocol
- Generate unique event_id for each event
- Add timestamp (created_at)
- Preserve message context and metadata
- Handle streaming completion
```

**Location**: Add as new section at end of file

---

### 7. **features/agentic_chat.md** - Add Protocol Note

**Current State**:
- Defines custom API contract
- Missing: Protocol bridge explanation

**Required Changes**:

Add note after API contract section:

```markdown
## Protocol Bridge Note

The API contract above defines the backend's internal custom format. However, when responses are sent to the ChatKit React SDK frontend, they are automatically translated to ChatKit protocol format via the protocol bridge layer.

**Frontend receives**: ChatKit protocol (ThreadStreamEvent objects)
**Backend uses internally**: Custom format (for flexibility with MCP tools)
**Bridge**: Translates between formats transparently

This allows the backend to maintain flexibility with MCP tool integration while providing the ChatKit SDK with the protocol format it expects.
```

**Location**: Add after API contract section

---

## Summary of Changes

### Files to Update

| File | Changes | Priority |
|------|---------|----------|
| **research.md** | Add ChatKit protocol requirements section | HIGH |
| **plan.md** | Add protocol bridge architecture section | HIGH |
| **tasks.md** | Replace Phase 4 with protocol bridge tasks | HIGH |
| **spec.md** | Add FR-017, FR-018, FR-019 requirements | MEDIUM |
| **architecture.md** | Update integration diagram with bridge | HIGH |
| **api/rest-endpoints.md** | Add protocol bridge documentation | MEDIUM |
| **features/agentic_chat.md** | Add protocol bridge note | LOW |

### Implementation Order

1. **Update research.md** - Document ChatKit protocol requirements
2. **Update plan.md** - Add protocol bridge architecture
3. **Update tasks.md** - Add protocol bridge implementation tasks
4. **Update architecture.md** - Update integration diagram
5. **Update spec.md** - Add protocol requirements
6. **Update api/rest-endpoints.md** - Document protocol bridge
7. **Update features/agentic_chat.md** - Add protocol bridge note

### Key Architectural Decision

**Protocol Bridge Location**: Backend (not frontend)
- **Rationale**: Keeps frontend simple, centralizes protocol logic, easier to maintain
- **Implementation**: `backend/src/services/protocol_bridge.py`
- **Integration**: Used in `stream_chat_response()` to translate all events

---

## Outcome

- ✅ Impact: Identified 7 specification files requiring updates to document protocol bridge layer and align with ChatKit SDK requirements
- 📁 Files: Analyzed research.md, plan.md, tasks.md, spec.md, architecture.md, api/rest-endpoints.md, features/agentic_chat.md
- 🔁 Next prompts: Update each specification file with protocol bridge documentation, Implement protocol_bridge.py in backend, Update ChatProvider.tsx to use correct CustomApiConfig, Test end-to-end ChatKit integration
- 🧠 Reflection: The root cause of the handshake failure was not a bug in the code, but a gap in the specifications. Specs documented what SHOULD happen without accounting for ChatKit SDK's protocol requirements. The solution is to document the protocol bridge layer that translates between the backend's custom format (for flexibility) and ChatKit's expected protocol (for SDK compatibility). This maintains the backend's flexibility while ensuring ChatKit SDK receives the protocol format it expects.

## Evaluation notes (flywheel)

- Failure modes observed: Specification gap (specs didn't account for ChatKit protocol requirements), Configuration type confusion (frontend mixed incompatible config types), Missing bridge documentation (no specs documented protocol translation), Implementation drift (tasks referenced ChatKitServer that was never implemented)
- Graders run and results (PASS/FAIL): Specification completeness: FAIL (protocol bridge not documented), Architecture clarity: FAIL (diagram doesn't show bridge), Task accuracy: FAIL (tasks reference non-existent ChatKitServer), Protocol documentation: FAIL (no specs explain ChatKit protocol requirements), Root cause analysis: PASS (identified specification gap as root cause)
- Prompt variant (if applicable): /sp.analyze with explicit instruction to compare specs with actual implementation, identify gaps, and document required changes
- Next experiment (smallest change to try): Update research.md to add ChatKit protocol requirements section, then update plan.md to add protocol bridge architecture section, then update tasks.md to replace Phase 4 with protocol bridge implementation tasks

