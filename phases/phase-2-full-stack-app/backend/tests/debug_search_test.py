"""
Debug version of search test to identify issues with search functionality
"""
from sqlmodel import Session
from schema.models import TaskCreate
from services.task_service_with_search import TaskServiceWithSearch as TaskService
from database.db import get_session

def test_keyword_search_debug():
    """Test that users can search their own tasks by keyword in title/description"""
    print("[DEBUG] Starting keyword search test...")

    session_gen = get_session()
    session = next(session_gen)

    try:
        # Create test user and tasks
        import uuid
        user_id = f"test_user_{uuid.uuid4().hex[:8]}"

        # Create tasks for the user
        task1 = TaskCreate(title="Research project", description="Need to research AI trends", priority="high", completed=False)
        task2 = TaskCreate(title="Shopping list", description="Buy groceries for dinner", priority="medium", completed=True)
        task3 = TaskCreate(title="Meeting notes", description="Review meeting notes from yesterday", priority="low", completed=False)

        print(f"[INFO] Creating task 1: {task1.title}")
        created_task1 = TaskService.create_task(session, task1, user_id)
        print(f"[SUCCESS] Created task 1 with ID: {created_task1.id}")

        print(f"[INFO] Creating task 2: {task2.title}")
        created_task2 = TaskService.create_task(session, task2, user_id)
        print(f"[SUCCESS] Created task 2 with ID: {created_task2.id}")

        print(f"[INFO] Creating task 3: {task3.title}")
        created_task3 = TaskService.create_task(session, task3, user_id)
        print(f"[SUCCESS] Created task 3 with ID: {created_task3.id}")

        # Test search by keyword in title
        print("\n[SEARCH] Testing search for 'research' in title...")
        results = TaskService.get_tasks_by_user_id(session, user_id, search="research")
        print(f"[RESULTS] Found {len(results)} results for 'research' search")
        for result in results:
            print(f"  - ID: {result.id}, Title: '{result.title}', Description: '{result.description}'")

        assert len(results) == 1, f"Expected 1 result for 'research' search, but got {len(results)}"
        assert "research" in results[0].title.lower(), f"'research' not found in title: {results[0].title}"

        # Test search by keyword in description
        print("\n[SEARCH] Testing search for 'groceries' in description...")
        results = TaskService.get_tasks_by_user_id(session, user_id, search="groceries")
        print(f"[RESULTS] Found {len(results)} results for 'groceries' search")
        for result in results:
            print(f"  - ID: {result.id}, Title: '{result.title}', Description: '{result.description}'")

        assert len(results) == 1, f"Expected 1 result for 'groceries' search, but got {len(results)}"
        assert "groceries" in results[0].description.lower(), f"'groceries' not found in description: {results[0].description}"

        # Test search with no matches
        print("\n[SEARCH] Testing search for 'nonexistent'...")
        results = TaskService.get_tasks_by_user_id(session, user_id, search="nonexistent")
        print(f"[RESULTS] Found {len(results)} results for 'nonexistent' search")

        assert len(results) == 0, f"Expected 0 results for 'nonexistent' search, but got {len(results)}"

        # Test search with partial matching
        print("\n[SEARCH] Testing search for 'meet'...")
        results = TaskService.get_tasks_by_user_id(session, user_id, search="meet")
        print(f"[RESULTS] Found {len(results)} results for 'meet' search")
        for result in results:
            print(f"  - ID: {result.id}, Title: '{result.title}', Description: '{result.description}'")

        assert len(results) == 1, f"Expected 1 result for 'meet' search, but got {len(results)}"
        assert "meeting" in results[0].title.lower(), f"'meeting' not found in title: {results[0].title}"

        print("[SUCCESS] Keyword search test passed!")
        return True

    except Exception as e:
        print(f"❌ Keyword search test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Close the session
        session.close()

if __name__ == "__main__":
    success = test_keyword_search_debug()
    if success:
        print("\n[SUCCESS] Keyword search debug test completed successfully!")
    else:
        print("\n[ERROR] Keyword search debug test failed!")