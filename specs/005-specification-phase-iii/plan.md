# Implementation Plan: ChatKit Frontend Integration for AI Chatbot

**Branch**: `005-specification-phase-iii` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-specification-phase-iii/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a ChatKit-powered AI chatbot frontend that connects to the backend `/api/{user_id}/chat` endpoint using JWT authentication from `authClient.getSession()`. The frontend will implement a stateless chat interface with advanced integration features including real-time streaming, error handling with exponential backoff, lazy loading, and multi-turn conversation support. All operations maintain user isolation via `/api/{user_id}/` scoping and support both development and production environments.

## Technical Context

**Language/Version**: TypeScript 5.3, React 19.2.3, Next.js 16.1.1
**Primary Dependencies**: ChatKit React SDK, Better Auth 1.4.10, Tailwind CSS v4, React 19
**Storage**: N/A (stateless frontend, conversation state managed by backend)
**Testing**: Jest, React Testing Library, Playwright (E2E)
**Target Platform**: Web (Next.js 16 App Router, modern browsers)
**Project Type**: Web application (frontend component of monorepo)
**Performance Goals**: <2s page load for 95% users, <3s chatbot response for 90% interactions, <1s error display for 95% errors
**Constraints**: Stateless operation (JWT + userId per request), user isolation via `/api/{user_id}/`, <100MB memory for 1000+ message conversations
**Scale/Scope**: 10+ concurrent chat sessions per user, 1000+ messages per conversation, real-time streaming for 95% messages

## Environment Configuration

**Toggle Mechanism**: `NEXT_PUBLIC_MOD` environment variable controls dev/prod behavior

**Configuration Structure** (`frontend/src/lib/config.ts`):
```typescript
const MOD = process.env.NEXT_PUBLIC_MOD || 'production';
export const IS_DEV = MOD === 'developer';

export const CONFIG = {
  API_BASE_URL: IS_DEV ? 'http://localhost:7860' : process.env.NEXT_PUBLIC_API_URL,
  AUTH_BASE_URL: IS_DEV ? 'http://localhost:3000' : process.env.NEXT_PUBLIC_BASE_URL,
  COOKIE_SECURE: !IS_DEV,
  HTTP_ONLY_TOKEN: !IS_DEV,
  REFRESH_CACHE: !IS_DEV,
};
```

**Environment-Specific Behavior**:
- **Development** (`NEXT_PUBLIC_MOD=developer`):
  - API_BASE_URL: `http://localhost:7860`
  - AUTH_BASE_URL: `http://localhost:3000`
  - COOKIE_SECURE: `false` (allows HTTP cookies)
  - HTTP_ONLY_TOKEN: `false` (enables debugging)
  - REFRESH_CACHE: `false` (disables caching for hot reload)

- **Production** (`NEXT_PUBLIC_MOD=production` or unset):
  - API_BASE_URL: From `NEXT_PUBLIC_API_URL` env var
  - AUTH_BASE_URL: From `NEXT_PUBLIC_BASE_URL` env var
  - COOKIE_SECURE: `true` (HTTPS-only cookies)
  - HTTP_ONLY_TOKEN: `true` (prevents XSS attacks)
  - REFRESH_CACHE: `true` (enables caching)

**Usage**: All components and services import from `config.ts` instead of hardcoding values. Never hardcode `true` or `false` for security settings.

## Backend Integration

**Agent Model Configuration**: Backend uses OpenAI models (gpt-4o, gpt-4-turbo) via OpenAI Agents SDK for chat processing

**Streaming Implementation**: Backend uses `Runner.run_streamed()` from OpenAI Agents SDK for token-by-token streaming

**Streaming Protocol**: Server-Sent Events (SSE) for real-time message streaming (FR-015)

**Backend Architecture**:
```python
# backend/src/services/chat_service.py
from agents import Agent, Runner, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent

async def run_agent_workflow_streamed(user_id: str, message: str, conversation_id: int):
    """
    Stream agent responses token-by-token using Runner.run_streamed().

    Uses OpenAI model (gpt-4o) for chat processing and streams events
    as Server-Sent Events (SSE) for real-time frontend display.
    """
    # Create agent with OpenAI model
    agent = Agent(
        name="TodoAssistant",
        model="gpt-4o",  # OpenAI model for chat processing
        instructions=SYSTEM_PROMPT,
        mcp_servers=[connection],
        model_settings=ModelSettings(temperature=0.7)
    )

    # Use Runner.run_streamed() for token-by-token streaming
    result = Runner.run_streamed(agent, input=conversation_text)

    # Stream events as they arrive
    async for event in result.stream_events():
        # Filter for text delta events (token-by-token)
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            yield {"type": "chunk", "content": event.data.delta}

        # Handle tool execution events
        elif event.type == "tool_end":
            yield {"type": "tool_call", "tool_name": event.tool.name}

# backend/src/api/chat.py
from fastapi.responses import StreamingResponse

@router.post("/{user_id}/chat")
async def chat_endpoint_streaming(user_id: str, request: ChatRequest):
    """
    Streaming chat endpoint using SSE protocol.

    Returns Server-Sent Events compatible with ChatKit SDK.
    """
    return StreamingResponse(
        stream_chat_response(user_id, request.conversation_id, request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

**Key Technical Decisions**:
- **Model**: OpenAI gpt-4o (can be configured via environment or Agent constructor)
- **Streaming Method**: `Runner.run_streamed()` from OpenAI Agents SDK v0.7.0
- **Event Filtering**: Filter `ResponseTextDeltaEvent` for text chunks, `tool_end` for tool calls
- **SSE Format**: `data: {"type": "chunk", "content": "..."}\n\n`
- **Integration**: MCP tools for task CRUD operations via `mcp_servers` parameter

**Key Responsibilities**:
- Handle SSE streaming protocol via `Runner.run_streamed()`
- Integrate with OpenAI Agents SDK using OpenAI models
- Route requests to MCP tools
- Fetch conversation history from Neon DB
- Enforce JWT verification via `auth_handler`

## Authentication Flow

**Complete Request Flow**:
```
1. ChatKit UI (Frontend)
   ↓ [User sends message with JWT token]
2. FastAPI Endpoint (/api/{user_id}/chat)
   ↓ [JWT verified by auth_handler middleware]
3. ChatKitServer
   ↓ [Initializes session, fetches thread history from Neon DB]
4. OpenAI Agents SDK
   ↓ [Processes message, determines tool calls]
5. MCP Tool (Task CRUD operations)
   ↓ [Executes database operations]
6. Neon PostgreSQL Database
   ↓ [Returns results]
7. SSE Stream Response
   ↓ [Streams back to frontend via ChatKitServer]
8. ChatKit UI (Frontend)
   [Displays streamed response in real-time]
```

**JWT Verification Points**:
- **Entry Point**: `auth_handler.py` middleware validates JWT before any processing
- **User Isolation**: Extracts `user_id` from JWT and verifies it matches path parameter
- **Scope Enforcement**: All requests scoped to `/api/{user_id}/` endpoints
- **Token Source**: `authClient.getSession().accessToken` from Better Auth 1.4.10

## Statelessness Architecture

**Frontend Statelessness**:
- Frontend does NOT persist conversation state locally
- Each request includes JWT + userId
- No localStorage or sessionStorage for conversation data
- ChatKit SDK manages UI state only (not conversation history)

**Backend State Management**:
- Backend IS responsible for conversation persistence
- Conversation history stored in Neon PostgreSQL database
- During ChatKit session initialization, backend fetches thread history from DB
- Backend maintains conversation context across requests via database queries

**Session Initialization Flow**:
```
1. User opens chat sidebar overlay
2. Frontend sends initialization request with JWT
3. Backend validates JWT and extracts user_id
4. Backend queries Neon DB for user's conversation threads
5. Backend returns thread list to frontend
6. User selects or creates conversation
7. Backend fetches full conversation history from DB
8. Backend initializes ChatKit session with history
9. Frontend displays conversation via ChatKit UI
```

**Data Flow**:
- **Frontend → Backend**: JWT + userId + message content
- **Backend → Database**: Query conversation history by user_id
- **Database → Backend**: Return conversation threads and messages
- **Backend → Frontend**: SSE stream with AI response
- **Backend → Database**: Persist new messages after processing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I - Spec-Driven Development**: ✅ PASS
- Feature originates from written specification (spec.md)
- Specification is the single source of truth
- Implementation will follow spec requirements

**Principle II - AI-Agent-First Approach**: ✅ PASS
- Claude Code is primary implementation agent
- Traceability between specs and code will be maintained
- Agent skills and subagents will be used where appropriate

**Principle III - Iterative & Phased Evolution**: ✅ PASS
- This is Phase 3 (AI-powered Chatbot Interface) of the evolution
- Builds on existing Phase 2 (Full-stack Web Todo App)
- Clean extension of existing architecture

**Principle IV - Clarity Over Cleverness**: ✅ PASS
- Architecture is explainable (ChatKit + Next.js + Better Auth)
- Specs are human-readable first
- No unnecessary complexity introduced

**Principle V - Future-Ready by Design**: ✅ PASS
- Stateless design allows clean scaling
- Component architecture supports future extensions
- Environment-aware configuration for dev/prod

**Principle VI - Test-First (NON-NEGOTIABLE)**: ⚠️ REQUIRES ATTENTION
- TDD mandatory: Tests → User approval → Red → Green → Refactor
- Must create test specifications before implementation
- Will be enforced during tasks phase

**Additional Constraints**: ✅ PASS
- Next.js with Tailwind CSS (frontend) ✓
- Better Auth for authentication ✓
- Follows monorepo structure ✓

**GATE STATUS**: ✅ PASS (with TDD enforcement required in tasks phase)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── tasks/
│   │   │   └── page.tsx             # Tasks page with sidebar chat overlay (FR-001)
│   │   ├── signin/                  # Existing auth pages
│   │   ├── signup/
│   │   ├── layout.tsx               # Root layout with Navigation
│   │   └── page.tsx                 # Home page
│   ├── components/
│   │   ├── chat/
│   │   │   └── ChatAssistant.tsx    # ChatKit SDK wrapper using <ChatKit /> (FR-002)
│   │   ├── ChatProvider.tsx         # Component using useChatKit hook for auth (FR-003)
│   │   ├── Navigation.tsx           # Existing navigation
│   │   ├── TaskList.tsx             # Existing task components
│   │   └── TaskForm.tsx
│   ├── lib/
│   │   ├── config.ts                # Environment configuration with NEXT_PUBLIC_MOD toggle
│   │   ├── chatkit-client.ts        # ChatKit SDK configuration (FR-003)
│   │   ├── api.ts                   # API client (existing, extended)
│   │   ├── auth-client.ts           # Better Auth integration (existing)
│   │   └── auth.ts                  # Auth configuration (existing)
│   ├── types/
│   │   ├── chat.ts                  # Chat TypeScript interfaces
│   │   └── task.ts                  # Existing task types
│   └── styles/
│       └── globals.css              # Global styles with Tailwind
└── tests/
    ├── components/
    │   └── ChatAssistant.test.tsx
    ├── integration/
    │   └── chat-flow.test.tsx
    └── e2e/
        └── chat.spec.ts

backend/
├── src/
│   ├── api/
│   │   └── chat.py                  # /api/{user_id}/chat endpoint with ChatKitServer
│   ├── services/
│   │   └── chat_service.py          # Chat service with Agent SDK integration
│   ├── middleware/
│   │   └── auth_handler.py          # JWT verification middleware
│   └── my_mcp_server/
│       └── server.py                # MCP server for task operations
└── tests/
```

**Structure Decision**: Simplified architecture using ChatKit SDK's built-in components. Frontend uses a single `<ChatAssistant />` wrapper around `@openai/chatkit-react`'s `<ChatKit />` component (receiving control object from useChatKit hook), eliminating the need for manual ChatWindow, ChatInput, and ChatMessage components. Backend implements `ChatKitServer` class from `openai-chatkit` Python SDK to handle SSE streaming protocol. Environment configuration centralized in `config.ts` using `NEXT_PUBLIC_MOD` toggle.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All complexity introduced is justified by functional requirements:

| Consideration | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| ChatKit SDK integration | Required for real-time features (FR-016, FR-017) and advanced chat capabilities | WebSocket implementation from scratch would be more complex and error-prone |
| Stateless architecture | Required by FR-007 for scalability and user isolation (FR-008) | Stateful frontend would violate user isolation requirements and complicate scaling |
| Advanced error handling | Required by FR-013 for production reliability and 99.9% availability (SC-005) | Basic error handling insufficient for success criteria and user experience |
| Environment-aware config | Required by FR-009 for dev/prod support | Single configuration would compromise security and debugging capabilities |

All complexity aligns with Constitution Principle IV (Clarity Over Cleverness) and Principle V (Future-Ready by Design).
