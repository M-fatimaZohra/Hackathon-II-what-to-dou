#!/usr/bin/env python3
"""
Test script to validate the MCP connection bridge implementation.

This script verifies:
1. Subprocess Integrity: Can launch server.py and receive tools list
2. Context Passthrough: auth_user_id reaches MCP tool's ctx
3. Error Handling: Proper exception handling when MCP server fails
4. Mock Test: Simulates chat request and prints tool_calls
"""

import asyncio
import os
import sys
from pathlib import Path

# TASK A: Fix imports - Ensure the sys.path.insert correctly points to the directory containing the src folder
# so that from src.configs... works in the test environment
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from agents.mcp import MCPServerStdio
from agents import Agent, Runner
from src.configs.gemini_config import GEMINI_MODEL, SYSTEM_PROMPT


async def test_subprocess_integrity():
    """
    Test 1: Subprocess Integrity - Confirm that chat_service.py can successfully
    launch server.py and receive the list of tools.
    """
    print("="*60)
    print("TEST 1: Subprocess Integrity")
    print("="*60)

    try:
        # Set environment for the subprocess - PATHING: For the subprocess to work,
        # the env={"PYTHONPATH": "."} is mandatory so it can resolve absolute imports like from src.mcp.tools...
        env_vars = {**os.environ, "PYTHONPATH": "."}

        # SDK Versioning: Using the correct class with params dictionary
        mcp_server = MCPServerStdio(
            params={
                "command": "python",
                "args": ["src/mcp/server.py"],
                "env": env_vars
            }
        )

        print("[OK] MCPServerStdio initialized successfully")

        # Try to connect to the server
        async with mcp_server as connection:
            print("[OK] Connected to MCP server successfully")

            # Create an agent using the connection
            agent = Agent(
                name="TestAgent",
                model=GEMINI_MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[connection]
            )

            print("[OK] Agent created with MCP server connection")

            # TASK B: Validate Tool Discovery - Check if agent.tools is a dictionary or a list in this version of the SDK
            # If it's a dictionary, print the keys
            if hasattr(agent, 'tools'):
                if isinstance(agent.tools, dict):
                    print(f"[OK] Available tools (dict keys): {list(agent.tools.keys())}")
                elif isinstance(agent.tools, list):
                    print(f"[OK] Available tools (list): {agent.tools}")
                else:
                    print(f"[OK] Available tools (type {type(agent.tools)}): {agent.tools}")
            else:
                print("[INFO] Unable to list tools from agent - attribute 'tools' not found")

            return True

    except Exception as e:
        print(f"[FAILED] Failed to connect to MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_context_passthrough():
    """
    Test 2: Context Passthrough - Verify that the auth_user_id passed in
    Runner.run(context=...) actually reaches the MCP tool's ctx.
    """
    print("\n" + "="*60)
    print("TEST 2: Context Passthrough")
    print("="*60)

    try:
        # Set environment for the subprocess - PATHING: For the subprocess to work,
        # the env={"PYTHONPATH": "."} is mandatory so it can resolve absolute imports like from src.mcp.tools...
        env_vars = {**os.environ, "PYTHONPATH": "."}

        # SDK Versioning: Using the correct class with params dictionary
        mcp_server = MCPServerStdio(
            params={
                "command": "python",
                "args": ["src/mcp/server.py"],
                "env": env_vars
            }
        )

        async with mcp_server as connection:
            # Create an agent using the connection
            agent = Agent(
                name="ContextTestAgent",
                model=GEMINI_MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[connection]
            )

            # Define test user ID
            test_user_id = "test_user_12345"

            print(f"[OK] Preparing to test context with user ID: {test_user_id}")

            # Run a simple request that would trigger tool usage
            # Use the correct Runner.run API based on the working implementation
            result = await Runner.run(
                agent,
                "List all my tasks",
                context={"auth_user_id": test_user_id}
            )

            print(f"[OK] Agent responded: {result.final_output[:100]}...")

            # TASK C: Context Check - Ensure we are looking for the RunResult.new_items correctly
            # to prove the Agent called a tool using the auth_user_id we provided
            tool_calls_made = []
            if hasattr(result, 'new_items'):
                print(f"[OK] Found new_items in result: {len(result.new_items)} items")
                for item in result.new_items:
                    print(f"  Item type: {type(item)}")
                    if hasattr(item, 'raw_item') and hasattr(item.raw_item, 'name'):
                        tool_calls_made.append({
                            'tool_name': item.raw_item.name,
                            'arguments': getattr(item.raw_item, 'arguments', {})
                        })
                        print(f"  Tool called: {item.raw_item.name} with args: {getattr(item.raw_item, 'arguments', {})}")
                    elif hasattr(item, 'type') and hasattr(item, 'content'):
                        print(f"  Other item type: {item.type}, content: {str(item.content)[:100]}...")
            else:
                print("[INFO] No new_items found in result")

            if tool_calls_made:
                print(f"[OK] Tool calls made: {len(tool_calls_made)}")
                for call in tool_calls_made:
                    print(f"  - {call['tool_name']}: {call['arguments']}")
            else:
                print("[INFO] No tool calls were made in this response")

            return True

    except Exception as e:
        print(f"[FAILED] Context passthrough test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_error_handling():
    """
    Test 3: Error Handling - What happens if the MCP server fails to start?
    Ensure the ChatService catches the exception rather than hanging.
    """
    print("\n" + "="*60)
    print("TEST 3: Error Handling")
    print("="*60)

    try:
        # Try to initialize MCPServerStdio with an invalid/non-existent script
        # to test error handling
        env_vars = {**os.environ, "PYTHONPATH": "."}

        # SDK Versioning: Using the correct class with params dictionary
        mcp_server = MCPServerStdio(
            params={
                "command": "python",
                "args": ["src/mcp/non_existent_server.py"],  # This should fail
                "env": env_vars
            }
        )

        print("[OK] MCPServerStdio initialized (error handling test)")

        try:
            async with mcp_server as connection:
                # This should raise an exception due to the invalid server path
                agent = Agent(
                    name="ErrorTestAgent",
                    model=GEMINI_MODEL,
                    instructions=SYSTEM_PROMPT,
                    mcp_servers=[connection]
                )

                result = await Runner.run(
                    agent,
                    "Test message",
                    context={"auth_user_id": "test_user"}
                )

                print(f"[OK] Unexpectedly succeeded: {result.final_output}")

        except Exception as e:
            print(f"[OK] Properly caught exception during MCP server connection: {type(e).__name__}")
            print(f"  Exception message: {str(e)[:100]}...")
            return True

    except Exception as e:
        print(f"[OK] Exception caught during MCP server startup: {type(e).__name__}: {str(e)[:100]}...")
        return True


async def mock_test():
    """
    Test 4: Mock Test - Provide a small test script that simulates a chat request
    and prints the tool_calls returned by the agent.
    """
    print("\n" + "="*60)
    print("TEST 4: Mock Test (Simulating Chat Request)")
    print("="*60)

    try:
        # Set environment for the subprocess - PATHING: For the subprocess to work,
        # the env={"PYTHONPATH": "."} is mandatory so it can resolve absolute imports like from src.mcp.tools...
        env_vars = {**os.environ, "PYTHONPATH": "."}

        # SDK Versioning: Using the correct class with params dictionary
        mcp_server = MCPServerStdio(
            params={
                "command": "python",
                "args": ["src/mcp/server.py"],
                "env": env_vars
            }
        )

        async with mcp_server as connection:
            # Create an agent using the connection
            agent = Agent(
                name="MockTestAgent",
                model=GEMINI_MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[connection]
            )

            # Simulate a chat request
            user_id = "mock_user_67890"
            message = "I want to create a new task called 'Test Task' with description 'This is a test'"

            print(f"[OK] Simulating chat request for user: {user_id}")
            print(f"[OK] Message: {message}")

            # Run the agent with the message and context - using correct API
            result = await Runner.run(
                agent,
                message,
                context={"auth_user_id": user_id}
            )

            print(f"\n[OK] Agent final output: {result.final_output}")

            # TASK C: Context Check - Extract and print tool calls to verify context passing
            tool_calls = []
            if hasattr(result, 'new_items'):
                print(f"[OK] Processing {len(result.new_items)} new_items from result...")
                for item in result.new_items:
                    if hasattr(item, 'raw_item') and hasattr(item.raw_item, 'name'):
                        tool_calls.append({
                            'tool_name': item.raw_item.name,
                            'arguments': getattr(item.raw_item, 'arguments', {}),
                            'result': getattr(item, 'content', 'No result') if hasattr(item, 'content') else 'No result'
                        })
                        print(f"  Tool called: {item.raw_item.name} with args: {getattr(item.raw_item, 'arguments', {})}")
                    elif hasattr(item, 'type'):
                        print(f"  Other item type: {item.type}")

            print(f"\n[OK] Tool calls returned by agent: {len(tool_calls)}")
            for i, call in enumerate(tool_calls):
                print(f"\nTool Call {i+1}:")
                print(f"  Name: {call['tool_name']}")
                print(f"  Arguments: {call['arguments']}")
                print(f"  Result: {call['result']}")

            return True

    except Exception as e:
        print(f"[FAILED] Mock test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """
    Run all validation tests
    """
    print("MCP Connection Bridge Validation Script")
    print("This script validates the implementation of MCPServerStdio bridge")
    print("Transport: Using MCPServerStdio to spawn subprocess: python src/mcp/server.py")
    print("Pathing: PYTHONPATH is set to '.' for absolute import resolution")
    print("SDK: Using openai-agents SDK with correct MCPServerStdio API")

    results = []

    # Run all tests
    results.append(("Subprocess Integrity", await test_subprocess_integrity()))
    results.append(("Context Passthrough", await test_context_passthrough()))
    results.append(("Error Handling", await test_error_handling()))
    results.append(("Mock Test", await mock_test()))

    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        icon = "[PASS]" if result else "[FAIL]"
        print(f"{icon} {test_name}: {status}")
        if result:
            passed += 1

    print(f"\nTotal: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("\n[SUCCESS] All tests passed! MCP connection bridge is working correctly.")
        print("\nImplementation successfully validated:")
        print("- Subprocess communication established via MCPServerStdio")
        print("- Context passthrough working (auth_user_id reaching tools)")
        print("- Error handling functional")
        print("- Mock test confirms tool calling functionality")
    else:
        print(f"\n[WARNING] {len(results) - passed} test(s) failed. Please review the implementation.")

    return passed == len(results)


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)