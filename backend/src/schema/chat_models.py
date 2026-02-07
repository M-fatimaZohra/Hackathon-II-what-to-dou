from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """
    Request model for the AI Chatbot endpoint.
    Defines the structure for incoming chat requests.
    """
    conversation_id: Optional[int] = Field(
        default=None,
        description="The ID of the existing conversation session, or None for a new session"
    )
    message: str = Field(
        description="The user's natural language input message"
    )


class ToolCallInfo(BaseModel):
    """
    Helper model to capture the details of an MCP tool invocation.
    Contains information about a specific tool call made by the AI agent.
    """
    tool_name: str = Field(
        description="The name of the MCP tool being called"
    )
    arguments: Dict[str, Any] = Field(
        description="The arguments passed to the MCP tool"
    )


class ChatResponse(BaseModel):
    """
    Response model for the AI Chatbot endpoint.
    Defines the structure for outgoing chat responses.
    """
    conversation_id: int = Field(
        description="The ID of the conversation session, either provided or newly created"
    )
    response: str = Field(
        description="The AI assistant's text response to the user's message"
    )
    tool_calls: List[ToolCallInfo] = Field(
        default_factory=list,
        description="List of tool calls made by the AI agent during processing"
    )