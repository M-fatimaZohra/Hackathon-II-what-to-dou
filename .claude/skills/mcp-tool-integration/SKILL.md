---
name: "mcp-tool-integration"
description: "Procedures for creating MCP servers using FastMCP and connecting those tools to OpenAI Agents. Use this to implement database CRUD operations and external integrations."
---

# MCP Tool Integration Skill

## 1. Creating the MCP Server (FastMCP)

The MCP server acts as the host for your tools. We use `FastMCP` for a clean, decorator-based setup.

**Procedure:**

1. Initialize the `FastMCP` server in a dedicated file (e.g., `src/mcp/server.py`).
2. Use the `@mcp.tool()` decorator to define functions.
3. **Important:** Every tool should accept `ctx: dict` to receive secure context (like `auth_user_id`).

```python
from mcp.server.fastmcp import FastMCP



mcp = FastMCP("TodoManager")



@mcp.tool()
async def create_todo(ctx: dict, title: str, priority: str = "medium") -> str:
    """
    Creates a new todo item.
    The 'ctx' provides the secure 'auth_user_id' from the backend.
    """
    user_id = ctx.get("auth_user_id")
    # Logic to save to database using user_id...
    return f"Created task '{title}' for user {user_id}"

```

## 2. Connecting MCP to OpenAI Agents

To allow the Agent to use these tools, you must connect the MCP server via a transport (Standard I/O is best for local backend services).

**Procedure:**

1. Use `MCPServerStdio` to point to your MCP server script.
2. Pass the server instance into the `Agent`'s `mcp_servers` list.

```python
from agents import Agent
from agents.mcp import MCPServerStdio



# Configure the connection to the server script

mcp_server = MCPServerStdio(

    name="TodoSkills",

    params={

        "command": "python",

        "args": ["src/mcp/server.py"]

    }

)



# Connect the server to the Agent

todo_agent = Agent(

    name="TodoAgent",

    instructions="Use tools to manage the user's tasks.",

    model=GEMINI_MODEL, # Defined in openai-agents-core

    mcp_servers=[mcp_server]

)

```

## 3. The Execution Lifecycle

Because MCP servers run as subprocesses, they must be connected before use and cleaned up afterward.

**Procedure:**

1. Call `await mcp_server.connect()`.
2. Run the `Runner.run()` logic.
3. Call `await mcp_server.cleanup()` to close the subprocess.

```python
async def handle_request(message, history, user_id):

    await mcp_server.connect()

    try:

        result = await Runner.run(

            todo_agent,

            message,

            history=history,

            context={"auth_user_id": user_id} # Securely inject ID

        )

        return result.final_output

    finally:

        await mcp_server.cleanup()

```

## Quality Criteria

* **Tool Docstrings:** Every `@mcp.tool` must have a docstring; the AI uses this to understand when to call the tool.
* **Context Security:** Never let the AI provide the `user_id` as a tool argument. Always pull it from `ctx.get("auth_user_id")`.
* **Atomic Operations:** Keep tools small. One tool for "Create," one for "List," one for "Delete."