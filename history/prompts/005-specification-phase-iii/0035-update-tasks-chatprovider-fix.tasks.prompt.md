---
id: 0035
title: Update tasks ChatProvider fix
stage: tasks
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.tasks
labels: [tasks-update, chatprovider-fix, customapiconfig, critical-tasks]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/tasks.md (updated)
tests:
 - none
---

## Prompt

/sp.tasks
update tasks based on new plan

## Response snapshot

**Context**: After updating all specifications to document the correct CustomApiConfig approach, needed to update tasks.md to reflect the simplified implementation strategy.

**User Request**: "just update task in task.md related to ChatProvider.tsx updates and NEXT_PUBLIC_OPENAI_DOMAIN_KEY"

**Action Taken**: Added Phase 4.5 to tasks.md with focused tasks for fixing ChatProvider configuration

**New Phase Added**: Phase 4.5: Fix ChatProvider Configuration (CRITICAL)

**Tasks Added** (13 new tasks: T050-T062):

### Environment Variable Setup (2 tasks)
- T050: Add NEXT_PUBLIC_OPENAI_DOMAIN_KEY='localhost-dev' to frontend/.env.local
- T051: Verify environment variable is accessible in config.ts

### ChatProvider.tsx Configuration Fix (7 tasks)
- T052: Fix ChatProvider.tsx lines 77-94 to use CustomApiConfig
- T053: Remove getClientSecret (incompatible with CustomApiConfig)
- T054: Add domainKey property
- T055: Add url property
- T056: Implement custom fetch function for JWT injection
- T057: Ensure fetch uses tokenRef.current (avoid closure issues)
- T058: Verify fetch returns merged headers with Authorization

### Validation (4 tasks)
- T059: Test initialization - verify no "Invalid input" error
- T060: Open sidebar - verify ChatKit UI renders
- T061: Send test message - verify it works
- T062: Check Network tab - verify Authorization header present

**Rationale**: These tasks provide a clear, step-by-step implementation guide for the critical fix. Each task is specific and actionable, focusing on the root cause of the integration failure.

## Outcome

- ✅ Impact: Added Phase 4.5 with 13 targeted tasks to fix ChatProvider.tsx configuration and resolve "Invalid input → at api" error - provides clear implementation roadmap for the critical fix
- 🧪 Tests: No automated tests - validation tasks included (T059-T062)
- 📁 Files: Updated specs/005-specification-phase-iii/tasks.md (added Phase 4.5 between Phase 4 and Phase 5)
- 🔁 Next prompts: Execute T050-T058 to fix ChatProvider.tsx configuration, Run T059-T062 to validate the fix works, Test end-to-end chat integration with MCP tools
- 🧠 Reflection: The tasks.md update provides a focused implementation plan for the critical fix. By adding Phase 4.5 specifically for the ChatProvider configuration fix, we've made it clear that this is the blocking issue that needs immediate attention. The 13 tasks break down the fix into small, verifiable steps: (1) environment setup, (2) configuration changes, (3) validation. This approach ensures the fix can be implemented methodically and validated at each step. The tasks are ordered logically and include specific file paths and line numbers, making them immediately actionable.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempt to regenerate entire tasks.md (user rejected - wanted targeted update only), Template-based generation (user wanted minimal changes to existing file)
- Graders run and results (PASS/FAIL): Task specificity: PASS (each task has clear action and file path), Task ordering: PASS (logical sequence from env setup to validation), Critical path identification: PASS (Phase 4.5 clearly marked as CRITICAL), Actionability: PASS (tasks can be executed immediately)
- Prompt variant (if applicable): User requested "/sp.tasks update tasks based on new plan" but then clarified to "just update task in task.md related to ChatProvider.tsx updates and NEXT_PUBLIC_OPENAI_DOMAIN_KEY" - proceeded with targeted update
- Next experiment (smallest change to try): Execute T050 (add environment variable) and T052-T058 (fix ChatProvider.tsx configuration), then run T059 to verify no "Invalid input" error
