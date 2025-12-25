# Todo CLI Application Quickstart Guide

**Feature**: Todo CLI Application (Phase I)
**Date**: 2025-12-25
**Related Plan**: [plan.md](plan.md)

## Overview

Interactive in-memory CLI Todo application implementing the five core features: Add, Delete, Update, View, and Mark Complete. The application displays a menu interface with options 1-6 and runs in a continuous loop, maintaining tasks in memory until the user selects exit. The application stores tasks in memory only (data lost on session end) and runs in a UV Python environment.

## Development Environment Setup

### Prerequisites
- Python 3.13 or higher
- UV package manager

### Project Initialization
```bash
# Initialize UV environment in src directory
uv init src
cd src

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Project Structure

```
src/
├── main.py              # Single file application with interactive menu interface
└── uv.lock              # UV environment file
```

## Running the Application

### Direct Execution
```bash
python src/main.py
```

### Interactive Menu Options
- `1`: Add a new task
  - Prompts for: task title, optional description
- `2`: Update task
  - Prompts for: task ID, new title (optional), new description (optional)
- `3`: Delete task
  - Prompts for: task ID to remove
- `4`: View all tasks
  - Displays all tasks with ID, title, description, and completion status
- `5`: Toggle task completion
  - Prompts for: task ID to change status
- `6`: Exit
  - Terminates the application loop

## Implementation Details

### Data Model
- Task stored as Python dictionary with id, title, description, and completed status
- Tasks stored in-memory using a dictionary with task ID as key
- Simple integer-based ID generation

### CLI Interface
- Interactive menu-based interface with continuous loop
- Single file implementation for simplicity
- All functionality contained in main.py