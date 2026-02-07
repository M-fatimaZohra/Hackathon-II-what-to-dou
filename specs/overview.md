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
- Basic task management functionality
- Core CRUD operations

### Phase II: Full-Stack Web Application
- Next.js frontend with TypeScript and Tailwind CSS
- FastAPI backend with Python and SQLModel
- Neon Serverless PostgreSQL for persistent storage
- Better Auth for authentication
- JWT-based security implementation

### Phase III: Backend Agentic Foundation
- AI-powered chatbot for natural language task management
- MCP SDK and OpenAI Agents SDK integration
- Conversation and message storage for chat history
- Production/development mode toggle capability

## Technology Stack
### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (client integration)

### Backend
- Python
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