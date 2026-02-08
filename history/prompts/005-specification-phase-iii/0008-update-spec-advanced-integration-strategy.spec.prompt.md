---
id: 0008
title: Update spec for Advanced Integration strategy
stage: spec
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: A.ZEE COMPUTERS
command: /sp.specify
labels: [spec-update, advanced-integration, sidebar-overlay, sse-streaming, sdk-first]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/spec.md
tests:
 -
---

## Prompt

/sp.specify

now i want to update @history/prompts/005-specification-phase-iii/ specifications and
@specs/api/rest-endpoints.md
@specs/architecture.md
@specs/overview.md
@specs/ui/components.md
@pages.md

before i update tasks.md

first update spec.md only

Please update spec.md based on our 'Advanced Integration' strategy.

Key changes to apply:

UI Shift: Change FR-001 from a separate /chat page to a Persistent Sidebar Overlay inside the /tasks page.

SDK-First: Remove requirements for manual components like ChatWindow.tsx and ChatInput.tsx. Replace with requirements for a single <ChatAssistant /> wrapper using the @openai/chatkit-react SDK's <ChatView />.

Streaming Protocol: Update FR-016 to specify Server-Sent Events (SSE) as the streaming protocol from the FastAPI backend.

Updated Success Criteria: Change SC-003 (Response Time) to Time to First Token (TTFT): 'The assistant must begin streaming text within 500ms of user input.'

User Isolation: Ensure all functional requirements mention that the baseUrl must be scoped to /api/{user_id}/chat and verified via JWT.

## Response snapshot

Successfully updated spec.md to reflect Advanced Integration strategy with sidebar overlay, SDK-first approach, SSE streaming, and enhanced JWT verification.

**Key Changes Made:**

1. **UI Shift - Sidebar Overlay:**
   - FR-001: Changed from `/chat/page.tsx` route to "persistent sidebar overlay chat interface on the `/tasks` page"
   - User Story 1 acceptance scenario: Updated "open the chat interface" to "open the chat sidebar overlay"
   - SC-007: Changed "Chat interface loads" to "Chat sidebar overlay loads"

2. **SDK-First Approach:**
   - FR-002: Replaced "ChatWindow component to display messages" with "single `<ChatAssistant />` wrapper component that uses `@openai/chatkit-react` SDK's `<ChatView />` component"
   - Removed FR-003 (old ChatInput component requirement)
   - Key Entities: Removed ChatWindow and ChatInput, added ChatAssistant as wrapper component

3. **SSE Streaming Protocol:**
   - FR-015: Changed from "real-time message streaming from ChatKit" to "real-time message streaming via Server-Sent Events (SSE) from the FastAPI backend"
   - FR-016: Updated to "connection pooling and intelligent reconnection logic for SSE connections"
   - User Story 1 acceptance scenario: Added "via SSE streaming" to response display
   - SC-012: Changed to "real-time SSE streaming for 95% of messages"
   - SC-013: Added "for SSE" to connection pooling success rate

4. **TTFT Performance Metric:**
   - SC-003: Replaced "Chatbot response time is under 3 seconds for 90% of interactions" with "Time to First Token (TTFT): The assistant must begin streaming text within 500ms of user input for 90% of interactions"

5. **Enhanced JWT Verification:**
   - FR-003: Added "baseUrl scoped to `/api/{user_id}/chat`" to ChatKit client configuration
   - FR-004: Added "with JWT verification" to backend endpoint connection
   - FR-007: Added "and verified via JWT" to user isolation enforcement
   - FR-010: Added specific endpoint path "via `/api/{user_id}/chat/{conversation_id}` with JWT verification"
   - SC-010: Added "with JWT verification" to user isolation success criteria
   - ChatKitProvider entity: Updated description to include "JWT token and baseUrl scoped to `/api/{user_id}/chat`"

**Functional Requirements Consolidation:**
- Reduced from 17 to 16 functional requirements by consolidating ChatKit configuration
- All requirements now explicitly mention JWT verification and user isolation where applicable

## Outcome

- ✅ Impact: Updated spec.md to align with Advanced Integration strategy, shifting from separate chat page to sidebar overlay, adopting SDK-first approach, specifying SSE streaming, and enhancing JWT verification requirements
- 🧪 Tests: No tests affected - specification update only
- 📁 Files: Updated specs/005-specification-phase-iii/spec.md
- 🔁 Next prompts: Ready to update remaining files (rest-endpoints.md, architecture.md, overview.md, components.md, pages.md) to match updated spec
- 🧠 Reflection: Advanced Integration strategy simplifies implementation by leveraging ChatKit SDK's built-in components, improves performance with SSE streaming and TTFT metrics, and strengthens security with explicit JWT verification requirements throughout

## Evaluation notes (flywheel)

- Failure modes observed: None - systematic updates applied to all relevant sections
- Graders run and results (PASS/FAIL): Consistency check: PASS (all FR references to JWT and user isolation updated), SDK-first validation: PASS (removed manual component requirements, added ChatAssistant wrapper), Streaming protocol: PASS (SSE specified in FR-015, FR-016, SC-012, SC-013), TTFT metric: PASS (SC-003 updated with 500ms target)
- Prompt variant (if applicable): /sp.specify with detailed Advanced Integration strategy requirements
- Next experiment (smallest change to try): Update remaining specification files (rest-endpoints.md, architecture.md, overview.md, components.md, pages.md) to maintain consistency with updated spec.md
