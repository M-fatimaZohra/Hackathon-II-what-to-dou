import os
from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Task
from mcp.server.fastmcp import Context


async def update_task(ctx: Context, task_id: int, title: str = None, description: str = None) -> str:
    """
    Updates a task for the authenticated user.
    The 'ctx' provides the secure 'auth_user_id' from the backend.
    The 'user_id' is extracted from context and NOT passed as a function argument
    to prevent the AI from manipulating other users' data.
    Verifies that the task belongs to the authenticated user before updating.
    """
    # Extract user_id from environment variable
    user_id = os.getenv("AUTH_USER_ID")

    if not user_id:
        return "ERROR: Authentication required"

    try:
        # Create database session and query for the task
        with Session(engine) as session:
            # Get the task and ensure it belongs to the authenticated user
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(stmt).first()

            if not task:
                return f"ERROR: Task with ID {task_id} not found or does not belong to user {user_id}"

            # Update the task if new values are provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            session.add(task)
            session.commit()
            session.refresh(task)

            return f"SUCCESS: Updated task to '{task.title}' (ID: {task.id})"

    except Exception as e:
        return f"ERROR: Error updating task: {str(e)}"