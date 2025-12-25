# How to Use the what-to-dou App

## Introduction

The what-to-dou app is a command-line interface (CLI) application designed for efficient task management. This application allows you to create, manage, and track your tasks directly from the terminal with a simple, menu-driven interface.

## Getting Started

### Prerequisites
- Python 3.13 or higher
- UV package manager

### Installation and Setup
1. Navigate to the project directory
2. Initialize the UV environment:
   ```bash
   cd src
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Running the Application
Execute the application using:
```bash
uv run main.py
```

## Application Features

### 1. Add Task
- Creates a new task with a required title and optional description
- Automatically assigns a unique ID to each task
- Provides immediate confirmation after successful creation

### 2. Update Task
- Modify existing task titles and/or descriptions
- Keep current values by pressing Enter without typing
- Validates task existence before making changes

### 3. Delete Task
- Remove tasks by their unique IDs
- Provides confirmation before deletion
- Validates task existence before removal

### 4. View All Tasks
- Displays all tasks in a tabular format
- Shows ID, title, description, and completion status
- Clear formatting for easy scanning of information

### 5. Toggle Task Completion
- Change task status between complete/incomplete
- Instant status update with confirmation
- Simple one-step process for status changes

## Best Practices

### For Optimal Use
- Use descriptive titles that clearly indicate the task purpose
- Add relevant details in the description field when needed
- Keep track of task IDs for efficient management
- Regularly review all tasks to maintain organization
- Exit the application properly using option 6

### Tips for Efficiency
- Add tasks immediately when they come to mind
- Use the description field for context, deadlines, or additional details
- Review tasks frequently to stay on track
- Use the toggle feature to mark completed tasks
- Organize tasks by priority mentally since there's no formal priority system yet

## Understanding the Interface

The application follows a consistent menu-driven approach:
1. Main menu displays all available options
2. Prompts guide you through each operation
3. Confirmation messages indicate successful operations
4. Error messages provide guidance when issues occur
5. "Press Enter to continue" allows you to review results

## Limitations to Consider

- All data is stored in memory and will be lost when the application exits
- No persistent storage in this version
- No search or filtering capabilities in the current version
- No due dates or priority levels implemented yet

## Troubleshooting

Common issues and solutions:
- Invalid choice error: Ensure you enter numbers 1-6 for menu options
- Task not found: Verify the task ID is correct and the task exists
- Empty title error: Remember that titles are required when adding tasks
- Unexpected exit: Use option 6 to exit properly rather than closing the terminal

## Next Steps

This CLI version serves as the foundation for future enhancements. The upcoming UI version will include persistent storage, advanced search capabilities, due dates, priority levels, and collaborative features.