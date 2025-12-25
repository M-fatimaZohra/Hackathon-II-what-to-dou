# Todo CLI Application

A simple interactive in-memory CLI Todo application that allows users to manage tasks through a menu-driven interface.

## Features

- Add new tasks with title and optional description
- View all tasks with their completion status
- Update existing tasks' title and/or description
- Delete tasks by ID
- Toggle task completion status
- All data is stored in-memory (lost on session end)

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

1. Install UV package manager if not already installed
2. Navigate to the project directory
3. Initialize the UV environment:
   ```bash
   cd src
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Usage

Run the application using:
```bash
uv run main.py
```

The application will present an interactive menu with the following options:

1. **Add task** - Create a new task with a title and optional description
2. **Update task** - Modify an existing task's title and/or description
3. **Delete task** - Remove a task by its ID
4. **View all tasks** - Display all tasks with their details and completion status
5. **Toggle task as complete** - Change a task's completion status
6. **Exit** - Quit the application

## How to Use

1. Run the application
2. Select an option from the menu by entering the corresponding number
3. Follow the prompts to provide required information
4. The application will process your request and return to the main menu
5. Select option 6 to exit the application

## Data Storage

All tasks are stored in memory only and will be lost when the application exits. This is an in-memory application by design.