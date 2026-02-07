---
id: 0005
title: explain-backend-architecture
stage: explainer
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.analyze
labels: ["analysis", "architecture", "backend", "explanation"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-agentic-foundation/spec.md
  - specs/004-agentic-foundation/plan.md
  - specs/004-agentic-foundation/tasks.md
  - specs/004-agentic-foundation/data-model.md
  - specs/004-agentic-foundation/quickstart.md
tests:
  - null
---

## Prompt


according to current specifications how will you build backend (do not implement, just explain)

## Response snapshot

Based on my analysis of all the specifications, I can now explain how the backend will be built according to the current specifications:

## How the Backend Will Be Built According to Current Specifications

The backend for the AI-powered chatbot feature will be built as an extension to the existing Python FastAPI application with the following architecture:

### 1. Technology Stack
- **Language**: Python 3.12
- **Framework**: FastAPI 0.104.1
- **ORM**: SQLModel 0.0.16
- **Database**: Neon PostgreSQL
- **External Libraries**: OpenAI Agents SDK, Official MCP SDK, python-jose, psycopg2-binary

### 2. Data Layer
- **New Tables**:
  - `conversations` table with columns for id, user_id (as VARCHAR), created_at, updated_at
  - `messages` table with columns for id, user_id, conversation_id, role (user/assistant), content, created_at
- **Relationships**: Foreign key constraints linking conversations and messages to users
- **Security**: User isolation enforced through user_id filtering on all queries

### 3. Architecture Components
- **MCP Server**: A new MCP (Model Context Protocol) server implementation with 5 task CRUD tools:
  - `task_create_tool.py`
  - `task_list_tool.py`
  - `task_update_tool.py`
  - `task_delete_tool.py`
  - `task_complete_tool.py`
- **Agent Service**: A stateless AI agent using OpenAI Agents SDK that communicates with the MCP server
- **Services Layer**:
  - `chat_service.py` - handles chatbot logic and agent communication
  - `conversation_service.py` - manages conversation lifecycle
  - `message_service.py` - handles message storage and retrieval

### 4. API Endpoints
- **New Endpoint**: POST `/api/{user_id}/chat` accepting `{conversation_id: int?, message: str}`
- **Response**: `{conversation_id: int, response: str, tool_calls: array}`
- **Authentication**: JWT token validation for all endpoints
- **User Isolation**: All operations filtered by user_id to prevent cross-user access

### 5. Environment Configuration
- **Toggle System**: Production/Development mode toggle via environment variables
- **Configuration**: Different security and logging settings based on environment mode
- **Database**: Separate configurations for dev/prod environments

### 6. Implementation Strategy
- **Phased Approach**:
  1. Setup phase (T001-T003): Project structure and dependencies
  2. Foundational phase (T004-T009): Core infrastructure
  3. User Story 1 (T010-T021): Core AI chatbot functionality
  4. User Story 2 (T022-T029): Conversation management
  5. User Story 3 (T030-T035): Environment toggle functionality

### 7. Security & Compliance
- **Data Isolation**: 100% prevention of cross-user access through user_id filtering
- **JWT Authentication**: All endpoints require valid JWT tokens
- **Role-based Access**: Messages have role distinction (user/assistant)
- **Constraint Enforcement**: Database-level constraints to maintain data integrity

### 8. Development Process
- **Test-First**: Following the constitution's mandate for TDD
- **Spec-Driven**: All implementation based on the written specifications
- **Modular Design**: Separate modules for different concerns (API, services, models, MCP tools)
- **Parallel Development**: Tasks designed to support parallel implementation where possible

The backend will essentially transform the existing task management system into an AI-powered assistant that can interpret natural language commands to perform task operations, while maintaining all the security and data isolation requirements of the original system.

## Outcome

- ✅ Impact: Comprehensive explanation of backend architecture based on current specifications
- 🧪 Tests: No tests needed for this analysis/explanation task
- 📁 Files: Referenced multiple spec files (spec.md, plan.md, tasks.md, data-model.md, quickstart.md)
- 🔁 Next prompts: Ready for implementation based on the explained architecture
- 🧠 Reflection: The backend architecture combines stateless AI agents with MCP protocol for secure task management

## Evaluation notes (flywheel)

- Failure modes observed: None - complete architecture overview provided
- Graders run and results (PASS/FAIL): Not applicable for this explanation task
- Prompt variant (if applicable): Standard analysis command
- Next experiment (smallest change to try): Begin implementation following the explained architecture