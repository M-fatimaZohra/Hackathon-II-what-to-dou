---
id: 0024
title: refactor-mcp-tools-centralized
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.implement
labels: ["mcp", "refactor", "architecture", "centralization"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/mcp/tools/task_create_tool.py
  - backend/src/mcp/tools/task_list_tool.py
  - backend/src/mcp/tools/task_update_tool.py
  - backend/src/mcp/tools/task_delete_tool.py
  - backend/src/mcp/tools/task_complete_tool.py
  - backend/src/mcp/server.py
tests:
  - null
---

## Prompt

# Goal: Refactor MCP Tools for Unified Server Registration

I am moving to a centralized MCP Hub architecture. Please refactor the following files:
`backend/src/mcp/tools/task_create_tool.py`, `task_list_tool.py`, `task_update_tool.py`, `task_delete_tool.py`, and `task_complete_tool.py`.

### 1. Refactor Tools
- **Remove** `from mcp.server.fastmcp import FastMCP` and the `mcp = FastMCP(...)` initialization from these files.
- **Remove** the `@mcp.tool()` decorators from the functions.
- Keep the logic, imports for `Session`, `engine`, `Task`, and the `ctx` parameter usage exactly as they are.

### 2. Create `backend/src/mcp/server.py`
- Initialize a single `mcp = FastMCP("TodoManager")`.
- Import all 5 functions from the refactored tool files.
- Register them using the manual registration pattern: `mcp.tool()(function_name)`.

### 3. Verification
Ensure `server.py` is now the single entry point for all Task-related MCP tools.

## Response snapshot

Successfully completed the MCP tools refactoring for unified server registration:

**Step 1: Refactored all tool files**
- Removed `from mcp.server.fastmcp import FastMCP` and `mcp = FastMCP(...)` from all 5 tool files
- Removed `@mcp.tool()` decorators from all functions while preserving all logic
- Kept all imports for `Session`, `engine`, `Task`, and `ctx` parameter usage unchanged
- Updated all 5 tool files:
  - `task_create_tool.py`
  - `task_list_tool.py`
  - `task_update_tool.py`
  - `task_delete_tool.py`
  - `task_complete_tool.py`

**Step 2: Created unified server**
- Created `backend/src/mcp/server.py` with centralized MCP server instance
- Initialized single `mcp = FastMCP("TodoManager")` instance
- Imported all 5 refactored tool functions using relative imports
- Registered all functions using manual registration pattern: `mcp.tool()(function_name)`
- Added proper async main execution pattern for stdio server

**Step 3: Verification**
- `server.py` now serves as the single entry point for all Task-related MCP tools
- All tools maintain their original functionality but with centralized registration
- Follows the centralized MCP Hub architecture pattern

The refactoring successfully transforms the architecture from distributed tool registration to centralized registration, making it easier to manage all MCP tools from a single location while maintaining their individual functionality.

## Outcome

- ✅ Impact: Centralized MCP tools architecture with unified server registration
- 🧪 Tests: No immediate tests affected, maintains same functionality
- 📁 Files: Updated 5 tool files and created 1 unified server file
- 🔁 Next prompts: Ready to update any references to the old tool structure
- 🧠 Reflection: Centralized architecture will simplify future tool management

## Evaluation notes (flywheel)

- Failure modes observed: None - all refactoring completed successfully
- Graders run and results (PASS/FAIL): Not applicable for refactoring task
- Prompt variant (if applicable): MCP architecture centralization
- Next experiment (smallest change to try): Update any agent/service code that references the old structure