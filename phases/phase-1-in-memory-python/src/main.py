import sys

# Global in-memory storage for tasks
tasks = {}

# Counter for generating unique IDs
task_id_counter = 1

def generate_unique_id():
    """
    Generate a unique ID for a new task.

    Returns:
        str: A unique ID string
    """
    global task_id_counter
    unique_id = str(task_id_counter)
    task_id_counter += 1
    return unique_id

# Task data structure
def create_task(title, description="", completed=False):
    """
    Create a new task with the given parameters.

    Args:
        title (str): The task title (required)
        description (str): The task description (optional)
        completed (bool): The completion status (default: False)

    Returns:
        dict: A task dictionary with id, title, description, and completed status
    """
    return {
        "id": generate_unique_id(),
        "title": title,
        "description": description,
        "completed": completed
    }


def add_task(title, description=""):
    """
    Add a new task to the in-memory storage.

    Args:
        title (str): The task title (required)
        description (str): The task description (optional)

    Returns:
        dict: The created task

    Raises:
        ValueError: If title is empty or None
    """
    if not title or title.strip() == "":
        raise ValueError("Task title is required")

    task = create_task(title, description, completed=False)
    tasks[task["id"]] = task
    return task

def list_tasks():
    """
    List all tasks in the in-memory storage.

    Returns:
        list: A list of all tasks
    """
    return list(tasks.values())

def toggle_task(task_id):
    """
    Toggle the completion status of a task.

    Args:
        task_id (str): The ID of the task to toggle

    Returns:
        dict: The updated task

    Raises:
        KeyError: If task ID does not exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task with ID {task_id} does not exist")

    task = tasks[task_id]
    task["completed"] = not task["completed"]
    return task

def update_task(task_id, title=None, description=None):
    """
    Update a task's title and/or description.

    Args:
        task_id (str): The ID of the task to update
        title (str, optional): The new title for the task
        description (str, optional): The new description for the task

    Returns:
        dict: The updated task

    Raises:
        KeyError: If task ID does not exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task with ID {task_id} does not exist")

    task = tasks[task_id]

    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description

    return task

def delete_task(task_id):
    """
    Delete a task from the in-memory storage.

    Args:
        task_id (str): The ID of the task to delete

    Returns:
        dict: The deleted task

    Raises:
        KeyError: If task ID does not exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task with ID {task_id} does not exist")

    deleted_task = tasks.pop(task_id)
    return deleted_task

def display_menu():
    """
    Display the main menu options to the user.
    """
    print("\n" + "="*40)
    print("Welcome to Todo App!")
    print("What would you like to do?")
    print("="*40)
    print("1) Add task")
    print("2) Update task")
    print("3) Delete task")
    print("4) View all tasks")
    print("5) Toggle task as complete")
    print("6) Exit")
    print("="*40)

def get_user_choice():
    """
    Get and validate the user's menu choice.

    Returns:
        str: The user's choice (1-6)
    """
    while True:
        try:
            choice = input("Enter your choice (1 - 6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting the application...")
            sys.exit(0)

def handle_add_task():
    """
    Handle the Add Task operation with interactive prompts.
    """
    try:
        print("\n--- Add New Task ---")
        title = input("Task title: ").strip()
        if not title:
            print("Error: Task title is required")
            return

        description = input("Description (optional): ").strip()
        task = add_task(title, description)
        print(f"Task added successfully with ID: {task['id']}")
    except ValueError as e:
        print(f"Error: {e}")

def handle_view_tasks():
    """
    Handle the View All Tasks operation.
    """
    print("\n--- All Tasks ---")
    all_tasks = list_tasks()
    if not all_tasks:
        print("No tasks found.")
    else:
        print(f"{'ID':<5} {'Title':<20} {'Description':<30} {'Completed':<10}")
        print("-" * 70)
        for task in all_tasks:
            status = "Yes" if task["completed"] else "No"
            print(f"{task['id']:<5} {task['title']:<20} {task['description']:<30} {status:<10}")

def handle_toggle_task():
    """
    Handle the Toggle Task Completion operation.
    """
    print("\n--- Toggle Task Completion ---")
    if not tasks:
        print("No tasks available to toggle.")
        return

    try:
        task_id = input("Enter task ID to toggle: ").strip()
        task = toggle_task(task_id)
        status = "completed" if task["completed"] else "not completed"
        print(f"Task {task['id']} is now {status}")
    except KeyError as e:
        print(f"Error: {e}")

def handle_update_task():
    """
    Handle the Update Task operation.
    """
    print("\n--- Update Task ---")
    if not tasks:
        print("No tasks available to update.")
        return

    try:
        task_id = input("Enter task ID to update: ").strip()

        # Check if task exists
        if task_id not in tasks:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        current_task = tasks[task_id]
        print(f"Current title: {current_task['title']}")
        print(f"Current description: {current_task['description']}")

        new_title = input(f"Update title (press Enter to keep '{current_task['title']}'): ").strip()
        new_description = input(f"Update description (press Enter to keep '{current_task['description']}'): ").strip()

        # Only update if user provided new values
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        # If user pressed Enter without typing, keep the original values
        if new_title == "":
            title_to_update = None
        if new_description == "":
            description_to_update = None

        task = update_task(task_id, title=title_to_update, description=description_to_update)
        print(f"Task {task['id']} updated successfully")
    except KeyError as e:
        print(f"Error: {e}")

def handle_delete_task():
    """
    Handle the Delete Task operation.
    """
    print("\n--- Delete Task ---")
    if not tasks:
        print("No tasks available to delete.")
        return

    try:
        task_id = input("Enter task ID to delete: ").strip()
        deleted_task = delete_task(task_id)
        print(f"Task {deleted_task['id']} deleted successfully")
    except KeyError as e:
        print(f"Error: {e}")

def main():
    """
    Main function to run the interactive menu-based Todo application.
    """
    print("Welcome to the Interactive Todo Application!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            handle_add_task()
        elif choice == '2':
            handle_update_task()
        elif choice == '3':
            handle_delete_task()
        elif choice == '4':
            handle_view_tasks()
        elif choice == '5':
            handle_toggle_task()
        elif choice == '6':
            print("\nThank you for using the Todo App. Goodbye!")
            break

        # Pause to let user see the result before showing the menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()