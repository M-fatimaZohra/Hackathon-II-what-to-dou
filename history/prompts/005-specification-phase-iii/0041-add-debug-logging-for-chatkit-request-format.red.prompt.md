---
id: 0041
title: Add debug logging for ChatKit request format
stage: red
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: [debugging, chatkit-integration, request-format, diagnostic, empty-messages]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/components/ChatProvider.tsx (updated)
tests:
 - none (diagnostic logging only)
---

## Prompt

Add this log at line 99 in ChatProvider.tsx:
console.log('[ChatProvider] RAW REQUEST:', JSON.stringify(originalBody, null, 2));

This will show us the exact field names ChatKit uses, so we can fix the extraction logic.

## Response snapshot

**Context**: After fixing conversation_id logic (PHR-0040), discovered that messages are being sent as empty strings to the backend. Database shows empty user messages, and frontend console shows `{message: ''}`.

**Problem Identified**:
- Frontend transformation extracts empty message: `{message: ''}`
- Backend receives and saves empty message to database
- OpenAI receives empty message, returns generic "Hello! How can I assist..." response
- Root cause: Transformation logic doesn't match ChatKit SDK's actual request format

**Current Extraction Logic** (lines 104-114):
```typescript
if (originalBody.messages && Array.isArray(originalBody.messages)) {
  const lastMessage = originalBody.messages[originalBody.messages.length - 1];
  message = lastMessage?.content || "";
} else if (originalBody.message) {
  message = originalBody.message;
} else if (originalBody.input) {
  message = originalBody.input;
}
```

**Assumptions Being Made**:
- ChatKit sends `{messages: [{content: "..."}]}`
- Or `{message: "..."}`
- Or `{input: "..."}`

**But we don't know what ChatKit actually sends!**

**Solution**: Add debug logging to see the raw request structure before transformation.

**Change Made**:

### frontend/src/components/ChatProvider.tsx (line 99-102)

**Before**:
```typescript
if (init?.body) {
  try {
    const originalBody = JSON.parse(init.body as string);

    // Extract message from various possible formats
    let message = "";
```

**After**:
```typescript
if (init?.body) {
  try {
    const originalBody = JSON.parse(init.body as string);

    // 🔍 DEBUG: Log the actual structure ChatKit sends
    console.log('[ChatProvider] RAW REQUEST:', JSON.stringify(originalBody, null, 2));

    // Extract message from various possible formats
    let message = "";
```

**What This Will Reveal**:
- Exact field names ChatKit SDK uses
- Structure of the request body (nested objects, arrays, etc.)
- Whether the message content is present at all
- Any additional metadata ChatKit sends

## Outcome

- ✅ Impact: Added diagnostic logging to reveal ChatKit SDK's actual request format. This debug log will show the raw request body structure before transformation, helping us identify why message extraction is failing and returning empty strings. Critical for fixing the empty message bug where database shows blank user messages.
- 🧪 Tests: No automated tests. Manual testing: restart frontend dev server, open chat UI, send a test message, check browser console for "[ChatProvider] RAW REQUEST:" log output, analyze the JSON structure to identify correct field names
- 📁 Files: Updated frontend/src/components/ChatProvider.tsx (added debug logging at line 101-102 in custom fetch function)
- 🔁 Next prompts: Restart frontend, Send test message in chat, Check browser console for RAW REQUEST log, Analyze the actual request structure, Update extraction logic to match ChatKit's format, Remove debug logging after fix is confirmed
- 🧠 Reflection: This is a classic debugging approach - when assumptions fail, add logging to see reality. We assumed ChatKit sends messages in certain formats, but the empty message bug proves our assumptions are wrong. The debug log will reveal the truth. Once we see the actual structure, we can fix the extraction logic in one targeted change. This is a "red" stage task because we're diagnosing the problem, not implementing the solution yet.

## Evaluation notes (flywheel)

- Failure modes observed: Initial assumption that ChatKit uses standard formats (rejected - empty messages prove otherwise), Considered checking ChatKit documentation (attempted but format unclear), Realized empirical observation is fastest path to truth
- Graders run and results (PASS/FAIL): Debug logging added: PASS (console.log with JSON.stringify), Placement: PASS (before extraction logic), Format: PASS (pretty-printed JSON for readability), Non-invasive: PASS (doesn't affect functionality)
- Prompt variant (if applicable): User requested specific debug logging after identifying empty message issue in database and console
- Next experiment (smallest change to try): Restart frontend, send single test message "hello", check console output, identify the actual field name ChatKit uses for message content, update extraction logic accordingly


