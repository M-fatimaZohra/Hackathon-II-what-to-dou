# System Architecture: AI Native Todo Application

## Overview
The AI Native Todo Application follows a modern full-stack architecture with clear separation between frontend and backend components. The system uses a REST API for communication between the Next.js frontend and FastAPI backend, with Neon Serverless PostgreSQL providing persistent storage. The architecture includes an AI agent layer with MCP SDK integration for natural language processing.

## Architecture Diagram
```
┌─────────────────┐    REST API     ┌──────────────────┐
│   Frontend      │◄────────────────►   Backend        │
│                 │                 │                  │
│  Next.js        │                 │  FastAPI         │
│  TypeScript     │                 │  Python         │
│  Tailwind CSS   │                 │  SQLModel       │
│  Better Auth    │                 │  JWT Auth       │
└─────────────────┘                 └──────────────────┘
                                          │
                              ┌─────────────┼─────────────┐
                              │             │             │
                              │      ┌──────▼──────┐     │
                              │      │    MCP      │     │
                              │      │   Server    │     │
                              │      └─────────────┘     │
                              │             │             │
                              │      ┌──────▼──────┐     │
                              │      │   OpenAI    │     │
                              │      │   Agent     │     │
                              │      └─────────────┘     │
                              │                          │
                              │      ┌───────────────────▼──────────────────┐
                              │      │             Database                 │
                              │      │                                      │
                              │      │  Neon Serverless                     │
                              │      │  PostgreSQL                          │
                              │      │  - Users (Better Auth)              │
                              │      │  - Tasks                            │
                              │      │  - Conversations                    │
                              │      │  - Messages                         │
                              │      └──────────────────────────────────────┘
                              │
                              │      ┌──────────────────────────────────────┐
                              │      │        Environment Toggle            │
                              │      │  - Development: localhost:3000     │
                              │      │  - Production: deployed domain       │
                              │      │  - CORS, logging, and reload config  │
                              │      └──────────────────────────────────────┘
```

## Component Breakdown

### Frontend Architecture
- **Framework**: Next.js (App Router) for server-side rendering and routing
- **Language**: TypeScript for type safety and better development experience
- **Styling**: Tailwind CSS for utility-first styling approach
- **Authentication**: Better Auth for client-side integration
- **State Management**: React hooks and context API for local state management

### Backend Architecture
- **Framework**: FastAPI for high-performance web API development
- **Language**: Python for backend logic and data processing
- **ORM**: SQLModel for database modeling and operations
- **Authentication**: JWT tokens for secure API access
- **API Design**: RESTful endpoints following standard conventions
- **AI Integration**: MCP SDK and OpenAI Agents SDK for natural language processing

### MCP Server Architecture
- **Protocol**: Official MCP SDK for standardized AI agent communication
- **Tools**: Specialized tools for task management operations (create, read, update, delete, complete)
- **Integration**: Seamless connection between AI agent and backend services
- **Security**: Validates user permissions for each AI-initiated action

### Database Architecture
- **Database**: Neon Serverless PostgreSQL for scalable, serverless database
- **Schema**: Users (managed by Better Auth), Tasks, Conversations, and Messages tables with foreign key relationships
- **Security**: Row-level security to ensure user data isolation
- **Indexing**: Proper indexing for search, filter, and conversation history operations

## Data Flow

### Authentication Flow
1. User registers/signs in via Better Auth
2. JWT token is generated and stored securely
3. JWT token is included in all authenticated API requests
4. Backend validates JWT and extracts user information
5. User-specific data is accessed based on extracted user ID

### Task Management Flow
1. Authenticated user requests tasks via API
2. Backend validates JWT and extracts user ID
3. Database query filters tasks by user ID
4. Tasks are returned to frontend
5. User can create, read, update, or delete tasks
6. All operations are validated to ensure user owns the task

### AI Chatbot Flow
1. User sends natural language message to `/api/{user_id}/chat` endpoint
2. Backend validates JWT and extracts user ID
3. Conversation history is fetched from database
4. MCP server processes natural language with OpenAI Agent
5. Appropriate MCP tools are called based on agent interpretation
6. Task operations are performed with user permission validation
7. Response and new message are stored in database
8. Response is returned to frontend

### Environment Toggle Flow
1. `ENVIRONMENT` variable determines configuration mode
2. Development mode enables CORS for localhost, hot reloading, and verbose logging
3. Production mode restricts CORS to specified domains and minimizes logging
4. Database connections and other resources adapt to environment requirements

## Security Architecture

### Authentication Security
- JWT tokens with appropriate expiration times
- Secure token storage and transmission
- Token refresh mechanisms
- Proper session management

### Data Security
- User data isolation through database-level filtering
- Input validation and sanitization
- SQL injection prevention through ORM usage
- Proper error handling to avoid information disclosure

### API Security
- All task endpoints require valid JWT
- User ID is extracted from JWT (not client-provided)
- Proper authorization checks for all operations
- Rate limiting to prevent abuse

### AI Agent Security
- MCP tools validate user permissions for each operation
- Natural language input is sanitized before processing
- Conversation access is restricted to owning user
- Tool calls are logged for audit trails

## Deployment Architecture

### Frontend Deployment
- Static site generation or server-side rendering
- CDN distribution for global access
- Environment-specific configurations

### Backend Deployment
- Containerized deployment or serverless functions
- Environment-specific configurations
- Health checks and monitoring

### Database Deployment
- Neon Serverless PostgreSQL for automatic scaling
- Connection pooling for optimal performance
- Backup and recovery procedures

## Integration Points

### Frontend-Backend Integration
- REST API endpoints for all data operations
- JWT-based authentication for all requests
- Consistent error handling and response formats
- Proper loading and error states in UI

### Backend-Database Integration
- SQLModel for type-safe database operations
- Connection pooling for performance
- Proper transaction management
- Query optimization and indexing

### Backend-MCP Server Integration
- Standardized MCP protocol for AI agent communication
- Tool-based architecture for specific task operations
- Secure validation of all AI-initiated actions
- Conversation history management

## Scalability Considerations

### Horizontal Scaling
- Stateless backend services for easy scaling
- Database connection pooling
- CDN for static assets

### Performance Optimization
- Database indexing for common queries
- Caching strategies where appropriate
- Optimized API responses
- Efficient data fetching patterns

### AI Agent Scaling
- Stateless agent operations (fetch history, process, store result)
- Efficient conversation history retrieval
- MCP tool optimization for common operations

## Monitoring and Observability
- API request logging and monitoring
- Database query performance tracking
- Error tracking and alerting
- User session monitoring for security
- AI agent interaction logging
- MCP tool usage analytics