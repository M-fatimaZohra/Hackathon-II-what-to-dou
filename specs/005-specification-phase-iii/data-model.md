# Data Model: ChatKit Frontend Integration

**Feature**: ChatKit Frontend Integration for AI Chatbot
**Date**: 2026-02-08
**Status**: Complete

## Overview

This document defines the TypeScript interfaces and data structures for the ChatKit frontend integration. All types are defined in `frontend/src/types/chat.ts`.

## Core Entities

### Message

Represents an individual chat message in a conversation.

```typescript
// frontend/src/types/chat.ts

export interface Message {
  id: string;                    // Unique message identifier
  userId: string;                // User who sent the message
  conversationId: string;        // Conversation this message belongs to
  content: string;               // Message text content
  role: 'user' | 'assistant' | 'system';  // Message sender role
  timestamp: Date;               // When message was sent
  status: MessageStatus;         // Delivery status
  metadata?: MessageMetadata;    // Optional metadata
}

export type MessageStatus =
  | 'pending'    // Message being sent
  | 'sent'       // Message sent to server
  | 'delivered'  // Message delivered to recipient
  | 'read'       // Message read by recipient
  | 'failed';    // Message failed to send

export interface MessageMetadata {
  mcpToolResponse?: string;      // MCP tool response (FR-006)
  errorMessage?: string;         // Error message if failed
  retryCount?: number;           // Number of retry attempts
}
```

**Validation Rules**:
- `id`: Must be unique, non-empty string
- `userId`: Must match authenticated user ID (FR-008)
- `conversationId`: Must be valid conversation ID
- `content`: Must be non-empty string, max 10,000 characters
- `role`: Must be one of 'user', 'assistant', 'system'
- `timestamp`: Must be valid Date object
- `status`: Must be valid MessageStatus

**State Transitions**:
```
pending → sent → delivered → read
pending → failed (on error)
failed → pending (on retry)
```

### Conversation

Represents a chat session between user and AI assistant.

```typescript
export interface Conversation {
  id: string;                    // Unique conversation identifier
  userId: string;                // User who owns this conversation
  title: string;                 // Conversation title
  createdAt: Date;               // When conversation was created
  updatedAt: Date;               // Last update timestamp
  lastMessageAt: Date;           // Timestamp of last message
  messageCount: number;          // Total number of messages
  status: ConversationStatus;    // Conversation status
}

export type ConversationStatus =
  | 'active'     // Conversation is active
  | 'archived'   // Conversation is archived
  | 'deleted';   // Conversation is deleted

```

**Validation Rules**:
- `id`: Must be unique, non-empty string
- `userId`: Must match authenticated user ID (FR-008)
- `title`: Max 200 characters
- `createdAt`, `updatedAt`, `lastMessageAt`: Must be valid Date objects
- `messageCount`: Must be non-negative integer
- `status`: Must be valid ConversationStatus

### ChatKitConfig

Configuration for ChatKit SDK initialization.

```typescript
export interface ChatKitConfig {
  instanceLocator: string;       // ChatKit instance locator
  tokenProviderUrl: string;      // Backend token endpoint URL
  debug: boolean;                // Enable debug logging
  reconnect: boolean;            // Enable automatic reconnection
  maxReconnectAttempts: number;  // Max reconnection attempts
}
```

**Validation Rules**:
- `instanceLocator`: Must be valid ChatKit instance locator format
- `tokenProviderUrl`: Must be valid URL
- `debug`: Boolean, true for development, false for production (FR-009)
- `reconnect`: Boolean, should be true for production
- `maxReconnectAttempts`: Must be positive integer, recommended 5

### ChatState

Global chat state managed by ChatProvider component using useChatKit hook.

```typescript
export interface ChatState {
  currentConversationId: string | null;  // Active conversation ID
  messages: Message[];                   // Messages in current conversation
  conversations: Conversation[];         // User's conversations
  isLoading: boolean;                    // Loading state
  isConnected: boolean;                  // ChatKit connection status
  error: ChatError | null;               // Current error state
  userId: string;                        // Authenticated user ID
}

export interface ChatError {
  code: string;                  // Error code
  message: string;               // Error message
  timestamp: Date;               // When error occurred
  retryable: boolean;            // Whether error is retryable
}
```

**Validation Rules**:
- `currentConversationId`: Must be valid conversation ID or null
- `messages`: Array of valid Message objects
- `conversations`: Array of valid Conversation objects
- `isLoading`: Boolean
- `isConnected`: Boolean
- `error`: Valid ChatError object or null
- `userId`: Must match authenticated user ID

## Component Props

### ChatWindowProps

Props for ChatWindow component (FR-002).

```typescript
export interface ChatWindowProps {
  conversationId: string;                    // Conversation to display
  messages: Message[];                       // Messages to display
  isLoading: boolean;                        // Loading state
  onLoadMore: () => void;                    // Load more messages callback
  hasMore: boolean;                          // Whether more messages available
  className?: string;                        // Optional CSS class
}
```

### ChatInputProps

Props for ChatInput component (FR-003).

```typescript
export interface ChatInputProps {
  onSend: (message: string) => Promise<void>;  // Send message callback
  disabled: boolean;                            // Whether input is disabled
  placeholder?: string;                         // Input placeholder text
  maxLength?: number;                           // Max message length
  className?: string;                           // Optional CSS class
}
```

### ChatMessageProps

Props for ChatMessage component.

```typescript
export interface ChatMessageProps {
  message: Message;                          // Message to display
  isCurrentUser: boolean;                    // Whether message is from current user
  showTimestamp?: boolean;                   // Whether to show timestamp
  className?: string;                        // Optional CSS class
}
```

### ChatProviderProps

Props for ChatProvider component (FR-004).

```typescript
export interface ChatProviderProps {
  children: React.ReactNode;                 // Child components
}
```

## API Request/Response Types

### SendMessageRequest

Request payload for sending a message to backend.

```typescript
export interface SendMessageRequest {
  conversationId: string;        // Target conversation ID
  message: string;               // Message content
  userId: string;                // User ID (for isolation, FR-008)
}
```

### SendMessageResponse

Response from backend after sending a message.

```typescript
export interface SendMessageResponse {
  messageId: string;             // Created message ID
  timestamp: Date;               // Message timestamp
  status: 'success' | 'error';   // Response status
  mcpToolResponse?: string;      // MCP tool response if applicable (FR-006)
  error?: string;                // Error message if status is error
}
```

### GetConversationHistoryRequest

Request payload for fetching conversation history.

```typescript
export interface GetConversationHistoryRequest {
  conversationId: string;        // Conversation ID
  userId: string;                // User ID (for isolation, FR-008)
  limit: number;                 // Number of messages to fetch
  offset: number;                // Offset for pagination
}
```

### GetConversationHistoryResponse

Response from backend with conversation history.

```typescript
export interface GetConversationHistoryResponse {
  messages: Message[];           // Array of messages
  total: number;                 // Total message count
  hasMore: boolean;              // Whether more messages available
}
```

## Environment Configuration Types

### EnvironmentConfig

Environment-specific configuration (FR-009).

```typescript
export interface EnvironmentConfig {
  isDevelopment: boolean;        // Whether in development mode
  apiUrl: string;                // Backend API URL
  chatkit: ChatKitConfig;        // ChatKit configuration
  logging: LoggingConfig;        // Logging configuration
}

export interface LoggingConfig {
  level: 'verbose' | 'info' | 'warn' | 'error';  // Log level
  enableConsole: boolean;                         // Enable console logging
  enableRemote: boolean;                          // Enable remote logging
}
```

## Error Types

### ChatErrorCode

Enumeration of possible error codes.

```typescript
export enum ChatErrorCode {
  // Network errors
  NETWORK_ERROR = 'NETWORK_ERROR',
  CONNECTION_LOST = 'CONNECTION_LOST',
  TIMEOUT = 'TIMEOUT',

  // Authentication errors
  AUTH_FAILED = 'AUTH_FAILED',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  UNAUTHORIZED = 'UNAUTHORIZED',

  // Validation errors
  INVALID_MESSAGE = 'INVALID_MESSAGE',
  MESSAGE_TOO_LONG = 'MESSAGE_TOO_LONG',
  INVALID_CONVERSATION = 'INVALID_CONVERSATION',

  // Server errors
  SERVER_ERROR = 'SERVER_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED',

  // ChatKit errors
  CHATKIT_ERROR = 'CHATKIT_ERROR',
  CHATKIT_CONNECTION_FAILED = 'CHATKIT_CONNECTION_FAILED',
}
```

### ChatException

Custom exception class for chat errors.

```typescript
export class ChatException extends Error {
  code: ChatErrorCode;
  timestamp: Date;
  retryable: boolean;
  originalError?: Error;

  constructor(
    code: ChatErrorCode,
    message: string,
    retryable: boolean = false,
    originalError?: Error
  ) {
    super(message);
    this.name = 'ChatException';
    this.code = code;
    this.timestamp = new Date();
    this.retryable = retryable;
    this.originalError = originalError;
  }
}
```

## Utility Types

### Pagination

Generic pagination type for list responses.

```typescript
export interface Pagination<T> {
  items: T[];                    // Array of items
  total: number;                 // Total item count
  limit: number;                 // Items per page
  offset: number;                // Current offset
  hasMore: boolean;              // Whether more items available
}
```

### AsyncState

Generic async operation state.

```typescript
export interface AsyncState<T> {
  data: T | null;                // Data result
  loading: boolean;              // Loading state
  error: ChatError | null;       // Error state
}
```

## Data Flow

### Message Sending Flow

```
User Input → ChatInput Component
  ↓
ChatProvider.sendMessage()
  ↓
API Client → POST /api/{userId}/chat
  ↓
Backend Processing (MCP Tools)
  ↓
Response → Update ChatState
  ↓
ChatWindow Re-render
```

### Message Receiving Flow (Real-time)

```
Backend → ChatKit Stream
  ↓
ChatProvider Event Handler
  ↓
Update ChatState.messages
  ↓
ChatWindow Re-render
```

### Conversation History Loading

```
Page Load → ChatProvider.initialize()
  ↓
API Client → GET /api/{userId}/chat/{conversationId}
  ↓
Backend → Fetch from Database
  ↓
Response → Update ChatState.messages
  ↓
ChatWindow Render
```

## Relationships

```
User (1) ──── (N) Conversation
Conversation (1) ──── (N) Message
Message (N) ──── (1) User (sender)
```

## Indexes and Performance

**Recommended Indexes** (Backend):
- `messages.conversationId` - For fetching conversation history
- `messages.timestamp` - For ordering messages
- `conversations.userId` - For user isolation (FR-008)
- `conversations.lastMessageAt` - For sorting conversations

**Frontend Caching Strategy**:
- Cache last 100 messages per conversation in memory
- Cache conversation list (max 50 conversations)
- Clear cache on logout or token expiration

## Validation Summary

All data models include validation rules to ensure:
- **User Isolation** (FR-008): userId validation on all operations
- **Data Integrity**: Type safety with TypeScript
- **Security**: Input sanitization and length limits
- **Performance**: Pagination for large datasets
- **Error Handling**: Comprehensive error types and codes

---

**Data Model Status**: ✅ Complete
**All Entities Defined**: ✅ Yes
**Validation Rules Specified**: ✅ Yes
**Ready for Implementation**: ✅ Yes