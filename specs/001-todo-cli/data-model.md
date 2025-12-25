# Todo CLI Application Data Model

**Feature**: Todo CLI Application (Phase I)
**Date**: 2025-12-24
**Related Plan**: [plan.md](plan.md)

## Core Data Structure

### Task Object

Simple Python dictionary structure representing a single todo item:

```python
task = {
    "id": str,           # Unique identifier
    "title": str,        # Required task title
    "description": str,  # Optional task description (default: "")
    "completed": bool    # Completion status (default: False)
}
```

### Task Storage

In-memory storage using Python dictionary:
- Key: task ID (string)
- Value: task object (dictionary)

Example:
```python
tasks = {
    "1": {"id": "1", "title": "Buy groceries", "description": "", "completed": False},
    "2": {"id": "2", "title": "Walk the dog", "description": "After dinner", "completed": True}
}
```

## Operations

### Add Task
- Generate unique ID (simple incrementing integer)
- Create task dictionary with provided title/description
- Set completed status to False
- Add to tasks dictionary

### List Tasks
- Iterate through tasks dictionary
- Display all task information (ID, title, description, completion status)

### Update Task
- Find task by ID in tasks dictionary
- Update title and/or description as specified
- Preserve other attributes

### Delete Task
- Remove task entry from tasks dictionary by ID

### Toggle Task
- Find task by ID in tasks dictionary
- Flip completion status (True ↔ False)