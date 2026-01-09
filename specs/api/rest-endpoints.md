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

## Authentication Endpoints

### POST /auth/register
Register a new user account.

#### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Response (201 Created)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_12345",
      "email": "user@example.com",
      "created_at": "2023-10-01T12:00:00Z"
    },
    "token": "jwt_token_here"
  },
  "message": "Account created successfully"
}
```

#### Validation
- Email must be valid format
- Password must meet strength requirements
- Email must not already exist

#### Error Responses
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists

---

### POST /auth/login
Authenticate user and return JWT token.

#### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_12345",
      "email": "user@example.com",
      "created_at": "2023-10-01T12:00:00Z"
    },
    "token": "jwt_token_here"
  },
  "message": "Login successful"
}
```

#### Error Responses
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials
- `429 Too Many Requests`: Rate limit exceeded

---

### POST /auth/logout
Logout the current user and invalidate session.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "message": "Logout successful"
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token

---

### GET /auth/me
Get current user information.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": "user_12345",
    "email": "user@example.com",
    "created_at": "2023-10-01T12:00:00Z"
  }
}
```

#### Error Responses
- `401 Unauthorized`: Invalid or expired token

---

## Task Endpoints

### GET /tasks
Retrieve all tasks for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Query Parameters
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 20, max: 100)
- `search` (optional): Search term for title/description
- `priority` (optional): Filter by priority (low|medium|high|urgent)
- `completed` (optional): Filter by completion status (true|false)
- `sort` (optional): Sort field (created_at|updated_at|priority) and direction (asc|desc)

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

### POST /tasks
Create a new task for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

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

---

### GET /tasks/{id}
Retrieve a specific task for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
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
- `403 Forbidden`: User does not own this task
- `404 Not Found`: Task does not exist

---

### PUT /tasks/{id}
Update a specific task for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
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
- `403 Forbidden`: User does not own this task
- `404 Not Found`: Task does not exist

---

### DELETE /tasks/{id}
Delete a specific task for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
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
- `403 Forbidden`: User does not own this task
- `404 Not Found`: Task does not exist

---

### PATCH /tasks/{id}/complete
Toggle the completion status of a specific task.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
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
- `403 Forbidden`: User does not own this task
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

## Rate Limiting
- Authentication endpoints: 5 requests per 15 minutes per IP
- Task endpoints: 100 requests per hour per authenticated user
- General API endpoints: 1000 requests per hour per authenticated user

## Security Considerations
- All endpoints (except auth) require valid JWT tokens
- User IDs are extracted from JWT tokens, not client-provided
- Tasks are filtered by user ID to ensure data isolation
- Input validation is performed on all requests
- SQL injection is prevented through ORM usage