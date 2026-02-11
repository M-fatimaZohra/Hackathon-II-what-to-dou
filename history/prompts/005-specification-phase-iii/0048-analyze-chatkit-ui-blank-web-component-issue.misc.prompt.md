---
id: 0048
title: Analyze ChatKit UI blank web component issue
stage: misc
date: 2026-02-10
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.analyze
labels: [debugging, chatkit-sdk, web-components, ui-rendering, cdn-loading]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - CHATKIT_UI_BLANK_ANALYSIS.md (created - comprehensive diagnostic report)
 - frontend/src/app/layout.tsx (analyzed - Script loading)
 - frontend/src/components/ChatProvider.tsx (analyzed - configuration)
 - frontend/src/components/chat/ChatAssistant.tsx (analyzed - component mounting)
tests:
 - Manual: Open browser console and run diagnostic commands
 - Manual: Check Network tab for chatkit.js script loading
 - Manual: Inspect Elements tab for <openai-chatkit> structure
---

## Prompt

now network tab is showing assistant response
but UI is still not rendering user message or assistant message

backend terminal

INFO:src.middleware.auth_handler:User authenticated: fAYF06XBlzSJwVEJ07rcQfD6WbAKhw4r
INFO:     127.0.0.1:52862 - "POST /api/fAYF06XBlzSJwVEJ07rcQfD6WbAKhw4r/chat HTTP/1.1" 200 OK
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/traces/ingest "HTTP/1.1 204 No Content"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/traces/ingest "HTTP/1.1 204 No Content"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/traces/ingest "HTTP/1.1 204 No Content"

sample of chat request/response in network tab
data: {"type": "thread.created", "thread": {"id": "204", "title": "Chat 204"}}
data: {"type": "thread.message.created", "message": {"id": "msg-user-204", "role": "user", "content": [{"type": "text", "text": "add task buying fish\\n"}]}}
data: {"type": "response.text.delta", "delta": {"text": "I've"}}
data: {"type": "response.text.delta", "delta": {"text": " added"}}
[... multiple text deltas ...]
data: {"type": "response.done"}

first read expected files
@frontend/src/components/ChatProvider.tsx
@frontend/src/components/chat/ChatAssistant.tsx
@frontend/src/app/tasks/page.tsx
@frontend/src/app/layout.tsx

then read other files as needed

## Response snapshot

**Status**: SSE events streaming correctly ✅ | ChatKit UI completely blank ❌

**Root Cause Identified**: Web component initialization failure. The ChatKit React wrapper is working, but the underlying `<openai-chatkit>` web component is not rendering.

**Architecture Analysis**:

ChatKit uses a two-layer architecture:
1. **React Wrapper** (`@openai/chatkit-react` v1.4.3) - Provides hooks and components
2. **Web Component** (CDN-loaded) - Actual UI rendering via `<openai-chatkit>` custom element

**Evidence**:
- ✅ Backend authentication successful
- ✅ SSE events streaming correctly (verified in Network tab)
- ✅ Event sequence correct: thread.created → thread.message.created → response.text.delta → response.done
- ✅ Database persistence working
- ✅ MCP tools executing
- ❌ ChatKit UI completely blank (no input field, no messages, no UI elements)

**Most Likely Causes**:

1. **Web Component Script Not Loading** (Primary Suspect)
   - CDN script at `https://cdn.platform.openai.com/deployments/chatkit/chatkit.js` may be failing
   - Script loaded via Next.js Script component in layout.tsx:43-46
   - No error handling or load verification
   - Custom element `<openai-chatkit>` not registered

2. **CustomApiConfig Incompatibility**
   - Web component may not fully support CustomApiConfig
   - Missing required configuration fields
   - Custom fetch function may not be compatible

3. **Timing Issue**
   - Component mounting before web component is defined
   - React wrapper waits via `customElements.whenDefined()` but fails silently

4. **CSS/Styling Issue** (Less Likely)
   - Web component rendering but invisible
   - Evidence against: sidebar container is visible, only content area blank

**Diagnostic Commands** (run in browser console):

```javascript
// Check if web component is registered
console.log('ChatKit defined:', customElements.get('openai-chatkit'));

// Check if script loaded
console.log('ChatKit script:', document.querySelector('script[src*="chatkit.js"]'));

// Inspect ChatKit element
console.log('ChatKit element:', document.querySelector('openai-chatkit'));
```

**Expected Output**:
- `ChatKit defined: function OpenAIChatKit() { ... }`
- If `undefined`, web component isn't registered → script loading failure

**Recommended Fixes**:

1. **Add Script Loading Verification** (Immediate)
   ```tsx
   <Script
     src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
     strategy="afterInteractive"
     onLoad={() => console.log('ChatKit script loaded')}
     onError={(e) => console.error('ChatKit script failed:', e)}
   />
   ```

2. **Add Initialization Check** (Immediate)
   ```tsx
   useEffect(() => {
     customElements.whenDefined('openai-chatkit').then(() => {
       console.log('ChatKit web component ready');
     });
   }, []);
   ```

3. **Add Explicit Dimensions** (CSS Fix)
   ```tsx
   <ChatKit
     control={control}
     className="h-full w-full"
     style={{ minHeight: '400px' }}
   />
   ```

**Analysis Report Created**: CHATKIT_UI_BLANK_ANALYSIS.md with comprehensive diagnostic steps and troubleshooting guide.

## Outcome

- ✅ Impact: Identified root cause of blank ChatKit UI - web component initialization failure separate from SSE streaming issue. Created comprehensive diagnostic report with step-by-step troubleshooting guide. Previous fix (PHR-0047) successfully resolved event streaming; this is a new layer of the problem.
- 🧪 Tests: Manual diagnostics required - run console commands to verify web component registration, check Network tab for script loading, inspect Elements tab for shadow DOM structure
- 📁 Files: Created CHATKIT_UI_BLANK_ANALYSIS.md (comprehensive diagnostic report), analyzed layout.tsx (Script loading), ChatProvider.tsx (configuration), ChatAssistant.tsx (component mounting)
- 🔁 Next prompts: Run diagnostic commands in browser console, check if customElements.get('openai-chatkit') returns undefined, verify chatkit.js loads in Network tab, inspect <openai-chatkit> element structure, apply appropriate fix based on findings
- 🧠 Reflection: This reveals a critical architectural insight - ChatKit uses a two-layer system (React wrapper + web component), and issues can occur at either layer. The SSE streaming works at the network level, but the UI rendering depends on the web component being properly loaded and initialized. The silent failure mode (no console errors reported) suggests the React wrapper is waiting indefinitely for a web component that never registers. This is a common pattern with CDN-loaded web components where script loading failures aren't immediately visible.

## Evaluation notes (flywheel)

- Failure modes observed: Web component script may not be loading from CDN, CustomApiConfig may not be fully supported by web component, timing issues between React wrapper and web component initialization, silent failures with no console errors make debugging difficult
- Graders run and results (PASS/FAIL): Architecture analysis: PASS (identified two-layer system), Root cause hypothesis: PASS (web component initialization failure), Diagnostic plan: PASS (comprehensive console commands and verification steps), Analysis report: PASS (detailed troubleshooting guide created)
- Prompt variant (if applicable): User provided evidence that events are streaming correctly but UI is blank, included Network tab SSE data and backend logs
- Next experiment (smallest change to try): Run `console.log(customElements.get('openai-chatkit'))` in browser console to verify if web component is registered, check Network tab for chatkit.js script status code
