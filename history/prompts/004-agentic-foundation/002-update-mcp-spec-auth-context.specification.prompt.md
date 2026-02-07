---
id: 2
title: Update MCP spec auth context
stage: spec
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.plan
labels: [specification, authentication, mcp, security, contract]
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

/sp.plan

Update the following files to explicitly reflect authentication context propagation (auth\_user\_id) from the API layer through the service layer to MCP tools:

specs/api/mcp-tools.md – Add a note for each tool showing that auth\_user\_id must be passed from the service layer and validated before any operation.

specs/004-agentic-foundation/plan.md – Include a short section under MCP SDK integration detailing that all MCP tool calls must propagate auth\_user\_id and follow the authentication contract.

specs/004-agentic-foundation/contracts/chat-api-contract.md – Update MCP tool references to specify that auth\_user\_id is required for each tool call, ensuring requests are validated against the JWT and ownership checks.

Ensure naming consistency for all tools (add\_task vs create\_task) and optionally reference conversation\_id where relevant for context tracing.

## Response snapshot

Perfect! I've successfully updated all the requested files to explicitly reflect the authentication context propagation requirements:

1. **specs/api/mcp-tools.md**: Added "Security" clauses for each tool noting that auth_user_id must be passed from the service layer via ctx.request_context, and included a new "Authentication Context Propagation" section detailing the flow from service layer to MCP tools.

2. **specs/004-agentic-foundation/plan.md**: Added an "Authentication Context Propagation" section under Technical Context that details the security contract for MCP SDK integration, outlining the responsibilities of each layer.

3. **specs/004-agentic-foundation/contracts/chat-api-contract.md**: Updated each MCP tool contract to include "Auth Context" requirements, added a mapping between create_task and add_task, and included an "Authentication Context Propagation" section with conversation ID context tracing notes.

All files now consistently reflect the authentication context propagation requirements, ensuring that auth_user_id is properly passed from the API layer through the service layer to MCP tools, with proper validation at each step.

## Outcome

- ✅ Impact: Updated MCP-related specifications with clear authentication context propagation requirements
- 🧪 Tests: No tests affected
- 📁 Files: specs/api/mcp-tools.md, specs/004-agentic-foundation/plan.md, specs/004-agentic-foundation/contracts/chat-api-contract.md updated with authentication context details
- 🔁 Next prompts: /sp.tasks to update tasks based on new specifications
- 🧠 Reflection: Systematic approach to securing MCP tools by clarifying authentication contract across all layers

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update tasks.md to reflect new authentication requirements