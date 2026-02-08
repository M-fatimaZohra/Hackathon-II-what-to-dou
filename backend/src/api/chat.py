import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv

from src.database.db import get_session
from src.services.chat_service import get_chat_response, run_agent_workflow_streamed
from src.middleware.auth_handler import get_verified_user
from src.schema.chat_models import ChatRequest, ChatResponse

# Load environment variables
load_dotenv(override=True)

router = APIRouter()

# Initialize OpenAI client for ChatKit
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SessionResponse(BaseModel):
    """Response model for session endpoint"""
    client_secret: str


@router.post("/{user_id}/chat/session", response_model=SessionResponse)
async def create_chat_session(
    user_id: str,
    current_user_id: str = Depends(get_verified_user)
):
    """
    Session exchange endpoint for ChatKit Advanced Integration.

    Creates a ChatKit session using OpenAI's ChatKit API and returns a client_secret
    for the frontend to use with the ChatKit SDK.

    Args:
        user_id: The ID of the authenticated user (from path)
        current_user_id: The ID of the authenticated user (from JWT, verified against path)

    Returns:
        SessionResponse: Contains client_secret for ChatKit SDK
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Get CHATKIT_WORKFLOW_ID from environment
    workflow_id = os.getenv("CHATKIT_WORKFLOW_ID")
    if not workflow_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CHATKIT_WORKFLOW_ID not configured"
        )

    # Verify OpenAI API key is configured
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OPENAI_API_KEY not configured"
        )

    try:
        # Create ChatKit session using OpenAI SDK with correct parameters
        session = client.beta.chatkit.sessions.create(
            user=user_id,
            workflow={'id': workflow_id}
        )

        # Return client_secret as expected by frontend
        return SessionResponse(client_secret=session.client_secret)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ChatKit session: {str(e)}"
        )


async def stream_chat_response(user_id: str, conversation_id: int, message: str):
    """
    Generator function that streams chat responses as SSE events.

    Yields raw OpenAI Responses API events for ChatKit SDK compatibility.
    The frontend useChatKit hook expects standard OpenAI event structures.

    Args:
        user_id: The ID of the authenticated user
        conversation_id: The ID of the conversation
        message: The user's input message

    Yields:
        SSE formatted events with raw OpenAI Responses API data
    """
    try:
        # Use the streaming function that yields raw event.data
        async for event_data in run_agent_workflow_streamed(user_id, message, conversation_id):
            # Serialize the raw event data to JSON for SSE
            # ChatKit SDK expects standard OpenAI Responses API format
            if isinstance(event_data, ResponseTextDeltaEvent):
                # Serialize ResponseTextDeltaEvent to dict
                event_dict = {
                    "type": "response.output_text.delta",
                    "delta": event_data.delta
                }
                yield f"data: {json.dumps(event_dict)}\n\n"

            elif hasattr(event_data, 'type'):
                # Handle other event types (tool_start, tool_end, error)
                if event_data.type == "tool_start":
                    event_dict = {
                        "type": "tool_start",
                        "tool_name": event_data.tool.name if hasattr(event_data, 'tool') else "unknown"
                    }
                    yield f"data: {json.dumps(event_dict)}\n\n"

                elif event_data.type == "tool_end":
                    event_dict = {
                        "type": "tool_end",
                        "tool_name": event_data.tool.name if hasattr(event_data, 'tool') else "unknown",
                        "output": getattr(event_data, 'output', None)
                    }
                    yield f"data: {json.dumps(event_dict)}\n\n"

                elif event_data.type == "error":
                    event_dict = {
                        "type": "error",
                        "message": getattr(event_data, 'message', str(event_data))
                    }
                    yield f"data: {json.dumps(event_dict)}\n\n"

    except Exception as e:
        # Send error event
        error_data = {
            "type": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"


@router.post("/{user_id}/chat")
async def chat_endpoint_streaming(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_verified_user)
):
    """
    Streaming chat endpoint that processes natural language input for task management.

    Returns Server-Sent Events (SSE) stream compatible with ChatKit SDK protocol.

    Args:
        user_id: The ID of the authenticated user (from path)
        request: The chat request containing message and conversation_id
        current_user_id: The ID of the authenticated user (from JWT, verified against path)

    Returns:
        StreamingResponse: SSE stream with chat responses and tool calls
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Determine conversation ID - use provided one from request or default to 1 if None
    conversation_id = request.conversation_id if request.conversation_id is not None else 1

    # Return streaming response with SSE
    return StreamingResponse(
        stream_chat_response(user_id, conversation_id, request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable buffering for nginx
        }
    )