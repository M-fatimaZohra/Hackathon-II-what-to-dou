---
id: 6
title: Fix Config YAML Structure
stage: plan
date_iso: 2025-12-28
surface: agent
model: claude-haiku-4-5-20251001
feature: todo-web-app
branch: 002-todo-web-app
user: user
command: /sp.plan
labels: ["planning", "todo-app", "monorepo", "spec-kit", "correction"]
links:
  spec: "specs/002-todo-web-app/spec.md"
  plan: "specs/002-todo-web-app/plan.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".spec-kit/config.yaml"
  - "specs/002-todo-web-app/plan.md"
tests_yaml: []
---

## Summary

Corrected the YAML structure in .spec-kit/config.yaml to fix the indentation error where 'phases' was incorrectly nested under 'structure'.

## Prompt Text

```
/sp.plan

there is mistake in structure of config.ymal
name: 00-ai-native-todo-app
version: "1.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
  phases:                     < ------- this should not be indent like this
    - name: phase1-console
      features: [todo_crud]
    - name: phase2-web
      features: [todo_crud, authentication]

because phases and structure are two different things

name: 00-ai-native-todo-app
version: "1.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
phases: < ------ now is correct
  - name: phase1-console
     features: [todo_crud]
  - name: phase2-web
     features: [todo_crud, authentication]
```

## Response Text

Corrected the YAML structure in .spec-kit/config.yaml. The file now has the proper structure where 'phases' is at the same indentation level as 'structure', not nested under it:

```yaml
name: 00-ai-native-todo-app
version: "1.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
phases:
  - name: phase1-console
    features: [todo_crud]
  - name: phase2-web
    features: [todo_crud, authentication]
```

Also updated the plan.md file to reflect the corrected configuration.

## Outcome

The .spec-kit/config.yaml file now has the correct YAML structure with proper indentation.

## Evaluation

The indentation error in the YAML configuration has been fixed. The 'phases' section is now properly positioned at the same level as 'structure' rather than being nested under it, which is the correct YAML syntax for separate top-level sections.