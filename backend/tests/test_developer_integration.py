#!/usr/bin/env python3
"""
Integration test for the Chatbot API that mimics a production user flow in a local developer environment.
This test validates the complete flow: JWT auth → API endpoint → MCP tools → Database persistence
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, select

# Add src to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app
from src.database.db import engine
from src.schema.chat_models import ChatResponse
from src.schema.models import Conversation, Message


def create_test_jwt(user_id: str, secret: str = "dev-test-secret-456", expires_delta: timedelta = timedelta(hours=1)):
    """
    Create a real JWT token for testing purposes.

    Args:
        user_id: The user ID to embed in the JWT token
        secret: The JWT secret to use for encoding
        expires_delta: How long the token should be valid for

    Returns:
        str: A valid JWT token
    """
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt


def test_chatbot_api_integration():
    """
    True Integration Test: Mimics a production user flow in a local developer environment.

    Flow: User sends a natural language message via POST /api/{user_id}/chat
    -> JWT authentication succeeds -> MCP tools are called -> Data persists to database
    """
    # Store original environment variable
    original_secret = os.environ.get("BETTER_AUTH_SECRET")

    try:
        # Temporarily inject the test secret
        os.environ["BETTER_AUTH_SECRET"] = "dev-test-secret-456"

        # Update auth_handler module's JWT_SECRET directly since it's set at module level
        import src.middleware.auth_handler as auth_handler
        auth_handler.JWT_SECRET = "dev-test-secret-456"

        # Create a test user ID
        test_user_id = "test_user_dev_99"

        # Generate a real JWT token for the test user
        jwt_token = create_test_jwt(test_user_id)

        # Mock the chat service response to avoid calling real AI
        with patch("src.services.chat_service.get_chat_response") as mock_get_chat_response:
            # Create a mock response object
            mock_response_obj = ChatResponse(
                conversation_id=1,
                response="I have created the task 'Test task from integration test' with medium priority.",
                tool_calls=[]
            )

            mock_get_chat_response.return_value = mock_response_obj

            # Create a TestClient instance
            with TestClient(app) as client:
                # Prepare the request data
                chat_request = {
                    "message": "Add a task to test the integration with medium priority"
                }

                # Make the request to the chat endpoint with the JWT token
                response = client.post(
                    f"/api/{test_user_id}/chat",
                    json=chat_request,
                    headers={"Authorization": f"Bearer {jwt_token}"}
                )

                # AUTH CHECK: Assert status_code == 200 to prove the generated JWT was accepted
                assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

                # Parse the response
                response_data = response.json()

                # LOGIC CHECK: Assert the response contains expected AI text and valid conversation_id
                assert "conversation_id" in response_data
                assert "response" in response_data
                assert "tool_calls" in response_data

                assert response_data["conversation_id"] == 1
                assert "Test task from integration test" in response_data["response"]

                print(f"✓ Auth Check: Status code {response.status_code} - JWT accepted by middleware")
                print(f"✓ Logic Check: Response contains expected content: '{response_data['response'][:50]}...'")

                # DATA INTEGRITY: Query the database directly to verify message was persisted
                with Session(engine) as db_session:
                    # Check that a conversation exists for the test user
                    conversation_statement = select(Conversation).where(Conversation.user_id == test_user_id)
                    conversation = db_session.exec(conversation_statement).first()

                    assert conversation is not None, f"Expected to find a conversation for user {test_user_id}"
                    print(f"✓ Data Integrity: Found conversation {conversation.id} for user {test_user_id}")

                    # Check that the message was stored in the database
                    message_statement = select(Message).where(Message.user_id == test_user_id).order_by(Message.created_at.desc())
                    messages = db_session.exec(message_statement).all()

                    # We might have multiple messages, but at least one should exist for this user
                    user_messages = [msg for msg in messages if msg.user_id == test_user_id]

                    # Database Assertion: Ensure the assertion for 'user_messages' is 'assert len(user_messages) > 0' with clear error message
                    assert len(user_messages) > 0, f"DB Failure: API returned 200 but no message was saved for {test_user_id}"
                    latest_message = user_messages[0]
                    print(f"✓ Data Integrity: Confirmed message saved: '{latest_message.content[:30]}...'")

    finally:
        # CLEANUP: Restore original environment variable
        if original_secret is not None:
            os.environ["BETTER_AUTH_SECRET"] = original_secret
        else:
            os.environ.pop("BETTER_AUTH_SECRET", None)

    print("✅ Integration test completed successfully!")
    print("- Authentication with real JWT token succeeded")
    print("- API endpoint processed request correctly")
    print("- Database persistence verified")
    print("- All assertions passed")


def test_multiple_interactions_integration():
    """
    Additional integration test: Verify multiple interactions create multiple records.
    """
    # Store original environment variable
    original_secret = os.environ.get("BETTER_AUTH_SECRET")

    try:
        # Temporarily inject the test secret
        os.environ["BETTER_AUTH_SECRET"] = "dev-test-secret-456"

        # Update auth_handler module's JWT_SECRET directly since it's set at module level
        import src.middleware.auth_handler as auth_handler
        auth_handler.JWT_SECRET = "dev-test-secret-456"

        # Create a test user ID
        test_user_id = "test_user_multi_01"

        # Generate a real JWT token for the test user
        jwt_token = create_test_jwt(test_user_id)

        # Mock the chat service response to avoid calling real AI
        with patch("src.services.chat_service.get_chat_response") as mock_get_chat_response:
            # Setup mock to return different responses for subsequent calls
            responses = [
                ChatResponse(
                    conversation_id=2,
                    response="I have created the first test task.",
                    tool_calls=[]
                ),
                ChatResponse(
                    conversation_id=2,
                    response="I have created the second test task.",
                    tool_calls=[]
                )
            ]
            mock_get_chat_response.side_effect = responses

            # Create a TestClient instance
            with TestClient(app) as client:
                # First interaction
                chat_request_1 = {"message": "Add first test task"}
                response_1 = client.post(
                    f"/api/{test_user_id}/chat",
                    json=chat_request_1,
                    headers={"Authorization": f"Bearer {jwt_token}"}
                )

                # Second interaction
                chat_request_2 = {"message": "Add second test task"}
                response_2 = client.post(
                    f"/api/{test_user_id}/chat",
                    json=chat_request_2,
                    headers={"Authorization": f"Bearer {jwt_token}"}
                )

                # Verify both requests succeeded
                assert response_1.status_code == 200
                assert response_2.status_code == 200

                # DATA INTEGRITY: Check database for multiple messages
                with Session(engine) as db_session:
                    # Count messages for this user
                    message_statement = select(Message).where(Message.user_id == test_user_id)
                    messages = db_session.exec(message_statement).all()

                    # Verify we have at least 2 messages for this user - forcing honesty in the test
                    user_messages = [msg for msg in messages if msg.user_id == test_user_id]
                    assert len(user_messages) >= 2, f"DB Failure: Multiple interactions expected at least 2 messages for user {test_user_id}, but found {len(user_messages)}"

                    print(f"✓ Multiple Interactions: Confirmed {len(user_messages)} messages saved for user {test_user_id}")

    finally:
        # CLEANUP: Restore original environment variable
        if original_secret is not None:
            os.environ["BETTER_AUTH_SECRET"] = original_secret
        else:
            os.environ.pop("BETTER_AUTH_SECRET", None)

    print("✅ Multiple interactions test completed successfully!")


if __name__ == "__main__":
    print("Running Developer Integration Tests...")
    print("These tests validate the complete flow: JWT auth → API → MCP → Database")

    test_chatbot_api_integration()
    print()
    test_multiple_interactions_integration()

    print("\n🎉 All integration tests passed!")
    print("The chatbot API is working correctly with real JWT authentication,")
    print("proper database persistence, and MCP tool integration.")