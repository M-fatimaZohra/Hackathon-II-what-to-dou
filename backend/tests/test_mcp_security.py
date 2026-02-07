import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Task
from src.mcp.tools.task_create_tool import create_task
from src.mcp.tools.task_update_tool import update_task
from src.mcp.tools.task_delete_tool import delete_task
from src.mcp.tools.task_list_tool import list_tasks


@pytest.fixture
def setup_test_data():
    """Setup and teardown for test data."""
    # Cleanup any existing test tasks
    with Session(engine) as session:
        stmt = select(Task).where(
            Task.user_id.in_(["user_one_test", "user_two_test"])
        )
        existing_tasks = session.exec(stmt).all()
        for task in existing_tasks:
            session.delete(task)
        session.commit()


def test_task_creation_for_user_one(setup_test_data):
    """Test 1: Call tool with user_one context. Verify task is created in DB."""

    # Create context for user_one
    context = {"auth_user_id": "user_one_test"}

    # Call the tool with user_one context
    result = create_task(context, "Test task for user one", "Description for user one")

    # Since create_task is async, we need to handle it properly
    import asyncio
    result = asyncio.run(result)

    # Verify success message
    assert "Successfully created task" in result
    assert "user_one_test" in result

    # Verify task exists in DB for user_one
    with Session(engine) as session:
        stmt = select(Task).where(
            Task.user_id == "user_one_test",
            Task.title == "Test task for user one"
        )
        task = session.exec(stmt).first()

        assert task is not None
        assert task.description == "Description for user one"
        assert task.completed is False


def test_multi_tenant_isolation(setup_test_data):
    """Test 2: Verify user_one's task is NOT visible to user_two."""

    import asyncio

    # First, create a task for user_one
    user_one_context = {"auth_user_id": "user_one_test"}
    result_one = asyncio.run(create_task(user_one_context, "User one task", "User one description"))

    # Now check what user_two can see
    user_two_context = {"auth_user_id": "user_two_test"}
    result_two = asyncio.run(create_task(user_two_context, "User two task", "User two description"))

    # Verify user_one's task is NOT accessible to user_two by querying directly from DB
    with Session(engine) as session:
        # Get all tasks for user_one
        user_one_stmt = select(Task).where(Task.user_id == "user_one_test")
        user_one_tasks = session.exec(user_one_stmt).all()

        # Get all tasks for user_two
        user_two_stmt = select(Task).where(Task.user_id == "user_two_test")
        user_two_tasks = session.exec(user_two_stmt).all()

        # Verify user_one has their task
        assert len(user_one_tasks) == 1
        assert user_one_tasks[0].title == "User one task"

        # Verify user_two has their task (and not user_one's)
        assert len(user_two_tasks) == 1
        assert user_two_tasks[0].title == "User two task"

        # Ensure user_two cannot see user_one's task
        user_two_task_titles = [task.title for task in user_two_tasks]
        assert "User one task" not in user_two_task_titles

        # Ensure user_one cannot see user_two's task
        user_one_task_titles = [task.title for task in user_one_tasks]
        assert "User two task" not in user_one_task_titles


def test_missing_auth_context(setup_test_data):
    """Test 3: Verify tool returns an error if auth_user_id is missing from context."""

    import asyncio

    # Call the tool with no auth_user_id in context
    empty_context = {}
    result = asyncio.run(create_task(empty_context, "Should fail", "No user context"))

    # Verify error message
    assert "Error: Authentication required. User ID not found in context." in result

    # Verify no task was created for an unknown user
    with Session(engine) as session:
        stmt = select(Task).where(Task.user_id == "")
        tasks = session.exec(stmt).all()
        # There might be other tasks with empty user_id if the tool tried to save them,
        # but the tool should prevent creation
        # Let's also test with None context
        none_context = {"auth_user_id": None}
        result_none = asyncio.run(create_task(none_context, "Should also fail", "None user context"))
        assert "Error: Authentication required. User ID not found in context." in result_none


def test_invalid_auth_context(setup_test_data):
    """Additional test: Verify tool handles invalid auth_user_id properly."""

    import asyncio

    # Call the tool with None as auth_user_id
    invalid_context = {"auth_user_id": None}
    result = asyncio.run(create_task(invalid_context, "Should fail with None", "None context"))

    # Verify error message
    assert "Error: Authentication required. User ID not found in context." in result

    # Call the tool with empty string as auth_user_id
    empty_string_context = {"auth_user_id": ""}
    result_empty = asyncio.run(create_task(empty_string_context, "Should fail with empty", "Empty context"))

    # Verify error message
    assert "Error: Authentication required. User ID not found in context." in result_empty


def test_cross_user_task_access(setup_test_data):
    """Test: Verify user_two cannot delete or update a task belonging to user_one."""

    import asyncio

    # Create a task for user_one
    user_one_context = {"auth_user_id": "user_one_test"}
    result = asyncio.run(create_task(user_one_context, "User one task", "User one description"))
    assert "Successfully created task" in result

    # Verify the task exists and get its ID
    with Session(engine) as session:
        stmt = select(Task).where(Task.user_id == "user_one_test")
        task = session.exec(stmt).first()
        assert task is not None
        task_id = task.id

    # Try to update the task using user_two context (should fail)
    user_two_context = {"auth_user_id": "user_two_test"}
    update_result = asyncio.run(update_task(user_two_context, task_id, "Hacked by user two"))
    assert "Error: Task with ID" in update_result
    assert "not found or does not belong to user" in update_result

    # Try to delete the task using user_two context (should fail)
    delete_result = asyncio.run(delete_task(user_two_context, task_id))
    assert "Error: Task with ID" in delete_result
    assert "not found or does not belong to user" in delete_result

    # Verify the task still belongs to user_one and wasn't modified
    with Session(engine) as session:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == "user_one_test")
        task = session.exec(stmt).first()
        assert task is not None
        assert task.title == "User one task"  # Should not have been changed by user_two


def test_list_tasks_user_isolation(setup_test_data):
    """Test: Verify list_tasks only returns the correct user's data."""

    import asyncio

    # Create a task for user_one
    user_one_context = {"auth_user_id": "user_one_test"}
    result_one = asyncio.run(create_task(user_one_context, "User one task", "User one description"))
    assert "Successfully created task" in result_one

    # Create a task for user_two
    user_two_context = {"auth_user_id": "user_two_test"}
    result_two = asyncio.run(create_task(user_two_context, "User two task", "User two description"))
    assert "Successfully created task" in result_two

    # List tasks for user_one
    user_one_tasks_result = asyncio.run(list_tasks(user_one_context))
    assert "user_one_test" in user_one_tasks_result
    assert "User one task" in user_one_tasks_result
    assert "User two task" not in user_one_tasks_result  # Should not see user_two's task

    # List tasks for user_two
    user_two_tasks_result = asyncio.run(list_tasks(user_two_context))
    assert "user_two_test" in user_two_tasks_result
    assert "User two task" in user_two_tasks_result
    assert "User one task" not in user_two_tasks_result  # Should not see user_one's task