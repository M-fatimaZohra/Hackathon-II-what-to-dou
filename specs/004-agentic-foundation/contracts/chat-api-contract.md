# API Contract: Chat Endpoint

## Overview
This document specifies the API contract for the AI Chatbot endpoint that processes natural language input for task management.

## Chat Endpoint

### POST /api/{user_id}/chat

Process natural language input and perform task management operations.

#### Authentication
All requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | The ID of the authenticated user (must match JWT) |

#### Request Body
```json
{
  "conversation_id": 123,  // Optional: integer or null for new conversation
  "message": "Add a task to buy groceries tomorrow"  // Required: string, the user's message
}
```

#### Response (200 OK)
```json
{
  "conversation_id": 123,  // The ID of the conversation (newly created if null was provided)
  "response": "I've created a task 'buy groceries' for tomorrow.",  // The AI's response to the user
  "tool_calls": [  // Array of tools called by the AI agent
    {
      "function": "create_task",
      "arguments": {
        "title": "buy groceries",
        "due_date": "tomorrow"
      }
    }
  ]
}
```

#### Validation
- `message` is required and must be 1-1000 characters
- `conversation_id` must be a valid conversation ID owned by the user, or null for new conversation
- `user_id` in path must match the user ID in the JWT token

#### Error Responses
- `400 Bad Request`: Invalid input data
  ```json
  {
    "detail": "Message is required and cannot exceed 1000 characters"
  }
  ```
- `401 Unauthorized`: Invalid or expired JWT token
  ```json
  {
    "detail": "Invalid or expired JWT token"
  }
  ```
- `403 Forbidden`: User ID mismatch between path and JWT
  ```json
  {
    "detail": "Access denied: User ID mismatch"
  }
  ```
- `500 Internal Server Error`: Unexpected server error during processing
  ```json
  {
    "detail": "Internal server error occurred while processing the chat request"
  }
  ```

## MCP Tool Contracts

### create_task (equivalent to add_task)
**Purpose**: Create a new task based on natural language input
**Input**: Object with task properties (title, description, priority, etc.)
**Output**: Descriptive string receipt in format "SUCCESS: Created task '[title]' (ID: [id])" or "ERROR: [reason]"
**Auth Context**: Requires auth_user_id to be passed from service layer via ctx.request_context for validation

### list_tasks
**Purpose**: Retrieve tasks based on natural language query
**Input**: Query parameters (search terms, filters, etc.)
**Output**: Descriptive string receipt listing tasks in format "SUCCESS: Found [n] task(s) for user (ID: [id]): '[title]' ([status])"
**Auth Context**: Requires auth_user_id to be passed from service layer via ctx.request_context for validation

### update_task
**Purpose**: Update an existing task based on natural language input
**Input**: Task ID and updated properties
**Output**: Descriptive string receipt in format "SUCCESS: Updated task to '[title]' (ID: [id])" or "ERROR: [reason]"
**Auth Context**: Requires auth_user_id to be passed from service layer via ctx.request_context for validation

### delete_task
**Purpose**: Delete a task based on natural language input
**Input**: Task ID or identifying information
**Output**: Descriptive string receipt in format "SUCCESS: Deleted task '[title]' (ID: [id])" or "ERROR: [reason]"
**Auth Context**: Requires auth_user_id to be passed from service layer via ctx.request_context for validation

### complete_task
**Purpose**: Mark a task as complete/incomplete based on natural language input
**Input**: Task ID and completion status
**Output**: Descriptive string receipt in format "SUCCESS: Completed task '[title]' (ID: [id])" or "ERROR: [reason]"
**Auth Context**: Requires auth_user_id to be passed from service layer via ctx.request_context for validation

## Authentication Context Propagation
- Each MCP tool call must include auth_user_id in ctx.request_context
- Service layer must extract authenticated user ID from API request and forward to tools
- Tools validate that auth_user_id matches user_id in request parameters
- Conversation ID may be included for context tracing where relevant

## Security Considerations
- All operations are validated against the user's JWT token
- Conversation access is restricted to the owning user
- Input validation prevents injection attacks
- MCP tools validate user permissions for each operation using auth_user_id
- Requests without valid auth_user_id are rejected by MCP tools

## MCP Tool Return Contract (Updated for Agent Reliability)
To prevent agent "fallback errors" and improve communication reliability:
- All MCP tools return descriptive string receipts instead of JSON objects
- Success format: "SUCCESS: [Action completed] (ID: [id])"
- Error format: "ERROR: [Reason]"
- Task IDs in return strings are for AI memory only and must be hidden from users in final UI response