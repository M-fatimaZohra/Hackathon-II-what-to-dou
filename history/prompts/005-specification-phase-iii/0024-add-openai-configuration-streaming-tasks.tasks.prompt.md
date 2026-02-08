---
id: 0024
title: Add OpenAI configuration and streaming tasks
stage: tasks
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.tasks
labels: [tasks-update, openai-configuration, runner-run-streamed, streaming-implementation, phase-4-refactor]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/tasks.md
tests:
 - none
---

## Prompt

/sp.tasks add tasks for backend openai configuration and streaming event setup

## Response snapshot

Successfully updated Phase 4 tasks in tasks.md to reflect OpenAI model configuration and Runner.run_streamed() streaming implementation approach.

**Phase 4 Reorganization:**

**OLD Structure (ChatKitServer abstraction):**
- Install openai-chatkit Python SDK
- Create ChatKitServer subclass
- Implement ChatKitServer methods
- Update endpoints to use ChatKitServer

**NEW Structure (Direct OpenAI Agents SDK):**
1. Backend Dependencies (T023-T024) - Verify SDKs installed
2. OpenAI Model Configuration (T025-T028) - NEW SECTION
3. Streaming Implementation with Runner.run_streamed() (T029-T035) - NEW SECTION
4. Session Endpoint Implementation (T036-T039) - Already completed
5. Streaming Endpoint Refactoring (T040-T045) - Partially completed
6. Authentication & User Isolation (T046-T049) - Already completed

**New Tasks Added:**

**OpenAI Model Configuration (T025-T028):**
- T025: Configure OPENAI_API_KEY environment variable
- T026: Create openai_config.py with model configuration
- T027: Create OPENAI_MODEL constant with gpt-4o
- T028: Add ModelSettings with temperature=0.7

**Streaming Implementation (T029-T035):**
- T029: Create run_agent_workflow_streamed() function
- T030: Implement Agent initialization with OpenAI model
- T031: Implement Runner.run_streamed() call
- T032: Implement ResponseTextDeltaEvent filtering
- T033: Implement tool event filtering (tool_start, tool_end)
- T034: Accumulate full_response from deltas
- T035: Save messages to database after streaming

**Session Endpoint (T036-T039):**
- Marked as [X] completed (implemented in PHR-0021)
- T036: Session endpoint created
- T037: client.beta.chatkit.sessions.create() implemented
- T038: SessionResponse with client_secret
- T039: JWT validation in session endpoint

**Streaming Endpoint (T040-T045):**
- T040: [X] StreamingResponse implemented
- T041: [X] stream_chat_response() generator created
- T042: [ ] Update to call run_agent_workflow_streamed() - PENDING
- T043: [ ] SSE event formatting - PENDING
- T044: [X] Content-Type header added
- T045: [X] Cache-Control headers added

**Authentication (T046-T049):**
- Marked as [X] completed (already implemented)
- All JWT validation tasks complete

**Task Status Summary:**

**Completed (13 tasks):**
- T023-T024: Dependencies verified
- T036-T039: Session endpoint complete
- T040-T041: Streaming response structure
- T044-T045: SSE headers
- T046-T049: Authentication complete

**Pending (11 tasks):**
- T025-T028: OpenAI configuration (NEW)
- T029-T035: Streaming implementation (NEW)
- T042-T043: Stream integration (UPDATED)

**Key Changes from Original Plan:**

1. **Removed ChatKitServer abstraction** (T025-T030 old)
   - No separate ChatKitServer class needed
   - Direct use of OpenAI Agents SDK primitives

2. **Added OpenAI-specific configuration** (T025-T028 new)
   - Environment variable setup
   - Model configuration file
   - Model constant and settings

3. **Added Runner.run_streamed() implementation** (T029-T035 new)
   - Streaming function creation
   - Event filtering logic
   - Database persistence after streaming

4. **Marked completed tasks** (T036-T039, T040-T041, T044-T049)
   - Session endpoint (PHR-0021)
   - Streaming response structure (PHR-0021)
   - Authentication (already implemented)

**Alignment with Documentation:**

Tasks now align with:
- ✅ PHR-0023: plan.md OpenAI model and streaming decisions
- ✅ PHR-0022: SKILL.md streaming documentation
- ✅ PHR-0021: Session and streaming endpoint implementation
- ✅ Context7 research on Runner.run_streamed()

**Implementation Path:**

```
Phase 4 Execution Order:
1. T025-T028: Configure OpenAI model (parallel possible)
2. T029-T035: Implement streaming function (sequential)
3. T042-T043: Integrate streaming with endpoint (sequential)
4. Test: Verify token-by-token streaming works
```

**Next Steps:**

1. Execute T025-T028: OpenAI configuration
2. Execute T029-T035: Streaming implementation
3. Execute T042-T043: Integration
4. Test streaming with frontend ChatKit SDK

## Outcome

- ✅ Impact: Updated Phase 4 tasks to reflect OpenAI model configuration and Runner.run_streamed() streaming approach, removing ChatKitServer abstraction and adding specific implementation tasks
- 🧪 Tests: No tests - task planning update
- 📁 Files: Updated tasks.md (Phase 4 reorganized with 11 new/updated tasks)
- 🔁 Next prompts: Execute T025-T028 to configure OpenAI model, then T029-T035 to implement streaming function, finally T042-T043 to integrate with endpoint
- 🧠 Reflection: Task breakdown should match actual implementation approach, not conceptual abstractions. Marking completed tasks ([X]) provides clear progress tracking and prevents duplicate work. Organizing tasks by technical component (configuration, streaming, integration) creates logical execution flow. Specific file paths and function names in task descriptions enable autonomous execution.

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward task reorganization based on plan.md updates
- Graders run and results (PASS/FAIL): Task structure: PASS (organized by component), Task specificity: PASS (file paths and function names included), Completion tracking: PASS (13 tasks marked complete, 11 pending), Alignment: PASS (matches plan.md and SKILL.md documentation), Checklist format: PASS (all tasks follow - [ ] TID format)
- Prompt variant (if applicable): /sp.tasks with request to add OpenAI configuration and streaming tasks
- Next experiment (smallest change to try): Execute T025 to add OPENAI_API_KEY to backend/.env, verify environment variable is accessible in Python code
