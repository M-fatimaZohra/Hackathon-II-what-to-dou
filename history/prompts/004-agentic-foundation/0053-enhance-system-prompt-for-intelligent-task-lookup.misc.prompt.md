---
id: 0053
title: Enhance system prompt for intelligent task lookup
stage: misc
date: 2026-02-07
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: M-fatimaZohra
command: /sp.implement
labels: ["system-prompt", "enhancement", "agent"]
links:
  spec: specs/features/agentic_chat.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/configs/gemini_config.py
tests:
 - (no tests run)
---

## Prompt

Plan for Enhancing the System Prompt

Based on the issue identified, here's my approach to enhancing the system prompt to enable intelligent task lookup by name:

1. System Prompt Enhancement Strategy

Modify the SYSTEM_PROMPT in src/configs/gemini_config.py to include a multi-step workflow for name-based operations:

Current flow: User says "Update task X" → Agent tries to call update with name → Fails due to missing ID

Enhanced flow: User says "Update task X" → Agent automatically calls list_tasks → Finds matching task by name → Calls update_task with correct ID → Responds naturally to user

2. Implementation Steps

1. Update the SYSTEM_PROMPT to include:
   - Priority rule: When user refers to a task by name/title, always call list_tasks first to get available task IDs
   - Matching logic: Use fuzzy matching to find the task that best matches the user's description
   - Workflow guidance: "If user wants to update/delete/complete a task by name, first list tasks and find the matching one before calling the specific operation"

2. Add Tool Chain Instructions:
   - When user mentions a task without an ID, instruct the agent to chain list_tasks → specific operation
   - Include examples in the prompt showing this workflow pattern

3. Preserve Security Model:
   - Continue using ID-based operations for security (no changes to the MCP tools themselves)
   - Only enhance the agent's approach to finding IDs internally
   - Maintain user data isolation (users can only see their own tasks)

3. Enhanced Prompt Pattern

The system prompt will include instructions like:

"When a user refers to a task by name (e.g., 'update the grocery task'), always call 'list_tasks' first to retrieve the user's tasks and their IDs. Then identify which task matches the user's description and call the appropriate operation with the correct task ID. Never ask the user for task IDs directly - handle the lookup internally."

This approach solves the UX concern by hiding the ID complexity while maintaining the secure, ID-based backend operations.

## Response snapshot

Implementation completed successfully. The SYSTEM_PROMPT in gemini_config.py has been enhanced with:

1. Clear tool descriptions with parameter requirements
2. Critical workflow section explaining the automatic lookup process
3. Three concrete example scenarios (update, delete, complete)
4. Security rules emphasizing internal ID handling
5. Explicit exception for when users provide numeric IDs

The agent will now automatically lookup tasks by name instead of asking users for IDs, improving UX while maintaining security.

## Outcome

- ✅ Impact: Users can now refer to tasks by name naturally without needing to know IDs. The agent automatically performs lookup, improving usability while maintaining secure ID-based operations.
- 🧪 Tests: No tests run - manual testing recommended: try "update the grocery task" and verify agent calls list_tasks then update with correct ID
- 📁 Files: 1 file modified: backend/src/configs/gemini_config.py
- 🔁 Next prompts: Test the new behavior; may need to refine fuzzy matching instructions if agent struggles with similar task names
- 🧠 Reflection: This is a pure prompt engineering enhancement - no code changes to MCP tools needed. The lookup workflow is now explicit and should handle most cases.

## Evaluation notes (flywheel)

- Failure modes observed: Agent might still struggle with ambiguous task names (multiple matches); may need additional guidance on selecting best match or listing options
- Graders run and results (PASS/FAIL): N/A - no automated tests
- Prompt variant (if applicable): baseline
- Next experiment (smallest change to try): Consider adding instruction for handling multiple matches (e.g., "if multiple tasks match, ask user to clarify")
