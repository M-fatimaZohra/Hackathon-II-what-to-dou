---
id: 0049
title: Update MCP return contract
stage: spec
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.specify
labels: [mcp, return-format, specification, refactor]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-agentic-foundation/spec.md
tests:
  - null
---

## Prompt

update mcp specs in spec.md

Change MCP tool return contract from JSON/dict to string. Why: Prevents Agent "fallback errors" by using LLM-native string receipts. Rule: Tools must return SUCCESS: [Title] (ID: [id]). IDs are for AI memory only; hide them from the user in the final UI response.

## Response snapshot

Updated the spec.md file to change the MCP tool return contract from JSON/dict to string format. Added a new "MCP Tool Return Contract" section that specifies:

- MCP tools must return descriptive string receipts instead of JSON objects
- Success pattern: "SUCCESS: [Action completed] (ID: [id])"
- Error pattern: "ERROR: [Reason]"
- Task IDs in return strings are for AI memory only and must be hidden from users
- Rationale for improved LLM parsing reliability

This change addresses the agent "fallback errors" issue by using LLM-native string receipts instead of complex JSON objects that cause parsing issues over the Stdio pipe.

## Outcome

- ✅ Impact: Updated spec to reflect string-based MCP tool return format
- 🧪 Tests: No tests affected
- 📁 Files: Updated specs/004-agentic-foundation/spec.md
- 🔁 Next prompts: Update implementation to match new spec
- 🧠 Reflection: Specification now properly reflects the "Secret String Receipt" pattern for agent compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update MCP tools implementation to return strings per new spec
