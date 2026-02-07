# MCP Tools and Commands: AI Native Todo Application

## Overview
This document specifies the Model Context Protocol (MCP) tools for the AI Native Todo Application. These tools are built using the Official MCP SDK to enable AI agents to perform CRUD operations on tasks through natural language interactions. The MCP tools provide a standardized interface between AI agents and the task management system.

## MCP Tool Return Contract (Updated)

To prevent agent "fallback errors" and improve LLM parsing reliability, all MCP tools now return descriptive string receipts instead of structured JSON objects. This approach uses LLM-native string responses that are more reliably transmitted through the Stdio communication channel.

**Return Format**: All tools return descriptive strings in the format:
- Success: `"SUCCESS: [Action completed] (ID: [id])"`
- Error: `"ERROR: [Reason]"`

**Important**: Task IDs in return strings are for AI memory only and should be hidden from the end-user in the final UI response.

## Official MCP SDK Integration

The application integrates with the Official MCP SDK to provide AI agents with secure, standardized access to task management functionality. All MCP tools validate user permissions and maintain data isolation.

## MCP Tools for AI Agents

### 1. add_task
**Description**: Create a new task based on natural language input from the AI agent.

**Input Parameters**:
- `user_id`: String, required - The ID of the user creating the task (validated against JWT)
- `title`: String, required - The title of the task
- `description`: String, optional - Detailed description of the task

**Output**:
- Returns descriptive string receipt with task details for AI memory and user feedback

**Security**: Validates that the requesting user has permission to create tasks for the specified user_id. Requires auth_user_id to be passed from service layer via ctx.request_context.

**Usage Example**:
```json
{
  "function": "add_task",
  "arguments": {
    "user_id": "user_12345",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }
}
```

**Expected Response**:
```
SUCCESS: Created task 'Buy groceries' (ID: 5)
```

### 2. list_tasks
**Description**: Retrieve tasks from the list based on natural language query from the AI agent.

**Input Parameters**:
- `user_id`: String, required - The ID of the user whose tasks to retrieve (validated against JWT)
- `status`: String, optional - Filter by status ("all", "pending", "completed")

**Output**: Returns descriptive string receipt listing matching tasks for AI memory and user feedback

**Security**: Validates that the requesting user has permission to access tasks for the specified user_id. Requires auth_user_id to be passed from service layer via ctx.request_context.

**Usage Example**:
```json
{
  "function": "list_tasks",
  "arguments": {
    "user_id": "user_12345",
    "status": "pending"
  }
}
```

**Expected Response**:
```
SUCCESS: Found 1 task for user (ID: 1): 'Buy groceries' (pending)
```

### 3. complete_task
**Description**: Mark a task as complete based on natural language input from the AI agent.

**Input Parameters**:
- `user_id`: String, required - The ID of the user who owns the task (validated against JWT)
- `task_id`: Integer, required - The ID of the task to update

**Output**: Returns descriptive string receipt with completion details for AI memory and user feedback

**Security**: Validates that the requesting user owns the task being updated. Requires auth_user_id to be passed from service layer via ctx.request_context.

**Usage Example**:
```json
{
  "function": "complete_task",
  "arguments": {
    "user_id": "user_12345",
    "task_id": 3
  }
}
```

**Expected Response**:
```
SUCCESS: Completed task 'Call mom' (ID: 3)
```

### 4. delete_task
**Description**: Remove a task from the list based on natural language input from the AI agent.

**Input Parameters**:
- `user_id`: String, required - The ID of the user who owns the task (validated against JWT)
- `task_id`: Integer, required - The ID of the task to delete

**Output**: Returns descriptive string receipt with deletion details for AI memory and user feedback

**Security**: Validates that the requesting user owns the task being deleted. Requires auth_user_id to be passed from service layer via ctx.request_context.

**Usage Example**:
```json
{
  "function": "delete_task",
  "arguments": {
    "user_id": "user_12345",
    "task_id": 2
  }
}
```

**Expected Response**:
```
SUCCESS: Deleted task 'Old task' (ID: 2)
```

### 5. update_task
**Description**: Modify task title or description based on natural language input from the AI agent.

**Input Parameters**:
- `user_id`: String, required - The ID of the user who owns the task (validated against JWT)
- `task_id`: Integer, required - The ID of the task to update
- `title`: String, optional - New title for the task
- `description`: String, optional - New description for the task

**Output**: Returns descriptive string receipt with update details for AI memory and user feedback

**Security**: Validates that the requesting user owns the task being updated. Requires auth_user_id to be passed from service layer via ctx.request_context.

**Usage Example**:
```json
{
  "function": "update_task",
  "arguments": {
    "user_id": "user_12345",
    "task_id": 1,
    "title": "Buy groceries and fruits"
  }
}
```

**Expected Response**:
```
SUCCESS: Updated task to 'Buy groceries and fruits' (ID: 1)
```

## Authentication Context Propagation

### Service Layer to MCP Tools
All MCP tools require that the auth_user_id be explicitly passed from the service layer through the context parameter (ctx.request_context). The service layer must extract the authenticated user ID from the API request context and forward it to each MCP tool invocation.

### Validation Flow
1. API layer extracts auth_user_id from JWT token
2. Service layer passes auth_user_id to MCP tools via context
3. MCP tools validate that auth_user_id matches the user_id in the request parameters
4. MCP tools perform user-specific operations with data isolation

## MCP Server Configuration

### MCP Server Startup
**Command**: Configure and start the MCP server to expose the above tools to AI agents.

**Configuration Parameters**:
- `server_port`: Integer - Port for the MCP server (default: 8080)
- `allowed_origins`: Array - Origins allowed to connect to the MCP server
- `authentication_required`: Boolean - Whether authentication is required for tool access

### Tool Registration
All MCP tools are registered with the Official MCP SDK and follow MCP protocol specifications for standardized communication with AI agents.

## Security Considerations

### Permission Validation
- All MCP tools validate that the requesting user has permission to perform the requested operation
- User ID is extracted from JWT token and compared with the requested user_id parameter
- Tools reject requests where user IDs don't match

### Data Isolation
- MCP tools ensure users can only access their own tasks
- All queries are filtered by user_id to maintain data isolation
- Cross-user data access is prevented through server-side validation

### Input Sanitization
- All inputs from AI agents are validated before processing
- MCP tools sanitize inputs to prevent injection attacks
- Input validation follows the same patterns as regular API endpoints

## AI Agent Tools (Phase III: Agentic Foundation)

### 16. Official MCP SDK Integration
**Tool**: `mcp-server-start`
**Description**: Start the official MCP server with registered tools for AI agent communication.

**Parameters**:
- `--config`: Path to MCP server configuration file
- `--port`: Port to run the MCP server on (default: 8080)
- `--implementation`: MCP server implementation type

**Usage**:
```bash
mcp mcp-server-start --config ./mcp-config.json --port 8080
```

**Tool**: `register-mcp-tools`
**Description**: Register MCP tools with the official MCP SDK for task management operations.

**Registered Tools** (using Official MCP SDK):
- `add_task`: Create a new task based on natural language input
- `list_tasks`: Retrieve tasks from the list based on natural language query
- `complete_task`: Mark a task as complete based on natural language input
- `delete_task`: Remove a task from the list based on natural language input
- `update_task`: Modify task title or description based on natural language input

**Implementation Details**:
- Built using Official MCP SDK for standardized AI agent communication
- Each tool validates user permissions for security
- Tools follow MCP protocol specifications for interoperability

**Usage**:
```bash
mcp register-mcp-tools --implementation official-sdk
```

### 17. MCP Integration Testing
**Tool**: `test-mcp-integration`
**Description**: Test the integration between MCP server and the task management system.

**Parameters**:
- `--scenarios`: Test scenarios to run (mcp_protocol, task_operations, conversation_context)
- `--mock-services`: Use mock services instead of real backend
- `--verbose`: Enable verbose output for debugging

**Usage**:
```bash
mcp test-mcp-integration --scenarios mcp_protocol,task_operations --verbose
```

## Troubleshooting Tools

### 18. Debug Setup
**Tool**: `debug-setup`
**Description**: Set up debugging configuration for development.

**Parameters**:
- `--frontend`: Enable frontend debugging
- `--backend`: Enable backend debugging
- `--database`: Enable database query logging
- `--mcp`: Enable MCP server debugging

**Usage**:
```bash
mcp debug-setup --frontend --backend --database --mcp
```

### 19. Rollback Operations
**Tool**: `rollback-deployment`
**Description**: Rollback deployment to a previous version.

**Parameters**:
- `--env`: Environment to rollback
- `--version`: Specific version to rollback to
- `--steps`: Number of versions to rollback

**Usage**:
```bash
mcp rollback-deployment --env prod --steps 1
```

## Usage Guidelines

### Best Practices
1. Always run `validate-specs` before implementing new features
2. Use `test-security` regularly to ensure authentication and data isolation
3. Run `health-check` after deployments
4. Use `analyze-logs` for proactive monitoring
5. Run `check-quality` before committing code

### Common Workflows

#### New Feature Development
```bash
mcp generate-component --type component --name new-feature
mcp generate-api --resource new-resource --operations create,read
mcp test-unit --frontend --backend
mcp test-integration
mcp validate-specs
```

#### Pre-Deployment Checklist
```bash
mcp test-security --auth --data-isolation
mcp check-quality --frontend --backend --fix
mcp perf-test --concurrent-users 50 --duration 120
mcp deploy-app --env staging
mcp health-check --frontend --backend --database
```

#### Post-Deployment Verification
```bash
mcp health-check --frontend --backend --database
mcp test-integration --api
mcp analyze-logs --timeframe last-hour --level error
```

## Error Handling
All MCP tools follow a consistent error reporting format:
- Exit codes: 0 for success, 1 for general errors, 2 for validation errors
- Error messages are prefixed with the tool name
- Detailed error information is available with the `--verbose` flag

## Versioning
- MCP tools follow semantic versioning (major.minor.patch)
- Breaking changes are indicated by major version increments
- New features are indicated by minor version increments
- Bug fixes are indicated by patch version increments