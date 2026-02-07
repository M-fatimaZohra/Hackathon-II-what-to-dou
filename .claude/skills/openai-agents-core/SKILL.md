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