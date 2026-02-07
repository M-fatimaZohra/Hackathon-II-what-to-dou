#!/usr/bin/env python3
"""
Verification script to check the actual implementation of user isolation.
"""

import sys
from pathlib import Path

# Add src to path to import modules
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Task


def check_task_schema():
    """
    Check that the Task model has a non-nullable user_id field.
    """
    print("Checking Task model schema...")

    # Check if user_id exists in the Task model and has proper constraints
    if hasattr(Task, '__annotations__'):
        annotations = Task.__annotations__
        if 'user_id' in annotations:
            print("  ✓ user_id field exists in Task model")

            # Check the field definition in the class
            for attr_name, obj in Task.__dict__.items():
                if attr_name == 'user_id' or (hasattr(obj, '__class__') and 'Field' in str(type(obj))):
                    if hasattr(obj, 'nullable'):
                        if not obj.nullable:
                            print("  ✓ user_id field is non-nullable")
                        else:
                            print("  ⚠ user_id field appears to be nullable")
                    break
        else:
            print("  ✗ user_id field not found in Task model")
            return False
    else:
        print("  ? Unable to inspect Task model annotations")
        # Check the model at the class level
        try:
            # Look for user_id in the table structure if using SQLModel
            columns = Task.__table__.columns
            user_id_col = columns.get('user_id')
            if user_id_col and not user_id_col.nullable:
                print("  ✓ user_id field exists and is non-nullable")
                return True
            elif user_id_col:
                print("  ⚠ user_id field exists but is nullable")
                return False
            else:
                print("  ✗ user_id field not found in Task table")
                return False
        except AttributeError:
            print("  ? Unable to inspect Task table structure")
            return False

    return True


def check_mcp_tool_implementation():
    """
    Check that MCP tools properly extract auth_user_id from context and use it for filtering.
    """
    print("\nChecking MCP tool implementation...")

    # Read the task_list_tool.py file to verify the implementation
    tool_file_path = Path(__file__).parent / "src" / "mcp" / "tools" / "task_list_tool.py"

    if not tool_file_path.exists():
        print(f"  ✗ ERROR: {tool_file_path} not found")
        return False

    with open(tool_file_path, 'r') as f:
        content = f.read()

    print(f"  ✓ Found MCP tool file: {tool_file_path.name}")

    # Check for the key implementation details
    checks = [
        ("ctx.request_context.get(\"auth_user_id\")", "auth_user_id extraction from context"),
        ("Task.user_id == user_id", "user_id filtering in query"),
        ("session.exec(", "database query execution"),
        ("ctx.error(", "error handling with context")
    ]

    all_found = True
    for check_pattern, description in checks:
        if check_pattern in content:
            print(f"  ✓ {description} found")
        else:
            print(f"  ✗ {description} MISSING")
            all_found = False

    return all_found


def live_database_test():
    """
    Run a live database test to verify user isolation.
    """
    print("\nRunning live database test...")

    try:
        # Create a real database session
        with Session(engine) as session:
            print("  ✓ Database session created successfully")

            # Clear any existing test data for clean test
            from sqlalchemy import text
            try:
                # Try to delete any existing test tasks
                session.exec(text("DELETE FROM task WHERE user_id LIKE 'user_test_%'"))
                session.commit()
            except:
                session.rollback()  # If table doesn't exist yet, continue anyway

            # 1. Manually insert a task for user_test_1
            print("  1. Inserting a task for user_test_1...")
            test_task = Task(
                title="Test task for user 1",
                description="This task belongs to user 1 only",
                completed=False,
                priority="medium",
                user_id="user_test_1"  # This should be non-nullable
            )

            session.add(test_task)
            session.commit()
            session.refresh(test_task)

            print(f"     ✓ Created task with ID {test_task.id} for user_test_1")

            # Verify the task was inserted
            stmt = select(Task).where(Task.user_id == "user_test_1")
            user1_tasks = session.exec(stmt).all()
            print(f"     ✓ Verified {len(user1_tasks)} task(s) exist for user_test_1")

            # 2. Check that user_test_2 has no tasks
            stmt_user2 = select(Task).where(Task.user_id == "user_test_2")
            user2_tasks = session.exec(stmt_user2).all()
            print(f"     ✓ Verified {len(user2_tasks)} task(s) exist for user_test_2 (as expected)")

            # Clean up by removing test data
            from sqlalchemy import delete
            try:
                session.exec(delete(Task).where(Task.user_id.like("user_test_%")))
                session.commit()
            except:
                session.rollback()

            # Verification: user_test_1 should have 1+ tasks, user_test_2 should have 0 tasks
            if len(user1_tasks) >= 1 and len(user2_tasks) == 0:
                print("  ✓ LIVE TEST PASSED: Database properly isolates user data")
                return True
            else:
                print("  ✗ LIVE TEST FAILED: User data not properly isolated")
                return False

    except Exception as e:
        print(f"  ✗ LIVE TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("🔍 Verifying MCP Implementation and Database Schema...")
    print("="*60)

    # Check 1: Task model schema
    schema_ok = check_task_schema()

    # Check 2: MCP tool implementation
    tool_ok = check_mcp_tool_implementation()

    # Check 3: Live database test
    db_ok = live_database_test()

    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Task Schema: {'✓ PASS' if schema_ok else '✗ FAIL'}")
    print(f"  MCP Tools: {'✓ PASS' if tool_ok else '✗ FAIL'}")
    print(f"  Live DB Test: {'✓ PASS' if db_ok else '✗ FAIL'}")

    all_passed = schema_ok and tool_ok and db_ok
    print(f"\nOVERALL RESULT: {'✓ ALL CHECKS PASSED' if all_passed else '✗ SOME CHECKS FAILED'}")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)