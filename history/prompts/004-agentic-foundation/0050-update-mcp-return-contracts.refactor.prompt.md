---
id: 0050
title: Update MCP return contracts
stage: refactor
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.plan
labels: [mcp, return-format, specification, refactor, api-contract]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/api/mcp-tools.md
  - specs/004-agentic-foundation/plan.md
  - specs/004-agentic-foundation/contracts/chat-api-contract.md
tests:
  - null
---

## Prompt

update mcp return contracts refactor specs/api/mcp-tools.md specs/004-agentic-foundation/plan.md specs/004-agentic-foundation/contracts/chat-api-contract.md

Change MCP tool return contract from JSON/dict to string. Why: Prevents Agent "fallback errors" by using LLM-native string receipts. Rule: Tools must return SUCCESS: [Title] (ID: [id]). IDs are for AI memory only; hide them from the user in the final UI response.

## Response snapshot

Successfully updated all MCP tool specification files to change the return contract from JSON/dict to string format:

1. **specs/api/mcp-tools.md**:
   - Added new "MCP Tool Return Contract" section explaining the string-based approach
   - Updated all 5 MCP tools (create, list, update, delete, complete) to return descriptive string receipts
   - Changed from JSON responses like `{"task_id": 5, "status": "created", "title": "Buy groceries"}` to string responses like `"SUCCESS: Created task 'Buy groceries' (ID: 5)"`
   - Updated expected responses for all tools to use the new string format

2. **specs/004-agentic-foundation/plan.md**:
   - Added new "MCP Tool Return Contract" section under Authentication Context Propagation
   - Documented the string-based return format approach to prevent agent fallback errors
   - Explained that task IDs in return strings are for AI memory only and should be hidden from end-users
   - Added implementation notes about agent reliability and Stdio communication improvements

3. **specs/004-agentic-foundation/contracts/chat-api-contract.md**:
   - Updated all 5 MCP tool contracts (create_task, list_tasks, update_task, delete_task, complete_task) to specify string return format
   - Changed from object/array returns to descriptive string receipts
   - Added detailed output specifications using "SUCCESS:" and "ERROR:" patterns
   - Added section explaining the MCP Tool Return Contract for agent reliability

The changes implement the "Secret String Receipt" pattern where tools return descriptive strings that contain IDs for AI memory but hide these from users in the final UI response. This approach prevents agent fallback errors by using LLM-native string receipts that are more reliably parsed through the Stdio communication channel.

## Outcome

- ✅ Impact: Updated all MCP tool contracts to use string-based return format for improved agent reliability
- 🧪 Tests: No tests affected during specification update
- 📁 Files: Updated 3 specification files (mcp-tools.md, plan.md, chat-api-contract.md)
- 🔁 Next prompts: Update MCP tool implementations to match new specification
- 🧠 Reflection: Specification now properly reflects string-based return contract for agent compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update MCP tool implementations to return strings per new spec
