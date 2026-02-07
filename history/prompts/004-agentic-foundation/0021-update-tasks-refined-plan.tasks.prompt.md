---
id: 0021
title: update-tasks-refined-plan
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.tasks
labels: ["tasks", "refinement", "architecture", "alignment"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

Update tasks.md to change all references from "backend/src/config.py" to "backend/src/configs/gemini_config.py" in tasks T009, T014, and T032 to align with the plan.md structure that uses configs/gemini_config.py for Gemini model parameters.
# Update task.md: Implementation Roadmap
Please rewrite the tasks in `task.md` to follow the refined plan:

1. **Environment (T009, T032)**: Ensure these tasks focus on loading the `.env` file within the main application entry point (`main.py`) or the relevant service.
2. **Gemini Config (T014)**: Create `backend/src/configs/gemini_config.py` to house the Agent's instructions and model settings.
3. **Chat Service (T015, T017, T018)**: Implement the Agent and Runner logic in `backend/src/services/chat_service.py`. It should pull settings from `gemini_config.py`.
4. **History Logic (T026, T027)**: Implement strictly in `backend/src/services/conversation_service.py`.
5. **API Flow (T019)**: The chat endpoint logic must:
   - Load history via `conversation_service`.
   - Get AI response via `chat_service`.
   - Save new messages via `conversation_service`.

Use absolute `src.` imports for all files.

## Response snapshot

Successfully updated tasks.md to align with the refined plan:

**Environment Configuration Updates:**
- T009: Updated from `backend/src/config.py` to `backend/src/main.py (loading .env file)`
- T014: Updated from `backend/src/config.py` to `backend/src/configs/gemini_config.py`
- T032: Updated from `backend/src/config.py` to `backend/src/main.py (loading .env file for environment toggle)`

**Gemini Config Task (T014):**
- Now correctly creates `backend/src/configs/gemini_config.py` to house Agent's instructions and model settings

**Chat Service Tasks (T015, T017, T018):**
- T015: Updated to configure OpenAI Agents SDK to pull settings from gemini_config.py in `backend/src/services/chat_service.py`
- T017: Updated to create stateless Agent initialization in `backend/src/services/chat_service.py` (pulls settings from gemini_config.py)
- T018: Updated to implement chatbot runner in `backend/src/services/chat_service.py` (chatbot engine that initializes Agent and handles Runner() logic)
- T018a: Updated to integrate agent with MCP server in `backend/src/services/chat_service.py`
- T018b: Updated to connect MCP server to agent in `backend/src/services/chat_service.py`

**History Logic Tasks (T026, T027):**
- T026: Updated to implement conversation history fetching in `backend/src/services/conversation_service.py` (CRUD for Conversation/Message tables)
- T027: Updated to implement storing and managing new messages in `backend/src/services/conversation_service.py` (CRUD for Conversation/Message tables)

**API Flow Task (T019):**
- Updated to reflect that chat endpoint loads history via conversation_service, gets AI response via chat_service, and saves new messages via conversation_service

**API Flow Task (T029):**
- Updated to reflect conversation management logic loads history via conversation_service, gets AI response via chat_service, and saves new messages via conversation_service

The tasks now accurately reflect the refined plan with proper separation of concerns and correct file paths.

## Outcome

- ✅ Impact: Updated tasks to align with refined plan architecture
- 🧪 Tests: No tests affected by task structure updates
- 📁 Files: Updated specs/004-agentic-foundation/tasks.md with correct architecture paths
- 🔁 Next prompts: Ready to continue with implementation following aligned architecture
- 🧠 Reflection: Tasks now properly aligned with refined plan structure

## Evaluation notes (flywheel)

- Failure modes observed: None - all updates completed successfully
- Graders run and results (PASS/FAIL): Not applicable for task structure update
- Prompt variant (if applicable): Architecture refinement task
- Next experiment (smallest change to try): Proceed with implementation following updated tasks