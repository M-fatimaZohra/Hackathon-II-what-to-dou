---
id: 0051
title: Update tasks for string return format
stage: refactor
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.tasks
labels: [mcp, return-format, tasks, refactor, specification]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

update task.md check points to match new mcp tools string base return

The changes implement the "Secret String Receipt" pattern
where tools return descriptive strings that contain IDs
for AI memory but hide these from users in the final UI
response. This approach prevents agent fallback errors by
using LLM-native string receipts that are more reliably
parsed through the Stdio communication channel.

## Response snapshot

Successfully updated the tasks.md file to reflect the MCP tools' string-based return format changes:

1. Removed duplicate Phase 6 section that contained redundant User Story 4 information
2. Created new Phase 6: User Story 4 - MCP Tool Return Value Fix that properly focuses on the "Secret String Receipt" pattern
3. Updated all task descriptions to reflect string return format requirements:
   - T045: Update task_create_tool to return "SUCCESS: Created task '[title]' (ID: [id])"
   - T046: Update task_list_tool to return "SUCCESS: Found [n] task(s) for user (ID: [id]): '[title]' ([status])"
   - T047: Update task_update_tool to return "SUCCESS: Updated task to '[title]' (ID: [id])"
   - T048: Update task_delete_tool to return "SUCCESS: Deleted task '[title]' (ID: [id])"
   - T049: Update task_complete_tool to return "SUCCESS: Completed task '[title]' (ID: [id])"
   - T051: Update error handling to return "ERROR: [reason]" strings instead of JSON
   - T053: Update API contract documentation to reflect string response changes

4. Updated the goal statement to emphasize the "Secret String Receipt" pattern where tools return descriptive strings containing IDs for AI memory while hiding them from users in the final UI response
5. Updated test requirements to verify string responses instead of JSON responses
6. Maintained the proper structure and organization of the tasks file

The changes align the tasks with the requirement to use string-based return values to prevent agent fallback errors and improve reliability through LLM-native string receipts.

## Outcome

- ✅ Impact: Updated tasks to reflect "Secret String Receipt" pattern for MCP tools
- 🧪 Tests: Updated test tasks to verify string responses instead of JSON
- 📁 Files: Updated specs/004-agentic-foundation/tasks.md
- 🔁 Next prompts: Begin implementation of string return format in MCP tools
- 🧠 Reflection: Tasks now properly reflect the string-based return contract needed for agent reliability

## Evaluation notes (flywheel)

- Failure modes observed: Duplicate phase sections in original tasks.md
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement the string return format changes in the actual MCP tools
