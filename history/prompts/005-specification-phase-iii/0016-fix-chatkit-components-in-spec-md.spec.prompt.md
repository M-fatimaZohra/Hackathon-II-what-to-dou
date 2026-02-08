---
id: 0016
title: Fix ChatKit components in spec.md
stage: spec
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.specify
labels: [spec-correction, chatkit-components, useChatKit-hook, ChatKit-component]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/spec.md
tests:
 -
---

## Prompt

/sp.specify fix chatkit related errors in spec.md only

Context: After discovering TypeScript import errors and researching correct ChatKit patterns via Context7 MCP, need to update spec.md to reflect accurate component names and implementation approach.

## Response snapshot

Successfully corrected all ChatKit component references in spec.md to align with official @openai/chatkit-react SDK documentation.

**Corrections Applied:**

**1. FR-002 (Line 78):**
- ❌ OLD: `Frontend MUST implement a single <ChatAssistant /> wrapper component that uses @openai/chatkit-react SDK's <ChatView /> component`
- ✅ NEW: `Frontend MUST implement a single <ChatAssistant /> wrapper component that uses @openai/chatkit-react SDK's <ChatKit /> component with control object from useChatKit hook`

**2. Key Entities - ChatAssistant (Line 96):**
- ❌ OLD: `Frontend wrapper component that integrates @openai/chatkit-react SDK's <ChatView /> component for the sidebar overlay`
- ✅ NEW: `Frontend wrapper component that integrates @openai/chatkit-react SDK's <ChatKit /> component for the sidebar overlay, receiving control object from useChatKit hook`

**3. Key Entities - ChatKitProvider → ChatProvider (Line 97):**
- ❌ OLD: `ChatKitProvider: Frontend context provider managing ChatKit client and authentication with JWT token and baseUrl scoped to /api/{user_id}/chat`
- ✅ NEW: `ChatProvider: Frontend component that uses useChatKit hook to configure ChatKit client with custom fetch function for JWT authentication and baseUrl scoped to /api/{user_id}/chat`

**Key Changes:**
- Component name: `<ChatView />` → `<ChatKit />`
- Provider pattern: `ChatKitProvider` wrapper → `ChatProvider` using `useChatKit` hook
- Architecture: Context provider pattern → Hook-based pattern with control object
- Authentication: Async headers/baseUrl functions → Custom fetch function

**Verification:**
- ✅ Ran grep to confirm no remaining `ChatKitProvider` or `ChatView` references in spec.md
- ✅ All three occurrences corrected
- ✅ Terminology now consistent with official ChatKit documentation

## Outcome

- ✅ Impact: Corrected spec.md to reflect accurate ChatKit React SDK component names and implementation patterns, ensuring specification aligns with official documentation and prevents implementation errors
- 🧪 Tests: No tests affected - specification correction only
- 📁 Files: Updated specs/005-specification-phase-iii/spec.md (3 corrections)
- 🔁 Next prompts: Update remaining specification files (plan.md, research.md, quickstart.md, data-model.md) and UI specs (components.md, pages.md) with correct ChatKit patterns
- 🧠 Reflection: Specification documents must accurately reflect library APIs to prevent implementation errors. Correcting spec.md first ensures the authoritative requirements document is accurate before propagating changes to other specification files.

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward find-and-replace corrections based on Context7 research findings
- Graders run and results (PASS/FAIL): FR-002 correction: PASS (ChatView → ChatKit with control object), ChatAssistant entity: PASS (updated to mention control object from useChatKit), ChatProvider entity: PASS (renamed from ChatKitProvider, updated to describe useChatKit hook pattern), Verification: PASS (grep confirms no remaining incorrect references)
- Prompt variant (if applicable): /sp.specify with targeted correction request for spec.md only
- Next experiment (smallest change to try): Update plan.md with same corrections (ChatView → ChatKit, ChatKitProvider → ChatProvider with useChatKit hook), then propagate to remaining specification files
