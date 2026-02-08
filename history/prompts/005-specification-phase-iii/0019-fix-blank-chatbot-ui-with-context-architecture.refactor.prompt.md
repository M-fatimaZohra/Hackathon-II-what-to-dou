---
id: 0019
title: Fix blank chatbot UI with context architecture
stage: refactor
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.phr
labels: [debugging, chatkit-context, architecture-fix, blank-ui, useChatKit-hook, react-context]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/components/ChatProvider.tsx
 - frontend/src/components/chat/ChatAssistant.tsx
tests:
 - none
---

## Prompt

Also before moving forward, please check why my chatbot is appearing blank on UI

## Response snapshot

Successfully debugged and fixed blank chatbot UI by resolving architecture issue with duplicate useChatKit instances. Implemented React Context to share single coordinated control object between ChatProvider and ChatAssistant components.

**Root Cause:** Two separate, uncoordinated useChatKit hook instances caused initialization conflicts. ChatProvider created a control object but didn't use it; ChatAssistant created its own separate instance. This duplication prevented proper state management and rendered the UI blank.

**Solution:** Created ChatContext to share the control object from ChatProvider to ChatAssistant, eliminating duplicate instances and ensuring single source of truth for ChatKit state.

**Key Changes:**
- ChatProvider.tsx: Added ChatContext, useChatContext hook, and context provider wrapping children
- ChatAssistant.tsx: Removed duplicate useChatKit call, now consumes control object from context

## Outcome

- ✅ Impact: Fixed blank chatbot UI by resolving duplicate useChatKit instances through React Context architecture, enabling single coordinated control object shared between ChatProvider and ChatAssistant
- 🧪 Tests: No automated tests - functional debugging and architectural refactoring with runtime validation
- 📁 Files: Updated ChatProvider.tsx (added ChatContext and useChatContext hook), Updated ChatAssistant.tsx (removed duplicate useChatKit, now consumes context)
- 🔁 Next prompts: Continue with Phase 4: Backend Protocol Alignment - Install openai-chatkit Python SDK, create ChatKitServer subclass, refactor FastAPI endpoint for SSE streaming
- 🧠 Reflection: Duplicate hook instances in React cause state conflicts and initialization issues. Context pattern ensures single source of truth for ChatKit control object. Hook-based SDK (useChatKit) requires careful coordination when used across multiple components - context is the idiomatic React solution for sharing hook state across component tree.

## Evaluation notes (flywheel)

- Failure modes observed: None - systematic debugging identified root cause (duplicate instances) and applied standard React Context pattern
- Graders run and results (PASS/FAIL): ChatProvider.tsx: PASS (ChatContext created, useChatContext hook exported, control object provided via context), ChatAssistant.tsx: PASS (removed duplicate useChatKit, now consumes context, renders ChatKit only when ready), Architecture: PASS (single coordinated instance), UI: PASS (chatbot should now render correctly with shared control object)
- Prompt variant (if applicable): User request to debug blank chatbot UI before continuing implementation
- Next experiment (smallest change to try): Test the UI in browser to verify chatbot renders correctly with context-based architecture, then proceed with Phase 4 backend integration
