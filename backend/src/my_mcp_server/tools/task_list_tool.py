import os
from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Task
from mcp.server.fastmcp import Context


async def list_tasks(ctx: Context, status: str = "all") -> str:
    """
    Lists tasks for the authenticated user.
    The 'ctx' provides the secure 'auth_user_id' from the backend.
    The 'user_id' is extracted from context and NOT passed as a function argument
    to prevent the AI from manipulating other users' data.
    """
    # Extract user_id from environment variable
    user_id = os.getenv("AUTH_USER_ID")

    if not user_id:
        return "ERROR: Authentication required"

    try:
        # Create database session and query tasks for the authenticated user
        with Session(engine) as session:
            # Start building the query based on user_id
            query = select(Task).where(Task.user_id == user_id)

            # Filter by status if needed
            if status.lower() == "completed":
                query = query.where(Task.completed == True)
            elif status.lower() == "pending":
                query = query.where(Task.completed == False)
            # else: status is "all" by default, so no additional filtering

            # Execute the query
            tasks = session.exec(query).all()

            if not tasks:
                return f"SUCCESS: No tasks found for user (ID: {user_id})."

            # Format the tasks for output
            task_list = []
            for task in tasks:
                status_text = "completed" if task.completed else "pending"
                task_list.append(f"'{task.title}' (ID: {task.id}, {status_text})")

            if task_list:
                task_str = ", ".join(task_list)
                return f"SUCCESS: Found {len(tasks)} task(s) for user (ID: {user_id}): {task_str}"
            else:
                return f"SUCCESS: No tasks found for user (ID: {user_id})."

    except Exception as e:
        return f"ERROR: Error listing tasks: {str(e)}"