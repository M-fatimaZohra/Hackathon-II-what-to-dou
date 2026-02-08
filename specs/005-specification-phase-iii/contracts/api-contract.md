# API Contract: Chat Endpoints

**Feature**: ChatKit Frontend Integration for AI Chatbot
**Date**: 2026-02-08
**Version**: 1.0.0

## Overview

This document defines the API contracts for the ChatKit frontend integration. All endpoints require JWT authentication and enforce user isolation via `/api/{user_id}/` path scoping (FR-008).

## Authentication

All endpoints require JWT authentication via Bearer token in the Authorization header.

```http
Authorization: Bearer <jwt_token>
```

**Token Source**: `authClient.getSession().accessToken` (Better Auth)

**Token Validation**:
- Backend MUST validate JWT signature
- Backend MUST verify token expiration
- Backend MUST extract userId from token
- Backend MUST verify path userId matches token userId (FR-008)

## Base URL

**Development**: `http://localhost:7860`
**Production**: `https://api.yourdomain.com`

## Endpoints

### 1. Send Message

Send a chat message to the AI assistant.

**Endpoint**: `POST /api/{user_id}/chat`

**Path Parameters**:
- `user_id` (string, required): Authenticated user ID

**Request Headers**:
```http
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

**Request Body**:
```json
{
  "conversationId": "string",
  "message": "string"
}
```

**Request Body Schema**:
```typescript
interface SendMessageRequest {
  conversationId: string;  // Conversation ID (required)
  message: string;         // Message content (required, max 10000 chars)
}
```

**Validation Rules**:
- `conversationId`: Required, non-empty string
- `message`: Required, non-empty string, max 10,000 characters
- `user_id` in path MUST match JWT token userId

**Success Response** (200 OK):
```json
{
  "messageId": "msg_123456",
  "timestamp": "2026-02-08T10:30:00Z",
  "status": "success",
  "mcpToolResponse": "Task created successfully: Buy groceries"
}
```

**Success Response Schema**:
```typescript
interface SendMessageResponse {
  messageId: string;           // Created message ID
  timestamp: string;           // ISO 8601 timestamp
  status: 'success';           // Response status
  mcpToolResponse?: string;    // MCP tool response (FR-006)
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "INVALID_MESSAGE",
  "message": "Message content is required",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Error Response** (403 Forbidden):
```json
{
  "error": "FORBIDDEN",
  "message": "User ID mismatch - access denied",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "SERVER_ERROR",
  "message": "Failed to process message",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Status Codes**:
- `200 OK`: Message sent successfully
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User ID mismatch (FR-008 violation)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: AI service temporarily unavailable

**Rate Limiting**:
- Max 60 requests per minute per user
- Max 1000 requests per hour per user

**Example Request**:
```bash
curl -X POST http://localhost:7860/api/user123/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "conversationId": "conv_456",
    "message": "Create a task to buy groceries"
  }'
```

---

### 2. Get Conversation History

Retrieve message history for a conversation.

**Endpoint**: `GET /api/{user_id}/chat/{conversation_id}`

**Path Parameters**:
- `user_id` (string, required): Authenticated user ID
- `conversation_id` (string, required): Conversation ID

**Query Parameters**:
- `limit` (integer, optional): Number of messages to return (default: 50, max: 100)
- `offset` (integer, optional): Offset for pagination (default: 0)

**Request Headers**:
```http
Authorization: Bearer <jwt_token>
```

**Validation Rules**:
- `user_id` in path MUST match JWT token userId
- `conversation_id` MUST belong to the authenticated user
- `limit`: Must be between 1 and 100
- `offset`: Must be non-negative integer

**Success Response** (200 OK):
```json
{
  "messages": [
    {
      "id": "msg_123",
      "userId": "user123",
      "conversationId": "conv_456",
      "content": "Create a task to buy groceries",
      "role": "user",
      "timestamp": "2026-02-08T10:30:00Z",
      "status": "delivered"
    },
    {
      "id": "msg_124",
      "userId": "assistant",
      "conversationId": "conv_456",
      "content": "I've created a task for you: Buy groceries",
      "role": "assistant",
      "timestamp": "2026-02-08T10:30:02Z",
      "status": "delivered",
      "metadata": {
        "mcpToolResponse": "Task created successfully: Buy groceries"
      }
    }
  ],
  "total": 42,
  "hasMore": true
}
```

**Success Response Schema**:
```typescript
interface GetConversationHistoryResponse {
  messages: Message[];     // Array of messages
  total: number;           // Total message count
  hasMore: boolean;        // Whether more messages available
}

interface Message {
  id: string;
  userId: string;
  conversationId: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: string;       // ISO 8601 timestamp
  status: 'pending' | 'sent' | 'delivered' | 'read' | 'failed';
  metadata?: {
    mcpToolResponse?: string;
    errorMessage?: string;
  };
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "NOT_FOUND",
  "message": "Conversation not found",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

**Status Codes**:
- `200 OK`: History retrieved successfully
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User ID mismatch or conversation access denied
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Server error

**Example Request**:
```bash
curl -X GET "http://localhost:7860/api/user123/chat/conv_456?limit=50&offset=0" \
  -H "Authorization: Bearer eyJhbGc..."
```

---

### 3. Create Conversation

Create a new conversation.

**Endpoint**: `POST /api/{user_id}/conversations`

**Path Parameters**:
- `user_id` (string, required): Authenticated user ID

**Request Headers**:
```http
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

**Request Body**:
```json
{
  "title": "Task Management Chat"
}
```

**Request Body Schema**:
```typescript
interface CreateConversationRequest {
  title?: string;  // Optional conversation title (max 200 chars)
}
```

**Success Response** (201 Created):
```json
{
  "id": "conv_789",
  "userId": "user123",
  "title": "Task Management Chat",
  "createdAt": "2026-02-08T10:30:00Z",
  "updatedAt": "2026-02-08T10:30:00Z",
  "lastMessageAt": "2026-02-08T10:30:00Z",
  "messageCount": 0,
  "status": "active"
}
```

**Success Response Schema**:
```typescript
interface CreateConversationResponse {
  id: string;
  userId: string;
  title: string;
  createdAt: string;       // ISO 8601 timestamp
  updatedAt: string;       // ISO 8601 timestamp
  lastMessageAt: string;   // ISO 8601 timestamp
  messageCount: number;
  status: 'active' | 'archived' | 'deleted';
}
```

**Status Codes**:
- `201 Created`: Conversation created successfully
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User ID mismatch
- `500 Internal Server Error`: Server error

**Example Request**:
```bash
curl -X POST http://localhost:7860/api/user123/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "title": "Task Management Chat"
  }'
```

---

### 4. List Conversations

List all conversations for a user.

**Endpoint**: `GET /api/{user_id}/conversations`

**Path Parameters**:
- `user_id` (string, required): Authenticated user ID

**Query Parameters**:
- `limit` (integer, optional): Number of conversations to return (default: 20, max: 50)
- `offset` (integer, optional): Offset for pagination (default: 0)
- `status` (string, optional): Filter by status ('active', 'archived', 'deleted')

**Request Headers**:
```http
Authorization: Bearer <jwt_token>
```

**Success Response** (200 OK):
```json
{
  "conversations": [
    {
      "id": "conv_789",
      "userId": "user123",
      "title": "Task Management Chat",
      "createdAt": "2026-02-08T10:30:00Z",
      "updatedAt": "2026-02-08T10:35:00Z",
      "lastMessageAt": "2026-02-08T10:35:00Z",
      "messageCount": 5,
      "status": "active"
    }
  ],
  "total": 10,
  "hasMore": false
}
```

**Status Codes**:
- `200 OK`: Conversations retrieved successfully
- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User ID mismatch
- `500 Internal Server Error`: Server error

---

### 5. Get ChatKit Token

Get a ChatKit authentication token for the authenticated user.

**Endpoint**: `POST /api/chatkit/token`

**Request Headers**:
```http
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-02-08T11:30:00Z"
}
```

**Success Response Schema**:
```typescript
interface ChatKitTokenResponse {
  token: string;       // ChatKit authentication token
  expiresAt: string;   // ISO 8601 timestamp
}
```

**Status Codes**:
- `200 OK`: Token generated successfully
- `401 Unauthorized`: Missing or invalid JWT token
- `500 Internal Server Error`: Server error

**Example Request**:
```bash
curl -X POST http://localhost:7860/api/chatkit/token \
  -H "Authorization: Bearer eyJhbGc..."
```

---

## Error Response Format

All error responses follow this standard format:

```typescript
interface ErrorResponse {
  error: string;       // Error code (e.g., "INVALID_MESSAGE")
  message: string;     // Human-readable error message
  timestamp: string;   // ISO 8601 timestamp
  details?: any;       // Optional additional error details
}
```

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_MESSAGE` | Message validation failed | 400 |
| `MESSAGE_TOO_LONG` | Message exceeds max length | 400 |
| `INVALID_CONVERSATION` | Invalid conversation ID | 400 |
| `UNAUTHORIZED` | Missing or invalid token | 401 |
| `TOKEN_EXPIRED` | JWT token expired | 401 |
| `FORBIDDEN` | User ID mismatch | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `SERVER_ERROR` | Internal server error | 500 |
| `SERVICE_UNAVAILABLE` | AI service unavailable | 503 |

## User Isolation (FR-008)

All endpoints enforce user isolation:

1. **Path Validation**: `user_id` in path MUST match JWT token userId
2. **Resource Access**: Users can only access their own conversations and messages
3. **Backend Validation**: Backend MUST validate userId on every request
4. **Error Response**: Return 403 Forbidden for user ID mismatch

**Example Violation**:
```bash
# User A tries to access User B's conversation
curl -X GET http://localhost:7860/api/userB/chat/conv_456 \
  -H "Authorization: Bearer <userA_token>"

# Response: 403 Forbidden
{
  "error": "FORBIDDEN",
  "message": "User ID mismatch - access denied",
  "timestamp": "2026-02-08T10:30:00Z"
}
```

## Stateless Operation (FR-007)

All requests are stateless:

1. **JWT + userId**: Every request includes JWT token and userId
2. **No Session State**: Frontend does not persist conversation state
3. **Backend State**: All conversation state managed by backend
4. **Conversation History**: Fetched from backend on page load

## MCP Tool Response Format (FR-006)

MCP tool responses are returned as strings in the `mcpToolResponse` field:

**Format**: `"<operation> <status>: <details>"`

**Examples**:
- `"Task created successfully: Buy groceries"`
- `"Task updated successfully: Buy groceries - Status: completed"`
- `"Task deleted successfully: Buy groceries"`
- `"Task list retrieved: 5 tasks found"`
- `"Error: Task not found"`

## Rate Limiting

**Per User Limits**:
- Send Message: 60 requests/minute, 1000 requests/hour
- Get History: 120 requests/minute, 2000 requests/hour
- Create Conversation: 10 requests/minute, 100 requests/hour
- List Conversations: 60 requests/minute, 1000 requests/hour

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1675854000
```

**Rate Limit Exceeded Response** (429):
```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again later.",
  "timestamp": "2026-02-08T10:30:00Z",
  "retryAfter": 30
}
```

## CORS Configuration

**Development**:
```
Access-Control-Allow-Origin: http://localhost:3000, http://127.0.0.1:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

**Production**:
```
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

## Testing

### Example Test Cases

**Test 1: Send Message Successfully**
```typescript
test('should send message successfully', async () => {
  const response = await fetch('http://localhost:7860/api/user123/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      conversationId: 'conv_456',
      message: 'Create a task to buy groceries'
    })
  });

  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data.status).toBe('success');
  expect(data.messageId).toBeDefined();
});
```

**Test 2: User Isolation Enforcement**
```typescript
test('should reject access to other user conversation', async () => {
  const response = await fetch('http://localhost:7860/api/userB/chat/conv_456', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${userAToken}`
    }
  });

  expect(response.status).toBe(403);
  const data = await response.json();
  expect(data.error).toBe('FORBIDDEN');
});
```

**Test 3: Handle Expired Token**
```typescript
test('should reject expired token', async () => {
  const response = await fetch('http://localhost:7860/api/user123/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${expiredToken}`
    },
    body: JSON.stringify({
      conversationId: 'conv_456',
      message: 'Test message'
    })
  });

  expect(response.status).toBe(401);
  const data = await response.json();
  expect(data.error).toBe('TOKEN_EXPIRED');
});
```

---

**Contract Status**: ✅ Complete
**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Compliance**: FR-005, FR-006, FR-007, FR-008