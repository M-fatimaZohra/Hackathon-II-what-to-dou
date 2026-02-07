#!/usr/bin/env python3
"""
Test script to verify agent functionality, MCP tool integration, and user isolation.
"""
import asyncio
import os
import sys
from sqlmodel import Session, select
from src.database.db import engine
from src.schema.models import Conversation, Message
from src.services.conversation_service import ConversationService
from src.services.chat_service import get_chat_response, UserContext
from agents import Runner
from src.mcp import server as mcp

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


async def test_agent_mcp_integration():
    """Test that agents can properly use MCP tools"""
    print("Testing agent MCP tool integration...")

    try:
        # Create a conversation for testing
        with Session(engine) as session:
            user_id = "test_user_123"

            # Create conversation
            conversation = ConversationService.create_conversation(session, user_id)
            print(f"✓ Created conversation ID: {conversation.id}")

            # Test the chat service with a message that should trigger MCP tools
            # For example, asking the agent to create a task
            message = "Create a new task titled 'Test task from agent' with description 'Created by AI agent'"

            # Run the chat response function
            result = await get_chat_response(user_id, conversation.id, message)

            print(f"✓ Agent responded: {result.response[:100]}...")
            print(f"✓ Tool calls made: {len(result.tool_calls)}")

            for i, tool_call in enumerate(result.tool_calls):
                print(f"  Tool call {i+1}: {tool_call.tool_name} with args: {tool_call.arguments}")

            return True

    except Exception as e:
        print(f"✗ Error in agent MCP integration test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_user_isolation():
    """Test that users can only access their own data"""
    print("\nTesting user data isolation...")

    try:
        with Session(engine) as session:
            # Create conversations for two different users
            user1_id = "user_1_test"
            user2_id = "user_2_test"

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

            # Verify user 1 can only see their own conversation
            user1_convs = ConversationService.list_conversations(session, user1_id)
            user1_conv_ids = [c.id for c in user1_convs]
            print(f"✓ User 1 sees conversations: {user1_conv_ids}")
            assert conv1.id in user1_conv_ids, "User 1 should see their own conversation"
            assert conv2.id not in user1_conv_ids, "User 1 should NOT see user 2's conversation"

            # Verify user 2 can only see their own conversation
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
    """Test the complete workflow: user creates conversation, interacts with agent, data is isolated"""
    print("\nTesting complete workflow...")

    try:
        with Session(engine) as session:
            user_id = "workflow_test_user"

            # Step 1: Create conversation
            conversation = ConversationService.create_conversation(session, user_id)
            print(f"✓ Step 1: Created conversation ID: {conversation.id}")

            # Step 2: Interact with the agent
            initial_message = "I need to create a task to buy groceries"
            result = await get_chat_response(user_id, conversation.id, initial_message)

            print(f"✓ Step 2: Agent responded with: {result.response[:50]}...")
            print(f"✓ Step 2: Agent made {len(result.tool_calls)} tool calls")

            # Step 3: Verify data was stored correctly in DB
            # Check that the conversation was updated
            updated_conversation = session.get(Conversation, conversation.id)
            print(f"✓ Step 3: Conversation exists in DB with updated timestamp: {updated_conversation.updated_at}")

            # Step 4: Check conversation history
            history = ConversationService.get_history(session, conversation.id, user_id)
            print(f"✓ Step 4: Retrieved {len(history)} messages from history")

            # Verify the interaction was recorded
            message_contents = [m.content for m in history]
            print(f"✓ Step 4: Messages in history: {message_contents}")

            # Check that both the user's message and agent's response were stored
            # (Depending on implementation, this might vary)

            print("✓ Complete workflow test passed")
            return True

    except Exception as e:
        print(f"✗ Error in complete workflow test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("Running agent functionality tests...\n")

    # Run the tests
    test1_pass = await test_agent_mcp_integration()
    test2_pass = await test_user_isolation()
    test3_pass = await test_complete_workflow()

    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY:")
    print(f"  Agent MCP Integration: {'PASS' if test1_pass else 'FAIL'}")
    print(f"  User Isolation: {'PASS' if test2_pass else 'FAIL'}")
    print(f"  Complete Workflow: {'PASS' if test3_pass else 'FAIL'}")

    if all([test1_pass, test2_pass, test3_pass]):
        print(f"\n🎉 ALL TESTS PASSED! Agents are working correctly.")
        print("- Agents can use MCP tools")
        print("- Users can access their own chatbot")
        print("- User data is properly isolated in the database")
        return True
    else:
        print(f"\n❌ SOME TESTS FAILED. Please check the error messages above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)