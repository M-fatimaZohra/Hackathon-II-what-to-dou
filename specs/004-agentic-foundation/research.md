# Research: Phase III – Backend Agentic Foundation

## Overview
This research document captures the investigation and decision-making process for implementing the stateless AI Chatbot using the Official MCP SDK and OpenAI Agents SDK with strict data modeling.

## Decision: MCP SDK vs Direct OpenAI Integration
**Rationale**: MCP SDK provides standardized communication protocols for AI agents, ensuring interoperability and extensibility. Direct OpenAI integration would be vendor-specific and harder to modify later.
**Alternatives considered**:
- Direct OpenAI API calls without MCP
- LangChain framework
- Custom communication protocol

## Decision: Stateless vs Stateful Agent Architecture
**Rationale**: Stateless agents are more scalable, easier to deploy, and don't require session persistence. Each request fetches conversation history from the database, processes it, and stores the result.
**Alternatives considered**:
- Stateful agents with in-memory conversation tracking
- Hybrid approach with cached conversation state
- Server-sent events for persistent connections

## Decision: Database Schema for Conversations
**Rationale**: Separate Conversation and Message tables provide clear data structure with proper relationships to existing Task model. This maintains user isolation and allows conversation history tracking.
**Alternatives considered**:
- Storing conversation history in Redis/cache
- Embedding conversation in Task metadata
- Flat table with JSONB fields

## Decision: Environment Toggle Implementation
**Rationale**: Using a single ENVIRONMENT variable in main.py allows easy switching between development and production modes without code changes. This affects CORS settings, logging levels, and reload behavior.
**Alternatives considered**:
- Multiple environment-specific configuration files
- Command-line arguments to uvicorn
- Docker environment variables only

## Decision: MCP Tool Design for Task Operations
**Rationale**: Creating separate MCP tools for each task operation (create, read, update, delete, complete) provides clear separation of concerns and proper validation for each action.
**Alternatives considered**:
- Single generic task tool with operation parameter
- Direct database access from agent without tools
- Batch operations combining multiple actions

## Decision: Authentication Integration with MCP
**Rationale**: Maintaining existing JWT-based authentication while integrating MCP tools ensures user isolation and security. Each MCP tool call respects user permissions.
**Alternatives considered**:
- Separate authentication for MCP tools
- Session-based authentication for chat interactions
- Removing authentication for development (insecure)

## Best Practices Identified
1. **Error Handling**: All MCP tools must return proper error messages to the agent
2. **Validation**: Input validation must occur at both API and MCP tool levels
3. **Logging**: Detailed logging for debugging while maintaining privacy
4. **Rate Limiting**: Prevent abuse of the chat interface
5. **Security**: Sanitize all inputs and validate user permissions for each operation