---
id: 4
title: MCP tool refactoring
stage: refactor
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.implement
labels: [refactor, mcp, authentication, context]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/my_mcp_server/tools/task_create_tool.py
  - backend/src/my_mcp_server/tools/task_update_tool.py
  - backend/src/my_mcp_server/tools/task_delete_tool.py
  - backend/src/my_mcp_server/tools/task_complete_tool.py
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

Refactor the MCP tool function signatures in the following files:

- task_create_tool.py
- task_list_tool.py
- task_update_tool.py
- task_delete_tool.py
- task_complete_tool.py

Requirement:
- `ctx: Context` must be the **first parameter** in all async functions.
- Move other arguments after `ctx`.
- Keep type hints intact.

Explain: This ensures MCP SDK injects Context properly. Tools fail if Context is not first.

## Response snapshot

Successfully refactored MCP tool function signatures to ensure `ctx: Context` is the first parameter in all async functions:

1. task_create_tool.py: Changed `create_task(title: str, ctx: Context, description: str = "")` to `create_task(ctx: Context, title: str, description: str = "")`
2. task_update_tool.py: Changed `update_task(task_id: int, ctx: Context, title: str = None, description: str = None)` to `update_task(ctx: Context, task_id: int, title: str = None, description: str = None)`
3. task_delete_tool.py: Changed `delete_task(task_id: int, ctx: Context)` to `delete_task(ctx: Context, task_id: int)`
4. task_complete_tool.py: Changed `complete_task(task_id: int, ctx: Context)` to `complete_task(ctx: Context, task_id: int)`
5. task_list_tool.py: Already had `ctx: Context` in the correct first position (no changes needed)
6. Also updated the synchronous wrapper functions and internal function calls to match the new signatures

All tasks in the tasks.md file for these changes have been marked as completed:
- T045: Update task_create_tool
- T046: Update task_list_tool
- T047: Update task_update_tool
- T048: Update task_delete_tool
- T049: Update task_complete_tool

## Outcome

- ✅ Impact: MCP tools now properly accept Context as first parameter
- 🧪 Tests: No tests affected yet
- 📁 Files: 5 MCP tool files updated, tasks.md updated
- 🔁 Next prompts: Continue with remaining User Story 4 tasks
- 🧠 Reflection: Proper function signatures ensure MCP SDK can inject Context correctly

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with T050-T054 tasks for chat_service refactoring and integration