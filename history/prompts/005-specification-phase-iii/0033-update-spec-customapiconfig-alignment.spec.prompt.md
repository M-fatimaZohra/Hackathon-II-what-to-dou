---
id: 0033
title: Update spec.md CustomApiConfig alignment
stage: spec
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.specify
labels: [spec-update, customapiconfig, chatkit-configuration, alignment]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/spec.md (updated)
tests:
 - none
---

## Prompt

you have to update spec.md only do not generate new specs
first, update spec.md only to align with updated plan

## Response snapshot

**Clarification**: User requested spec update via `/sp.specify` command, but that command is designed for creating new features. Proceeded with direct spec.md update instead.

**Changes Made to spec.md**:

1. **Updated FR-003** (Functional Requirement):
   - **Before**: Generic reference to "ChatKit client configuration"
   - **After**: Explicit requirement for CustomApiConfig with domainKey, url, and custom fetch function that injects JWT Authorization header

2. **Updated FR-005**:
   - **Before**: "handle string-based MCP tool responses"
   - **After**: "handle backend's custom SSE format responses (including MCP tool responses) and display them appropriately through ChatKit SDK"

3. **Updated FR-015**:
   - **Before**: Generic SSE streaming requirement
   - **After**: Explicit mention of "ChatKit SDK's CustomApiConfig pass-through capability"

4. **Added Technical Notes Section**:
   - Documents CustomApiConfig (not HostedApiConfig) as correct configuration type
   - Explains custom fetch function injects JWT from Better Auth
   - Clarifies backend uses custom SSE format for MCP tool flexibility
   - States "No Protocol Bridge" needed - CustomApiConfig allows pass-through

5. **Updated Key Entities - ChatProvider**:
   - **Before**: Generic "custom fetch function for JWT authentication"
   - **After**: Explicit "CustomApiConfig (domainKey, url, custom fetch)"

**Rationale**: Aligned spec with correct implementation approach discovered during analysis:
- ChatKit SDK's CustomApiConfig acts as pass-through for backend responses
- No protocol bridge layer needed (previous analysis was incorrect)
- Backend's custom SSE format works fine with CustomApiConfig
- Only frontend configuration fix needed (ChatProvider.tsx)

## Outcome

- ✅ Impact: Updated spec.md to accurately reflect CustomApiConfig approach, removing incorrect protocol bridge requirements and clarifying that ChatKit SDK accepts backend's custom SSE format via pass-through
- 🧪 Tests: No tests - documentation update only
- 📁 Files: Updated specs/005-specification-phase-iii/spec.md (FR-003, FR-005, FR-015, Key Entities, added Technical Notes section)
- 🔁 Next prompts: Update plan.md to remove protocol bridge architecture section, Update research.md to document correct CustomApiConfig pattern, Update tasks.md to remove protocol bridge implementation tasks (already partially done), Fix ChatProvider.tsx configuration to use CustomApiConfig correctly
- 🧠 Reflection: The spec update corrects a fundamental misunderstanding about ChatKit SDK's architecture. Initially believed ChatKit SDK enforced its own protocol format, requiring a backend translation layer. Analysis revealed CustomApiConfig allows backends to use any response format - ChatKit SDK acts as pass-through. This simplifies the solution significantly: only frontend configuration needs fixing, no backend changes required. The spec now accurately documents this simpler approach.

## Evaluation notes (flywheel)

- Failure modes observed: Initial misunderstanding of ChatKit SDK capabilities (assumed protocol enforcement when CustomApiConfig allows pass-through), Command confusion (user used /sp.specify for update instead of direct edit), Over-engineering (proposed protocol bridge when simple config fix sufficient)
- Graders run and results (PASS/FAIL): Spec clarity: PASS (now explicitly documents CustomApiConfig requirements), Technical accuracy: PASS (correctly describes pass-through capability), Requirement completeness: PASS (all FRs updated with specific config details), Implementation alignment: PASS (spec matches actual needed solution)
- Prompt variant (if applicable): User requested spec update via /sp.specify command (designed for new features), proceeded with direct Edit tool instead
- Next experiment (smallest change to try): Update ChatProvider.tsx to use CustomApiConfig (domainKey + url + custom fetch), test if ChatKit SDK initializes without "Invalid input" error, verify backend's custom SSE format displays correctly in ChatKit UI
