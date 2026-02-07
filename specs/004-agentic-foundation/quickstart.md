# Quickstart Guide: Phase III – Backend Agentic Foundation

## Overview
This guide explains how to set up, run, and use the stateless AI Chatbot functionality in the Todo application.

## Prerequisites
- Python 3.12+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- OpenAI API key
- MCP SDK compatible environment

## Setup

### 1. Environment Variables
Create/update your `.env` file in the backend directory:

```
# Environment mode (development or production)
ENVIRONMENT=development

# Database URL for Neon Serverless PostgreSQL
DATABASE_URL='postgresql://your_username:your_password@your_endpoint.your_region.neon.tech/your_database?sslmode=require'
NEON_DATABASE_URL='postgresql://your_username:your_password@your_endpoint.your_region.neon.tech/your_database?sslmode=require'

# Better Auth Secret - must match frontend
BETTER_AUTH_SECRET="your_better_auth_secret_here"

# Frontend URL for CORS
FRONTEND_API_URL=http://localhost:3000

# OpenAI API key for agent functionality
OPENAI_API_KEY="your_openai_api_key_here"

# Application Configuration
APP_NAME=What To Dou
API_V1_STR=/api
DEBUG=True
```

### 2. Install Dependencies
```bash
cd backend
pip install poetry
poetry install
# OR if using pip directly:
pip install -r requirements.txt
```

### 3. Database Setup
The application will automatically create the necessary tables (including the new Conversation and Message tables) when started if they don't exist.

## Running the Application

### Development Mode
```bash
cd backend
poetry run python src/main.py
# OR
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 7860
```

### Production Mode
```bash
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 7860
```

The application will detect the `ENVIRONMENT` variable and adjust settings accordingly:
- In development: enables CORS for localhost, hot reloading, and detailed logging
- In production: restricts CORS to specified domains and minimizes logging

## Using the Chat API

### Authentication
All chat endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Chat Endpoint
POST to `/api/{user_id}/chat` to interact with the AI chatbot:

Request body:
```json
{
  "conversation_id": 123,  // Optional, null for new conversation
  "message": "Add a task to buy groceries tomorrow"
}
```

Response:
```json
{
  "conversation_id": 123,
  "response": "I've created a task 'buy groceries' for tomorrow.",
  "tool_calls": [
    {
      "function": "create_task",
      "arguments": {"title": "buy groceries", "due_date": "tomorrow"}
    }
  ]
}
```

## MCP Server Integration

The application includes an MCP server that provides tools for the AI agent to interact with the task management system. The tools available are:

- `add_task`: Creates a new task based on natural language input
- `list_tasks`: Retrieves tasks from the list based on natural language query
- `complete_task`: Marks a task as complete
- `delete_task`: Removes a task from the list
- `update_task`: Modifies task title or description

## Development Mode Features

### Environment Toggle
To switch between development and production modes, simply change the `ENVIRONMENT` variable in your `.env` file:
- `ENVIRONMENT=development`: Enables CORS for localhost, hot reloading, and verbose logging
- `ENVIRONMENT=production`: Restricts CORS and reduces logging

### Testing the Chat Functionality
1. Obtain a valid JWT token from your authentication system
2. Make POST requests to `/api/{your_user_id}/chat` with the authorization header
3. Observe how the AI interprets natural language and performs task operations

## Troubleshooting

### Common Issues
1. **CORS errors**: Ensure your `ENVIRONMENT` variable is set correctly and `FRONTEND_API_URL` matches your frontend URL
2. **Database connection errors**: Verify your `DATABASE_URL` is correct and the database is accessible
3. **Authentication errors**: Confirm your JWT token is valid and `BETTER_AUTH_SECRET` matches the frontend
4. **AI agent not responding**: Check that your `OPENAI_API_KEY` is valid and has sufficient quota

### Development Mode Specific
- Enable debug logging by setting `DEBUG=True` in your environment
- Hot reloading should automatically restart the server when code changes are detected
- Use the development database settings to avoid impacting production data

## Next Steps
1. Integrate the chat interface into your frontend application
2. Test the AI's ability to understand natural language task requests
3. Fine-tune the MCP tools based on user feedback
4. Monitor performance and optimize as needed