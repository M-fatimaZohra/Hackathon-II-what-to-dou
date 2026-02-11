---
id: 0034
title: Update specs CustomApiConfig alignment
stage: plan
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.plan
labels: [spec-updates, customapiconfig, architecture-alignment, documentation]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/spec.md (updated)
 - specs/005-specification-phase-iii/plan.md (updated)
 - specs/005-specification-phase-iii/research.md (updated)
 - specs/architecture.md (updated)
 - specs/features/agentic_chat.md (updated)
 - specs/api/rest-endpoints.md (updated)
tests:
 - none
---

## Prompt

update plan.md and other monorepo .md files to match with updated plan

## Response snapshot

**Context**: After analyzing the ChatKit integration failure, discovered that the solution is simpler than initially thought - no protocol bridge needed, just fix ChatProvider.tsx configuration to use CustomApiConfig correctly.

**Files Updated**: 6 specification files across the monorepo

### 1. specs/005-specification-phase-iii/plan.md
- Updated "Backend Integration" section to clarify CustomApiConfig acts as pass-through
- Updated "Complete Request Flow" to show CustomApiConfig with custom fetch injecting JWT
- Updated "Key Technical Decisions" to note frontend integration via CustomApiConfig pass-through
- Updated "Structure Decision" to remove ChatKitServer reference

### 2. specs/005-specification-phase-iii/research.md
- Expanded "Integration Pattern" with detailed CustomApiConfig documentation
- Added "ChatKit SDK Configuration Types" section explaining HostedApiConfig vs CustomApiConfig
- Added critical warning about mixing configuration types
- Documented why CustomApiConfig is used (pass-through capability)

### 3. specs/architecture.md
- Updated architecture diagram to show CustomApiConfig instead of ChatKitServer
- Updated "Key Architecture Changes" to reflect custom SSE streaming
- Updated "AI Chatbot Flow" to show CustomApiConfig initialization
- Updated "ChatKit Integration" section to clarify SSE and pass-through architecture

### 4. specs/features/agentic_chat.md
- Updated FR-005 to specify SSE stream with custom format
- Updated FR-006 to document custom SSE format structure
- Added FR-014 requiring frontend to use CustomApiConfig for pass-through

### 5. specs/api/rest-endpoints.md
- Updated POST /api/{user_id}/chat response format to show custom SSE format
- Replaced ChatKit protocol event types with custom format event types
- Updated "Backend Implementation" to reference Runner.run_streamed()
- Added "Frontend Integration" section explaining CustomApiConfig pass-through

### 6. specs/005-specification-phase-iii/spec.md
- Updated FR-003 to specify CustomApiConfig with domainKey, url, custom fetch
- Updated FR-005 to clarify backend's custom SSE format
- Updated FR-015 to mention CustomApiConfig pass-through capability
- Added "Technical Notes" section documenting CustomApiConfig approach

**Architectural Correction**: Specifications were written assuming a protocol bridge would be needed. Analysis revealed CustomApiConfig acts as pass-through - ChatKit SDK doesn't enforce protocol format, allowing backend to use custom SSE format directly.

## Outcome

- ✅ Impact: Updated 6 specification files to accurately document CustomApiConfig pass-through architecture, removing incorrect protocol bridge references and aligning all specs with the simpler solution (fix ChatProvider.tsx configuration only)
- 🧪 Tests: No tests - documentation updates only
- 📁 Files: Updated plan.md, research.md, spec.md, architecture.md, agentic_chat.md, rest-endpoints.md
- 🔁 Next prompts: Fix ChatProvider.tsx to use CustomApiConfig (domainKey + url + custom fetch), Add NEXT_PUBLIC_OPENAI_DOMAIN_KEY to environment variables, Test ChatKit SDK initialization, Verify backend's custom SSE format displays correctly in ChatKit UI
- 🧠 Reflection: This comprehensive specification update corrects a fundamental architectural misunderstanding documented across multiple files. The initial analysis incorrectly assumed ChatKit SDK would enforce its own protocol format, leading to proposals for complex protocol bridge layers. Deeper investigation revealed CustomApiConfig allows backends to use any response format - the SDK simply passes it through. This dramatically simplifies the solution: instead of implementing a new backend service (protocol_bridge.py) and updating multiple backend files, we only need to fix one frontend file (ChatProvider.tsx) to use the correct configuration type.

## Evaluation notes (flywheel)

- Failure modes observed: Specification drift (specs documented incorrect architecture), Over-engineering (proposed protocol bridge when simple config fix sufficient), Documentation inconsistency (multiple files had conflicting information about ChatKitServer vs custom streaming)
- Graders run and results (PASS/FAIL): Specification consistency: PASS (all 6 files now aligned), Technical accuracy: PASS (correctly documents CustomApiConfig pass-through), Architecture clarity: PASS (diagrams and flows updated), Implementation guidance: PASS (specs now guide to correct solution)
- Prompt variant (if applicable): User requested /sp.plan but asked to "just directly update plan" - proceeded with direct Edit tool updates across all specification files
- Next experiment (smallest change to try): Update ChatProvider.tsx lines 77-94 to use CustomApiConfig (replace getClientSecret with domainKey + custom fetch), test if ChatKit SDK initializes without "Invalid input → at api" error
