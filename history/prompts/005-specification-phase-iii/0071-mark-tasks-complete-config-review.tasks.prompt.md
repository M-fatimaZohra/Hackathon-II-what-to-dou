---
id: 0071
title: mark-tasks-complete-config-review
stage: tasks
date: 2026-02-11
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: ["tasks", "config-review", "production", "validation"]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-specification-phase-iii/tasks.md
  - frontend/src/lib/config.ts
tests:
  - Verify 68 tasks marked [X] in tasks.md
  - Verify 21 remaining tasks are all Phase 5 (testing)
  - Verify config.ts throws on missing NEXT_PUBLIC_API_URL in production
  - Verify config.ts throws on missing NEXT_PUBLIC_BASE_URL in production
  - Verify config.ts still works in developer mode without production env vars
---

## Prompt

mark tasks in tasks.md as complete
and check if @frontend/src/lib/config.ts dev production switch is perfect for production mode

## Response snapshot

### Task Completion (tasks.md)

**Before:** 46 completed, 43 incomplete
**After:** 68 completed, 21 incomplete

Phases marked complete:
- Phase 1 (T001-T006): All 6 tasks marked [X] — config.ts, ChatKit SDK, env vars, api.ts, auth-client.ts
- Phase 4.5 (T050-T068): All 19 tasks marked [X] — CustomApiConfig fix, threads.list interception, backend metadata

Remaining 21 tasks are all **Phase 5 (Real-time Validation)** — manual QA tests for TTFT, MCP tool rendering, error handling, and E2E integration.

### Config.ts Production Review

**3 findings:**

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | `process.env.NEXT_PUBLIC_API_URL!` non-null assertion — `undefined` at runtime if env var missing | Added `throw new Error()` validation |
| 2 | CRITICAL | `process.env.NEXT_PUBLIC_BASE_URL!` same issue | Added `throw new Error()` validation |
| 3 | OK | Default to `'production'` when `NEXT_PUBLIC_MOD` not set | Correct (fail-closed security) |

**Fix applied:** Replaced weak `console.warn` (only warned about `NEXT_PUBLIC_MOD`) with strict `throw new Error()` that validates both `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_BASE_URL` are set when in production mode. App now fails fast at build/startup time instead of silently breaking at runtime.

## Outcome

- ✅ Impact: Tasks accurately reflect implementation state; config.ts now fails fast on missing production env vars instead of silently serving `undefined` URLs
- 🧪 Tests: Pending — verify dev mode still works, verify production build catches missing vars
- 📁 Files: tasks.md (mark 22 tasks complete), config.ts (production validation fix)
- 🔁 Next prompts: Complete Phase 5 QA testing tasks
- 🧠 Reflection: Non-null assertions (`!`) should always be backed by runtime validation in configuration files. TypeScript's `!` only silences the compiler — it doesn't protect against missing env vars at runtime.

## Evaluation notes (flywheel)

- Failure modes observed: Non-null assertion on env vars is a common pattern that creates silent production failures
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
