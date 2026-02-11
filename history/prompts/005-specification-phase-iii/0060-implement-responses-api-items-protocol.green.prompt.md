---
id: 0060
title: implement-responses-api-items-protocol
stage: green
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "responses-api", "items-protocol", "streaming", "protocol-fix"]
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

User identified critical protocol mismatch: Backend was sending Assistants API format (`thread.message.*` events) but ChatKit expects **Responses API (Items Protocol)** format.

User provided exact requirements:
1. Do NOT use `thread.message.*` events
2. Use `conversation.item.created` for user message (fixes invisible user bubble)
3. Use correct hierarchy for assistant response:
   - `response.created` (Initialize stream)
   - `response.output_item.added` (Create message container)
   - `response.content_part.added` (Create text container)
   - `response.text.delta` (Stream text chunks)
   - `response.output_item.done` (Finalize message)
   - `response.done` (Commit to history)

Task: Rewrite `stream_chat_response` function to strictly follow OpenAI Responses API streaming sequence.

## Response snapshot

**Complete Protocol Rewrite:**

Replaced Assistants API format with Responses API (Items Protocol) format in `backend/src/api/chat.py`:

**Old Format (Assistants API - WRONG):**
```python
# thread.message.created (user)
# thread.message.created (assistant, in_progress)
# thread.message.in_progress
# thread.message.delta (streaming)
# thread.message.completed
```

**New Format (Responses API - CORRECT):**
```python
# 1. thread.created - Thread anchor
# 2. conversation.item.created - User message (completed)
# 3. response.created - Initialize response stream
# 4. response.output_item.added - Create message container
# 5. response.content_part.added - Create text container
# 6. response.text.delta - Stream text chunks (linked to response_id, output_index, content_index)
# 7. response.content_part.done - Finalize content part
# 8. response.output_item.done - Finalize message item
# 9. response.done - Commit to history
```

**Key Implementation Details:**

1. **User Message (conversation.item.created):**
   ```python
   {
       "type": "conversation.item.created",
       "item": {
           "id": "msg-user-123",
           "type": "message",
           "role": "user",
           "content": [{"type": "input_text", "text": message}],
           "status": "completed"
       }
   }
   ```

2. **Response Initialization:**
   ```python
   response_id = f"resp_{int(time.time())}"
   output_item_id = f"item_{int(time.time())}"
   ```

3. **Streaming Deltas (CRITICAL - Must link to IDs):**
   ```python
   {
       "type": "response.text.delta",
       "response_id": response_id,
       "item_id": output_item_id,
       "output_index": 0,
       "content_index": 0,
       "delta": text_chunk
   }
   ```

4. **Finalization Sequence:**
   - content_part.done → output_item.done → response.done
   - Each includes complete accumulated text

**Changes Made:**
- Removed all `thread.message.*` events
- Removed SSE `event:` prefixes (use `data:` only)
- Added proper response/item/content hierarchy
- Linked all deltas to response_id, output_index, content_index
- Changed user message from `thread.message.created` to `conversation.item.created`
- Implemented 9-step streaming sequence exactly as specified

## Outcome

- ✅ Impact: Complete protocol rewrite from Assistants API to Responses API (Items Protocol) format
- 🧪 Tests: Ready for manual testing with authenticated session
- 📁 Files: Rewrote backend/src/api/chat.py stream_chat_response function (200+ lines changed)
- 🔁 Next prompts: Test with login, verify real-time streaming display and message persistence
- 🧠 Reflection: This is the third protocol attempt (thread.item.* → thread.message.* → conversation.item.* + response.*). The Responses API format should be correct as it matches ChatKit's Items Protocol expectations.

## Evaluation notes (flywheel)

- Failure modes observed: Previous attempts used wrong protocol (Assistants API instead of Responses API)
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with authenticated user to verify streaming works and messages persist
