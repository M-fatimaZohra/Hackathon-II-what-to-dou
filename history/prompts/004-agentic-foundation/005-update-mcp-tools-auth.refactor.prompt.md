---
id: 5
title: MCP tools auth update
stage: refactor
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.implement
labels: [refactor, mcp, authentication, environment]
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
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

Update all MCP tools in:

- task_create_tool.py
- task_list_tool.py
- task_update_tool.py
- task_delete_tool.py
- task_complete_tool.py

Changes needed:
- Replace `user_id = ctx.request_context.get("auth_user_id")` with:
    user_id = os.getenv("AUTH_USER_ID")
- Remove any dependency on ctx.request_context for auth.
- If user_id is None, return a structured error:
    {"status": "error", "code": "unauthorized", "message": "Authentication required"}

Explain: StdIO MCP runs in a separate process. Context is not propagated. Only env works.

## Response snapshot

Successfully updated all MCP tools to use environment variables for authentication instead of ctx.request_context:

1. task_create_tool.py:
   - Added `import os`
   - Changed user_id extraction from `ctx.request_context.get("auth_user_id")` to `os.getenv("AUTH_USER_ID")`
   - Updated error handling to return structured error: `{"status": "error", "code": "unauthorized", "message": "Authentication required"}`
   - Updated exception error handling to return structured error

2. task_list_tool.py:
   - Added `import os`
   - Changed user_id extraction from `ctx.request_context.get("auth_user_id")` to `os.getenv("AUTH_USER_ID")`
   - Updated error handling to return structured error
   - Updated exception error handling to return structured error

3. task_update_tool.py:
   - Added `import os`
   - Changed user_id extraction from `ctx.request_context.get("auth_user_id")` to `os.getenv("AUTH_USER_ID")`
   - Updated error handling to return structured error
   - Updated "task not found" error to return structured error
   - Updated exception error handling to return structured error

4. task_delete_tool.py:
   - Added `import os`
   - Changed user_id extraction from `ctx.request_context.get("auth_user_id")` to `os.getenv("AUTH_USER_ID")`
   - Updated error handling to return structured error
   - Updated "task not found" error to return structured error
   - Updated exception error handling to return structured error

5. task_complete_tool.py:
   - Added `import os`
   - Changed user_id extraction from `ctx.request_context.get("auth_user_id")` to `os.getenv("AUTH_USER_ID")`
   - Updated error handling to return structured error
   - Updated "task not found" error to return structured error
   - Updated exception error handling to return structured error

6. Updated task T051 in tasks.md to mark as completed: "[x] T051 [US4] Add error handling for missing auth_user_id in MCP tools"

All tools now properly use environment variables for authentication since StdIO MCP runs in a separate process where ctx.request_context is not propagated.

## Outcome

- ✅ Impact: MCP tools now use environment variables for auth propagation
- 🧪 Tests: No tests affected yet
- 📁 Files: 5 MCP tool files updated, tasks.md updated
- 🔁 Next prompts: Continue with remaining User Story 4 tasks
- 🧠 Reflection: Proper auth context now works in separate MCP process via environment variables

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with T050, T052-T054 tasks for chat_service refactoring and integration