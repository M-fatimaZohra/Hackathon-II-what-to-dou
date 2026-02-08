---
id: 0009
title: Update all specs for Advanced Integration
stage: plan
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: A.ZEE COMPUTERS
command: /sp.plan
labels: [spec-update, advanced-integration, sse-streaming, chatkit-server, sidebar-overlay, sdk-first]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/plan.md
 - specs/ui/components.md
 - specs/ui/pages.md
 - specs/api/rest-endpoints.md
 - specs/architecture.md
 - specs/overview.md
tests:
 -
---

## Prompt

/sp.plan

now i want to update @history/prompts/005-specification-phase-iii/ specifications and
@specs/api/rest-endpoints.md
@specs/architecture.md
@specs/overview.md
@specs/ui/components.md
@pages.md

first update plan.md then update above mention files according to their need to plan

Please update plan.md to align with the simplified ChatKit architecture.

Technical Context Updates:

Directory Structure: Remove the manual chat components from the list. The new structure should only include frontend/src/components/chat/ChatAssistant.tsx and frontend/src/lib/config.ts.

Environment Toggle: Add a section for 'Environment Configuration' using NEXT_PUBLIC_MOD. Detail how IS_DEV will toggle the API_BASE_URL and security settings (as defined in our Skill).

Backend Integration: Explicitly state that the backend must implement the ChatKitServer class from the openai-chatkit Python SDK to handle the streaming protocol correctly.

Authentication Flow: Document the flow: ChatKit UI -> FastAPI (Verified by auth_handler) -> Agent SDK -> MCP Tool -> Neon DB.

Statelessness: Clarify that while the frontend is stateless, the Backend is responsible for fetching thread history from Neon DB during the ChatKit session initialization.

## Response snapshot

Successfully updated all specification files to align with Advanced Integration strategy featuring sidebar overlay, SDK-first approach, SSE streaming, and ChatKitServer implementation.

**Files Updated (6 files):**

1. **plan.md** - Added comprehensive sections:
   - Environment Configuration: NEXT_PUBLIC_MOD toggle with IS_DEV logic, CONFIG object structure
   - Backend Integration: ChatKitServer class implementation, SSE protocol handling
   - Authentication Flow: Complete 8-step flow from ChatKit UI to Neon DB
   - Statelessness Architecture: Frontend stateless, backend manages conversation persistence
   - Updated directory structure: Removed manual components, added ChatAssistant wrapper

2. **components.md** - SDK-first transformation:
   - Removed: ChatWindow, ChatInput, ChatMessage, ChatStatusIndicator, ConversationList components
   - Added: ChatAssistant wrapper component using @openai/chatkit-react SDK's <ChatView />
   - Updated: ChatKitProvider with SSE connection management and baseUrl scoping
   - Included: TypeScript code example showing SDK integration

3. **pages.md** - Sidebar overlay integration:
   - Updated: Tasks page now includes persistent chat sidebar overlay
   - Removed: Separate /chat page section (no longer needed)
   - Added: Detailed chat sidebar flow with 12 steps including SSE streaming
   - Updated: Protected routes list (removed /chat route)
   - Added: Performance targets including TTFT < 500ms

4. **rest-endpoints.md** - SSE streaming specification:
   - Updated: POST /api/{user_id}/chat endpoint with SSE response format
   - Added: Accept: text/event-stream header requirement
   - Added: SSE event types (message, mcp_tool, complete, error)
   - Added: Backend implementation details with ChatKitServer class
   - Added: TTFT < 500ms performance target
   - Enhanced: JWT verification via auth_handler middleware

5. **architecture.md** - Simplified architecture diagram:
   - Updated: Architecture diagram showing sidebar overlay and SSE streaming
   - Removed: WebSocket references, replaced with SSE
   - Added: ChatKitServer component in backend layer
   - Updated: AI Chatbot Flow with 12-step SSE streaming process
   - Added: Key architecture changes summary for Phase III

6. **overview.md** - Phase III comprehensive update:
   - Expanded: Phase III description from 8 to 15 bullet points
   - Added: UI approach (sidebar overlay), SDK-first strategy
   - Added: Streaming protocol (SSE), backend implementation (ChatKitServer)
   - Added: Performance metrics (TTFT < 500ms)
   - Added: Authentication flow, statelessness clarification
   - Added: Environment toggle details, integration flow

**Key Changes Across All Files:**

1. **UI Shift**: Separate /chat page → Persistent sidebar overlay on /tasks page
2. **SDK-First**: Manual components → Single ChatAssistant wrapper using ChatKit SDK
3. **Streaming**: WebSocket/ChatKit streaming → Server-Sent Events (SSE) from FastAPI
4. **Backend**: Generic chat endpoint → ChatKitServer class from openai-chatkit SDK
5. **Performance**: Generic response time → TTFT < 500ms target
6. **Architecture**: Complex component tree → Simplified SDK-based approach
7. **Environment**: Implicit config → Explicit NEXT_PUBLIC_MOD toggle with CONFIG object
8. **Authentication**: Basic JWT → Enhanced with auth_handler middleware and baseUrl scoping
9. **Statelessness**: Ambiguous → Clear frontend stateless, backend manages DB persistence

**Consistency Maintained:**
- All files reference SSE streaming protocol
- All files mention ChatKitServer implementation
- All files specify JWT verification via auth_handler
- All files reference sidebar overlay approach
- All files include TTFT < 500ms performance target
- All files mention baseUrl scoped to /api/{user_id}/chat

## Outcome

- ✅ Impact: Comprehensive specification update across 6 files to align with Advanced Integration strategy, simplifying architecture while enhancing performance and security
- 🧪 Tests: No tests affected - specification updates only
- 📁 Files: Updated plan.md, components.md, pages.md, rest-endpoints.md, architecture.md, overview.md
- 🔁 Next prompts: Ready to update tasks.md to reflect simplified architecture, then proceed with implementation
- 🧠 Reflection: Advanced Integration strategy significantly simplifies implementation by leveraging ChatKit SDK's built-in components, improves performance with SSE streaming and TTFT metrics, strengthens security with explicit JWT verification flow, and provides clear environment configuration guidance

## Evaluation notes (flywheel)

- Failure modes observed: None - systematic updates applied consistently across all specification files
- Graders run and results (PASS/FAIL): Consistency check: PASS (all files reference SSE, ChatKitServer, sidebar overlay, TTFT), Completeness check: PASS (all required sections added to plan.md), SDK-first validation: PASS (manual components removed, ChatAssistant wrapper added), Architecture alignment: PASS (all files reflect simplified architecture)
- Prompt variant (if applicable): /sp.plan with detailed Advanced Integration requirements and file-by-file update instructions
- Next experiment (smallest change to try): Update tasks.md to reflect simplified architecture, then validate that all specification files remain consistent during task generation
