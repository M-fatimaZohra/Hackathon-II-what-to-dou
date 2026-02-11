---
id: 0062
title: refactor-responses-api-protocol-alignment
stage: green
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "responses-api", "sse", "protocol-alignment", "refactor", "streaming"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/chat.py
  - frontend/src/components/ChatProvider.tsx
tests:
  - Manual testing: login, send message, verify ChatKit renders messages
  - Verify console shows no SSE parsing errors
  - Verify ChatKit SDK handles streaming internally
---

## Prompt

Refactor the backend streaming and frontend fetch logic to align strictly with the OpenAI Responses API protocol required by ChatKit v1.5.0.

### 1. Backend Fix (backend/src/api/chat.py)

Update the `stream_chat_response` generator. The current implementation uses Realtime API event names which are incompatible with ChatKit's REST expectations.

- Change all `response.text.delta` events to `response.output_text.delta`.
- Ensure the event sequence is: response.created -> response.output_item.added -> response.content_part.added -> response.output_text.delta (repeated) -> response.output_text.done -> response.output_item.done -> response.done.
- Use unique UUIDs for `response_id` and `item_id`.

### 2. Frontend Fix (frontend/src/components/ChatProvider.tsx)

The current fetch interceptor is over-engineered and breaking the stream.

- Remove the `response.body.tee()` logic and the manual SSE parsing loop.
- Remove the `setMessageHistory` state updates inside the fetch function.
- Simplify the fetcher to simply inject the Authorization header and return the raw Response object to the ChatKit SDK.
- Ensure the 'Content-Type': 'application/json' header is present in the return.

### 3. Verification

The goal is to let the @openai/chatkit-react SDK handle all state management and rendering via its internal streaming logic. The backend must strictly act as a proxy for the OpenAI Responses Item protocol.

## Response snapshot

**Backend Changes (backend/src/api/chat.py):**

1. Renamed `response.text.delta` to `response.output_text.delta` (REST Responses API, not Realtime API)
2. Added new `response.output_text.done` event (step 7) with complete text after streaming loop
3. Updated event sequence to 10 steps: thread.created -> conversation.item.created -> response.created -> response.output_item.added -> response.content_part.added -> response.output_text.delta (repeated) -> response.output_text.done -> response.content_part.done -> response.output_item.done -> response.done
4. Updated docstring to reflect correct event names and sequence

**Frontend Changes (frontend/src/components/ChatProvider.tsx):**

1. Removed `messageHistory` state (`useState<Array<{type: string, content: string}>>`)
2. Removed `response.body.tee()` stream cloning logic
3. Removed entire manual SSE parsing loop (async IIFE with ReadableStream reader)
4. Removed `onResponseStart` and `onResponseEnd` debug callbacks
5. Simplified fetch to: inject Authorization header, transform body, return raw `fetch()` response
6. ChatKit SDK now handles all SSE parsing and state management internally

**Key Insight from Context7 Research:**
- ChatKit Python SDK uses `stream_agent_response()` which automatically converts agent events to ChatKit wire format
- The widget streaming example confirmed `response.output_text.delta` is the correct REST event name
- `response.text.delta` is a Realtime API name, incompatible with ChatKit's REST expectations

## Outcome

- ✅ Impact: Aligned backend SSE events with OpenAI Responses API protocol; removed frontend stream interference that was preventing ChatKit from managing state
- 🧪 Tests: Pending manual testing - login, send message, verify ChatKit renders streaming response
- 📁 Files: Modified backend/src/api/chat.py (event type rename + new event) and frontend/src/components/ChatProvider.tsx (removed tee/parsing, simplified fetch)
- 🔁 Next prompts: Test with authenticated session; if still blank, investigate ChatKit Python SDK integration (chatkit-python) as official backend approach
- 🧠 Reflection: Previous 4 attempts added complexity to the frontend (stream parsing, message tracking, tee cloning). The correct approach is the opposite: simplify the frontend and let ChatKit SDK do its job. The backend was using wrong event type names (Realtime vs REST API).

## Evaluation notes (flywheel)

- Failure modes observed: Using Realtime API event names (response.text.delta) instead of REST Responses API names (response.output_text.delta); frontend stream.tee() was consuming/interfering with the stream before ChatKit could process it
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If ChatKit still shows blank UI, investigate using chatkit-python SDK (ChatKitServer + stream_agent_response) as the official backend protocol handler instead of manually constructing SSE events
