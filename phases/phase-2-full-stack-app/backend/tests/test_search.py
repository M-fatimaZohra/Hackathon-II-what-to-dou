"""
Backend integration tests for search functionality verifying:
- Keyword matching in title/description
- Priority filtering
- Strict User ID isolation (User A cannot search User B's tasks)
"""
from sqlmodel import Session
from schema.models import TaskCreate
from services.task_service_with_search import TaskServiceWithSearch as TaskService
from database.db import engine, get_session

def test_keyword_search():
    """Test that users can search their own tasks by keyword in title/description"""
    from database.db import get_session

    with next(get_session()) as session:
        # Create test user and tasks
        import uuid
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

        # Create tasks for the user
        task1 = TaskCreate(title="Research project", description="Need to research AI trends", priority="high", completed=False)
        task2 = TaskCreate(title="Shopping list", description="Buy groceries for dinner", priority="medium", completed=True)
        task3 = TaskCreate(title="Meeting notes", description="Review meeting notes from yesterday", priority="low", completed=False)

        created_task1 = TaskService.create_task(session, task1, user_id)
        created_task2 = TaskService.create_task(session, task2, user_id)
        created_task3 = TaskService.create_task(session, task3, user_id)

        # Test search by keyword in title
        results = TaskService.get_tasks_by_user_id(session, user_id, search="research")
        assert len(results) == 1
        assert "research" in results[0].title.lower()

        # Test search by keyword in description
        results = TaskService.get_tasks_by_user_id(session, user_id, search="groceries")
        assert len(results) == 1
        assert "groceries" in results[0].description.lower()

        # Test search with no matches
        results = TaskService.get_tasks_by_user_id(session, user_id, search="nonexistent")
        assert len(results) == 0

        # Test search with partial matching
        results = TaskService.get_tasks_by_user_id(session, user_id, search="meet")
        assert len(results) == 1
        assert "meeting" in results[0].title.lower()


def test_priority_filtering():
    """Test that users can filter their tasks by priority"""
    from database.db import get_session

    with next(get_session()) as session:
        # Create test user and tasks with different priorities
        import uuid
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

        # Create tasks with different priorities
        low_task = TaskCreate(title="Low priority task", description="This is low priority", priority="low", completed=False)
        medium_task = TaskCreate(title="Medium priority task", description="This is medium priority", priority="medium", completed=True)
        high_task = TaskCreate(title="High priority task", description="This is high priority", priority="high", completed=False)
        urgent_task = TaskCreate(title="Urgent task", description="This is urgent", priority="urgent", completed=True)

        TaskService.create_task(session, low_task, user_id)
        TaskService.create_task(session, medium_task, user_id)
        TaskService.create_task(session, high_task, user_id)
        TaskService.create_task(session, urgent_task, user_id)

        # Test filtering by low priority
        results = TaskService.get_tasks_by_user_id(session, user_id, priority="low")
        assert len(results) == 1
        assert results[0].priority == "low"

        # Test filtering by high priority
        results = TaskService.get_tasks_by_user_id(session, user_id, priority="high")
        assert len(results) == 1
        assert results[0].priority == "high"

        # Test filtering by urgent priority
        results = TaskService.get_tasks_by_user_id(session, user_id, priority="urgent")
        assert len(results) == 1
        assert results[0].priority == "urgent"

        # Test filtering with non-existent priority
        results = TaskService.get_tasks_by_user_id(session, user_id, priority="nonexistent")
        assert len(results) == 0


def test_status_filtering():
    """Test that users can filter their tasks by completion status"""
    from database.db import get_session

    with next(get_session()) as session:
        # Create test user and tasks with different completion statuses
        import uuid
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

        # Create completed and incomplete tasks
        completed_task1 = TaskCreate(title="Completed task 1", description="This is completed", priority="medium", completed=True)
        completed_task2 = TaskCreate(title="Completed task 2", description="This is also completed", priority="high", completed=True)
        incomplete_task1 = TaskCreate(title="Incomplete task 1", description="This is not completed", priority="low", completed=False)
        incomplete_task2 = TaskCreate(title="Incomplete task 2", description="This is also not completed", priority="urgent", completed=False)

        TaskService.create_task(session, completed_task1, user_id)
        TaskService.create_task(session, completed_task2, user_id)
        TaskService.create_task(session, incomplete_task1, user_id)
        TaskService.create_task(session, incomplete_task2, user_id)

        # Test filtering by completed status
        results = TaskService.get_tasks_by_user_id(session, user_id, completed=True)
        assert len(results) == 2
        for task in results:
            assert task.completed is True

        # Test filtering by incomplete status
        results = TaskService.get_tasks_by_user_id(session, user_id, completed=False)
        assert len(results) == 2
        for task in results:
            assert task.completed is False


def test_user_isolation_security_trap():
    """Test that a user cannot access another user's tasks by manipulating query parameters"""
    from database.db import get_session

    with next(get_session()) as session:
        # Create tasks for two different users
        import uuid
        user_a_id = f"user_a_{uuid.uuid4().hex[:8]}"
        user_b_id = f"user_b_{uuid.uuid4().hex[:8]}"

        # Create tasks for user A
        user_a_task1 = TaskCreate(title="User A Task 1", description="Owned by user A", priority="high", completed=False)
        user_a_task2 = TaskCreate(title="User A Task 2", description="Also owned by user A", priority="medium", completed=True)
        TaskService.create_task(session, user_a_task1, user_a_id)
        TaskService.create_task(session, user_a_task2, user_a_id)

        # Create tasks for user B
        user_b_task1 = TaskCreate(title="User B Task 1", description="Owned by user B", priority="low", completed=False)
        user_b_task2 = TaskCreate(title="User B Task 2", description="Also owned by user B", priority="urgent", completed=True)
        TaskService.create_task(session, user_b_task1, user_b_id)
        TaskService.create_task(session, user_b_task2, user_b_id)

        # Verify User A can only see their own tasks
        user_a_results = TaskService.get_tasks_by_user_id(session, user_a_id)
        assert len(user_a_results) == 2
        for task in user_a_results:
            assert task.user_id == user_a_id

        # Verify User B can only see their own tasks
        user_b_results = TaskService.get_tasks_by_user_id(session, user_b_id)
        assert len(user_b_results) == 2
        for task in user_b_results:
            assert task.user_id == user_b_id

        # Attempt to search User B's tasks while authenticated as User A (Security Trap Test)
        # This should return no results for User B's tasks
        user_a_search_results = TaskService.get_tasks_by_user_id(session, user_a_id, search="user b")
        # Should return 0 results since User A shouldn't find User B's tasks
        assert len(user_a_search_results) == 0

        # Even if we try to filter for User B's priority while authenticated as User A
        user_a_priority_results = TaskService.get_tasks_by_user_id(session, user_a_id, priority="urgent")
        # Should only return User A's urgent tasks (if any), not User B's
        for task in user_a_priority_results:
            assert task.user_id == user_a_id


def test_combined_filters():
    """Test that multiple filters work together correctly"""
    from database.db import get_session

    with next(get_session()) as session:
        # Create test user and tasks
        import uuid
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

        # Create various tasks
        task1 = TaskCreate(title="Urgent completed task", description="Very important and done", priority="urgent", completed=True)
        task2 = TaskCreate(title="Urgent incomplete task", description="Very important but not done", priority="urgent", completed=False)
        task3 = TaskCreate(title="Low completed task", description="Not important and done", priority="low", completed=True)
        task4 = TaskCreate(title="Low incomplete task", description="Not important and not done", priority="low", completed=False)

        TaskService.create_task(session, task1, user_id)
        TaskService.create_task(session, task2, user_id)
        TaskService.create_task(session, task3, user_id)
        TaskService.create_task(session, task4, user_id)

        # Test combined priority and status filter
        results = TaskService.get_tasks_by_user_id(session, user_id, priority="urgent", completed=True)
        assert len(results) == 1
        assert results[0].priority == "urgent" and results[0].completed is True

        # Test combined search and priority filter
        results = TaskService.get_tasks_by_user_id(session, user_id, search="important", priority="urgent")
        assert len(results) == 2  # Both urgent tasks contain "important" in description

        # Test combined search and status filter
        results = TaskService.get_tasks_by_user_id(session, user_id, search="done", completed=True)
        assert len(results) == 2  # Both completed tasks contain "done" in description


if __name__ == "__main__":
    # Run the tests
    test_keyword_search()
    print("[SUCCESS] Keyword search test passed")

    test_priority_filtering()
    print("[SUCCESS] Priority filtering test passed")

    test_status_filtering()
    print("[SUCCESS] Status filtering test passed")

    test_user_isolation_security_trap()
    print("[SUCCESS] User isolation security trap test passed")

    test_combined_filters()
    print("[SUCCESS] Combined filters test passed")

    print("\n[ALL PASSED] All backend search integration tests passed!")