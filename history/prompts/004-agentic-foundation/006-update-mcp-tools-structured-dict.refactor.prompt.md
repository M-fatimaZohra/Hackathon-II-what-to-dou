---
id: 6
title: MCP tools structured dict
stage: refactor
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.implement
labels: [refactor, mcp, structured-return]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/my_mcp_server/tools/task_create_tool.py
  - backend/src/my_mcp_server/tools/task_list_tool.py
  - backend/src/my_mcp_server/tools/task_update_tool.py
  - backend/src/my_mcp_server/tools/task_delete_tool.py
  - backend/src/my_mcp_server/tools/task_complete_tool.py
tests:
  - null
---

## Prompt

In all MCP tools (task_create_tool, task_list_tool, task_update_tool, task_delete_tool, task_complete_tool):

- Remove any calls to `ctx.error(...)`
- Replace with structured dicts:

Success example:
  {"status": "ok", "task": {...}}  # include task_id, title, completed if relevant

Error example:
  {"status": "error", "code": "not_found", "message": "Task not found"}
  {"status": "error", "code": "exception", "message": str(exception)}

Explain: Returning ctx.error() causes MCP to fail silently. Structured returns are safer.

## Response snapshot

Successfully updated all MCP tools to use structured dictionaries for return values instead of strings or ctx.error() calls:

1. task_create_tool.py:
   - Updated success case to return: `{"status": "ok", "task": {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed, "user_id": task.user_id}}`
   - Error cases already correctly return structured dictionaries

2. task_list_tool.py:
   - Updated empty list case to return: `{"status": "ok", "tasks": [], "message": f"No tasks found for user {user_id}"}}`
   - Updated success case to return: `{"status": "ok", "tasks": task_objects}}` where task_objects is a list of task dictionaries
   - Error cases already correctly return structured dictionaries

3. task_update_tool.py:
   - Updated success case to return: `{"status": "ok", "task": {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed, "user_id": task.user_id}}`
   - Error cases already correctly return structured dictionaries

4. task_delete_tool.py:
   - Updated success case to return: `{"status": "ok", "message": f"Successfully deleted task ID {task_id}", "task_id": task_id}`
   - Error cases already correctly return structured dictionaries

5. task_complete_tool.py:
   - Updated success case to return: `{"status": "ok", "task": {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed, "user_id": task.user_id}}`
   - Error cases already correctly return structured dictionaries

All MCP tools now return consistent structured dictionaries that include success/error status and relevant data, making them safer for the MCP protocol and preventing silent failures.

## Outcome

- ✅ Impact: MCP tools now use structured return values consistently
- 🧪 Tests: No tests affected yet
- 📁 Files: 5 MCP tool files updated
- 🔁 Next prompts: Continue with remaining User Story 4 tasks
- 🧠 Reflection: Consistent structured returns prevent MCP silent failures

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with T050, T052-T054 tasks for chat_service refactoring and integration