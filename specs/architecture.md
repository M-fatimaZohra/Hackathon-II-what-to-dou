# System Architecture: AI Native Todo Application

## Overview
The AI Native Todo Application follows a modern full-stack architecture with clear separation between frontend and backend components. The system uses a REST API for communication between the Next.js frontend and FastAPI backend, with Neon Serverless PostgreSQL providing persistent storage. The architecture includes an AI agent layer with MCP SDK integration for natural language processing.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 16)                    │
│                                                             │
│  ┌──────────────┐    ┌─────────────────────────────────┐  │
│  │ Tasks Page   │    │   ChatAssistant (Sidebar)       │  │
│  │              │◄───┤   - Uses @openai/chatkit-react  │  │
│  │ - TaskList   │    │   - <ChatKit /> SDK component   │  │
│  │ - TaskForm   │    │   - CustomApiConfig with JWT    │  │
│  └──────────────┘    └─────────────────────────────────┘  │
│         │                          │                        │
│         │                          │ SSE Stream             │
│         │ REST API                 │ (text/event-stream)    │
└─────────┼──────────────────────────┼────────────────────────┘
          │                          │
          │                          │
┌─────────▼──────────────────────────▼────────────────────────┐
│              Backend (FastAPI + Python 3.12)                │
│                                                             │
│  ┌──────────────┐    ┌─────────────────────────────────┐  │
│  │ auth_handler │    │   Chat Service                  │  │
│  │ (JWT verify) │───►│   - SSE streaming (custom fmt)  │  │
│  └──────────────┘    │   - Runner.run_streamed()       │  │
│                      │   - History fetch from DB       │  │
│                      └──────────┬──────────────────────┘  │
│                                 │                          │
│                      ┌──────────▼──────────────────────┐  │
│                      │   OpenAI Agents SDK             │  │
│                      │   - Message processing          │  │
│                      │   - Tool call routing           │  │
│                      └──────────┬──────────────────────┘  │
│                                 │                          │
│                      ┌──────────▼──────────────────────┐  │
│                      │   MCP Server                    │  │
│                      │   - Task CRUD tools             │  │
│                      │   - Database operations         │  │
│                      └──────────┬──────────────────────┘  │
└─────────────────────────────────┼────────────────────────┘
                                  │
                      ┌───────────▼──────────────────────┐
                      │  Neon PostgreSQL Database        │
                      │  - Users (Better Auth)          │
                      │  - Tasks                        │
                      │  - Conversations                │
                      │  - Messages                     │
                      └──────────────────────────────────┘
```

**Key Architecture Changes (Phase III)**:
- **Frontend**: Sidebar overlay on `/tasks` page using ChatKit SDK's `<ChatKit />` with CustomApiConfig
- **Backend**: Custom SSE streaming format (not ChatKitServer) via `Runner.run_streamed()`
- **Communication**: Server-Sent Events (SSE) for real-time streaming (not WebSocket)
- **State Management**: Backend fetches conversation history from DB on request
- **Authentication**: JWT verification via `auth_handler` middleware before processing
- **Integration**: ChatKit SDK's CustomApiConfig acts as pass-through for custom backend format

## Component Breakdown

### Frontend Architecture
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Authentication**: Better Auth
- **Real-time**: ChatKit React SDK
- **State Management**: React hooks and Context API

### Backend Architecture
- **Framework**: FastAPI
- **Language**: Python 3.12
- **ORM**: SQLModel
- **Authentication**: JWT tokens
- **AI Integration**: MCP SDK and OpenAI Agents SDK

### Database Architecture
- **Database**: Neon Serverless PostgreSQL
- **Schema**: Users, Tasks, Conversations, Messages
- **Security**: Row-level security for user data isolation
- **Indexing**: Optimized for search and conversation queries

## Data Flow

### Authentication Flow
1. User signs in via Better Auth
2. JWT token generated and stored
3. Token included in all API requests
4. Backend validates JWT and extracts user ID
5. User-specific data accessed based on user ID

### Task Management Flow
1. User requests tasks via API
2. Backend validates JWT
3. Database query filters by user ID
4. Tasks returned to frontend
5. All operations validated for user ownership

### AI Chatbot Flow (Phase III - SSE Streaming)
1. User opens chat sidebar overlay on `/tasks` page
2. Frontend ChatProvider initializes useChatKit with CustomApiConfig (domainKey, url, custom fetch)
3. User sends message - custom fetch injects JWT Authorization header
4. Backend `auth_handler` middleware validates JWT and extracts user_id
5. Verifies path `user_id` matches JWT token user_id (403 if mismatch)
6. Chat service fetches conversation history from Neon DB
7. Request routed to OpenAI Agents SDK for processing via `Runner.run_streamed()`
8. Agent SDK determines required MCP tool calls
9. MCP tools execute task operations (create, read, update, delete)
10. Response streamed via SSE in custom format:
   - Format: `{"type": "response.output_text.delta", "delta": "..."}`
   - First token sent within 500ms (TTFT target)
   - Subsequent tokens streamed in real-time
   - MCP tool responses included in stream
   - Completion event sent when done
11. Frontend ChatKit SDK receives custom format via CustomApiConfig pass-through
12. `<ChatKit />` component displays streamed response in real-time
13. New messages persisted to Neon DB
14. Task list automatically updates if task operations performed

## Security Architecture

### Authentication Security
- JWT tokens with expiration
- Secure token storage
- Token refresh mechanisms

### Data Security
- User data isolation via database filtering
- Input validation and sanitization
- SQL injection prevention through ORM

### API Security
- All endpoints require valid JWT
- User ID extracted from JWT (not client-provided)
- Authorization checks for all operations
- Rate limiting

## Integration Points

### Frontend-Backend Integration
- REST API for all operations
- JWT authentication
- Consistent error handling
- Loading and error states

### Backend-Database Integration
- SQLModel for type-safe operations
- Connection pooling
- Transaction management
- Query optimization

### Backend-MCP Server Integration
- Standardized MCP protocol
- Tool-based architecture
- Secure validation of AI actions
- Conversation history management

### ChatKit Integration
- Real-time messaging via SSE (not WebSocket)
- CustomApiConfig for self-hosted backend integration
- Custom fetch function for JWT token injection
- Stateless frontend operation (backend manages conversation state)
- Pass-through architecture (ChatKit SDK accepts custom backend format)