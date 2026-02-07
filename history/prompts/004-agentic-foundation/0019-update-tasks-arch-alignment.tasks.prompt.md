---
id: 0019
title: update-tasks-arch-alignment
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.tasks
labels: ["tasks", "architecture", "alignment", "file-paths"]
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

 update tasks to include missing mcp server and init_db files
# Mandatory Architectural Alignment
We are strictly following the directory structure defined in `Plan.md`.

1. **Discard** any file paths proposed in `task.md` that contradict `Plan.md`.
2. **Key Locations**:
   - MCP Server: `src/mcp/server.py`
   - Chat Schemas (Pydantic): `src/schema/chat_models.py`
   - DB Tables (SQLModel): `src/schema/models.py`
3. **Requirement**: All imports must use the `src.` prefix (e.g., `from src.services.task_service import ...`).
4. **Action**: Update `task.md` to reflect these paths so the roadmap matches the architecture.

## Response snapshot

Successfully updated tasks.md to align with Plan.md architectural structure:

**Added missing foundational components:**
- T004a: Added database initialization framework task at `backend/src/database/init_db.py`
- T005a: Added MCP server implementation task at `backend/src/mcp/server.py`
- T007a: Added chat-specific models task at `backend/src/schema/chat_models.py`

**Updated User Story 2 to reflect proper structure:**
- T024: Updated to define Pydantic models for conversation in `backend/src/schema/chat_models.py`
- T025: Updated to define SQLModel tables in `backend/src/schema/models.py`

**Enhanced User Story 1 with proper agent integration:**
- T017: Maintained stateless Agent for chatbot service in `backend/src/agents/chatbot.py`
- T018: Maintained chatbot runner implementation in `backend/src/services/chat_service.py`
- T018a: Added integration with MCP server in `backend/src/agents/chatbot.py`
- T018b: Added connection to MCP server in `backend/src/services/chat_service.py`
- T020: Added validation and error handling for chat endpoint in `backend/src/api/chat.py`
- T021: Added logging for user story 1 operations

**Updated dependencies and integration points:**
- T028: Updated to integrate conversation context in `backend/src/services/chat_service.py` (depends on T017)
- T029: Updated to add conversation management logic in `backend/src/api/chat.py` (depends on T019)

The tasks now correctly reflect the architecture defined in Plan.md with proper separation of concerns between core models and chat-specific models, dedicated MCP server implementation, and database initialization framework.

## Outcome

- ✅ Impact: Updated tasks to align with Plan.md architectural structure
- 🧪 Tests: No tests affected by task structure updates
- 📁 Files: Updated specs/004-agentic-foundation/tasks.md with correct architecture paths
- 🔁 Next prompts: Ready to continue with implementation following aligned architecture
- 🧠 Reflection: Tasks now properly aligned with Plan.md directory structure

## Evaluation notes (flywheel)

- Failure modes observed: None - all task updates completed successfully
- Graders run and results (PASS/FAIL): Not applicable for task structure update
- Prompt variant (if applicable): Architecture alignment task
- Next experiment (smallest change to try): Proceed with implementation following updated tasks