---
id: 0007
title: Create dev-prod-toggle-config skill
stage: misc
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: A.ZEE COMPUTERS
command: user-request
labels: [skill-creation, dev-prod-toggle, environment-config, frontend-setup]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/dev-prod-toggle-config/Skill.md
tests:
 -
---

## Prompt

i want you to create skill in @.claude/skills/
file extention should be .md and file must be written in yaml style

Skill.md (add below data in SKILL.md)
---
name: dev-prod-toggle-config
description: Configures the dynamic environment toggle (developer vs production) for the frontend. Use this when setting up or modifying lib/config.ts to handle environment-specific logic like secure cookies and base URLs.
---

# Dev-Prod Toggle Config Skill

This skill creates a centralized `config.ts` that dynamically adjusts application settings based on the `NEXT_PUBLIC_MOD` environment variable.

## File Generation
Create or update `frontend/src/lib/config.ts` with the following structure:

```typescript
const MOD = process.env.NEXT_PUBLIC_MOD || 'production';
export const IS_DEV = MOD === 'developer';

export const CONFIG = {
  API_BASE_URL: IS_DEV ? 'http://localhost:8000' : process.env.NEXT_PUBLIC_API_URL,
  AUTH_BASE_URL: IS_DEV ? 'http://localhost:3000' : process.env.NEXT_PUBLIC_BASE_URL,
  COOKIE_SECURE: !IS_DEV,
  HTTP_ONLY_TOKEN: !IS_DEV,
  REFRESH_CACHE: !IS_DEV,
};

Usage Rules
NEVER hardcode true or false for security settings in auth.ts.

ALWAYS use CONFIG.COOKIE_SECURE for cookie attributes.

Use IS_DEV for conditional logging or debug overlays in the UI.

## Response snapshot

Successfully created dev-prod-toggle-config skill in `.claude/skills/` directory.

**Skill Structure:**
- Created directory: `.claude/skills/dev-prod-toggle-config/`
- Created file: `Skill.md` with YAML frontmatter

**Skill Content:**
- Name: dev-prod-toggle-config
- Description: Configures dynamic environment toggle (developer vs production) for frontend
- Purpose: Centralized config.ts for environment-specific logic (secure cookies, base URLs)
- File Generation: TypeScript config structure using NEXT_PUBLIC_MOD environment variable
- Usage Rules: Security best practices for cookie settings and environment detection

**Key Features:**
- YAML-style frontmatter with name and description
- TypeScript code template for `frontend/src/lib/config.ts`
- Environment detection using `NEXT_PUBLIC_MOD` variable
- Security-focused configuration (COOKIE_SECURE, HTTP_ONLY_TOKEN, REFRESH_CACHE)
- Clear usage rules to prevent hardcoded security settings

**Integration:**
- Skill is now available in Claude Code's skill system
- Can be invoked when setting up or modifying environment configuration
- Aligns with Phase 2 (Foundational) tasks in tasks.md (T004-T009)

## Outcome

- ✅ Impact: Created reusable skill for environment toggle configuration, enabling consistent dev/prod setup across frontend implementation
- 🧪 Tests: No tests required - skill is documentation/template only
- 📁 Files: Created .claude/skills/dev-prod-toggle-config/Skill.md
- 🔁 Next prompts: Ready to use skill during Phase 2 (Foundational) implementation, particularly for T004-T009 tasks
- 🧠 Reflection: Skill provides clear template and security guidelines for environment configuration, reducing risk of hardcoded security settings and ensuring consistent environment detection

## Evaluation notes (flywheel)

- Failure modes observed: None - skill creation followed standard structure and user requirements
- Graders run and results (PASS/FAIL): Skill format validation: PASS (YAML frontmatter + markdown content), Content completeness: PASS (includes file generation template and usage rules), Security guidelines: PASS (emphasizes CONFIG.COOKIE_SECURE usage)
- Prompt variant (if applicable): Direct skill creation request with specific YAML structure and content
- Next experiment (smallest change to try): Use this skill during T004-T009 implementation to validate template effectiveness and identify any missing configuration options
