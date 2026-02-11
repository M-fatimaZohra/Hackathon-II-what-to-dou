---
id: 0064
title: fix-magic-string-and-chatkit-css
stage: green
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "magic-string", "css", "shadow-dom", "rendering-fix"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/chat.py
  - frontend/src/app/layout.tsx
tests:
  - Manual testing: login, send message, verify user + assistant message bubbles render
  - Verify ChatKit Shadow DOM components have visible height and opacity
  - Verify no blank UI after streaming completes
---

## Prompt

Fix the ChatKit v1.5.0 rendering issue by aligning the backend object schema and frontend styles.

### 1. Backend Fix (chat.py):

- Update the `object` field in `response.created` and `response.done` events from `"response"` to `"realtime.response"`. This is the mandatory "Magic String" the SDK's internal state machine requires to trigger the message list render.

- Ensure the `id` in `response.created` and `response.done` remains consistent throughout the stream.

### 2. Frontend Fix (layout.tsx):

- Add the official ChatKit CSS stylesheet to the `<head>` of layout.tsx.

- Insert: `<link rel="stylesheet" href="https://cdn.platform.openai.com/deployments/chatkit/chatkit.css" />`

- This ensures the Shadow DOM components inside `<openai-chatkit>` have visible height and opacity.

### 3. State Handshake:

- In `chat.py`, ensure the `user_item_event` (conversation.item.created) strictly uses `type: "text"` and NOT `type: "input_text"`.

## Response snapshot

**Fix 1 - Backend Magic String (backend/src/api/chat.py):**
- Changed `"object": "response"` back to `"object": "realtime.response"` in both `response.created` (line 97) and `response.done` (line 189) events
- This is the mandatory string ChatKit's internal state machine checks to trigger message list rendering
- Both events use the same `response_id` variable (generated once at line 61), ensuring consistency

**Fix 2 - ChatKit CSS (frontend/src/app/layout.tsx):**
- Added `<head>` section with ChatKit CSS stylesheet link
- `<link rel="stylesheet" href="https://cdn.platform.openai.com/deployments/chatkit/chatkit.css" />`
- This provides styles for the Shadow DOM components inside `<openai-chatkit>` web component
- Without this, the Shadow DOM elements have zero height/opacity and appear invisible

**Fix 3 - Content Type Verification:**
- Confirmed `conversation.item.created` already uses `"type": "text"` (line 83)
- No instances of `"input_text"` found in the file
- This was fixed in PHR-0063 (Atomic Response Initialization)

## Outcome

- ✅ Impact: Fixed two critical rendering blockers - SDK magic string for state machine and CSS for Shadow DOM visibility
- 🧪 Tests: Pending manual testing with authenticated session
- 📁 Files: Modified backend/src/api/chat.py (object field) and frontend/src/app/layout.tsx (CSS link)
- 🔁 Next prompts: Test with login + send message; verify message bubbles are visible and styled
- 🧠 Reflection: ChatKit uses Shadow DOM for rendering, which means it needs its own CSS loaded externally. Without the CSS, the web component elements exist in the DOM but have no visible dimensions. The "realtime.response" object string is an internal SDK requirement that triggers the state machine transition from "waiting" to "rendering" mode.

## Evaluation notes (flywheel)

- Failure modes observed: Missing CSS caused Shadow DOM elements to be invisible (zero height/opacity); wrong object string prevented SDK state machine from entering render mode
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If still blank, inspect browser DevTools for <openai-chatkit> Shadow DOM elements and check if they have computed styles with non-zero height
