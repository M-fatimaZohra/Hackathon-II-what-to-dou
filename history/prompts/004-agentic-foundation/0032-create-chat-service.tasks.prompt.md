---
id: 0032
title: create-chat-service
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.implement
labels: ["service", "chat", "agent", "mcp", "integration"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/services/chat_service.py
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

# Goal: Build the ChatService using openai-agents

Please create `backend/src/services/chat_service.py`. This file will handle the reasoning loop where the Agent decides which MCP tools to call.

### 1. Requirements & Imports
- Import `Agent`, `Runner`, and `RunContextWrapper` from `agents`.
- Import `GEMINI_MODEL` and `SYSTEM_PROMPT` from `src.configs.gemini_config`.
- Import `mcp` from `src.mcp.server`.
- Import your Pydantic models: `ChatRequest`, `ChatResponse`, `ToolCallInfo` from `src.schema.chat_models`.

### 2. Context Definition
- Create a small `@dataclass` called `UserContext` that holds `auth_user_id: str`.
- This is what will be passed to the MCP tools.

### 3. Agent Implementation
- Initialize the `Agent`:
   - `name="TodoAssistant"`
   - `model=GEMINI_MODEL`
   - `instructions=SYSTEM_PROMPT`
   - `tools=mcp.tools`

### 4. Main Function: `get_chat_response`
Create an `async` function that:
- Takes `user_id`, `conversation_id`, and `message`.
- Initializes the `UserContext(auth_user_id=user_id)`.
- Uses `await Runner.run(...)` to start the agent loop.
- **Pass the context**: Ensure the `context` argument in `Runner.run` is set to your `UserContext` instance.
- **Collect Tool Calls**: Iterate through the `result.runs` to extract any tool names and arguments used during the process.
- **Return**: A `ChatResponse` containing the final text, the `conversation_id`, and the list of `ToolCallInfo`.

### 5. Note on History
For now, keep the message history simple (passing the current message as a string). We will add DB-backed `Session` persistence in the next step.

## Response snapshot

Successfully created the chat_service.py file with all the requested functionality:

1. **Imports**: Added all required imports including Agent, Runner, RunContextWrapper from agents; GEMINI_MODEL and SYSTEM_PROMPT from gemini_config; mcp from the server; and Pydantic models from chat_models.

2. **Context Definition**: Created the `UserContext` dataclass with `auth_user_id: str` field to securely pass user context to MCP tools.

3. **Agent Implementation**: Initialized the `todo_assistant` Agent with:
   - name="TodoAssistant"
   - model=GEMINI_MODEL
   - instructions=SYSTEM_PROMPT
   - tools=mcp.mcp.tools

4. **Main Function `get_chat_response`**: Created an async function that:
   - Takes `user_id`, `conversation_id`, and `message` as parameters
   - Creates `UserContext(auth_user_id=user_id)`
   - Uses `await Runner.run()` with the agent and context
   - Collects tool calls from the result by iterating through result.runs
   - Returns a `ChatResponse` with the conversation_id, AI response, and tool call information

5. **Task Update**: Marked T017 as completed in tasks.md since this task involved creating the stateless Agent initialization in the chat service.

The implementation properly handles secure user context passing to MCP tools, collects tool calls made during the AI interaction, and returns a structured response following the defined Pydantic models.

## Outcome

- ✅ Impact: Created complete chat service with AI agent integration and MCP tool handling
- 🧪 Tests: No tests affected by service creation (would be added separately)
- 📁 Files: Created backend/src/services/chat_service.py and updated tasks.md
- 🔁 Next prompts: Ready to continue with chat endpoint and conversation service integration
- 🧠 Reflection: Service properly implements agent-loop with secure context and tool call collection

## Evaluation notes (flywheel)

- Failure modes observed: None - all components implemented successfully per requirements
- Graders run and results (PASS/FAIL): Not applicable for service implementation
- Prompt variant (if applicable): Chat service with agent integration
- Next experiment (smallest change to try): Implement the chat API endpoint that uses this service