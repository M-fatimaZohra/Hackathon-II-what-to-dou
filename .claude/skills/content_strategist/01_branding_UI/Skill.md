# Skill Name

branding_ui

---

## Skill Purpose

Define and manage the visual identity of the application, including brand name, color palette, font themes, and overall styling, based on user prompts and specifications.

---

## Skill Tasks

* Interpret branding-related prompts and specs
* Select or refine color palettes
* Choose font families and typography rules
* Define a consistent brand name and visual tone
* Provide styling guidance for UI implementation

---

## How the Skill Performs Its Tasks

* Reads branding requirements from user prompts and `/specs/*` (if available)
* Translates abstract branding ideas into concrete UI tokens
* Outputs brand decisions in a clear, reusable format
* Keeps branding consistent across phases and features

Branding output may include:

* Primary / secondary colors
* Font families and usage rules
* Spacing or visual tone notes
* Brand name and short description

---

## Required Inputs

* Brand name or naming preferences (optional)
* Color preferences or mood (e.g. minimal, bold, soft)
* Font preferences (optional)
* Relevant specs or UI constraints

Example:

```
Brand name: TodoFlow
Style: minimal, calm
Primary color: blue
Font: modern sans-serif
```

---

## Expected Output

* Clear branding definition (colors, fonts, name)
* UI styling guidance usable by UI agents
* Consistent visual identity across the app

Focus: simplicity, consistency, and reusability.