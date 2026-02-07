# Backend Guidelines
## Stack
- Python 3.12
- FastAPI 0.128.0
- SQLModel 0.0.16 (ORM)
- Neon PostgreSQL
- OpenAI Agents SDK
- Official MCP SDK
- python-jose
- psycopg2-binary

## Project Structure
- `src/main.py` - FastAPI app entry point with environment toggle
- `src/configs/` - Configuration files
  - `gemini_config.py` - Stores Gemini model parameters, reads GEMINI_API_KEY from env
  - `groq_config.py` - Stores Groq model parameters, reads GROQ_API_KEY from env
- `src/schema/` - Database models and schemas
  - `models.py` - SQLModel database models (updated with Conversation/Message models)
  - `chat_models.py` - Chat-specific models
- `src/api/` - API route handlers
  - `tasks.py` - Existing task endpoints
  - `chat.py` - Chat endpoint with MCP integration
- `src/services/` - Business logic services
  - `task_service.py` - Existing task service
  - `chat_service.py` - Chat/MCP service layer
  - `conversation_service.py` - Conversation management
- `src/middleware/auth_handler.py` - Authentication middleware
- `src/database/` - Database connection
  - `db.py` - Database connection with environment toggle
  - `init_db.py` - Database initialization
- `src/my_mcp_server/` - MCP server implementation
  - `server.py` - MCP server implementation
  - `tools/` - MCP tools for task operations
    - `task_create_tool.py` - Tool for creating tasks
    - `task_list_tool.py` - Tool for listing tasks
    - `task_update_tool.py` - Tool for updating tasks
    - `task_delete_tool.py` - Tool for deleting tasks
    - `task_complete_tool.py` - Tool for completing tasks
- `tests/` - Test files
  - `test_chat.py` - Chat endpoint tests
  - `test_conversation.py` - Conversation model tests
  - `test_mcp_integration.py` - MCP integration tests

## API Conventions
- All routes under `/api/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- Include JWT authentication for all endpoints with user isolation
- Implement environment-specific configurations (development/production)

## Database
- Use SQLModel for all database operations
- Connection string from environment variable: DATABASE_URL
- Updated schema with Conversation and Message tables for chat persistence
- User data isolation (100% cross-user access prevention)

## Environment Configuration
- Use `ENVIRONMENT` variable to toggle between development and production modes
- In development: enable docs/redoc, allow localhost:3000 and http://127.0.0.1:3000 for CORS
- In production: disable docs/redoc, restrict CORS to FRONTEND_API_URL

## Running
uvicorn main:app --reload --port 7860