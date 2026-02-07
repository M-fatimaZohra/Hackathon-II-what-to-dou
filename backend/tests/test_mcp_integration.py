import os
import pytest
import asyncio
from sqlmodel import Session, select
from src.schema.models import Task
from src.database.db import engine
from src.my_mcp_server.tools.task_create_tool import create_task
from src.my_mcp_server.tools.task_list_tool import list_tasks
from src.my_mcp_server.tools.task_update_tool import update_task
from src.my_mcp_server.tools.task_delete_tool import delete_task
from src.my_mcp_server.tools.task_complete_tool import complete_task


@pytest.fixture
def test_user():
    """Fixture that provides a test user ID."""
    return "test_user_123"


@pytest.fixture
def setup_auth(test_user):
    """Fixture that sets up the authentication environment."""
    original_auth = os.environ.get("AUTH_USER_ID")
    os.environ["AUTH_USER_ID"] = test_user
    yield test_user
    if original_auth is not None:
        os.environ["AUTH_USER_ID"] = original_auth
    else:
        os.environ.pop("AUTH_USER_ID", None)


@pytest.mark.asyncio
async def test_create_task_integration(setup_auth, test_user):
    """Test creating a task via MCP tool."""
    # Call the create_task function directly
    result = await create_task(None, "Test Task", "Test Description")

    # Verify the result structure
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "task" in result
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["user_id"] == test_user

    # Verify the task was created in the database
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.user_id == test_user)).first()
        assert task is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False


@pytest.mark.asyncio
async def test_list_tasks_integration(setup_auth, test_user):
    """Test listing tasks via MCP tool."""
    # First, create a task to list
    create_result = await create_task(None, "List Test Task", "Description for listing")
    assert create_result["status"] == "ok"

    # Call the list_tasks function
    result = await list_tasks(None, "all")

    # Verify the result structure
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "tasks" in result
    assert len(result["tasks"]) >= 1

    # Verify the task exists in the results
    found_task = next((t for t in result["tasks"] if t["title"] == "List Test Task"), None)
    assert found_task is not None
    assert found_task["user_id"] == test_user

    # Verify the database state
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == test_user)).all()
        assert len(tasks) >= 1


@pytest.mark.asyncio
async def test_update_task_integration(setup_auth, test_user):
    """Test updating a task via MCP tool."""
    # First, create a task to update
    create_result = await create_task(None, "Original Task", "Original Description")
    assert create_result["status"] == "ok"
    task_id = create_result["task"]["id"]

    # Call the update_task function
    result = await update_task(None, task_id, "Updated Task Title", "Updated Description")

    # Verify the result structure
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "task" in result
    assert result["task"]["title"] == "Updated Task Title"
    assert result["task"]["description"] == "Updated Description"

    # Verify the database was updated
    with Session(engine) as session:
        task = session.get(Task, task_id)
        assert task is not None
        assert task.title == "Updated Task Title"
        assert task.description == "Updated Description"


@pytest.mark.asyncio
async def test_complete_task_integration(setup_auth, test_user):
    """Test completing a task via MCP tool."""
    # First, create a task to complete
    create_result = await create_task(None, "Task to Complete", "Description")
    assert create_result["status"] == "ok"
    task_id = create_result["task"]["id"]

    # Verify the task is initially not completed
    with Session(engine) as session:
        task = session.get(Task, task_id)
        assert task is not None
        assert task.completed is False

    # Call the complete_task function
    result = await complete_task(None, task_id)

    # Verify the result structure
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "task" in result
    assert result["task"]["completed"] is True

    # Verify the database was updated
    with Session(engine) as session:
        task = session.get(Task, task_id)
        assert task is not None
        assert task.completed is True


@pytest.mark.asyncio
async def test_delete_task_integration(setup_auth, test_user):
    """Test deleting a task via MCP tool."""
    # First, create a task to delete
    create_result = await create_task(None, "Task to Delete", "Description")
    assert create_result["status"] == "ok"
    task_id = create_result["task"]["id"]

    # Verify the task exists in the database
    with Session(engine) as session:
        task = session.get(Task, task_id)
        assert task is not None

    # Call the delete_task function
    result = await delete_task(None, task_id)

    # Verify the result structure
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "task_id" in result
    assert result["task_id"] == task_id

    # Verify the task was deleted from the database
    with Session(engine) as session:
        task = session.get(Task, task_id)
        assert task is None


@pytest.mark.asyncio
async def test_unauthorized_access(setup_auth, test_user):
    """Test error handling when no auth user is set."""
    # Temporarily remove the AUTH_USER_ID
    original_auth = os.environ.pop("AUTH_USER_ID", None)

    try:
        # Attempt to create a task without authentication
        result = await create_task(None, "Unauthorized Task", "Should fail")

        # Verify error response structure
        assert isinstance(result, dict)
        assert result["status"] == "error"
        assert result["code"] == "unauthorized"
        assert "message" in result
    finally:
        # Restore the authentication
        if original_auth is not None:
            os.environ["AUTH_USER_ID"] = original_auth
        else:
            os.environ["AUTH_USER_ID"] = test_user


@pytest.mark.asyncio
async def test_task_not_found(setup_auth):
    """Test error handling when a task doesn't exist."""
    # Try to update a non-existent task
    result = await update_task(None, 99999, "Non-existent Task", "Should fail")

    # Verify error response structure
    assert isinstance(result, dict)
    assert result["status"] == "error"
    assert result["code"] == "not_found"
    assert "message" in result
    assert "99999" in result["message"]


@pytest.mark.asyncio
async def test_structured_dict_format_consistency(setup_auth, test_user):
    """Test that all MCP tools return properly structured dictionaries."""
    # Test create_task structure
    create_result = await create_task(None, "Structure Test", "Testing structure")
    assert isinstance(create_result, dict)
    assert "status" in create_result
    assert create_result["status"] in ["ok", "error"]

    if create_result["status"] == "ok":
        assert "task" in create_result
        task = create_result["task"]
        assert "id" in task
        assert "title" in task
        assert "user_id" in task
    else:
        assert "code" in create_result
        assert "message" in create_result

    # Test list_tasks structure
    list_result = await list_tasks(None, "all")
    assert isinstance(list_result, dict)
    assert "status" in list_result
    assert list_result["status"] in ["ok", "error"]

    if list_result["status"] == "ok":
        assert "tasks" in list_result
    else:
        assert "code" in list_result
        assert "message" in list_result

    # Test update_task structure (after creating a task to update)
    create_result = await create_task(None, "Update Structure Test", "Testing structure")
    assert create_result["status"] == "ok"
    task_id = create_result["task"]["id"]

    update_result = await update_task(None, task_id, "Updated Title", "Updated Description")
    assert isinstance(update_result, dict)
    assert "status" in update_result
    assert update_result["status"] in ["ok", "error"]

    if update_result["status"] == "ok":
        assert "task" in update_result
    else:
        assert "code" in update_result
        assert "message" in update_result


if __name__ == "__main__":
    pytest.main([__file__])