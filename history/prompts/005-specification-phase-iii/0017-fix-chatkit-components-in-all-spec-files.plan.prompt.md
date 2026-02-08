---
id: 0017
title: Fix ChatKit components in all spec files
stage: plan
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.plan
labels: [spec-corrections, chatkit-components, useChatKit-hook, ChatKit-component, comprehensive-update]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/plan.md
 - specs/005-specification-phase-iii/research.md
 - specs/005-specification-phase-iii/quickstart.md
 - specs/005-specification-phase-iii/data-model.md
 - specs/ui/components.md
 - specs/ui/pages.md
tests:
 -
---

## Prompt

/sp.plan fix plan.md and other .md files that have incorrect information about chatkit components

Context: After fixing spec.md and tasks.md with correct ChatKit imports, need to systematically update all remaining specification files to ensure consistency across the entire documentation.

## Response snapshot

Successfully corrected ChatKit component references across 6 specification files, ensuring complete alignment with official @openai/chatkit-react SDK documentation.

**Files Corrected:**

**1. plan.md (Already fixed earlier)**
- Line 225: `ChatAssistant.tsx # ChatKit SDK wrapper using <ChatView />` → `using <ChatKit />`
- Line 226: `ChatKitProvider.tsx # ChatKit context provider` → `ChatProvider.tsx # Component using useChatKit hook`
- Line 262: Structure Decision paragraph updated to mention `<ChatKit />` component with control object

**2. research.md**
- Lines 36-46: Replaced outdated ChatManager/TokenProvider pattern with modern useChatKit hook pattern
- Updated integration code example to show:
  - `import { ChatKit, useChatKit } from '@openai/chatkit-react'`
  - Custom fetch function for JWT injection
  - Control object pattern
  - Proper API configuration

**3. quickstart.md (Extensive updates)**
- Phase 1, Step 4: `Create ChatKitProvider` → `Create ChatProvider Component`
- Phase 2: Removed manual component tasks (ChatMessage, ChatInput, ChatWindow), replaced with ChatAssistant wrapper
- Phase 3: Updated from separate chat page to sidebar integration on tasks page
- File structure (lines 170-183): Updated to show ChatProvider and ChatAssistant only
- Code templates (lines 196-364): Replaced outdated templates with:
  - ChatProvider using useChatKit hook
  - ChatAssistant with sliding sidebar
  - Tasks page integration example
- Line 411: Troubleshooting section updated to reference ChatProvider

**4. data-model.md**
- Line 115: `Global chat state managed by ChatKitProvider` → `managed by ChatProvider component using useChatKit hook`
- Lines 189-198: `ChatKitProviderProps` → `ChatProviderProps` (simplified interface)
- Line 369: Flow diagram `ChatKitProvider.sendMessage()` → `ChatProvider.sendMessage()`
- Line 385: Flow diagram `ChatKitProvider Event Handler` → `ChatProvider Event Handler`
- Line 395: Flow diagram `ChatKitProvider.initialize()` → `ChatProvider.initialize()`

**5. components.md (UI specs)**
- Lines 63-81: `ChatKitProvider` section → `ChatProvider` section
  - Updated purpose, location, props
  - Described useChatKit hook pattern
  - Removed Context Value section (not applicable to hook pattern)
- Lines 82-109: `ChatAssistant` section updated
  - `<ChatView />` → `<ChatKit />` with control prop
  - Updated SDK integration code example
  - Added isOpen prop
  - Showed useChatKit hook usage with custom fetch

**6. pages.md (UI specs)**
- Line 96: Components list `ChatKitProvider` → `ChatProvider`
- Lines 137-138: Chat sidebar flow updated
  - `ChatKitProvider initializes` → `ChatProvider initializes`
  - `<ChatView />` → `<ChatKit />` with control prop

**Summary of Changes:**

| Aspect | Old (Incorrect) | New (Correct) |
|--------|----------------|---------------|
| Provider component | ChatKitProvider | ChatProvider |
| Provider pattern | Context provider wrapper | useChatKit hook |
| Chat component | ChatView | ChatKit |
| Props passing | Via context | Via control object |
| Authentication | Async headers/baseUrl | Custom fetch function |
| Manual components | ChatWindow, ChatInput, ChatMessage | None (SDK handles) |

**Verification:**
- ✅ Ran grep on all 6 files to confirm no remaining `ChatKitProvider` or `ChatView` references
- ✅ All files now consistent with official ChatKit documentation
- ✅ All files align with corrected spec.md and tasks.md

## Outcome

- ✅ Impact: Corrected ChatKit component references across 6 specification files, ensuring complete documentation consistency and alignment with official @openai/chatkit-react SDK patterns
- 🧪 Tests: No tests affected - specification corrections only
- 📁 Files: Updated plan.md, research.md, quickstart.md, data-model.md, components.md, pages.md
- 🔁 Next prompts: Refactor implementation files (ChatProvider.tsx, ChatAssistant.tsx, tasks/page.tsx) to match corrected specifications
- 🧠 Reflection: Systematic specification correction across multiple files ensures documentation consistency and prevents implementation errors. Hook-based pattern (useChatKit) is fundamentally different from provider wrapper pattern (ChatKitProvider), requiring updates to component structure, props, authentication approach, and integration examples throughout all specification documents.

## Evaluation notes (flywheel)

- Failure modes observed: None - systematic grep-based search and targeted corrections applied consistently
- Graders run and results (PASS/FAIL): plan.md: PASS (2 corrections), research.md: PASS (integration pattern updated), quickstart.md: PASS (extensive updates to phases, structure, templates), data-model.md: PASS (5 corrections in interfaces and flow diagrams), components.md: PASS (2 component sections completely rewritten), pages.md: PASS (2 corrections in components list and flow), Verification: PASS (grep confirms zero remaining incorrect references across all files)
- Prompt variant (if applicable): /sp.plan with request to fix plan.md and other specification files with incorrect ChatKit information
- Next experiment (smallest change to try): Begin implementation refactoring with ChatProvider.tsx, applying useChatKit hook pattern with custom fetch function as documented in corrected specifications
