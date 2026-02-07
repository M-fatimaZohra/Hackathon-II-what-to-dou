from fastapi import APIRouter, Depends, HTTPException, status

from src.database.db import get_session
from src.services.chat_service import get_chat_response
from src.middleware.auth_handler import get_verified_user
from src.schema.chat_models import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_verified_user)
):
    """
    Chat endpoint that processes natural language input for task management.

    Args:
        user_id: The ID of the authenticated user (from path)
        request: The chat request containing message and conversation_id
        current_user_id: The ID of the authenticated user (from JWT, verified against path)

    Returns:
        ChatResponse: The AI's response with conversation ID and any tool calls
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    # Determine conversation ID - use provided one from request or default to 1 if None
    # The service layer should handle None case appropriately
    conversation_id = request.conversation_id if request.conversation_id is not None else 1

    # Call the chat service to get the AI response
    response = await get_chat_response(
        user_id=user_id,
        conversation_id=conversation_id,
        message=request.message
    )

    return response