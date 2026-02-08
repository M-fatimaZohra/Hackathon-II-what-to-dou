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
│  │ - TaskList   │    │   - <ChatView /> SDK component  │  │
│  │ - TaskForm   │    │   - JWT auth via Better Auth    │  │
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
│  │ auth_handler │    │   ChatKitServer                 │  │
│  │ (JWT verify) │───►│   - SSE streaming               │  │
│  └──────────────┘    │   - Session init                │  │
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
- **Frontend**: Sidebar overlay on `/tasks` page using ChatKit SDK's `<ChatView />`
- **Backend**: `ChatKitServer` class handles SSE streaming protocol
- **Communication**: Server-Sent Events (SSE) for real-time streaming (not WebSocket)
- **State Management**: Backend fetches conversation history from DB on session init
- **Authentication**: JWT verification via `auth_handler` middleware before processing

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
2. Frontend sends message to `/api/{user_id}/chat` with JWT token
3. Backend `auth_handler` middleware validates JWT and extracts user_id
4. Verifies path `user_id` matches JWT token user_id (403 if mismatch)
5. `ChatKitServer` initializes session and fetches conversation history from Neon DB
6. Request routed to OpenAI Agents SDK for processing
7. Agent SDK determines required MCP tool calls
8. MCP tools execute task operations (create, read, update, delete)
9. Response streamed via SSE (Server-Sent Events):
   - First token sent within 500ms (TTFT target)
   - Subsequent tokens streamed in real-time
   - MCP tool responses included in stream
   - Completion event sent when done
10. Frontend `<ChatView />` displays streamed response in real-time
11. New messages persisted to Neon DB
12. Task list automatically updates if task operations performed

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
- Real-time messaging via WebSocket
- JWT token exchange via backend
- Stateless frontend operation
- Connection pooling and reconnection