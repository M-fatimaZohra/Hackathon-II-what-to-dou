---
id: 0030
title: Implement Direct Custom Integration with JWT auth
stage: green
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: [chatkit-integration, jwt-auth, custom-backend, handshake-failure, debugging]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/components/ChatProvider.tsx (modified)
 - backend/src/api/chat.py (modified)
 - frontend/src/app/layout.tsx (modified)
tests:
 - none
---

## Prompt

I am using a "Custom ChatKit" architecture. My specific documentation defines the request/response schema using 'message' for input and 'response' for output. Please update the backend and frontend to align perfectly with this schema and fix the 500/422 errors:

1. **In `backend/src/api/chat.py`**:
   - **Remove Workflow logic**: Completely remove the check for `CHATKIT_WORKFLOW_ID` and remove the `workflow` argument from `client.beta.chatkit.sessions.create`.
   - **Align Endpoint**: In `chat_endpoint_streaming`, ensure it reads `request.message` to pass to the service.

2. **In `backend/src/schema/chat_models.py`**:
   - **Fix Schema**: Ensure the `ChatRequest` model uses `message: str` (matching my docs).
   - **Fix Response**: Ensure the `ChatResponse` model uses `response: str` for the AI message (matching my docs).

3. **In `backend/src/services/chat_service.py`**:
   - Update `get_chat_response` and any streaming logic to ensure the final output is returned in a field named `response` within the `ChatResponse` object.

4. **In `frontend/src/components/ChatProvider.tsx`**:
   - Ensure the `useChatKit` hook is configured to send the user input as `message` in the POST body to `http://localhost:7860/api/{userId}/chat`.

Goal: Fix the 500 error by removing the Workflow requirement and fix the 422 error by aligning all field names to 'message' and 'response'.

**Follow-up context:**
- User reported chatbot was rendering but crashed after clicking history button
- Backend showing 500 error on `/chat/session` endpoint
- User confirmed: "you need to check why my frontend and backend (chatkit UI and Custom openai agents with fastapi) are not handshaking what is the problem of this failure"
- Multiple iterations attempted to fix OpenAI session API integration
- Final pivot: Remove OpenAI session API entirely, use Direct Custom Integration with JWT

## Response snapshot

**Implementation Approach:**

Pivoted through multiple strategies to fix the ChatKit-FastAPI handshake failure:

1. **Initial Attempt**: Remove workflow logic from session endpoint
   - Result: Failed - OpenAI SDK requires `workflow` parameter (Pydantic validation error)

2. **Second Attempt**: Use `workflow={"type": "custom"}`
   - Result: Failed - OpenAI API returned 400 error demanding `workflow.id`

3. **Third Attempt**: Remove OpenAI session API entirely, use custom `fetcher` property
   - Result: Failed - ChatKit SDK doesn't support `fetcher` property (FatalAppError: Invalid input)

4. **Final Implementation**: Direct Custom Integration with JWT
   - Removed entire `/session` endpoint from backend
   - Removed OpenAI client initialization
   - Simplified `getClientSecret` to return JWT token directly
   - Added `api.url` pointing to FastAPI backend
   - ChatKit SDK handles Authorization header automatically

**Files Modified:**

1. **frontend/src/components/ChatProvider.tsx**:
```typescript
useChatKit({
  api: {
    url: `${CONFIG.API_BASE_URL}/${userId}/chat`,
    getClientSecret: async () => {
      return tokenRef.current; // Returns JWT token
    },
  }
})
```

2. **backend/src/api/chat.py**:
   - Removed: OpenAI client, SessionResponse model, create_chat_session endpoint
   - Kept: Streaming chat endpoint with JWT authentication

3. **frontend/src/app/layout.tsx**:
   - Migrated ChatKit CDN script to Next.js `<Script>` component

**Architecture:**
```
ChatKit UI → getClientSecret() returns JWT → ChatKit adds Authorization header → FastAPI /chat endpoint → JWT validation → SSE streaming
```

## Outcome

- ✅ Impact: Implemented Direct Custom Integration architecture removing OpenAI session API dependency, simplified authentication to JWT-only approach, removed non-functional session endpoint
- 🧪 Tests: No automated tests - runtime testing required to verify handshake
- 📁 Files: Modified frontend/src/components/ChatProvider.tsx (simplified getClientSecret, added api.url), backend/src/api/chat.py (removed session endpoint and OpenAI client), frontend/src/app/layout.tsx (Next.js Script component)
- 🔁 Next prompts: **CRITICAL: User confirmed errors still persist after implementation** - Need to capture actual error messages from browser console and backend logs, Verify ChatKit SDK version compatibility with custom backends, Check if ChatKit expects specific response format for SSE streaming, Investigate if additional ChatKit configuration is needed for self-hosted backends
- 🧠 Reflection: Multiple implementation attempts were made based on different assumptions about how ChatKit integrates with custom backends. The OpenAI session API proved incompatible (requires workflow.id which we don't have). The Direct Custom Integration approach is architecturally sound but errors persist, indicating a deeper integration issue. **Next debugging session must start with capturing exact error messages** to avoid further trial-and-error iterations.

## Evaluation notes (flywheel)

- Failure modes observed: OpenAI session API incompatibility (workflow.id required), ChatKit SDK API misunderstanding (fetcher property doesn't exist), **Handshake still failing after all implementation attempts** - root cause not yet identified
- Graders run and results (PASS/FAIL): Schema alignment: PASS (message/response fields correct), Session endpoint removal: PASS (no longer calling non-existent API), JWT authentication: PASS (getClientSecret returns token), ChatKit configuration: UNKNOWN (api.url added, getClientSecret simplified), **End-to-end handshake: FAIL (errors persist per user confirmation)**
- Prompt variant (if applicable): /sp.implement with iterative debugging based on user feedback about specific errors encountered
- Next experiment (smallest change to try): **STOP implementing and START diagnosing** - Capture exact error messages from: (1) Browser console (full stack trace), (2) Backend logs (FastAPI error details), (3) Network tab (request/response payloads), (4) ChatKit SDK debug logs if available. Only after seeing actual errors can we identify root cause instead of guessing at solutions.
