---
id: 0058
title: fix-chatkit-event-type-mismatch
stage: green
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: continue
labels: ["chatkit", "sse", "event-types", "debugging", "root-cause-analysis"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/chat.py
tests:
  - Manual testing required with authenticated user session
---

## Prompt

User requested continuation from compacted session. Previous context showed:
- ChatKit UI goes blank after streaming completes despite all SSE events being received correctly
- Backend returns 200 OK, all events stream properly (thread.created, thread.message.created, response.text.delta, response.done)
- Frontend successfully intercepts threads.list requests
- Thread IDs match between frontend and backend (223 = 223)
- User directed investigation to layout.tsx ChatKit script loading and Context7 MCP documentation

Task: Diagnose why ChatKit receives all events but doesn't render messages, causing blank UI after response.done.

## Response snapshot

**Investigation Process:**

1. **Attempted Context7 MCP query** - Library "/openai/chatkit" not found
2. **Attempted WebSearch** - API error (400)
3. **Examined ChatKit package structure:**
   - Read frontend/node_modules/@openai/chatkit-react/dist/index.d.ts
   - Read frontend/node_modules/@openai/chatkit/types/index.d.ts
   - Found ChatKitEvents type definitions but no SSE event format details
4. **Analyzed ChatKit CDN script** via WebFetch:
   - URL: https://cdn.platform.openai.com/deployments/chatkit/chatkit.js
   - **CRITICAL DISCOVERY:** Found expected event types:
     - `thread.item.user_message`
     - `thread.item.assistant_message`
     - NOT `thread.message.created` or `thread.message.*`
5. **Examined OpenAI Python SDK ChatKit types:**
   - Read backend/.venv/Lib/site-packages/openai/types/beta/chatkit/chatkit_thread_user_message_item.py
   - Read backend/.venv/Lib/site-packages/openai/types/beta/chatkit/chatkit_thread_assistant_message_item.py
   - Confirmed structure uses `type: "chatkit.user_message"` and `type: "chatkit.assistant_message"`
6. **Checked assistant_stream_event.py:**
   - Found `event: Literal["thread.message.created"]` for Assistants API
   - But ChatKit uses different event naming convention

**Root Cause Identified:**

ChatKit web component expects `thread.item.*` event types with specific structure, but backend was sending `thread.message.*` events. This mismatch caused ChatKit to:
- Receive all events successfully (network logs showed 200 OK)
- Parse SSE format correctly (no protocol errors)
- BUT ignore events due to unrecognized type names
- Result: Blank UI after streaming completes

**Fixes Implemented in backend/src/api/chat.py:**

1. **User message event (lines 55-70):**
   ```python
   # Changed from:
   {
       "type": "thread.message.created",
       "message": {
           "id": f"msg-user-{conversation_id}",
           "role": "user",
           "content": [{"type": "text", "text": message}],
           ...
       }
   }

   # Changed to:
   {
       "type": "thread.item.user_message",
       "item": {
           "id": f"msg-user-{conversation_id}",
           "type": "user_message",
           "thread_id": str(conversation_id),
           "content": [{"type": "input_text", "text": message}],
           "status": "completed",
           "created_at": int(time.time())
       }
   }
   ```

2. **Added assistant message completion event (lines 104-117):**
   - Accumulate assistant response text during streaming
   - Send `thread.item.assistant_message` event with complete response
   - Position BEFORE `response.done` to ensure persistence
   ```python
   assistant_message_event = {
       "type": "thread.item.assistant_message",
       "item": {
           "id": f"msg-assistant-{conversation_id}-{int(time.time())}",
           "type": "assistant_message",
           "thread_id": str(conversation_id),
           "content": [{"type": "text", "text": assistant_response_text}],
           "status": "completed",
           "created_at": int(time.time())
       }
   }
   ```

**Key Changes:**
- Event type: `thread.message.created` → `thread.item.user_message`
- Wrapper key: `message` → `item`
- Content type: `{"type": "text"}` → `{"type": "input_text"}`
- Added type discriminator: `"type": "user_message"`
- Added thread_id field to item structure
- Added assistant message completion event with accumulated text

## Outcome

- ✅ Impact: Critical fix for ChatKit UI blank issue - identified and corrected event type mismatch between backend SSE events and ChatKit web component expectations
- 🧪 Tests: Manual testing required with authenticated user session (login → /tasks → send message → verify persistence)
- 📁 Files: Modified backend/src/api/chat.py (2 event structures updated, text accumulation added)
- 🔁 Next prompts: Test with actual login credentials, verify messages persist after streaming, potentially update specs to document correct event format
- 🧠 Reflection: Deep investigation through ChatKit package structure, CDN script analysis, and OpenAI SDK types revealed the root cause. The issue wasn't in the SSE protocol or network layer, but in semantic event naming conventions that ChatKit's web component strictly expects.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempts to use Context7 MCP and WebSearch failed, requiring direct package inspection. Event type mismatch is a subtle bug that passes all protocol-level checks but fails at semantic layer.
- Graders run and results (PASS/FAIL): Not applicable - requires manual testing with authenticated session
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with login credentials to verify fix works, then consider updating FR-017 and FR-018 in spec.md to document correct event type names for future reference
