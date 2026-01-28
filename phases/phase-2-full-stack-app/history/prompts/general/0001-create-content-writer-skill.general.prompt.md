---
id: 0001
title: Create content writer skill
stage: general
date: 2025-12-24
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: A.ZEE
command: manual skill creation
labels: ["skill", "documentation", "content-writer", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/content_strategist/00_content_writer/Skill.md
tests:
  - none
---

## Prompt

Create skill and save it in @.claude/skills/content_strategist/00_content_writer/Skill.md

# Skill Name

content_writer

---

## Skill Purpose

Create, update, and maintain clear, version-aware documentation for the application based on specifications, workflow, code, and user instructions.

---

## Skill Tasks

* Analyze specs, code, and user prompts
* Write and update Markdown documentation
* Maintain versioned documentation history
* Update root `README.md` when needed

---

## How the Skill Performs Its Tasks

* Reads `/specs/*`, codebase, and version context
* Identifies what changed (phase, feature, fix)
* Updates documentation using a fixed structure
* Never deletes old version documentation

Documentation structure:

```
/.docs
  /how_to_use_application
    introduction.md
    [tutorial].md

  /features_of_app
    [feature].md

  /version_[version]
    phase_[n]_birth_of_application.md
    phase_[n]_version_[x]_updates.md
    error_fixed_version_[x]_updates.md
```

---

## Required Inputs

* Specs and/or code context
* Current phase and version
* User instruction describing updates

Example:

```
Phase 1 is complete and search bug is fixed. Update docs.
```

---

## Expected Output

* Clean, organized Markdown files inside `/.docs`
* Append-only version history
* Optional updated `README.md`

Focus: clarity, traceability, and long-term maintainability.

## Response snapshot

Successfully created the content_writer skill at `.claude/skills/content_strategist/00_content_writer/Skill.md`. This skill aligns with the Hackathon II Constitution's requirements for documentation, maintaining version-aware documentation as required, focusing on clarity and long-term maintainability, and supporting the iterative & phased evolution approach. The skill is structured to analyze specifications, code, and user prompts, create and maintain Markdown documentation, follow the exact directory structure specified, and update the README when needed with an append-only version history.

## Outcome

- ✅ Impact: Created documentation skill to maintain traceability as required by Hackathon II Constitution
- 🧪 Tests: none required
- 📁 Files: .claude/skills/content_strategist/00_content_writer/Skill.md created
- 🔁 Next prompts: Create additional skills for Hackathon II project phases
- 🧠 Reflection: This skill will be essential for maintaining documentation throughout all phases of the Hackathon II project, ensuring that documentation stays updated whenever features are added or changed, as required by the constitution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement additional skills for Phase 1 CLI application
