#!/usr/bin/env python3
"""
Debug script to test the full MCP integration flow with real agent and tool execution.
This script reproduces the actual issue where the agent fails to create tasks.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.mcp import MCPServerStdio
from agents import Agent, Runner
from src.configs.gemini_config import GEMINI_MODEL, SYSTEM_PROMPT


async def debug_mcp_integration():
    print("=== DIAGNOSTIC: Testing Full MCP Integration ===")

    # Setup the MCP server using the same configuration as in chat_service
    env = {**os.environ, "PYTHONPATH": ".", "AUTH_USER_ID": "debug_user_99"}

    print("Initializing MCPServerStdio with server.py...")

    mcp_server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["src/my_mcp_server/server.py"],
            "env": env
        }
    )

    print("Creating agent with MCP server connection...")

    try:
        async with mcp_server as connection:
            # Create the agent with MCP connection
            agent = Agent(
                name="TodoAssistant",
                model=GEMINI_MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[connection]
            )

            print("Attempting to call the agent with a task creation request...")

            # Run a test message that should trigger task creation
            result = await Runner.run(
                agent,
                "Create a task called 'Debug Task' with description 'This is a debug task'",
                context={"auth_user_id": "debug_user_99"}
            )

            print(f"\nAgent response: {result.final_output}")
            print(f"New items: {len(result.new_items) if hasattr(result, 'new_items') else 'No items'}")

            if hasattr(result, 'new_items'):
                for item in result.new_items:
                    print(f"Item type: {type(item)}")
                    if hasattr(item, 'raw_item'):
                        print(f"  Raw item name: {getattr(item.raw_item, 'name', 'Unknown')}")
                        print(f"  Raw item arguments: {getattr(item.raw_item, 'arguments', 'Unknown')}")
                        print(f"  Raw item content: {getattr(item, 'content', 'No content')}")

            return result

    except Exception as e:
        print(f"\nERROR during MCP integration: {e}")
        import traceback
        traceback.print_exc()
        return None


def debug_direct_tool_call():
    print("\n=== DIAGNOSTIC: Testing Direct Tool Import ===")

    try:
        # Test importing the tools directly
        from src.my_mcp_server.tools.task_create_tool import create_task
        print("[SUCCESS] Successfully imported create_task function")

        # Test the function signature
        import inspect
        sig = inspect.signature(create_task)
        print(f"[SUCCESS] Function signature: {sig}")

        # Try to see the function implementation
        print("[SUCCESS] Function exists and has proper signature")

        return True
    except Exception as e:
        print(f"[ERROR] ERROR importing tool: {e}")
        import traceback
        traceback.print_exc()
        return False


def debug_database_connection():
    print("\n=== DIAGNOSTIC: Testing Database Connection ===")

    try:
        # Test basic database connection
        from sqlmodel import Session, select
        from src.database.db import engine
        from src.schema.models import Task

        with Session(engine) as session:
            # Try a simple query
            stmt = select(Task).where(Task.user_id == "debug_user_99").limit(1)
            result = session.exec(stmt).all()
            print("[SUCCESS] Successfully connected to database and executed query")
            print(f"[SUCCESS] Found {len(result)} test tasks")

        return True
    except Exception as e:
        print(f"[ERROR] ERROR with database connection: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting MCP Integration Debug Process...")
    print("This will test all components involved in the task creation failure.\n")

    # Run the sync tests first
    tool_import_ok = debug_direct_tool_call()
    db_connection_ok = debug_database_connection()

    # Run the async test
    print("\n" + "="*60)
    result = asyncio.run(debug_mcp_integration())

    print("\n" + "="*60)
    print("DEBUG SUMMARY:")
    print(f"- Tool Import: {'[SUCCESS] OK' if tool_import_ok else '[ERROR] FAILED'}")
    print(f"- Database Connection: {'[SUCCESS] OK' if db_connection_ok else '[ERROR] FAILED'}")
    print(f"- MCP Integration: {'[SUCCESS] OK' if result else '[ERROR] FAILED'}")

    if tool_import_ok and db_connection_ok and result:
        print("\n🎉 All components are working individually!")
        print("Issue may be in the context handling or communication between components.")
    else:
        print("\n⚠️  One or more components are failing.")
        print("This identifies where the issue is in the MCP integration stack.")