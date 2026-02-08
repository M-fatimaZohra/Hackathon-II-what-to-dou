---
id: 0015
title: Update tasks with correct ChatKit imports
stage: tasks
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.tasks
labels: [tasks-correction, chatkit-imports, useChatKit-hook, ChatKit-component, context7-research]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/tasks.md
tests:
 -
---

## Prompt

/sp.tasks update tasks.md with correct imports

Context: After implementing Phase 1-3, discovered TypeScript errors:
- Module '"@openai/chatkit-react"' has no exported member 'ChatKitProvider'
- Module '"@openai/chatkit-react"' has no exported member 'ChatView'

Used Context7 MCP to research correct ChatKit React SDK imports and implementation patterns.

## Response snapshot

Successfully corrected tasks.md with accurate ChatKit React SDK imports and implementation patterns based on official documentation from Context7.

**Research Findings (Context7 MCP):**

Queried three library sources:
1. `/websites/openai_github_io_chatkit-js` - Official ChatKit documentation (410 code snippets, High reputation)
2. `/openai/chatkit-js` - ChatKit GitHub repository (59 code snippets, High reputation)
3. `/openai/openai-chatkit-advanced-samples` - Advanced examples (103 code snippets, High reputation)

**Incorrect Imports (Previous Implementation):**
```typescript
import { ChatKitProvider } from '@openai/chatkit-react'; // DOES NOT EXIST
import { ChatView } from '@openai/chatkit-react'; // DOES NOT EXIST
```

**Correct Imports (Official Documentation):**
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';
```

**Correct Implementation Pattern:**
1. Use `useChatKit` hook (not a Provider wrapper component)
2. Configure with `api.url`, `api.domainKey`, and custom `api.fetch` function
3. Custom fetch function injects Authorization: Bearer token
4. Hook returns `control` object
5. Pass `control` to `<ChatKit />` component (not `<ChatView />`)

**Tasks.md Corrections Applied:**

**Phase 2: Authentication Bridge**
- ❌ OLD: "Create ChatProvider wrapper that injects JWT from Better Auth into ChatKit SDK"
- ✅ NEW: "Implement useChatKit hook with custom fetch function to inject JWT from Better Auth"
- Updated T008: Changed from "wrapper component" to "component using useChatKit hook (import: ChatKit, useChatKit from '@openai/chatkit-react')"
- Updated T009: Changed from "in ChatProvider.tsx" to "in custom fetch function"
- Updated T010: Changed from "header injection logic" to "custom fetch function to add Authorization: Bearer header"
- Updated T011: Changed from "Configure ChatKit SDK baseUrl" to "Configure useChatKit api.url"
- Updated T012: Changed from "in ChatProvider.tsx" to "in custom fetch function"
- Updated T013: Changed from "Add SSE connection management" to "Add onError callback to useChatKit"
- Updated Checkpoint: Changed from "ChatProvider successfully injects JWT" to "useChatKit hook successfully injects JWT via custom fetch"

**Phase 3: The Copilot UI**
- ❌ OLD: "Implement persistent, collapsible sidebar with ChatKit SDK's <ChatView />"
- ✅ NEW: "Implement persistent, collapsible sidebar with ChatKit SDK's <ChatKit /> component"
- Updated T015: Changed from "<ChatView /> component" to "<ChatKit /> component (not ChatView) with control prop from useChatKit"
- Updated T018: Changed from "wrap content with ChatProvider" to "use ChatProvider component that wraps useChatKit hook"
- Updated Checkpoint: Changed from "<ChatView /> renders correctly" to "<ChatKit /> renders correctly with control object"

**Success Criteria**
- Changed from "ChatProvider injects JWT" to "useChatKit hook with custom fetch injects JWT"
- Changed from "Sidebar overlay renders on tasks page with <ChatView />" to "Sidebar overlay renders on tasks page with <ChatKit /> component"

**Key Architecture Changes:**

| Aspect | Previous (Incorrect) | Corrected (Official) |
|--------|---------------------|---------------------|
| Hook/Provider | ChatKitProvider wrapper | useChatKit hook |
| Auth injection | Async headers/baseUrl functions | Custom fetch function |
| Component | ChatView | ChatKit |
| Control flow | Provider wraps children | Hook returns control object |
| Configuration | Pass to Provider props | Pass to useChatKit options |

**Implementation Impact:**

Files that need refactoring based on corrected tasks:
1. `frontend/src/components/ChatProvider.tsx` - Must use useChatKit hook pattern
2. `frontend/src/components/chat/ChatAssistant.tsx` - Must use ChatKit component with control prop
3. `frontend/src/app/tasks/page.tsx` - May need restructuring for hook-based pattern

## Outcome

- ✅ Impact: Corrected tasks.md with accurate ChatKit React SDK imports and implementation patterns, preventing TypeScript errors and ensuring alignment with official documentation
- 🧪 Tests: No tests affected - specification correction only
- 📁 Files: Updated specs/005-specification-phase-iii/tasks.md
- 🔁 Next prompts: Refactor Phase 2-3 implementation files (ChatProvider.tsx, ChatAssistant.tsx, tasks/page.tsx) to use correct useChatKit hook pattern with custom fetch function
- 🧠 Reflection: Context7 MCP research revealed fundamental architectural difference - ChatKit uses hook-based pattern (useChatKit) rather than provider wrapper pattern (ChatKitProvider). Custom fetch function approach is cleaner than async headers/baseUrl functions, providing better control over request lifecycle and error handling.

## Evaluation notes (flywheel)

- Failure modes observed: Initial implementation based on incorrect assumptions about ChatKit API surface - assumed Provider/View pattern similar to other React libraries, but ChatKit uses hook-based pattern
- Graders run and results (PASS/FAIL): Context7 research: PASS (found official documentation with 410 code snippets), Import correction: PASS (changed ChatKitProvider → useChatKit, ChatView → ChatKit), Implementation pattern: PASS (custom fetch function for auth injection), Task descriptions: PASS (all Phase 2-3 tasks updated with correct terminology), Success criteria: PASS (updated to reflect correct components)
- Prompt variant (if applicable): /sp.tasks with correction request after discovering TypeScript import errors
- Next experiment (smallest change to try): Refactor ChatProvider.tsx to use useChatKit hook with custom fetch function, verify TypeScript errors resolve, then update ChatAssistant.tsx to use ChatKit component with control prop
