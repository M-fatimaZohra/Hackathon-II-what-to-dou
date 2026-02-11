---
id: 0061
title: add-event-ids-status-sse-parser-chatkit
stage: green
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "sse", "event-ids", "status-field", "message-tracking", "streaming-fix"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/chat.py
  - frontend/src/components/ChatProvider.tsx
tests:
  - Manual testing required with authenticated user session
  - Verify console logs show message tracking
  - Verify UI renders and persists messages after streaming
---

## Prompt

User provided 3 specific fixes to resolve ChatKit UI blank screen issue after 3 previous protocol attempts failed:

**Fix 1 (Backend):** Add unique `id` field to EVERY SSE event in backend/src/api/chat.py
- Import uuid module
- Create event counter function next_event_id()
- Add "id" field to all 9 events (thread.created, conversation.item.created, response.created, response.output_item.added, response.content_part.added, response.text.delta, response.content_part.done, response.output_item.done, response.done)
- Generate unique response_id and output_item_id using timestamp + uuid

**Fix 2 (Backend):** Add `"status": "completed"` to the item object in output_item_done_event
- Add to output_item_done_event item object
- Add to response.done event output array

**Fix 3 (Frontend):** Implement SSE event parser in frontend/src/components/ChatProvider.tsx custom fetch function
- Add messageHistory state to track messages
- Use response.body.tee() to clone SSE stream (stream1 for ChatKit, stream2 for parsing)
- Parse stream2 to track conversation.item.created (user messages) and response.output_item.done (assistant messages)
- Add onResponseStart and onResponseEnd callbacks to useChatKit config for debugging

**Expected Result:** Messages will render and persist in ChatKit UI instead of going blank after streaming completes.

## Response snapshot

**Implementation Complete - All 3 Fixes Applied:**

**Backend Changes (backend/src/api/chat.py):**

1. **Added UUID Import and Event Counter:**
```python
import uuid

async def stream_chat_response(user_id: str, conversation_id: int, message: str):
    # Event ID counter for unique SSE event IDs
    event_counter = 0
    def next_event_id():
        nonlocal event_counter
        event_counter += 1
        return f"evt_{event_counter}"
```

2. **Generated Unique IDs with UUID:**
```python
response_id = f"resp_{int(time.time())}_{uuid.uuid4().hex[:8]}"
output_item_id = f"item_{int(time.time())}_{uuid.uuid4().hex[:8]}"
```

3. **Added "id" Field to All 9 Events:**
- thread_event: `"id": next_event_id()`
- user_item_event: `"id": next_event_id()`
- response_created_event: `"id": next_event_id()`
- output_item_added_event: `"id": next_event_id()`
- content_part_added_event: `"id": next_event_id()`
- text_delta_event: `"id": next_event_id()` (in streaming loop)
- content_part_done_event: `"id": next_event_id()`
- output_item_done_event: `"id": next_event_id()`
- response_done_event: `"id": next_event_id()`

4. **Added "status": "completed" to Message Items:**
```python
# output_item_done_event
output_item_done_event = {
    "id": next_event_id(),
    "type": "response.output_item.done",
    "response_id": response_id,
    "output_index": 0,
    "item": {
        "id": output_item_id,
        "type": "message",
        "role": "assistant",
        "status": "completed",  # ADDED
        "content": [{"type": "text", "text": assistant_response_text}]
    }
}

# response_done_event
response_done_event = {
    "id": next_event_id(),
    "type": "response.done",
    "response": {
        "id": response_id,
        "object": "realtime.response",
        "status": "completed",
        "output": [{
            "id": output_item_id,
            "type": "message",
            "role": "assistant",
            "status": "completed",  # ADDED
            "content": [{"type": "text", "text": assistant_response_text}]
        }]
    }
}
```

**Frontend Changes (frontend/src/components/ChatProvider.tsx):**

1. **Added Message History State:**
```typescript
const [messageHistory, setMessageHistory] = useState<Array<{type: string, content: string}>>([]);
```

2. **Implemented SSE Event Parser in Custom Fetch:**
```typescript
// Check if response is SSE stream and parse events for message tracking
const contentType = response.headers.get('content-type');
if (contentType?.includes('text/event-stream') && response.body) {
  console.log('[ChatProvider] 📡 SSE stream detected - setting up event parser');

  // Clone the response so ChatKit can still read it
  const [stream1, stream2] = response.body.tee();

  // Parse stream2 for message tracking (async, non-blocking)
  (async () => {
    const reader = stream2.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const eventData = JSON.parse(line.slice(6));

              // Track user messages (conversation.item.created)
              if (eventData.type === 'conversation.item.created' && eventData.item?.role === 'user') {
                const userText = eventData.item.content?.[0]?.text || '';
                console.log('[ChatProvider] 👤 User message tracked:', userText);
                setMessageHistory(prev => [...prev, { type: 'user', content: userText }]);
              }

              // Track assistant messages (response.output_item.done)
              if (eventData.type === 'response.output_item.done' && eventData.item?.role === 'assistant') {
                const assistantText = eventData.item.content?.[0]?.text || '';
                console.log('[ChatProvider] 🤖 Assistant message tracked:', assistantText);
                setMessageHistory(prev => [...prev, { type: 'assistant', content: assistantText }]);
              }
            } catch (e) {
              // Ignore JSON parse errors for non-JSON data lines
            }
          }
        }
      }
    } catch (error) {
      console.error('[ChatProvider] SSE parsing error:', error);
    } finally {
      reader.releaseLock();
    }
  })();

  // Return response with stream1 for ChatKit to consume
  return new Response(stream1, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
}
```

3. **Added Response Lifecycle Callbacks:**
```typescript
// Response lifecycle callbacks for debugging
onResponseStart: () => {
  console.log('[ChatProvider] 🟢 Response started - assistant streaming begins');
},
onResponseEnd: () => {
  console.log('[ChatProvider] 🔴 Response ended - streaming complete');
  console.log('[ChatProvider] 📊 Message history:', messageHistory);
},
```

**Key Technical Details:**
- Used response.body.tee() to clone ReadableStream without blocking ChatKit
- SSE parser runs asynchronously and non-blocking
- Message tracking provides debugging visibility into what ChatKit receives
- Unique event IDs prevent ChatKit from ignoring duplicate events
- "status": "completed" signals to ChatKit that messages should persist

## Outcome

- ✅ Impact: Implemented 3 critical fixes to resolve ChatKit UI blank screen issue after 3 previous protocol attempts failed
- 🧪 Tests: Ready for manual testing - login, send message, verify console logs show message tracking and UI renders/persists messages
- 📁 Files: Modified backend/src/api/chat.py (added uuid import, event IDs, status fields) and frontend/src/components/ChatProvider.tsx (added SSE parser, message tracking, lifecycle callbacks)
- 🔁 Next prompts: Test with authenticated session, verify real-time streaming display and message persistence, analyze console logs
- 🧠 Reflection: This is the 4th attempt to fix ChatKit streaming. Previous attempts focused on protocol format (thread.item.*, thread.message.*, conversation.item.* + response.*). This attempt adds missing metadata (event IDs, status fields) and frontend visibility (SSE parser). The combination of unique event IDs and status fields should allow ChatKit to properly track and persist messages.

## Evaluation notes (flywheel)

- Failure modes observed: Previous 3 attempts used correct protocol format but missing event IDs and status fields prevented ChatKit from rendering/persisting messages
- Graders run and results (PASS/FAIL): Pending manual testing with authenticated user session
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with login, send message, check console logs for "[ChatProvider] 👤 User message tracked" and "[ChatProvider] 🤖 Assistant message tracked", verify UI shows messages
