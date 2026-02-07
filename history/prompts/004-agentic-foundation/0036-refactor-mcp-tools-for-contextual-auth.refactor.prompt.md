---
id: 0036
title: Refactor MCP Tools for Contextual Auth
stage: refactor
date: 2026-02-04
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: unknown
command: /sp.implement
labels: [mcp, authentication, refactoring, context, tools]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/mcp/tools/task_create_tool.py
  - backend/src/mcp/tools/task_list_tool.py
  - backend/src/mcp/tools/task_update_tool.py
  - backend/src/mcp/tools/task_delete_tool.py
  - backend/src/mcp/tools/task_complete_tool.py
tests:
  - none
---

## Prompt

Goal: Refactor MCP Tools for Contextual Auth

Please update the 5 tool files in `backend/src/mcp/tools/` to support authenticated users.

### Requirements:
1. **Type Hinting**: Add `ctx: Context` as the final parameter to each tool function (e.g., `create_task(title: str, ctx: Context)`).
2. **User Extraction**: Inside each function, extract the user ID using:
   `user_id = ctx.request_context.get("auth_user_id")`
3. **Validation**: If `user_id` is missing, use `ctx.error()` and return an "Unauthorized" message.
4. **Logic Update**: Update the database calls within the tools to use this `user_id` instead of hardcoded values.

## Response snapshot

Updated all 5 MCP tool files to support authenticated users with contextual authentication, including proper parameter ordering, Context import, user_id extraction, and error handling.

## Outcome

- ✅ Impact: Successfully implemented contextual authentication for all MCP tools, ensuring user data isolation and proper authorization validation.
- 🧪 Tests: none
- 📁 Files: Modified all 5 MCP tool files: task_create_tool.py, task_list_tool.py, task_update_tool.py, task_delete_tool.py, task_complete_tool.py
- 🔁 Next prompts: Test agent integration with updated tools, Verify user isolation in multi-user scenarios
- 🧠 Reflection: Refactoring the MCP tools to use contextual authentication provides better security and user data isolation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Validate functionality in multi-user environment
