---
name: "openai-agents-core"
description: "Procedures for setting up Gemini models, initializing agents, and executing them using the OpenAI Agents Python SDK. Use this knowledge to build stateless chat logic."
---

# OpenAI Agents SDK Skill

## 1. Gemini Model Configuration

To use Gemini with the OpenAI Agents SDK, you must use the `OpenAIChatCompletionsModel` wrapper. This allows the SDK to communicate with Google's OpenAI-compatible endpoint.

**Procedure:**

1. Import `AsyncOpenAI` from `openai`.
2. Set the `base_url` to `https://generativelanguage.googleapis.com/v1beta/openai/`.
3. Initialize the `OpenAIChatCompletionsModel` using your Gemini API Key.

```python
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

# Disable tracing to avoid 401 errors if no OpenAI Key is present
set_tracing_disabled(True)

gemini_client = AsyncOpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Use this object in the 'model' field of Agent()
GEMINI_MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

```

## 1b. Alternative Model Configuration (Gemini 2.5 Flash Lite)

For lighter operations or cost optimization, you can also use the `gemini-2.5-flash-lite` model:

```python
# Alternative model configuration
GEMINI_LITE_MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=gemini_client
)
```

## 2. Creating a Simple Agent

An Agent requires a name and instructions. For a **Stateless** architecture, avoid hardcoding user-specific data in instructions; pass them via context instead.

**Procedure:**

* Use the `Agent` class.
* Pass the `GEMINI_MODEL` defined above.

```python
from agents import Agent

my_agent = Agent(
    name="TodoAssistant",
    instructions="You help users manage tasks. Be concise and professional.",
    model=GEMINI_MODEL
)

```

## 3. Running the Agent (Stateless Execution)

To maintain a stateless backend, every execution must include the conversation history fetched from the database.

**Procedure:**

1. Fetch history from PostgreSQL (format: `[{"role": "user", "content": "..."}, ...]`).
2. Use `Runner.run()` to get the response.

```python
from agents import Runner

async def get_response(user_message, chat_history):
    # The Runner handles the Thought/Tool/Response loop
    result = await Runner.run(
        my_agent,
        user_message,
        history=chat_history
    )
    return result.final_output

```

## 1c. Groq Model Configuration

To use Groq with the OpenAI Agents SDK, you must use the `OpenAIChatCompletionsModel` wrapper. This allows the SDK to communicate with Groq's OpenAI-compatible endpoint.

**Procedure:**

1. Import `AsyncOpenAI` from `openai`.
2. Set the `base_url` to `https://api.groq.com/openai/v1`.
3. Initialize the `OpenAIChatCompletionsModel` using your Groq API Key.

```python
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

# Disable tracing to avoid 401 tracing errors if no OpenAI Key is present
set_tracing_disabled(True)

groq_client = AsyncOpenAI(
    api_key="GROQ_API_KEY",
    base_url="https://api.groq.com/openai/v1"
)

# Use this object in the 'model' field of Agent()
GROQ_MODEL = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=groq_client
)

```

## 1d. OpenAI Model Configuration (Native)

To use native OpenAI models (GPT-4, GPT-4o, etc.), you can simply pass the model name as a string to the Agent constructor. The SDK will use the OpenAI API key from the environment variable `OPENAI_API_KEY`.

**Procedure:**

1. Set `OPENAI_API_KEY` environment variable
2. Pass model name directly to Agent

```python
from agents import Agent, ModelSettings

# Simple configuration - uses OPENAI_API_KEY from environment
openai_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o"  # or "gpt-4", "gpt-4-turbo", etc.
)

# With ModelSettings for fine-tuning behavior
openai_agent_configured = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    model_settings=ModelSettings(temperature=0.7)
)
```

**Available OpenAI Models:**
- `gpt-4o` - Latest GPT-4 Optimized model
- `gpt-4-turbo` - Fast GPT-4 variant
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - Cost-effective option

## 2b. Agent with ModelSettings

You can configure model behavior using `ModelSettings` to control parameters like temperature, top_p, and more.

**Procedure:**

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="TodoAssistant",
    instructions="You help users manage tasks.",
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.7,  # Controls randomness (0.0-2.0)
        # top_p=0.9,      # Nucleus sampling (optional)
        # max_tokens=1000 # Maximum response length (optional)
    )
)
```

**Common ModelSettings Parameters:**
- `temperature` (float): Controls randomness. Lower = more focused, Higher = more creative
- `top_p` (float): Nucleus sampling threshold
- `max_tokens` (int): Maximum tokens in response

## 4. Streaming Responses with Runner.run_streamed()

For real-time chat applications, use `Runner.run_streamed()` to stream responses token-by-token as they are generated.

**Procedure:**

1. Use `Runner.run_streamed()` instead of `Runner.run()`
2. Iterate over `stream_events()` to get events
3. Filter for `ResponseTextDeltaEvent` to get text chunks

```python
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

async def stream_response(user_message, chat_history):
    """
    Stream agent responses token-by-token for real-time display.

    Yields text deltas as they are generated by the model.
    """
    agent = Agent(
        name="TodoAssistant",
        instructions="You help users manage tasks.",
        model="gpt-4o"
    )

    # Use run_streamed() for streaming
    result = Runner.run_streamed(agent, input=user_message, history=chat_history)

    # Stream events as they arrive
    async for event in result.stream_events():
        # Filter for text delta events (token-by-token)
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            yield event.data.delta  # Yield each token as it arrives

        # Handle tool execution events
        elif event.type == "tool_start":
            yield f"\n[Tool: {event.tool.name}]\n"

        elif event.type == "tool_end":
            yield f"\n[Tool completed: {event.tool.name}]\n"
```

**Event Types:**
- `raw_response_event` with `ResponseTextDeltaEvent` - Text tokens
- `tool_start` - Tool execution begins
- `tool_end` - Tool execution completes
- `agent_start` - Agent begins processing
- `agent_end` - Agent completes processing

## 5. SSE Streaming for Web Applications

For Server-Sent Events (SSE) streaming in FastAPI, wrap the streaming function in a generator that formats events for SSE protocol.

**Procedure:**

```python
import json
from fastapi.responses import StreamingResponse

async def sse_stream_response(user_id: str, message: str, conversation_id: int):
    """
    Stream responses as SSE events for web clients.

    Yields SSE-formatted events: data: {"type": "chunk", "content": "..."}
    """
    agent = Agent(
        name="TodoAssistant",
        instructions="You help users manage tasks.",
        model="gpt-4o"
    )

    result = Runner.run_streamed(agent, input=message)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # Format as SSE event
            chunk_data = {
                "type": "chunk",
                "content": event.data.delta
            }
            yield f"data: {json.dumps(chunk_data)}\n\n"

        elif event.type == "tool_end":
            tool_data = {
                "type": "tool_call",
                "tool_name": event.tool.name,
                "output": event.output
            }
            yield f"data: {json.dumps(tool_data)}\n\n"

    # Send completion event
    complete_data = {"type": "complete"}
    yield f"data: {json.dumps(complete_data)}\n\n"

# FastAPI endpoint
@router.post("/{user_id}/chat")
async def chat_endpoint(user_id: str, request: ChatRequest):
    return StreamingResponse(
        sse_stream_response(user_id, request.message, request.conversation_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

**SSE Event Format:**
- Each event: `data: {JSON}\n\n`
- Event types: `chunk`, `tool_call`, `complete`, `error`
- Compatible with ChatKit SDK and EventSource API

