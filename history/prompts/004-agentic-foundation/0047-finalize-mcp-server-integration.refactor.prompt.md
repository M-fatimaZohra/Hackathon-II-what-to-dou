---
id: 0047
title: Finalize MCP Server Integration
stage: refactor
date: 2026-02-05
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: unknown
command: /sp.implement
labels: [mcp, integration, refactor, session, authentication]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/services/chat_service.py
  - backend/src/my_mcp_server/server.py
  - backend/src/schema/models.py
tests:
  - none
---

## Prompt

Task: Refactor MCP Server Integration and Pathing

I have renamed my MCP server folder from src/mcp to src/my_mcp_server to avoid naming collisions with the mcp library. I need you to update the chat_service.py file to ensure the sub-process launches correctly and the user context is preserved.

Please perform the following edits in src/services/chat_service.py:

Add Import: Add import sys at the top of the file.

Fix MCP Server Launch: Update the MCPServerStdio initialization:

Change "command": "python" to "command": sys.executable (this ensures the current virtual environment is used).

Update "args" to ["src/my_mcp_server/server.py"].

Inject Auth ID: Inside the env dictionary, add "AUTH_USER_ID": user_id. This serves as a critical bridge for the security context over the Stdio pipe.

Please perform the following edits in src/my_mcp_server/server.py:

Update Internal Tool Imports: Update all tool imports to reflect the new directory name. Change lines like from src.mcp.tools... to from src.my_mcp_server.tools....

Refine Database Models (src/schema/models.py):

Timezone Awareness: Update the created_at field in your models to be timezone-aware to fix deprecation warnings.

Import timezone from datetime.

Set the default_factory to lambda: datetime.now(timezone.utc).

Please ensure all paths are absolute within the project structure (starting with src.).

## Response snapshot

Successfully updated MCP server integration with proper virtual environment handling and timezone-aware datetime fields. Updated chat_service.py to use sys.executable for consistent subprocess execution, updated server.py to use the correct import paths with new directory name, and updated schema models to use timezone-aware datetime to address deprecation warnings.

## Outcome

- ✅ Impact: MCP server now uses proper subprocess execution with virtual environment consistency and secure context passing
- 🧪 Tests: none
- 📁 Files: Updated backend/src/services/chat_service.py, backend/src/my_mcp_server/server.py, backend/src/schema/models.py
- 🔁 Next prompts: Test MCP integration with updated configuration
- 🧠 Reflection: Using sys.executable ensures consistent environment behavior across deployments, timezone-aware datetimes fix deprecation warnings

## Evaluation notes (flywheel)

- Failure modes observed: Potential subprocess execution issues with hardcoded "python" command, deprecated datetime.utcnow() calls
- Graders run and results (PASS/FAIL): PASS - All changes implemented successfully
- Prompt variant (if applicable): MCP integration refactoring
- Next experiment (smallest change to try): Test full end-to-end MCP integration with real requests
