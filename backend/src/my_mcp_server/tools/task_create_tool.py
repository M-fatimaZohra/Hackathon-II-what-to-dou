import os
from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Task, TaskCreate
from mcp.server.fastmcp import Context


async def create_task(ctx: Context, title: str, description: str = "") -> str:
    """
    Creates a new task for the authenticated user.
    The 'ctx' provides the secure 'auth_user_id' from the backend.
    The 'user_id' is extracted from context and NOT passed as a function argument
    to prevent the AI from manipulating other users' data.
    """
    # Extract user_id from environment variable
    user_id = os.getenv("AUTH_USER_ID")

    if not user_id:
        return "ERROR: Authentication required"

    try:
        # Create a new task using the extracted user_id
        task_data = TaskCreate(
            title=title,
            description=description if description else "",
            completed=False,
            priority="medium"
        )

        # Create database session and add the task
        with Session(engine) as session:
            # Create the task object with the authenticated user's ID
            task = Task(
                **task_data.model_dump(),
                user_id=user_id
            )

            session.add(task)
            session.commit()
            session.refresh(task)

            return f"SUCCESS: Created task '{task.title}' (ID: {task.id})"

    except Exception as e:
        return f"ERROR: Error creating task: {str(e)}"


# Also provide a sync version for testing
def create_task_sync(ctx: Context, title: str, description: str = "") -> str:
    """
    Synchronous version of create_task for testing purposes.
    """
    import asyncio

    async def run_async():
        return await create_task(ctx, title, description)

    return asyncio.run(run_async())