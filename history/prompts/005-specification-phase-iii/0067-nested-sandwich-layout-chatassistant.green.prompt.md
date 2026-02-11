---
id: 0067
title: nested-sandwich-layout-chatassistant
stage: green
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["chatkit", "nested-sandwich", "fallback-ui", "layout", "flex"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/chat/ChatAssistant.tsx
tests:
  - Manual: login, send message, verify fallback message bubbles appear above ChatKit input bar
  - Verify ChatKit input bar remains visible and usable at bottom (h-40 when messages exist)
  - Verify fallback messages are scrollable with pointer-events-auto
  - Verify warm background color (rgba(255,251,237,0.5)) distinguishes fallback from SDK area
  - Verify ChatKit takes full height when no fallback messages exist (initial state)
---

## Prompt

Restructure ChatAssistant.tsx to create a 'Nested Sandwich' layout where fallback messages are visible alongside the OpenAI UI components.

1. Remove the 'absolute inset-0' and 'bg-white' from the fallback message container.
2. Change the parent container to 'flex flex-col h-full overflow-hidden'.
3. Wrap the <ChatKit /> component in a div with a conditional height. If `messages.length > 0`, set this div to a fixed height (e.g., 'h-32' or 'h-40') to focus solely on the OpenAI input bar.
4. Place the fallback message <div> in the middle of the stack with 'flex-1 overflow-y-auto'.
5. Ensure the fallback messages have a slight background color (like '#FFFBED/50') to distinguish them from the SDK background.
6. Add 'pointer-events-auto' to the fallback area to ensure scrolling works, while keeping the rest of the UI interactive.

## Response snapshot

**ChatAssistant.tsx Changes (lines 93-129):**

1. Parent container: Changed from `h-[calc(100%-64px)] overflow-hidden relative` to `h-[calc(100%-64px)] flex flex-col overflow-hidden`
2. Fallback messages: Removed `absolute inset-0 bg-white`, now uses `flex-1 overflow-y-auto p-4 space-y-4 pointer-events-auto` with `backgroundColor: rgba(255, 251, 237, 0.5)` inline style
3. Fallback messages placed ABOVE ChatKit in DOM order (top of flex column)
4. ChatKit wrapper: Added conditional class `flex-shrink-0 ${messages.length > 0 ? 'h-40' : 'flex-1'}` — shrinks to input bar height when fallback messages exist, takes full height otherwise
5. Message bubbles unchanged: user (blue, right-aligned) and assistant (gray, left-aligned)

**Layout Flow:**
```
┌─────────────────────────┐
│ Header (64px fixed)     │
├─────────────────────────┤
│ Fallback Messages       │ ← flex-1, overflow-y-auto, #FFFBED/50 bg
│ (scrollable bubbles)    │
├─────────────────────────┤
│ ChatKit SDK (h-40)      │ ← flex-shrink-0, contains input bar
└─────────────────────────┘
```

When no messages exist, ChatKit takes full remaining height (`flex-1`) and no fallback area renders.

## Outcome

- ✅ Impact: Fallback messages now coexist with ChatKit input bar instead of covering it entirely. Users can see their conversation AND use the ChatKit input to send follow-up messages.
- 🧪 Tests: Pending manual testing - verify message bubbles appear above ChatKit input bar
- 📁 Files: Modified ChatAssistant.tsx (layout restructure from absolute overlay to flex column sandwich)
- 🔁 Next prompts: Test with login + send message; if input bar works for multi-turn, the fallback approach is viable long-term
- 🧠 Reflection: The absolute overlay approach (PHR-0066) made messages visible but completely covered ChatKit, including its input component. The Nested Sandwich layout preserves ChatKit's input bar at the bottom while showing our own message bubbles above it, enabling multi-turn conversation through the ChatKit input even when its rendering engine fails to display messages.

## Evaluation notes (flywheel)

- Failure modes observed: Previous absolute overlay (PHR-0066) covered ChatKit's input bar, preventing follow-up messages
- Graders run and results (PASS/FAIL): Pending manual testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): If ChatKit input bar is not visible in h-40, try increasing to h-48 or h-52. If input still doesn't send messages properly, may need to add a custom input field in the fallback area.
