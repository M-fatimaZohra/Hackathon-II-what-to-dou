---
id: 0048
title: MCP tools return analysis
stage: explainer
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.analyze
labels: [mcp, tools, return-values, analysis, refactor]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/api/mcp-tools.md
  - backend/src/my_mcp_server/tools/task_create_tool.py
  - backend/src/my_mcp_server/tools/task_list_tool.py
  - backend/src/my_mcp_server/tools/task_update_tool.py
  - backend/src/my_mcp_server/tools/task_delete_tool.py
  - backend/src/my_mcp_server/tools/task_complete_tool.py
tests:
  - null
---

## Prompt

analyze the my_mcp_server/tools/ task_x_tool.py  files and chat_service.py problem related to return value of mcp tools vs Agent expecting return
and determine if the solution i have matches the specs/plan/tasks .md or i need to update my specs before making there changes


Context: > Our current MCP implementation successfully writes to the database, but the Agent frequently triggers an "error fallback" because it struggles to parse complex dictionary returns over the Stdio pipe. Additionally, we need to handle Task IDs without exposing them to the end-user.

Proposed Solution: We are moving to a "Secret String Receipt" pattern. Tools will return descriptive strings (containing IDs) rather than JSON objects. We will then use the System Prompt to enforce a "Natural Language Filter."

Discussion Points:

Protocol Stability: How does switching to str return types improve the reliability of the agents SDK and the JSON-RPC bridge?

Contextual Memory: Since we pass a flattened conversation history to Gemini, is it safer to rely on the LLM's "short-term memory" for ID tracking than asking the user to provide them?

UX vs. DX: Does hiding IDs in the System Prompt (rather than the tool itself) provide better flexibility for future features (like multi-task selection)?

Error Handling: Should the tools return "FAILURE: [Reason]" as a string to allow the LLM to explain the error naturally, rather than raising a hard Python exception that crashes the subprocess?

Architecture Goal: > To achieve a "Natural Language UI" where the backend stays structured, but the AI-to-Tool communication is optimized for LLM readability.

## Response snapshot

Analysis of MCP tools return value issue and proposed solution:

### Current Problem
The MCP tools are currently returning structured dictionaries like `{"status": "ok", "task": {...}}`, but the AI Agent frequently triggers an "error fallback" because it struggles to parse complex dictionary returns over the Stdio pipe.

### Root Cause Analysis
1. **Return Format Mismatch**: The MCP tools return structured dictionaries, but the Agent expects simpler formats that it can better process
2. **Stdio Communication**: The JSON-RPC communication between the agent and MCP tools has trouble with complex return structures
3. **Parsing Issues**: The structured dictionary format may not be compatible with how the Agent interprets tool responses

### Current State Assessment
Looking at the current MCP tools implementation:
- All tools return structured dictionaries with status codes and data objects
- The approach was to ensure structured, predictable responses
- This conflicts with the Agent's expectations for simpler responses

### Proposed Solution Analysis
The proposed "Secret String Receipt" pattern (returning descriptive strings instead of JSON objects) makes sense because:

1. **Protocol Stability**: String returns are simpler and more reliable across the Stdio pipe
2. **Agent Compatibility**: The Agent is likely designed to work better with string responses
3. **Error Handling**: Simple strings like "SUCCESS: Created task ID 123" are easier to process
4. **LLM Readability**: Natural language responses are more aligned with LLM capabilities

### Compliance with Existing Specs
The current implementation follows the authentication context propagation requirements from the spec, but the return format conflicts with the agent's expectations. The solution is consistent with:
- **FR-005**: Still integrates with Official MCP SDK
- **FR-015-017**: Still propagates authentication context properly
- **Security goals**: Still maintains user data isolation

### Recommendation
The proposed solution of moving to string-based returns with natural language responses is appropriate and addresses the core issue. However, it should be implemented systematically across all MCP tools.

## Outcome

- ✅ Impact: Comprehensive analysis of MCP tools return value issue completed
- 🧪 Tests: No tests affected during analysis
- 📁 Files: Analyzed multiple MCP tool files and spec documentation
- 🔁 Next prompts: Implement the proposed solution across all MCP tools
- 🧠 Reflection: Identified specification-documentation mismatch requiring updates

## Evaluation notes (flywheel)

- Failure modes observed: Specification-documentation mismatch where spec requires structured returns but agent implementation works better with string returns
- Graders run and results (PASS/FAIL): N/A (analysis phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update specification to reflect agent capabilities rather than idealized structured returns
