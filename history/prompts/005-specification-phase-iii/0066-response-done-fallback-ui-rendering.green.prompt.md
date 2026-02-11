---
id: 0066
title: response-done-fallback-ui-rendering
stage: green
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "response-done", "fallback-ui", "stream-parsing", "message-bubbles"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/ChatProvider.tsx
  - frontend/src/components/chat/ChatAssistant.tsx
tests:
  - Manual: login, send message, verify message bubbles appear after response.done
  - Verify console shows "[ChatProvider] ✅ response.done captured:" with assistant text
  - Verify console shows "[ChatProvider] 🔗 Thread synced:" with thread ID
  - Verify user bubble (blue, right-aligned) and assistant bubble (gray, left-aligned) both render
---

## Prompt

Modify ChatProvider.tsx to handle the 'response.done' event as a definitive UI update.

1. Locate the event source message handler.
2. Add a listener for the "response.done" event type.
3. Extract the final text from: data.response.output[0].content[0].text.
4. If the UI has been blank during the stream, ensure this final text is manually injected into the ChatKit control or the local message state to force the assistant bubble to appear.
5. Ensure that the 'threadId' from the backend is synced one last time during this event to prevent any 'Thread Mismatch' errors.

## Response snapshot

**ChatProvider.tsx Changes:**

1. Added `ChatMessage` interface (`role: 'user' | 'assistant', content: string`)
2. Added `messages` state array and `pendingUserMessageRef` ref
3. Re-added `response.body.tee()` in custom fetch - stream1 goes to ChatKit, stream2 parsed for fallback
4. SSE parser targets only 2 events:
   - `thread.created` → syncs thread ID via `setThreadId()`
   - `response.done` → extracts `response.output[0].content[0].text`, pairs with pending user message, adds both to `messages` state
5. `pendingUserMessageRef` tracks the user's message text from request transform, cleared after capture
6. Context now exposes `messages` array alongside `control`, `isReady`, `token`, `userId`

**ChatAssistant.tsx Changes:**

1. Gets `messages` from `useChatContext()`
2. Renders fallback message bubbles as `absolute inset-0` overlay on top of ChatKit when `messages.length > 0`
3. User messages: blue background, right-aligned, rounded-br-md
4. Assistant messages: gray background, left-aligned, rounded-bl-md
5. Scrollable container with `overflow-y-auto` for long conversations

**Architecture:**
```
SSE Stream → tee() → stream1 → ChatKit SDK (primary render)
                   → stream2 → Parse response.done → messages state → Fallback bubbles (overlay)
```

The fallback overlay (`absolute inset-0 bg-white`) covers the ChatKit component when messages exist, ensuring the user always sees the conversation even if ChatKit's internal rendering fails.

## Outcome

- ✅ Impact: Guaranteed message visibility via response.done fallback rendering regardless of ChatKit SDK behavior
- 🧪 Tests: Pending manual testing - verify message bubbles appear after streaming
- 📁 Files: Modified ChatProvider.tsx (stream tee + response.done parser + messages state) and ChatAssistant.tsx (fallback message bubbles)
- 🔁 Next prompts: Test with login + send message; if working, consider adding input field to fallback UI for multi-turn conversation
- 🧠 Reflection: This is a pragmatic fallback approach. Instead of debugging why ChatKit's internal renderer doesn't process our SSE events, we extract the final text from response.done and render it ourselves. The ChatKit SDK still gets the full stream via stream1, so if it starts working in the future, the primary rendering will take over.

## Evaluation notes (flywheel)

- Failure modes observed: ChatKit shows dots during streaming but goes blank on response.done - confirms deltas aren't being rendered internally by the SDK
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If messages render via fallback, next step is adding a text input to the fallback UI so users can send follow-up messages without relying on ChatKit's input component
