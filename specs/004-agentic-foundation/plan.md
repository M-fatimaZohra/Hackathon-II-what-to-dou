# Implementation Plan: Phase III – Backend Agentic Foundation

**Branch**: `004-agentic-foundation` | **Date**: 2026-02-03 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-agentic-foundation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements a stateless AI Chatbot using the Official MCP SDK and OpenAI Agents SDK with strict data modeling. The implementation will add Conversation and Message models to the existing backend, implement an MCP server with tools for task management, and create a chat endpoint that processes natural language input for task operations. Additionally, this plan includes updating all monorepo documentation to reflect the current state of the application and prepare for the new functionality.

## Technical Context

**Language/Version**: Python 3.12, FastAPI 0.128.0, SQLModel 0.0.16, Neon PostgreSQL
**Primary Dependencies**: FastAPI, SQLModel ORM, OpenAI Agents SDK, Official MCP SDK, python-jose, psycopg2-binary
**Storage**: Neon PostgreSQL database with existing Task table and new Conversation/Message tables
**Testing**: pytest for backend testing, with test-first approach for MCP integration and agent functionality
**Target Platform**: Linux server deployment with containerization support
**Project Type**: web - extends existing backend with new agentic capabilities
**Performance Goals**: <3 second response time for 90% of chatbot interactions, 95% success rate for task operations
**Constraints**: User data isolation (100% cross-user access prevention), JWT authentication for all endpoints, stateless agent operations
**Scale/Scope**: Multi-user support with conversation history, natural language processing for task management

## Authentication Context Propagation

### MCP SDK Integration Security Contract
All MCP tool calls must propagate the authenticated user ID (auth_user_id) from the API layer through the service layer to MCP tools. This ensures that each tool call includes proper authentication context and maintains data isolation:

- **API Layer**: Extracts auth_user_id from JWT token and passes to service layer
- **Service Layer**: Explicitly passes auth_user_id to MCP tools via context parameter
- **MCP Tools**: Validate that auth_user_id matches the user_id in request parameters and reject operations without valid auth_user_id

### MCP Tool Return Contract (Updated for Agent Reliability)
To address agent "fallback errors" and improve communication reliability with the LLM, all MCP tools now return descriptive string receipts instead of structured JSON objects:

- **Return Format**: All tools return descriptive strings in format "SUCCESS: [Action completed] (ID: [id])" or "ERROR: [Reason]"
- **Purpose**: Prevents parsing issues between agent and MCP tools over Stdio pipe
- **User Experience**: Task IDs in return strings are for AI memory only and must be hidden from end-user in final UI response
- **Agent Compatibility**: String responses are more reliably processed by LLM compared to complex JSON structures

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-Driven Development (SDD)**: ✓ Plan originates from written specification in spec.md
2. **AI-Agent-First Approach**: ✓ Plan incorporates OpenAI Agents SDK and MCP SDK as primary implementation tools
3. **Iterative & Phased Evolution**: ✓ Plan extends existing Phase II application to Phase III with AI-powered chatbot
4. **Clarity Over Cleverness**: ✓ Plan uses clear, understandable architecture with stateless agent cycles
5. **Future-Ready by Design**: ✓ Plan prepares for future AI integration while maintaining existing functionality
6. **Test-First (NON-NEGOTIABLE)**: ✓ Plan includes test-first implementation with pytest suites

## Project Structure

### Documentation (this feature)

```text
specs/004-agentic-foundation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extends existing structure)

```text
backend/
├── src/
│   ├── configs/
│   │   └── gemini_config.py       # NEW: Stores Gemini model parameters, reads GEMINI_API_KEY from env
│   │   └── groq_config.py          # NEW: Groq model configuration for backup/rate-limit avoidance
│   ├── main.py                    # Updated with environment toggle
│   ├── api/
│   │   ├── tasks.py               # Existing task endpoints
│   │   └── chat.py                # NEW: Chat endpoint with MCP integration
│   ├── models/                    # DEPRECATED: moved to schema/
│   ├── schema/
│   │   ├── models.py              # Updated with Conversation/Message models
│   │   └── chat_models.py         # NEW: Chat-specific models
│   ├── services/
│   │   ├── task_service.py        # Existing task service
│   │   ├── chat_service.py        # NEW: Chat/MCP service layer (chatbot engine that initializes Agent and handles Runner() logic)
│   │   └── conversation_service.py # NEW: Database service for chat history (CRUD for Conversation/Message tables)
│   ├── middleware/
│   │   └── auth_handler.py        # Existing auth middleware
│   ├── database/
│   │   ├── db.py                  # Updated with environment toggle
│   │   └── init_db.py             # Database initialization
│   └── my_mcp_server/
│       ├── server.py              # NEW: MCP server implementation
│       └── tools/                 # NEW: MCP tools for task operations
│           ├── task_create_tool.py
│           ├── task_list_tool.py
│           ├── task_update_tool.py
│           ├── task_delete_tool.py
│           └── task_complete_tool.py
└── tests/
    ├── test_chat.py               # NEW: Chat endpoint tests
    ├── test_conversation.py       # NEW: Conversation model tests
    └── test_mcp_integration.py    # NEW: MCP integration tests
```

### Updated Monorepo Documentation

```text
specs/
├── overview.md                   # Updated to reflect current state
├── architecture.md               # Updated with agentic architecture
├── branding.md                   # Updated if needed
├── features/
│   ├── todo_crud.md              # Updated to reflect current implementation
│   ├── authentication.md         # Updated to reflect current implementation
│   └── agentic_chat.md           # NEW: Chatbot-specific features
├── api/
│   ├── rest-endpoints.md         # Updated with chat endpoints
│   └── mcp-tools.md              # NEW: MCP tool specifications
├── database/
│   └── schema.md                 # Updated with Conversation/Message tables
└── ui/
    ├── components.md             # Updated to reflect current components
    └── pages.md                  # Updated to reflect current pages
```

**Structure Decision**: Extends existing web application structure by adding new chat-specific modules while maintaining existing task management functionality. New MCP server component handles agent-tool communication, and new data models support conversation history.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP SDK Integration | Required for standardized AI agent communication | Direct API calls would lack standardization and extensibility |
| Stateless Agent Architecture | Required for scalability and session independence | Stateful agents would complicate deployment and scaling |
