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