---
id: 0069
title: immediate-user-msg-chatkit-overlay-layout
stage: green
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "immediate-message", "overlay-layout", "view-toggle", "history"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/ChatProvider.tsx
  - frontend/src/components/chat/ChatAssistant.tsx
tests:
  - Manual: Send message, verify user bubble appears IMMEDIATELY (before assistant responds)
  - Manual: Verify assistant message appears only after response.done event
  - Manual: Verify ChatKit header with new-chat and history icons visible at top
  - Manual: Verify ChatKit input bar visible at bottom
  - Manual: Click History tab, verify custom messages hide and ChatKit native view shows
  - Manual: Click Chat tab, verify custom messages reappear
  - Manual: Verify auto-scroll to latest message on new message arrival
---

## Prompt

can you immediately make user message appear on custom message UI and then add assistant message after assistant message generate
make sure to match Chatkit UI as much as possible like shown in image
also, is there a way to make history and new chat icons of chatkit stay on top while custom UI still appear in frontend of Chatkit Message UI as alternative if Chatkit UI failed to display messages

## Response snapshot

**Three features implemented across 2 files:**

### 1. Immediate User Message (ChatProvider.tsx:169-173)
- `setMessages(prev => [...prev, { role: 'user', content: message }])` called BEFORE the fetch request
- User bubble appears instantly when pressing send
- `response.done` handler now only appends the assistant message (line 234-237)

### 2. ChatKit Header Visibility + View Toggle (ChatAssistant.tsx)
Layout architecture:
- ChatKit renders full-height as background layer (lines 103-108)
- Toggle strip at `top: 52px` (below ChatKit header) with Chat/History tabs (lines 111-138)
- Custom messages overlay at `top: 88px, bottom: 118px` (lines 142-167)
- ChatKit header (new chat + history icons) stays visible at top (0-52px)
- ChatKit input bar stays visible at bottom (last 118px)

View mode toggle:
- `viewMode` state: 'chat' | 'history'
- Chat tab (💬): Shows custom messages overlay (default)
- History tab (🕐): Hides overlay, reveals ChatKit's native UI (including its history panel)

### 3. UI Details
- Auto-scroll via `messagesEndRef` with smooth scrolling
- Lucide icons: `MessageCircle` for Chat tab, `Clock` for History tab
- Active tab: `text-[#0D0D0D] border-b-2 border-[#0D0D0D]`
- Inactive tab: `text-gray-400 hover:text-gray-600`

**Visual Layout:**
```
┌──────────────────────────────┐
│ AI Assistant              [X] │ ← Our sidebar header
├──────────────────────────────┤
│ CK Header: title    📝 🕐    │ ← ChatKit header (52px, visible)
├──[💬 Chat]──[🕐 History]────┤ ← Toggle strip (36px, z-20)
│                              │
│ CHAT MODE:                   │
│  Custom message bubbles      │ ← z-10 overlay, bg-white
│  [user →]                    │
│  [← assistant]               │
│                              │
│ HISTORY MODE:                │
│  ChatKit native view         │ ← Overlay hidden, CK visible
│                              │
├──────────────────────────────┤
│ CK Input: Ask a question...  │ ← ChatKit input (118px, visible)
└──────────────────────────────┘
```

## Outcome

- ✅ Impact: User messages appear instantly for responsive UX; ChatKit header icons remain accessible; view toggle lets user switch between custom messages and ChatKit native view (including history)
- 🧪 Tests: Pending manual testing
- 📁 Files: ChatProvider.tsx (immediate user message), ChatAssistant.tsx (overlay layout + view toggle + auto-scroll)
- 🔁 Next prompts: Test end-to-end flow; adjust pixel offsets if needed; verify history panel renders in ChatKit native view
- 🧠 Reflection: The overlay approach keeps ChatKit rendering normally while covering only its blank message area. The view toggle gives users explicit control over switching between custom fallback and ChatKit native view, avoiding fragile Shadow DOM event interception.

## Evaluation notes (flywheel)

- Failure modes observed: Cannot intercept Shadow DOM clicks in ChatKit header; solved with separate toggle strip
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If offset values (52px, 88px, 118px) don't match ChatKit's actual header/input sizes, measure with DevTools and adjust
