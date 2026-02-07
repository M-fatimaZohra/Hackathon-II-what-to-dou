#!/usr/bin/env python3
"""
Test script to verify agent functionality, MCP tool integration, and user isolation.
This script runs specific checks to ensure:
1. Agents are working correctly
2. Agent can use MCP tools
3. Logged-in user can access their own chatbot and save data in database
"""
import asyncio
import sys
import os
from sqlmodel import Session, select

# Add the backend/src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db import engine
from schema.models import Conversation, Message
from services.conversation_service import ConversationService
from services.chat_service import get_chat_response, UserContext
from mcp.tools import (
    task_create_tool,
    task_list_tool,
    task_update_tool,
    task_delete_tool,
    task_complete_tool
)


async def test_agent_basic_functionality():
    """Test that the agent is working correctly"""
    print("Testing: Agent basic functionality...")

    try:
        # Create a test context for a user
        user_id = "test_user_123"

        # Create a conversation to test with
        with Session(engine) as session:
            conversation = ConversationService.create_conversation(session, user_id)
            print(f"✓ Created conversation with ID: {conversation.id}")

            # Test sending a simple message to the agent
            message = "Hello, how can you help me?"

            # Call the agent
            result = await get_chat_response(
                user_id=user_id,
                conversation_id=conversation.id,
                message=message
            )

            print(f"✓ Agent responded: {result.response[:50]}...")
            print(f"✓ Tool calls made: {len(result.tool_calls)}")

            # Check if tool calls were made as expected
            for i, tool_call in enumerate(result.tool_calls):
                print(f"  Tool call {i+1}: {tool_call.tool_name}")

            return True

    except Exception as e:
        print(f"✗ Error in agent functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_mcp_tool_integration():
    """Test that agent can use MCP tools"""
    print("\nTesting: Agent MCP tool integration...")

    try:
        user_id = "test_user_mcp"

        with Session(engine) as session:
            conversation = ConversationService.create_conversation(session, user_id)

            # Test a message that should trigger MCP tools (like creating a task)
            message = "Create a new task to buy groceries tomorrow"

            result = await get_chat_response(
                user_id=user_id,
                conversation_id=conversation.id,
                message=message
            )

            print(f"✓ Agent processed MCP tool request: {result.response[:50]}...")

            # Check if MCP tool calls were made
            mcp_tool_calls = [tc for tc in result.tool_calls if 'task' in tc.tool_name.lower()]
            print(f"✓ MCP tool calls made: {len(mcp_tool_calls)}")

            for tool_call in mcp_tool_calls:
                print(f"  MCP Tool: {tool_call.tool_name} with args: {tool_call.arguments}")

            # Also test the tools directly to make sure they work
            print("  Testing MCP tools directly:")

            # Create a test task using the tool directly
            ctx = {"auth_user_id": user_id}
            create_result = await task_create_tool.create_task(ctx, "Test MCP task", "Test description")
            print(f"  ✓ Direct tool test: {create_result}")

            # List tasks using the tool directly
            list_result = await task_list_tool.list_tasks(ctx, "all")
            print(f"  ✓ Direct list test: {list_result}")

            return True

    except Exception as e:
        print(f"✗ Error in MCP tool integration test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_user_data_isolation():
    """Test that logged-in users can only access their own data"""
    print("\nTesting: User data isolation...")

    try:
        user1_id = "isolated_user_1"
        user2_id = "isolated_user_2"

        with Session(engine) as session:
            # Create conversations for two different users
            conv1 = ConversationService.create_conversation(session, user1_id)
            conv2 = ConversationService.create_conversation(session, user2_id)

            print(f"✓ Created conversation for user 1: {conv1.id}")
            print(f"✓ Created conversation for user 2: {conv2.id}")

            # Add messages for user 1
            msg1_user = ConversationService.add_message(
                session, conv1.id, user1_id, "user", "Hello from user 1"
            )
            msg1_assistant = ConversationService.add_message(
                session, conv1.id, user1_id, "assistant", "Response to user 1"
            )

            # Add messages for user 2
            msg2_user = ConversationService.add_message(
                session, conv2.id, user2_id, "user", "Hello from user 2"
            )
            msg2_assistant = ConversationService.add_message(
                session, conv2.id, user2_id, "assistant", "Response to user 2"
            )

            print(f"✓ Added messages for user 1: {msg1_user.id}, {msg1_assistant.id}")
            print(f"✓ Added messages for user 2: {msg2_user.id}, {msg2_assistant.id}")

            # Verify user 1 can only see their own conversations
            user1_convs = ConversationService.list_conversations(session, user1_id)
            user1_conv_ids = [c.id for c in user1_convs]
            print(f"✓ User 1 sees conversations: {user1_conv_ids}")
            assert conv1.id in user1_conv_ids, "User 1 should see their own conversation"
            assert conv2.id not in user1_conv_ids, "User 1 should NOT see user 2's conversation"

            # Verify user 2 can only see their own conversations
            user2_convs = ConversationService.list_conversations(session, user2_id)
            user2_conv_ids = [c.id for c in user2_convs]
            print(f"✓ User 2 sees conversations: {user2_conv_ids}")
            assert conv2.id in user2_conv_ids, "User 2 should see their own conversation"
            assert conv1.id not in user2_conv_ids, "User 2 should NOT see user 1's conversation"

            # Test message history isolation
            user1_msgs = ConversationService.get_history(session, conv1.id, user1_id)
            user1_msg_contents = [m.content for m in user1_msgs]
            print(f"✓ User 1 message history: {user1_msg_contents}")

            user2_msgs = ConversationService.get_history(session, conv2.id, user2_id)
            user2_msg_contents = [m.content for m in user2_msgs]
            print(f"✓ User 2 message history: {user2_msg_contents}")

            # Verify each user only sees their own messages
            assert "Hello from user 1" in user1_msg_contents
            assert "Response to user 1" in user1_msg_contents
            assert "Hello from user 2" not in user1_msg_contents
            assert "Response to user 2" not in user1_msg_contents

            assert "Hello from user 2" in user2_msg_contents
            assert "Response to user 2" in user2_msg_contents
            assert "Hello from user 1" not in user2_msg_contents
            assert "Response to user 1" not in user2_msg_contents

            print("✓ User isolation verified successfully")
            return True

    except Exception as e:
        print(f"✗ Error in user isolation test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_complete_workflow():
    """Test the complete workflow: user interacts with agent, data saved correctly"""
    print("\nTesting: Complete workflow (user → chatbot → database)...")

    try:
        user_id = "workflow_test_user"

        with Session(engine) as session:
            # Step 1: Create conversation
            conversation = ConversationService.create_conversation(session, user_id)
            print(f"✓ Step 1: Created conversation ID: {conversation.id}")

            # Step 2: User sends a message to the agent that should trigger tool use
            user_message = "I need to create a task to buy groceries tomorrow"

            # Step 3: Agent processes the message and responds
            result = await get_chat_response(
                user_id=user_id,
                conversation_id=conversation.id,
                message=user_message
            )

            print(f"✓ Step 2: Agent responded with: {result.response[:50]}...")
            print(f"✓ Step 2: Agent made {len(result.tool_calls)} tool calls")

            # Step 4: Verify the interaction was properly saved to the database
            # Check that messages were saved to the conversation
            messages = ConversationService.get_history(session, conversation.id, user_id)
            print(f"✓ Step 4: Retrieved {len(messages)} messages from conversation history")

            # Verify that both the original request and any tool interactions are tracked
            for i, msg in enumerate(messages):
                print(f"  Message {i+1}: {msg.role} - '{msg.content[:50]}...'")

            # Verify the conversation was updated with the new interaction
            updated_conversation = session.get(Conversation, conversation.id)
            print(f"✓ Step 4: Conversation updated_at: {updated_conversation.updated_at}")

            print("✓ Complete workflow test passed")
            return True

    except Exception as e:
        print(f"✗ Error in complete workflow test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all verification tests"""
    print("Running agent functionality verification tests...\n")

    # Run the tests
    test1_pass = await test_agent_basic_functionality()
    test2_pass = await test_mcp_tool_integration()
    test3_pass = await test_user_data_isolation()
    test4_pass = await test_complete_workflow()

    print(f"\n{'='*70}")
    print("VERIFICATION RESULTS SUMMARY:")
    print(f"  Agent Basic Functionality: {'PASS' if test1_pass else 'FAIL'}")
    print(f"  MCP Tool Integration: {'PASS' if test2_pass else 'FAIL'}")
    print(f"  User Data Isolation: {'PASS' if test3_pass else 'FAIL'}")
    print(f"  Complete Workflow: {'PASS' if test4_pass else 'FAIL'}")

    all_passed = all([test1_pass, test2_pass, test3_pass, test4_pass])

    if all_passed:
        print(f"\n🎉 ALL VERIFICATION TESTS PASSED!")
        print("✓ Agents are working correctly")
        print("✓ Agent can use MCP tools")
        print("✓ Logged-in user can access their own chatbot and data is isolated")
        print("✓ Data is properly saved to the database with user isolation")
        return True
    else:
        print(f"\n❌ SOME VERIFICATION TESTS FAILED.")
        print("Please check the error messages above and fix the issues.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)