---
id: 1
title: Update spec auth context propagation
stage: spec
date: 2026-02-06
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: A.ZEE COMPUTERS
command: /sp.specify
labels: [specification, authentication, mcp, security]
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

/sp.specify

update 004-agentic-foundation only


Pre-Specification Conversation Prompts:

What is the expected behavior if auth\_user\_id is missing in MCP tools?

Which layer is responsible for propagating authentication context to MCP tools?

Are there existing tasks or specs that document this contract?

Should this be treated as a clarification/spec update before implementation?

Specification Update Sections:

Intent: Enforce secure authentication context propagation from API → Service Layer → MCP Tools. MCP tools must never operate without auth\_user\_id.

Constraints:

auth\_user\_id must be passed explicitly from the service layer.

MCP tools must verify auth\_user\_id for all operations.

API layer extracts auth from JWT; Service Layer forwards it.

Success Criteria (SMART):

SC-MCP-001: All MCP tool calls for user-facing operations have auth\_user\_id in ctx.request\_context.

SC-MCP-002: MCP tools reject any operation without valid auth\_user\_id.

SC-MCP-003: 100% of task operations remain isolated by user\_id.

Edge Cases:

Background jobs or system calls must not use MCP tools requiring user auth.

Attempted calls with invalid/missing auth\_user\_id should log and return an error.

Non-Goals: Do not change API endpoints, data models, or task operations themselves; this is purely authentication propagation enforcement.

## Response snapshot

Perfect! I have successfully updated the 004-agentic-foundation specification to address the authentication context propagation issue. Here's what was added:

1. **Functional Requirements** (FR-015, FR-016, FR-017) were added to explicitly require:
   - Propagation of authenticated user context from API to service to MCP tools
   - Explicit passing of auth_user_id from service to MCP tools
   - Validation that MCP tools reject operations without valid auth_user_id

2. **Authentication Context Propagation Contract** section was added defining the responsibilities of each layer:
   - API Layer: Extract auth from JWT
   - Service Layer: Pass auth_user_id to MCP tools
   - MCP Server: Validate proper authentication context
   - MCP Tools: Verify user permissions using auth_user_id

3. **Success Criteria** (SC-MCP-001, SC-MCP-002, SC-MCP-003) were added to measure:
   - MCP tool calls have auth_user_id in context
   - MCP tools reject operations without valid auth
   - 100% user data isolation

4. **User Story 1** was enhanced with additional acceptance scenarios for authentication validation

5. **Edge Cases** section was updated to include specific questions about auth_user_id handling

The specification now clearly defines the contract for authentication propagation from the API layer through the service layer to MCP tools, addressing the issue systematically before implementation. This satisfies the requirement to treat this as a spec clarification first before updating tasks and implementation.

## Outcome

- ✅ Impact: Updated specification with clear authentication context propagation requirements
- 🧪 Tests: No tests affected
- 📁 Files: specs/004-agentic-foundation/spec.md updated with new requirements and contract
- 🔁 Next prompts: /sp.tasks to update tasks based on new specification
- 🧠 Reflection: Systematic approach to fixing authentication issue by clarifying spec first before implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update tasks.md to reflect new requirements