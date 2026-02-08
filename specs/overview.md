# Project Overview: AI Native Todo Application

## Purpose
The AI Native Todo Application is a full-stack web application designed to help users manage their tasks efficiently. The application provides a modern, responsive interface with secure authentication, persistent task storage, and AI-powered natural language task management.

## Project Structure
The project follows a monorepo structure with organized specifications:

```
specs/
├── overview.md           # Project overview
├── architecture.md       # System architecture
├── branding.md           # Branding guidelines and visual identity
├── features/
│   ├── todo_crud.md      # Task management features
│   ├── authentication.md # Authentication features
│   └── agentic_chat.md   # AI chatbot features
├── api/
│   ├── rest-endpoints.md # REST API endpoints
│   └── mcp-tools.md      # MCP tools for AI agent communication
├── database/
│   └── schema.md         # Users, tasks, conversations, and messages schema
└── ui/
    ├── components.md     # Reusable components
    └── pages.md          # Pages: login, signup, task list, task detail
```

## Phases
The project is developed in multiple phases:

### Phase I: Console Application
- In-memory todo CLI application
- Basic task management (CRUD operations)

### Phase II: Full-Stack Web Application
- Next.js 16 frontend with TypeScript and Tailwind CSS
- FastAPI backend with Python 3.12 and SQLModel
- Neon Serverless PostgreSQL
- Better Auth for authentication
- JWT-based security

### Phase III: ChatKit Frontend Integration (Advanced Integration)
- **UI**: Persistent sidebar overlay on `/tasks` page (no separate /chat page)
- **SDK-First**: Single `<ChatAssistant />` wrapper using `@openai/chatkit-react` SDK's `<ChatView />` component
- **Streaming**: Server-Sent Events (SSE) for real-time message streaming from FastAPI backend
- **Backend**: `ChatKitServer` class from `openai-chatkit` Python SDK handles SSE protocol
- **Performance**: Time to First Token (TTFT) < 500ms for 90% of interactions
- **Authentication**: JWT verification via `auth_handler` middleware, baseUrl scoped to `/api/{user_id}/chat`
- **Stateless Frontend**: JWT + userId per request, no local conversation persistence
- **Stateful Backend**: Fetches conversation history from Neon DB on session initialization
- **User Isolation**: All requests scoped to `/api/{user_id}/` endpoints with JWT verification
- **Environment Toggle**: `NEXT_PUBLIC_MOD` variable controls dev/prod behavior (API URLs, security settings)
- **Integration Flow**: ChatKit UI → FastAPI (auth_handler) → Agent SDK → MCP Tools → Neon DB
- **Multi-turn Conversations**: Backend manages conversation context via database queries
- **MCP SDK and OpenAI Agents SDK integration**: For natural language task processing
- **Conversation and message storage**: Persistent chat history in Neon PostgreSQL

## Technology Stack
### Frontend
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS v4
- Better Auth (client integration)
- ChatKit React SDK (real-time messaging)

### Backend
- Python 3.12
- FastAPI
- SQLModel (ORM)
- JWT authentication
- OpenAI Agents SDK
- Official MCP SDK

### Database
- Neon Serverless PostgreSQL

## Security
- JWT-based authentication for API protection
- User data isolation (users can only access their own tasks)
- Secure credential handling
- Input validation and sanitization
- MCP tool permissions validation

## Goals
1. Provide a secure, user-friendly task management application
2. Implement robust authentication and authorization
3. Ensure data persistence and reliability
4. Create a responsive, accessible user interface
5. Follow best practices for security and performance
6. Enable AI-powered natural language task management
7. Support seamless development and production environment toggling