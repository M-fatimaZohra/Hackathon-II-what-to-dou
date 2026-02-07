from mcp.server.fastmcp import FastMCP
# Import all refactored tool functions using absolute imports
from src.my_mcp_server.tools.task_create_tool import create_task
from src.my_mcp_server.tools.task_list_tool import list_tasks
from src.my_mcp_server.tools.task_update_tool import update_task
from src.my_mcp_server.tools.task_delete_tool import delete_task
from src.my_mcp_server.tools.task_complete_tool import complete_task


# Initialize a single MCP server instance
mcp = FastMCP("TodoManager")


# Register all tool functions with the MCP server
mcp.tool()(create_task)
mcp.tool()(list_tasks)
mcp.tool()(update_task)
mcp.tool()(delete_task)
mcp.tool()(complete_task)


# For running the server
if __name__ == "__main__":
    mcp.run()