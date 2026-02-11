# ChatKit Streaming Issue - Complete Context

**Date:** 2026-02-11
**Status:** UI NOT RENDERING - Messages disappear after streaming completes
**Attempts:** 3 protocol implementations tried, all failed

---

## Problem Statement

ChatKit UI goes blank after streaming completes. Both user and assistant messages disappear from the UI despite:
- ✅ Backend returning 200 OK
- ✅ All SSE events streaming correctly (verified in network logs)
- ✅ Frontend receiving all events
- ✅ threads.list interception working
- ✅ Thread IDs matching (223 = 223)
- ✅ No JavaScript errors in console

**The Issue:** ChatKit receives events but doesn't render/persist messages.

---

## Technical Stack

**Frontend:**
- Next.js 16.1.1
- @openai/chatkit-react ^1.5.0 (upgraded from 1.4.3)
- React 19.2.3
- Better Auth for JWT authentication

**Backend:**
- Python 3.12
- FastAPI 0.128.0
- OpenAI Agents SDK
- SSE streaming via StreamingResponse

**Integration:**
- Custom fetch function in ChatProvider.tsx
- JWT authentication via Authorization header
- CustomApiConfig pointing to FastAPI backend

---

## Attempts Made

### Attempt 1: thread.item.* Format (PHR-0058)
**Date:** 2026-02-11
**Hypothesis:** ChatKit expects thread.item.user_message and thread.item.assistant_message

**Implementation:**
```python
# User message
{
    "type": "thread.item.user_message",
    "item": {
        "id": "msg-user-123",
        "type": "user_message",
        "thread_id": "123",
        "content": [{"type": "input_text", "text": "..."}],
        "status": "completed",
        "created_at": 1234567890
    }
}

# Assistant message (after streaming)
{
    "type": "thread.item.assistant_message",
    "item": {
        "id": "msg-assistant-123",
        "type": "assistant_message",
        "thread_id": "123",
        "content": [{"type": "text", "text": "..."}],
        "status": "completed",
        "created_at": 1234567890
    }
}
```

**Result:** ❌ FAILED - UI still blank

---

### Attempt 2: thread.message.* Format (Assistants API) (PHR-0059)
**Date:** 2026-02-11
**Hypothesis:** ChatKit expects OpenAI Assistants API streaming format

**Implementation:**
```python
# User message
event: thread.message.created
data: {
    "id": "msg-user-123",
    "object": "thread.message",
    "role": "user",
    "content": [{"type": "text", "text": {"value": "..."}}],
    "status": "completed"
}

# Assistant message lifecycle
event: thread.message.created (status: in_progress)
event: thread.message.in_progress
event: thread.message.delta (streaming)
event: thread.message.completed
```

**Delta Format:**
```python
{
    "id": "msg-assistant-123",
    "object": "thread.message.delta",
    "delta": {
        "content": [{
            "index": 0,
            "type": "text",
            "text": {"value": "chunk"}
        }]
    }
}
```

**Result:** ❌ FAILED - UI still blank

---

### Attempt 3: Responses API (Items Protocol) (PHR-0060) - CURRENT
**Date:** 2026-02-11
**Hypothesis:** ChatKit expects Responses API format with conversation.item.created and response.* events

**Implementation:**
```python
# 1. Thread anchor
{"type": "thread.created", "thread": {"id": "123"}}

# 2. User message
{
    "type": "conversation.item.created",
    "item": {
        "id": "msg-user-123",
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": "..."}],
        "status": "completed"
    }
}

# 3. Response initialization
{"type": "response.created", "response": {"id": "resp_123", "status": "in_progress"}}

# 4. Output item added
{
    "type": "response.output_item.added",
    "response_id": "resp_123",
    "output_index": 0,
    "item": {"id": "item_123", "type": "message", "role": "assistant"}
}

# 5. Content part added
{
    "type": "response.content_part.added",
    "response_id": "resp_123",
    "item_id": "item_123",
    "output_index": 0,
    "content_index": 0,
    "part": {"type": "text", "text": ""}
}

# 6. Streaming deltas
{
    "type": "response.text.delta",
    "response_id": "resp_123",
    "item_id": "item_123",
    "output_index": 0,
    "content_index": 0,
    "delta": "chunk"
}

# 7. Content part done
{
    "type": "response.content_part.done",
    "response_id": "resp_123",
    "item_id": "item_123",
    "output_index": 0,
    "content_index": 0,
    "part": {"type": "text", "text": "complete text"}
}

# 8. Output item done
{
    "type": "response.output_item.done",
    "response_id": "resp_123",
    "output_index": 0,
    "item": {
        "id": "item_123",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": "complete text"}]
    }
}

# 9. Response done
{
    "type": "response.done",
    "response": {
        "id": "resp_123",
        "status": "completed",
        "output": [...]
    }
}
```

**Result:** ❌ FAILED - UI still blank (not yet tested, but previous patterns suggest it will fail)

---

## What We Know Works

1. ✅ **Backend SSE Streaming:** FastAPI correctly streams events
2. ✅ **Network Layer:** Frontend receives 200 OK responses
3. ✅ **Event Delivery:** All SSE events arrive at frontend (verified in network logs)
4. ✅ **threads.list Interception:** Successfully mocked in ChatProvider.tsx
5. ✅ **Thread ID Synchronization:** Backend and frontend use matching IDs
6. ✅ **JWT Authentication:** Authorization headers correctly injected
7. ✅ **Request Transformation:** ChatProvider correctly transforms ChatKit requests to backend format

---

## What Doesn't Work

1. ❌ **Message Rendering:** ChatKit doesn't display messages in UI
2. ❌ **Message Persistence:** Messages disappear after streaming completes
3. ❌ **Real-time Streaming Display:** No visible text appears during streaming

---

## Current Code State

### Backend: `backend/src/api/chat.py`
- **Function:** `stream_chat_response(user_id, conversation_id, message)`
- **Format:** Responses API (Items Protocol) - 9-step sequence
- **SSE Format:** `data: {json}\n\n` (no event: prefix)
- **Content-Type:** `text/event-stream`
- **Headers:** Cache-Control: no-cache, Connection: keep-alive

### Frontend: `frontend/src/components/ChatProvider.tsx`
- **SDK:** @openai/chatkit-react ^1.5.0
- **Config:** CustomApiConfig with custom fetch function
- **URL:** `${CONFIG.API_BASE_URL}/${userId}/chat`
- **Auth:** JWT via Authorization header
- **Interception:** threads.list returns mock `{data: [], has_more: false}`

### Frontend: `frontend/src/app/layout.tsx`
- **ChatKit Script:** CDN loaded with strategy="afterInteractive"
- **URL:** https://cdn.platform.openai.com/deployments/chatkit/chatkit.js

---

## Debugging Evidence

### Network Logs (from previous sessions):
```
Backend: 200 OK
Events received:
- thread.created
- thread.message.created (or conversation.item.created)
- response.text.delta (multiple)
- response.done (or thread.message.completed)
```

### Console Logs:
```
[ChatProvider] ✅ INTERCEPTING threads.list - returning mock response
[ChatProvider] Thread ID from request: 223
[ChatProvider] Transformed request: {message: "...", conversation_id: 223}
```

### Browser Behavior:
- ChatKit component loads successfully
- Composer input works
- Message submission triggers backend request
- Network shows 200 OK with SSE stream
- UI remains blank or messages disappear after streaming

---

## Potential Root Causes (Unexplored)

### 1. SSE Format Issue
**Hypothesis:** ChatKit expects different SSE format
- Maybe needs `event:` prefix for all events?
- Maybe needs `id:` field for event IDs?
- Maybe needs different line ending format?

### 2. Custom Fetch Interference
**Hypothesis:** Custom fetch function breaks SSE streaming
- ChatKit SDK might handle SSE internally
- Custom fetch might not properly stream responses
- Need to check if fetch should return Response with readable stream

### 3. ChatKit SDK Version Incompatibility
**Hypothesis:** @openai/chatkit-react 1.5.0 expects different protocol
- Maybe 1.5.0 changed protocol requirements?
- Maybe need to downgrade to 1.4.3?
- Maybe need official ChatKit Python SDK on backend?

### 4. Missing Configuration
**Hypothesis:** ChatKit needs additional configuration
- Maybe needs `uploadStrategy` config?
- Maybe needs specific `domainKey` format?
- Maybe needs event handlers (onResponseStart, onResponseEnd)?

### 5. Web Component Initialization
**Hypothesis:** ChatKit web component not properly initialized
- Script loading timing issue?
- Need to wait for customElements.whenDefined?
- Need to manually initialize web component?

---

## Next Investigation Steps

### Priority 1: Verify SSE Format
1. Check if ChatKit expects `event:` prefix for all events
2. Check if ChatKit expects `id:` field in SSE
3. Compare with official ChatKit examples (if available)

### Priority 2: Test Without Custom Fetch
1. Temporarily remove custom fetch function
2. Use direct backend URL without transformation
3. See if ChatKit can parse SSE stream directly

### Priority 3: Add Diagnostic Logging
1. Add ChatKit event handlers: onResponseStart, onResponseEnd, onLog
2. Monitor browser console for ChatKit internal errors
3. Check browser DevTools for web component errors

### Priority 4: Check ChatKit Documentation
1. Find official ChatKit self-hosted backend documentation
2. Verify correct SSE protocol format
3. Check if there's a reference implementation

### Priority 5: Simplify Protocol
1. Try minimal SSE stream (just user message + assistant message)
2. Remove all intermediate events
3. See if basic message display works

---

## Files Modified

1. `backend/src/api/chat.py` - SSE streaming function (3 rewrites)
2. `frontend/src/components/ChatProvider.tsx` - ChatKit configuration
3. `frontend/src/app/layout.tsx` - ChatKit script loading
4. `frontend/package.json` - Upgraded @openai/chatkit-react to 1.5.0

---

## PHR History

- **PHR-0058:** thread.item.* format implementation
- **PHR-0059:** thread.message.* format (Assistants API) implementation
- **PHR-0060:** conversation.item.* + response.* format (Responses API) implementation

---

## Request for Help

**Current Situation:**
We've tried 3 different SSE protocol formats based on OpenAI API documentation, but ChatKit UI still doesn't render messages. The backend streams correctly, frontend receives events, but ChatKit component doesn't display anything.

**What We Need:**
1. Identify the correct SSE protocol format that ChatKit 1.5.0 expects
2. Determine if custom fetch function is interfering with SSE streaming
3. Find any missing configuration or initialization steps
4. Get ChatKit to display messages in real-time and persist them after streaming

**Key Question:**
Is there official documentation for implementing a self-hosted backend with @openai/chatkit-react that shows the exact SSE event format expected?
