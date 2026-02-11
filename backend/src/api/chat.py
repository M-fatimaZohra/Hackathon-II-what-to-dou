import os
import json
import time
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from sqlmodel import Session

# Import proper types from OpenAI Agents SDK for type-safe event handling
from agents import RawResponsesStreamEvent, RunItemStreamEvent, AgentUpdatedStreamEvent

from src.database.db import get_session
from src.services.chat_service import get_chat_response, run_agent_workflow_streamed
from src.services.conversation_service import ConversationService
from src.middleware.auth_handler import get_verified_user, get_current_user
from src.schema.chat_models import ChatRequest, ChatResponse

# Load environment variables
load_dotenv(override=True)

router = APIRouter()


async def stream_chat_response(user_id: str, conversation_id: int, message: str):
    """
    Generator function that streams chat responses as SSE events.

    Yields OpenAI Responses API events using Atomic Response Initialization:
    1. thread.created - Thread anchor for conversation
    2. conversation.item.created - User's message (content type: "text")
    3. response.created - Atomic init with assistant output item pre-populated
    4. response.output_text.delta - Stream text chunks in real-time (repeated)
    5. response.output_text.done - Finalize streamed text
    6. response.output_item.done - Finalize message item
    7. response.done - Commit to history

    Uses Atomic Response Initialization: response.created includes the assistant
    output item upfront, eliminating separate output_item.added and content_part
    events. This matches ChatKit v1.5.0 expectations.

    Args:
        user_id: The ID of the authenticated user
        conversation_id: The ID of the conversation
        message: The user's input message

    Yields:
        SSE formatted events compatible with OpenAI Responses API / ChatKit SDK
    """

    # Event ID counter for unique SSE event IDs
    event_counter = 0
    def next_event_id():
        nonlocal event_counter
        event_counter += 1
        return f"evt_{event_counter}"

    try:
        thread_id = str(conversation_id)
        response_id = f"resp_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        output_item_id = f"item_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        # 1. Thread Anchor - Establishes conversation context
        thread_event = {
            "id": next_event_id(),
            "type": "thread.created",
            "thread": {
                "id": thread_id
            }
        }
        yield f"data: {json.dumps(thread_event)}\n\n"

        # 2. User Message - conversation.item.created
        # Content type MUST be "text" (not "input_text") for ChatKit to render it
        user_item_event = {
            "id": next_event_id(),
            "type": "conversation.item.created",
            "item": {
                "id": f"msg-user-{conversation_id}",
                "type": "message",
                "role": "user",
                "content": [{"type": "text", "text": message}],
                "status": "completed"
            }
        }
        yield f"data: {json.dumps(user_item_event)}\n\n"

        # 3. Atomic Response Created - response.created
        # CRITICAL: Pre-populate output array with the assistant item immediately
        # This tells ChatKit the message container exists from the start
        response_created_event = {
            "id": next_event_id(),
            "type": "response.created",
            "response": {
                "id": response_id,
                "object": "realtime.response",
                "status": "in_progress",
                "output": [{
                    "id": output_item_id,
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": ""}]
                }]
            }
        }
        yield f"data: {json.dumps(response_created_event)}\n\n"

        # 4. Stream Text Deltas - response.output_text.delta
        # Real-time streaming of assistant response
        assistant_response_text = ""

        async for event_data in run_agent_workflow_streamed(user_id, message, conversation_id):

            # Handle RawResponsesStreamEvent (text deltas from OpenAI)
            if isinstance(event_data, RawResponsesStreamEvent):
                # Check if the data is ResponseTextDeltaEvent
                if isinstance(event_data.data, ResponseTextDeltaEvent):
                    # Accumulate text for final message
                    assistant_response_text += event_data.data.delta

                    # Send response.output_text.delta event for real-time streaming display
                    # CRITICAL: Must link to response_id, output_index, content_index
                    text_delta_event = {
                        "id": next_event_id(),
                        "type": "response.output_text.delta",
                        "response_id": response_id,
                        "item_id": output_item_id,
                        "output_index": 0,
                        "content_index": 0,
                        "delta": event_data.data.delta
                    }
                    yield f"data: {json.dumps(text_delta_event)}\n\n"

            # Handle RunItemStreamEvent (tool calls from Agents SDK)
            elif isinstance(event_data, RunItemStreamEvent):
                # Check if this is a tool_call_item
                if hasattr(event_data, 'item') and hasattr(event_data.item, 'type'):
                    if event_data.item.type == "tool_call_item":
                        tool_name = getattr(event_data.item, 'name', 'unknown')
                        # Optional: Send tool execution event if needed
                        pass

            # Handle AgentUpdatedStreamEvent (agent state changes)
            elif isinstance(event_data, AgentUpdatedStreamEvent):
                # Optional: Log or handle agent updates if needed
                pass

        # 5. Output Text Done - response.output_text.done
        # Finalizes the streamed text output
        output_text_done_event = {
            "id": next_event_id(),
            "type": "response.output_text.done",
            "response_id": response_id,
            "item_id": output_item_id,
            "output_index": 0,
            "content_index": 0,
            "text": assistant_response_text
        }
        yield f"data: {json.dumps(output_text_done_event)}\n\n"

        # 6. Output Item Done - response.output_item.done
        # Finalizes the message item with complete content
        output_item_done_event = {
            "id": next_event_id(),
            "type": "response.output_item.done",
            "response_id": response_id,
            "output_index": 0,
            "item": {
                "id": output_item_id,
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{
                    "type": "text",
                    "text": assistant_response_text
                }]
            }
        }
        yield f"data: {json.dumps(output_item_done_event)}\n\n"

        # 7. Response Done - response.done
        # Commits the complete response to history
        response_done_event = {
            "id": next_event_id(),
            "type": "response.done",
            "response": {
                "id": response_id,
                "object": "realtime.response",
                "status": "completed",
                "output": [{
                    "id": output_item_id,
                    "type": "message",
                    "role": "assistant",
                    "status": "completed",
                    "content": [{
                        "type": "text",
                        "text": assistant_response_text
                    }]
                }]
            }
        }
        yield f"data: {json.dumps(response_done_event)}\n\n"

    except Exception as e:
        # Send error event
        error_data = {
            "id": next_event_id(),
            "type": "error",
            "error": {
                "message": str(e)
            }
        }
        yield f"data: {json.dumps(error_data)}\n\n"


@router.post("/{user_id}/chat")
async def chat_endpoint_streaming(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Streaming chat endpoint that processes natural language input for task management.

    Returns Server-Sent Events (SSE) stream compatible with ChatKit SDK protocol.

    Args:
        user_id: The ID of the authenticated user (from path)
        request: The chat request containing message and conversation_id
        current_user_id: The ID of the authenticated user (from JWT)
        session: Database session for conversation management

    Returns:
        StreamingResponse: SSE stream with chat responses and tool calls
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Handle conversation_id: create new conversation if None, or verify existing one
    if request.conversation_id is None:
        # Create a new conversation for this user
        conversation = ConversationService.create_conversation(session, user_id)
        conversation_id = conversation.id
    else:
        # Verify that the provided conversation belongs to the user
        try:
            ConversationService.get_history(session, request.conversation_id, user_id)
            conversation_id = request.conversation_id
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conversation not found or does not belong to the user"
            )

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