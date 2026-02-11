import os
import sys
from typing import List, Dict, Any, AsyncGenerator
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, set_default_openai_api
from agents.mcp import MCPServerStdio
from agents.result import RunResult
from openai.types.responses import ResponseTextDeltaEvent
from sqlmodel import Session as SQLSession
from src.schema.chat_models import ChatResponse, ToolCallInfo
from src.services.conversation_service import ConversationService
from src.database.db import get_session

# Load environment variables
load_dotenv(override=True)

# Configure OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    set_default_openai_api(OPENAI_API_KEY)

# OpenAI Model Configuration - hardcoded to gpt-4.1-nano
OPENAI_MODEL = "gpt-4.1-nano"


# System prompt for the TodoAssistant agent
SYSTEM_PROMPT = """You are a helpful TodoAssistant that helps users manage their tasks through natural language.
You can create, list, update, delete, and mark tasks as complete based on the user's requests.
Use the available tools to interact with the task management system:

AVAILABLE TOOLS:
- create_task: Add new tasks (requires title, optional description)
- list_tasks: Show existing tasks (optional status filter: "all", "pending", "completed")
- update_task: Modify existing tasks (requires task_id, optional title/description)
- delete_task: Remove tasks (requires task_id)
- complete_task: Mark tasks as completed (requires task_id)

CRITICAL WORKFLOW - TASK LOOKUP BY NAME:
When a user refers to a task by name/title (e.g., "update the grocery task", "delete my meeting task"), you MUST:
1. FIRST call list_tasks to retrieve all the user's tasks
2. THEN examine the results to find the task whose title best matches the user's description
3. FINALLY use the found task's ID to call the appropriate operation (update_task, delete_task, or complete_task)

EXAMPLE SCENARIOS:

User: "Update the grocery task to include eggs"
You: Should call list_tasks first, find the task with title matching "grocery", then call update_task with that task's ID.

User: "Delete the meeting task"
You: Should call list_tasks first, find the task with title matching "meeting", then call delete_task with that task's ID.

User: "Mark the workout task as complete"
You: Should call list_tasks first, find the task with title matching "workout", then call complete_task with that task's ID.

SECURITY RULES:
- Never ask users for task IDs - handle the lookup internally
- Always verify the task belongs to the user (the tools do this automatically)
- Users can only access their own tasks (enforced by AUTH_USER_ID)
- Always respect user data isolation

If the user provides an explicit numeric task ID (e.g., "update task 123"), you can use it directly without lookup."""

from contextlib import contextmanager


async def run_agent_workflow_streamed(user_id: str, message: str, conversation_id: int) -> AsyncGenerator[Any, None]:
    """
    Stream agent workflow responses using Native Responses API Protocol for ChatKit compatibility.

    Yields raw event.data from the OpenAI Agents SDK in standard Responses API format.
    The frontend useChatKit hook expects standard OpenAI event structures.

    Args:
        user_id: The ID of the authenticated user
        message: The user's input message
        conversation_id: The ID of the conversation to fetch history for

    Yields:
        Raw event.data from OpenAI Agents SDK (Responses API format)
    """
    from sqlmodel import Session
    from src.database.db import engine

    # Fetch conversation history from the database
    with Session(engine) as session:
        messages = ConversationService.get_history(session, conversation_id, user_id)
        history = [{"role": m.role, "content": m.content} for m in messages]
        history.append({"role": "user", "content": message})
        conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in history)

    # Initialize MCP server
    mcp_server = MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["src/my_mcp_server/server.py"],
            "env": {**os.environ, "PYTHONPATH": ".", "AUTH_USER_ID": user_id}
        }
    )

    full_response = ""

    try:
        async with mcp_server as connection:
            # Create agent with OpenAI model
            agent = Agent(
                name="TodoAssistant",
                model=OPENAI_MODEL,  # gpt-4.1-nano
                instructions=SYSTEM_PROMPT,
                mcp_servers=[connection]
            )

            # Use Runner.run_streamed() for token-by-token streaming
            result = Runner.run_streamed(agent, input=conversation_text)

            # Stream events as they arrive - yield raw event.data for ChatKit compatibility
            async for event in result.stream_events():
                # Handle text delta events - yield raw event (Responses API format)
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    # Accumulate for database persistence
                    delta = event.data.delta
                    full_response += delta

                    # Yield full event object (RawResponsesStreamEvent wrapper)
                    # This ensures chat.py's isinstance(event_data, RawResponsesStreamEvent) check passes
                    yield event

                # Handle tool execution events - yield raw event data
                elif event.type == "tool_start":
                    yield event

                elif event.type == "tool_end":
                    yield event

        # Save messages to database after streaming completes
        with Session(engine) as session:
            ConversationService.add_message(session, conversation_id, user_id, "user", message)
            ConversationService.add_message(session, conversation_id, user_id, "assistant", full_response)

    except Exception as e:
        # Yield error event
        class ErrorEvent:
            def __init__(self, message):
                self.type = "error"
                self.message = message

        yield ErrorEvent(str(e))


async def run_agent_workflow(user_id: str, message: str, conversation_id: int) -> RunResult:
    """
    Main function to run the agent workflow by connecting to the local MCP server process.

    Args:
        user_id: The ID of the authenticated user
        message: The user's input message
        conversation_id: The ID of the conversation to fetch history for

    Returns:
        RunResult: The result from running the agent
    """
    # Fetch conversation history from the database
    # Create a database session to access conversation history
    from sqlmodel import Session
    from src.database.db import engine

    with Session(engine) as session:
        # Get the history for the conversation
        messages = ConversationService.get_history(session, conversation_id, user_id)

        # Map these messages into a list of dictionaries: [{"role": m.role, "content": m.content} for m in messages]
        history = [{"role": m.role, "content": m.content} for m in messages]

        # Add the new user message to the history
        history.append({"role": "user", "content": message})

        # Convert the history to a flattened string format to stabilize tool selection
        conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in history)

    # Initialize MCPServerStdio to communicate with the local MCP server via stdio
    mcp_server = MCPServerStdio(
        params={
            "command": sys.executable,  # Use the current virtual environment Python
            "args": ["src/my_mcp_server/server.py"],
            "env": {**os.environ, "PYTHONPATH": ".", "AUTH_USER_ID": user_id}  # Inject auth user ID and ensure modules can be found
        }
    )

    # Use the context manager to handle server lifecycle
    async with mcp_server as connection:
        # Instantiate the Agent with OpenAI model
        agent = Agent(
            name="TodoAssistant",
            model=OPENAI_MODEL,  # Use OpenAI model (gpt-4o-mini or configured model)
            instructions=SYSTEM_PROMPT,
            mcp_servers=[connection]  # Use MCP server instead of direct function injection
        )

        # Use Runner.run_streamed() for ChatKit compatibility
        result = Runner.run_streamed(agent, input=conversation_text)

        # Collect the final output from streaming
        full_response = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                full_response += event.data.delta

    # Save the user message to the database after connecting to the agent
    with Session(engine) as session:
        ConversationService.add_message(session, conversation_id, user_id, "user", message)

    # Save the assistant's response to the database (collected from streaming)
    with Session(engine) as session:
        ConversationService.add_message(session, conversation_id, user_id, "assistant", full_response)

    # Return a mock RunResult for compatibility
    class StreamResult:
        def __init__(self, output):
            self.final_output = output

    return StreamResult(full_response)


async def get_chat_response(user_id: str, conversation_id: int, message: str):
    """
    Main function to process chat messages and return AI responses.

    Args:
        user_id: The ID of the authenticated user
        conversation_id: The ID of the conversation
        message: The user's input message

    Returns:
        ChatResponse: The response containing the AI's reply, conversation ID, and any tool calls made
    """
    # Run the agent workflow with the conversation history
    result = await run_agent_workflow(
        user_id=user_id,
        message=message,
        conversation_id=conversation_id
    )

    # Extract tool calls from the result
    tool_calls = []
    # Access the tool call information from the result
    if hasattr(result, 'new_items'):
        for item in result.new_items:
            if hasattr(item, 'raw_item') and hasattr(item.raw_item, 'name'):
                arguments = getattr(item.raw_item, 'arguments', {})
                # Ensure arguments is a dictionary, not a string
                if isinstance(arguments, str):
                    import json
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}

                tool_calls.append(ToolCallInfo(
                    tool_name=item.raw_item.name,
                    arguments=arguments
                ))

    # Return the ChatResponse with the final output, conversation ID, and tool calls
    return ChatResponse(
        conversation_id=conversation_id,
        response=result.final_output,
        tool_calls=tool_calls
    )