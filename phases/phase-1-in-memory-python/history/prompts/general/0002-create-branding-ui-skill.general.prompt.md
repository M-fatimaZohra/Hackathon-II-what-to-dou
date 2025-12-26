---
id: 0002
title: Create branding UI skill
stage: general
date: 2025-12-24
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: A.ZEE
command: manual skill creation
labels: ["skill", "branding", "ui", "design", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/content_strategist/01_branding_UI/Skill.md
tests:
  - none
---

## Prompt

create new small skill for branding and save it to  @.claude/skills/content\_strategist/01\_branding\_UI/Skill.md

\# Skill Name

branding\_ui

---

\## Skill Purpose

Define and manage the visual identity of the application, including brand name, color palette, font themes, and overall styling, based on user prompts and specifications.

---

\## Skill Tasks

\* Interpret branding-related prompts and specs
\* Select or refine color palettes
\* Choose font families and typography rules
\* Define a consistent brand name and visual tone
\* Provide styling guidance for UI implementation

---

\## How the Skill Performs Its Tasks

\* Reads branding requirements from user prompts and `/specs/\*` (if available)
\* Translates abstract branding ideas into concrete UI tokens
\* Outputs brand decisions in a clear, reusable format
\* Keeps branding consistent across phases and features

Branding output may include:

\* Primary / secondary colors
\* Font families and usage rules
\* Spacing or visual tone notes
\* Brand name and short description

---

\## Required Inputs

\* Brand name or naming preferences (optional)
\* Color preferences or mood (e.g. minimal, bold, soft)
\* Font preferences (optional)
\* Relevant specs or UI constraints

Example:

```
Brand name: TodoFlow
Style: minimal, calm
Primary color: blue
Font: modern sans-serif
```

---

\## Expected Output

\* Clear branding definition (colors, fonts, name)
\* UI styling guidance usable by UI agents
\* Consistent visual identity across the app

Focus: simplicity, consistency, and reusability.

## Response snapshot

Successfully created the branding_ui skill at `.claude/skills/content_strategist/01_branding_UI/Skill.md`. This skill will define and manage the visual identity of the application, including brand name, color palette, font themes, and overall styling. The skill is designed to interpret branding-related prompts, select appropriate color palettes and fonts, define consistent brand identity, and provide styling guidance for UI implementation. It follows the Hackathon II Constitution's principles of clarity, consistency, and reusability while maintaining visual identity across all phases of the project.

## Outcome

- ✅ Impact: Created branding skill to manage visual identity as required by Hackathon II project
- 🧪 Tests: none required
- 📁 Files: .claude/skills/content_strategist/01_branding_UI/Skill.md created
- 🔁 Next prompts: Create additional skills for Hackathon II project phases
- 🧠 Reflection: This skill will ensure consistent visual identity across all phases of the Hackathon II project, supporting the "Clarity Over Cleverness" principle from the constitution by providing clear, reusable branding definitions.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement additional skills for Phase 1 CLI application
