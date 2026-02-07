---
id: 0043
title: Finalize AI Native Todo API Implementation
stage: refactor
date: 2026-02-05
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: unknown
command: /sp.implement
labels: [ai, mcp, agents, chatbot, integration, testing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/api/chat.py
  - backend/src/main.py
  - backend/tests/test_chat_endpoint.py
  - backend/src/services/chat_service.py
tests:
  - test_chat_endpoint.py
---

## Prompt

# Role: Python Backend & FastAPI Expert
# Task: Finalize AI-Native Todo API Implementation

Please execute the following four steps to connect our verified MCP logic to the FastAPI gateway.


### 1. Create `src/api/chat.py`
Create the endpoint `POST /api/{user_id}/chat`.
- Input: `user_id` (from path), `ChatRequest` (from body).
- Implementation: Call `get_chat_response` from `src.services.chat_service`.
- Constraint: Ensure it passes the `user_id` from the URL path directly to the service layer.


### 2. Update `src/main.py`
- Import the new `chat` module from `api`.
- Register the chat router using `app.include_router(chat.router, prefix="/api", tags=["chat"])`.
- Ensure this is added alongside the existing `tasks.router`.


### 3. Create `tests/test_chat_endpoint.py`
Create a robust integration test using `httpx` or `FastAPI.TestClient`.
- Test Case: "End-to-End Chat Task Creation".
- Flow: Use `test_user_ai_99` as the path parameter. Send a message: "Add a task to record the demo video with high priority".
- Validation: Assert status code 200 and check that the response contains the expected final output string.


### 4. Technical Requirements (Strict)
- Use absolute imports (e.g., `from src.services...`).
- Ensure the `chat_service` call uses the verified positional arguments: `result = await Runner.run(agent, message, session=history, context={"auth_user_id": user_id})`.
- The environment must remain production-ready (no hardcoded test IDs in `src/`).

## Response snapshot

Successfully completed all four steps to finalize the AI-Native Todo API implementation with MCP integration. Created the chat endpoint, updated main.py to include the chat router, implemented comprehensive integration tests, and ensured proper session handling for the agents SDK. Both integration tests are now passing, validating the complete flow from JWT authentication through MCP tools to database persistence.

## Outcome

- ✅ Impact: Fully operational AI chatbot API with MCP integration, JWT authentication, and conversation persistence
- 🧪 Tests: Both integration tests passing (test_chatbot_api_integration and test_multiple_interactions_integration)
- 📁 Files: Created backend/src/api/chat.py, updated backend/src/main.py, created backend/tests/test_chat_endpoint.py, fixed backend/src/services/chat_service.py session handling
- 🔁 Next prompts: Deploy and validate in staging environment
- 🧠 Reflection: Proper session handling with the agents SDK was critical for successful MCP integration

## Evaluation notes (flywheel)

- Failure modes observed: Initially incorrect session object handling in agents SDK caused TypeError
- Graders run and results (PASS/FAIL): PASS - All integration tests passing
- Prompt variant (if applicable): AI agent integration
- Next experiment (smallest change to try): Add conversation history functionality to enhance AI context
