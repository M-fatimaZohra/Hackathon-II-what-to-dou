# REST API Endpoints: AI Native Todo Application

## Overview
This document specifies all REST API endpoints for the AI Native Todo Application. All endpoints require JWT authentication in the Authorization header, except for authentication-specific endpoints. The API follows RESTful principles with consistent response formats.

## Authentication

### Authentication Headers
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Base URL
```
https://api.example.com/v1
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional detailed error information"
  }
}
```

## Better Auth Integration

The application uses Better Auth for user authentication and session management. Better Auth provides secure JWT-based authentication with HS256 algorithm. The system integrates with Better Auth's official endpoints and handles JWT token extraction for backend API communication.

### Better Auth Endpoints

Better Auth provides the following official endpoints accessible via the frontend:
- `/api/auth/[[...all]]` - Handles all Better Auth operations including sign-in, sign-up, and session management

### JWT Token Handling for Backend API

The frontend uses Better Auth's built-in session management, but for communication with the backend API, JWT tokens are extracted from Better Auth's cookies:

- Token extraction from `better-auth.session_data` or `__Secure-better-auth.session_data` cookies
- Validation ensures the token uses HS256 algorithm
- Tokens are included in the Authorization header for backend API calls: `Authorization: Bearer <extracted_jwt_token>`
- The user ID is extracted from the JWT token for backend API requests and passed as part of the URL path

### Session Management

- Sessions are managed by Better Auth with JWT tokens stored in cookies
- Session tokens are automatically refreshed based on Better Auth's configuration
- The frontend accesses session data via Better Auth's client-side API
- Backend API calls use the extracted JWT token for authentication

---

## Task Endpoints

### GET /{user_id}/tasks
Retrieve all tasks for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user whose tasks to retrieve (must match JWT token)

#### Query Parameters
- `search` (optional): Search term for title/description
- `priority` (optional): Filter by priority (low|medium|high|urgent)
- `completed` (optional): Filter by completion status (true|false)

#### Response (200 OK)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": "user_12345",
      "title": "Complete project proposal",
      "description": "Finish and submit the project proposal document",
      "completed": false,
      "priority": "high",
      "created_at": "2023-10-01T12:00:00Z",
      "updated_at": "2023-10-01T12:00:00Z"
    }
  ]
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "user_id": "user_12345",
        "title": "Complete project proposal",
        "description": "Finish and submit the project proposal document",
        "completed": false,
        "priority": "high",
        "created_at": "2023-10-01T12:00:00Z",
        "updated_at": "2023-10-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 1,
      "total_pages": 1
    }
  }
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token

---

### POST /{user_id}/tasks
Create a new task for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user for whom to create the task (must match JWT token)

#### Request
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "priority": "medium"  // low, medium, high, urgent
}
```

#### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user_12345",
    "title": "New task title",
    "description": "Optional task description",
    "completed": false,
    "priority": "medium",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z"
  },
  "message": "Task created successfully"
}
```

#### Validation
- Title is required and must be 1-255 characters
- Description is optional and can be up to 1000 characters
- Priority must be one of: low, medium, high, urgent

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT

---

### GET /{user_id}/tasks/{id}
Retrieve a specific task for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user whose task to retrieve (must match JWT token)
- `id`: Task ID

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user_12345",
    "title": "Complete project proposal",
    "description": "Finish and submit the project proposal document",
    "completed": false,
    "priority": "high",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z"
  }
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT
- `404 Not Found`: Task does not exist

---

### PUT /{user_id}/tasks/{id}
Update a specific task for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user whose task to update (must match JWT token)
- `id`: Task ID

#### Request
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "priority": "high",
  "completed": false
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user_12345",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "priority": "high",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-02T15:30:00Z"
  },
  "message": "Task updated successfully"
}
```

#### Validation
- Title must be 1-255 characters if provided
- Description can be up to 1000 characters if provided
- Priority must be one of: low, medium, high, urgent if provided
- Completed must be boolean if provided

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT
- `404 Not Found`: Task does not exist

---

### DELETE /{user_id}/tasks/{id}
Delete a specific task for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user whose task to delete (must match JWT token)
- `id`: Task ID

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT
- `404 Not Found`: Task does not exist

---

### PATCH /{user_id}/tasks/{id}/complete
Toggle the completion status of a specific task for the specified user (authenticated user must match user_id in JWT).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the user whose task to update (must match JWT token)
- `id`: Task ID

#### Request
```json
{
  "completed": true  // true to complete, false to uncomplete
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user_12345",
    "title": "Complete project proposal",
    "description": "Finish and submit the project proposal document",
    "completed": true,
    "priority": "high",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-02T16:00:00Z"
  },
  "message": "Task completion status updated successfully"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User ID mismatch between path and JWT
- `404 Not Found`: Task does not exist

---

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_INPUT` | Provided input data is invalid |
| `UNAUTHORIZED` | User is not authenticated |
| `FORBIDDEN` | User does not have permission for this action |
| `NOT_FOUND` | Requested resource does not exist |
| `DUPLICATE_EMAIL` | Email already exists during registration |
| `INVALID_CREDENTIALS` | Provided credentials are invalid |
| `RATE_LIMIT_EXCEEDED` | Rate limit has been exceeded |
| `INTERNAL_ERROR` | An unexpected server error occurred |

## Chat Endpoints (Phase III: Agentic Foundation)

### POST /{user_id}/chat
Process natural language input and perform task management operations through AI agent.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
- `user_id`: The ID of the authenticated user (must match JWT)

#### Request
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
    "success": false,
    "error": {
      "code": "INVALID_INPUT",
      "message": "Message is required and cannot exceed 1000 characters"
    }
  }
  ```
- `401 Unauthorized`: Invalid or expired JWT token
  ```json
  {
    "success": false,
    "error": {
      "code": "UNAUTHORIZED",
      "message": "Invalid or expired JWT token"
    }
  }
  ```
- `403 Forbidden`: User ID mismatch between path and JWT
  ```json
  {
    "success": false,
    "error": {
      "code": "FORBIDDEN",
      "message": "Access denied: User ID mismatch"
    }
  }
  ```
- `500 Internal Server Error`: Unexpected server error during processing
  ```json
  {
    "success": false,
    "error": {
      "code": "INTERNAL_ERROR",
      "message": "Internal server error occurred while processing the chat request"
    }
  }
  ```

## Rate Limiting
- Authentication endpoints: 5 requests per 15 minutes per IP
- Task endpoints: 100 requests per hour per authenticated user
- Chat endpoints: 50 requests per hour per authenticated user (due to AI processing costs)
- General API endpoints: 1000 requests per hour per authenticated user

## Security Considerations
- All endpoints (except auth) require valid JWT tokens
- User IDs are extracted from JWT tokens, not client-provided
- Tasks are filtered by user ID to ensure data isolation
- Conversations are restricted to owning user
- Input validation is performed on all requests
- SQL injection is prevented through ORM usage
- MCP tools validate user permissions for each operation
- Natural language input is sanitized before processing