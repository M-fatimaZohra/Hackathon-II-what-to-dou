---
id: 0045
title: Update Plan MD MCP Directory Name
stage: refactor
date: 2026-02-05
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: unknown
command: /sp.plan
labels: [directory, naming, mcp, architecture]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-agentic-foundation/plan.md
tests:
  - none
---

## Prompt

Update the source code structure section in plan.md. Change the directory from mcp/ to my_mcp_server/ to avoid name shadowing with the MCP package imports.

What to change: In the "Source Code (extends existing structure)" subsection, replace the entire mcp/ directory block with my_mcp_server/. Keep all file paths and comments identical, just rename the parent directory from mcp to my_mcp_server

## Response snapshot

Updated plan.md to change the directory from mcp/ to my_mcp_server/ to prevent name shadowing with the MCP package imports. This resolves the import conflict where the local mcp/server.py was shadowing the external mcp.server.fastmcp module.

## Outcome

- ✅ Impact: Resolved import naming conflict that was preventing MCP server from starting
- 🧪 Tests: none
- 📁 Files: Updated specs/004-agentic-foundation/plan.md with new directory structure
- 🔁 Next prompts: Update tasks.md and CLAUDE.md to reflect new directory name
- 🧠 Reflection: Directory naming conflicts can cause subtle import errors that break functionality

## Evaluation notes (flywheel)

- Failure modes observed: Name shadowing between local mcp directory and external mcp package
- Graders run and results (PASS/FAIL): PASS - Directory structure updated correctly
- Prompt variant (if applicable): Naming convention fix
- Next experiment (smallest change to try): Update implementation files to match new directory structure
