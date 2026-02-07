---
id: 0015
title: complete-mcp-toolset
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.implement
labels: ["mcp", "tools", "security", "testing", "backend"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/mcp/tools/task_list_tool.py
  - backend/src/mcp/tools/task_update_tool.py
  - backend/src/mcp/tools/task_delete_tool.py
  - backend/src/mcp/tools/task_complete_tool.py
  - backend/tests/test_mcp_security.py
tests:
  - backend/tests/test_mcp_security.py
---

## Prompt

/sp.implement

# Goal: Complete the Task MCP Toolset with Security

According to plan, Please implement the following 4 tools in `src/mcp/tools/` using the same `ctx` security pattern used in `task_create_tool.py`.

1. `task_list_tool.py`: `list_tasks(status: str = "all")`. Must filter by `auth_user_id`.
2. `task_update_tool.py`: `update_task(task_id: int, title: str = None, description: str = None)`. Must verify `task.user_id == auth_user_id` before saving.
3. `task_delete_tool.py`: `delete_task(task_id: int)`. Must verify `task.user_id == auth_user_id` before deleting.
4. `task_complete_tool.py`: `complete_task(task_id: int)`. Must verify `task.user_id == auth_user_id` before marking `completed=True`.

# Testing Requirement

Update `tests/test_mcp_security.py` to include:

- A test where `user_two` tries to delete or update a task belonging to `user_one` (Verify it fails/returns an error).
- A test for `list_tasks` verifying it only returns the correct user's data.

## Response snapshot

Successfully completed all requested tasks:

**Complete MCP Toolset Implementation:**
1. **task_list_tool.py**: Implemented `list_tasks(status: str = "all")` with proper user filtering by `auth_user_id`. Includes support for "all", "completed", and "pending" status filters.
2. **task_update_tool.py**: Implemented `update_task(task_id: int, title: str = None, description: str = None)` with verification that `task.user_id == auth_user_id` before allowing updates.
3. **task_delete_tool.py**: Implemented `delete_task(task_id: int)` with verification that `task.user_id == auth_user_id` before allowing deletion.
4. **task_complete_tool.py**: Implemented `complete_task(task_id: int)` with verification that `task.user_id == auth_user_id` before marking tasks as completed.

**Security Pattern Consistency:**
- All tools use the same `ctx: dict` pattern to extract `user_id = ctx.get("auth_user_id")`
- No user_id is accepted as a function argument to prevent security bypass
- All tools verify the authenticated user owns the target task before performing operations

**Enhanced Security Tests:**
- Added `test_cross_user_task_access` to verify user_two cannot delete/update user_one's tasks
- Added `test_list_tasks_user_isolation` to verify list_tasks only returns correct user's data
- All 6 tests pass: original 4 + 2 new security tests

The complete MCP toolset now enforces proper user isolation across all task operations, ensuring AI agents can only perform actions on behalf of the authenticated user and cannot access other users' data.

## Outcome

- ✅ Impact: Complete MCP toolset with full security isolation across all task operations
- 🧪 Tests: All 6 security tests passed, including cross-user access protection
- 📁 Files: Created 4 MCP tools and updated security tests with comprehensive coverage
- 🔁 Next prompts: Ready to integrate MCP tools into chatbot service
- 🧠 Reflection: All tools consistently enforce user isolation through context authentication

## Evaluation notes (flywheel)

- Failure modes observed: None - all security tests passed including cross-user attempts
- Graders run and results (PASS/FAIL): All 6 tests passed successfully
- Prompt variant (if applicable): Complete MCP toolset implementation
- Next experiment (smallest change to try): Integrate tools with chatbot service and OpenAI Agents