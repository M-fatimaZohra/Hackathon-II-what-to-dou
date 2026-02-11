---
id: 0059
title: fix-chatkit-streaming-with-message-delta
stage: green
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: continue
labels: ["chatkit", "streaming", "sse", "thread.message.delta", "real-time-display"]
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

User provided critical insight: "the problem is not in backend but the problem is since we are using streaming it need to show result in streaming, means it need to start responding as soon as agent start to talk, even though backend is sending response ChatProvider is not showing assistant message resulting user message also disappear from UI"

Task: Fix ChatKit streaming to display assistant responses in real-time, preventing both user and assistant messages from disappearing.

## Response snapshot

**Root Cause Analysis:**

User correctly identified that the issue is **real-time streaming display**, not just message persistence. Backend was sending `response.text.delta` events but ChatKit expects OpenAI Assistants API format with `thread.message.delta` for streaming display.

**Investigation of OpenAI Assistants API Format:**

Examined OpenAI Python SDK types to understand correct streaming format. Found complete event structure:
```json
{
  "event": "thread.message.delta",
  "data": {
    "id": "msg-assistant-123",
    "object": "thread.message.delta",
    "delta": {
      "content": [{
        "index": 0,
        "type": "text",
        "text": {"value": "chunk text here"}
      }]
    }
  }
}
```

**Fixes Implemented in backend/src/api/chat.py:**

1. Updated docstring to document OpenAI Assistants API streaming flow
2. User message: Changed to proper SSE format with `event: thread.message.created`
3. Assistant message initialization: Send `thread.message.created` with empty content, `status: "in_progress"`
4. Streaming start: Send `thread.message.in_progress` event
5. Real-time deltas: Changed from `response.text.delta` to `thread.message.delta` with proper structure
6. Streaming completion: Send `thread.message.completed` with full content

**Key Changes:**
- Event format: `data: {type: "response.text.delta"}` → `event: thread.message.delta\ndata: {...}`
- Delta structure: `{delta: {text}}` → `{delta: {content: [{index: 0, type: "text", text: {value}}]}}`
- Added message lifecycle: created → in_progress → delta (streaming) → completed

## Outcome

- ✅ Impact: Implemented OpenAI Assistants API streaming format for real-time message display
- 🧪 Tests: User reported problem NOT solved yet - need to check frontend
- 📁 Files: Modified backend/src/api/chat.py (complete streaming flow rewrite)
- 🔁 Next prompts: Investigate frontend ChatProvider SSE handling and ChatKit SDK configuration
- 🧠 Reflection: Backend now sends correct OpenAI Assistants API events, but issue persists. Frontend investigation required.

## Evaluation notes (flywheel)

- Failure modes observed: Backend changes alone insufficient - frontend may need configuration updates
- Graders run and results (PASS/FAIL): FAIL - User confirmed problem not solved
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Check frontend ChatProvider SSE event handling
