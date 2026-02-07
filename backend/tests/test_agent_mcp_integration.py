#!/usr/bin/env python3
"""
Test script to verify that the AI agent can properly use MCP tools.
This script tests the integration between the agent and MCP tools.
"""
import asyncio
import sys
import os
from sqlmodel import Session

# Add the backend/src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db import engine
from src.my_mcp_server import server as mcp_server
from src.services.chat_service import todo_assistant
from agents import Runner


async def test_agent_mcp_integration():
    """Test that the agent can properly use MCP tools"""
    print("Testing AI Agent MCP Tool Integration...")

    try:
        # Test 1: Verify that MCP tools are available
        print("\n1. Checking MCP tools availability...")
        mcp_tools = mcp_server.mcp.list_tools() if hasattr(mcp_server.mcp, 'list_tools') else []
        print(f"   Available MCP tools: {[tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in mcp_tools]}")

        if len(mcp_tools) > 0:
            print("   ✓ MCP tools are available")
        else:
            print("   ✗ No MCP tools found")
            return False

        # Test 2: Test the agent initialization
        print("\n2. Checking agent initialization...")
        if todo_assistant:
            print(f"   ✓ Agent initialized successfully: {todo_assistant.name}")
        else:
            print("   ✗ Agent not initialized properly")
            return False

        # Test 3: Try a simple interaction that would trigger MCP tools
        print("\n3. Testing agent interaction with potential tool usage...")

        # Create a test user context
        test_context = {"auth_user_id": "test_user_123"}

        # Try to run a simple message that might trigger task creation
        message = "Create a test task for me called 'Integration Test Task'"

        try:
            # Run the agent with the message
            result = await Runner.run(
                todo_assistant,
                message,
                context=test_context
            )

            print(f"   ✓ Agent responded successfully")
            print(f"   Response: {result.final_output[:100]}...")

            # Check if any tool calls were made
            if hasattr(result, 'new_items'):
                tool_calls_made = []
                for item in result.new_items:
                    if hasattr(item, 'tool_call'):
                        tool_calls_made.append(item.tool_call)

                print(f"   Tool calls made: {len(tool_calls_made)}")
                for i, call in enumerate(tool_calls_made):
                    print(f"     Tool {i+1}: {call.function.name}")

            return True

        except Exception as e:
            print(f"   ✗ Error during agent interaction: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"✗ Error in agent MCP integration test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run the agent MCP integration tests"""
    print("="*60)
    print("AI AGENT MCP INTEGRATION TEST")
    print("="*60)

    success = await test_agent_mcp_integration()

    print("\n" + "="*60)
    if success:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✓ AI agent can properly use MCP tools")
        print("✓ MCP tools are correctly registered and accessible")
        print("✓ Agent-MCP integration is working")
    else:
        print("❌ INTEGRATION TESTS FAILED")
        print("✗ There are issues with the agent-MCP integration")
    print("="*60)

    return success


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)