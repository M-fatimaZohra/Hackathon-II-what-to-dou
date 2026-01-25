# Implementation Plan: Phase II – Full-Stack Todo Web Application

**Feature Branch**: `002-todo-web-app`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Plan the implementation of the full-stack Todo Web Application with authentication, persistent storage, and modern UI"

## Overview

This plan outlines the implementation of the full-stack Todo Web Application with authentication, persistent storage, and modern UI using the specified tech stack and monorepo structure.

## Architecture Summary

### Tech Stack
- **Frontend**: Next.js (App Router) + TypeScript + Tailwind CSS + Better Auth
- **Backend**: FastAPI + Python + SQLModel (ORM) + JWT token validation
- **Database**: Neon Serverless PostgreSQL
- **Security**: User data isolation; JWT tokens validate all API endpoints

### Architecture Decision Records (ADRs)

#### ADR-004: Server-Side Dynamic Query Building
**Decision**: Use FastAPI `Query` parameters and SQLModel conditional `.where()` chaining for search and filter functionality.
**Rationale**: To maintain user data isolation and prevent 422 errors, we will use FastAPI `Query` parameters and SQLModel conditional `.where()` chaining. This ensures a stable API contract without modifying path parameters.
**Status**: Accepted
**Date**: 2026-01-22

### System Architecture
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
                                            │ Database
                                            ▼
                                ┌─────────────────────────┐
                                │    Database             │
                                │                         │
                                │  Neon Serverless        │
                                │  PostgreSQL             │
                                └─────────────────────────┘
```

## Monorepo Structure

### Directory Structure
The project follows the monorepo structure as specified, with all specification documents organized in a logical hierarchy:

```
specs/
├── overview.md           # Project overview
├── architecture.md       # System architecture
├── branding.md           # Branding guidelines and visual identity
├── features/
│   ├── todo_crud.md      # Task management features
│   └── authentication.md # Authentication features
├── api/
│   ├── rest-endpoints.md # REST API endpoints
│   └── mcp-tools.md      # Commands/tools related to implementation
├── database/
│   └── schema.md         # Users and tasks schema
└── ui/
    ├── components.md     # Reusable components
    └── pages.md          # Pages: login, signup, task list, task detail
```

This structure has been implemented and all files have been created as specified.

### .spec-kit/config.yaml
The configuration file has been created at `.spec-kit/config.yaml` with the following corrected content:

```yaml
name: 00-ai-native-todo-app
version: "1.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
phases:
  - name: 001-todo-cli
    features: [todo_crud]
  - name: 002-todo-web-app
    features: [todo_crud, authentication]
```

This configuration properly connects the phases, specs, and tasks as requested in the requirements with the correct YAML structure.

## Implementation Phases

### Phase 1: Project Setup and Monorepo Structure
**Priority**: P1
**Dependencies**: None

**Tasks**:
- Set up Next.js project with TypeScript and Tailwind CSS
- Configure FastAPI backend project
- Set up Neon Serverless PostgreSQL connection
- Create the complete specs/ folder structure
- Configure .spec-kit/config.yaml with proper phase mapping
- Integrate Better Auth for frontend authentication

**Acceptance Criteria**:
- Next.js development server runs without errors
- FastAPI server starts and responds to basic requests
- Database connection established
- Complete directory structure created
- Configuration file properly set up

### Phase 2: Better Auth Integration and JWT Configuration
**Priority**: P1
**Dependencies**: Phase 1

**Tasks**:
- Configure Better Auth with JWT plugin enabled
- Configure shared secret (BETTER_AUTH_SECRET) for JWT signing
- Implement frontend authentication components using Better Auth
- Create backend middleware to validate JWT tokens
- Implement JWT token handling in API requests
- Ensure user data isolation (users can only access their own tasks)

**Acceptance Criteria**:
- Better Auth properly configured with JWT support
- Frontend authentication flows work seamlessly and issue JWT tokens
- Backend properly validates JWT tokens with shared secret
- Protected routes reject requests without valid JWT
- Users cannot access other users' tasks

### Phase 3: Todo Task CRUD Implementation
**Priority**: P1
**Dependencies**: Phase 2

**Tasks**:
- Create SQLModel models for tasks
- Implement database schema for tasks
- Create API endpoints for task management that validate JWT tokens:
  - GET /api/{user_id}/tasks - List all tasks for the specified user
  - POST /api/{user_id}/tasks - Create a new task for the specified user
  - GET /api/{user_id}/tasks/{id} - Get specific task (must belong to user)
  - PUT /api/{user_id}/tasks/{id} - Update specific task (must belong to user)
  - DELETE /api/{user_id}/tasks/{id} - Delete specific task (must belong to user)
  - PATCH /api/{user_id}/tasks/{id}/complete - Toggle task completion (must belong to user)
- Implement task validation and error handling
- Add proper foreign key relationships between users and tasks
- Ensure all operations validate JWT token and compare user_id from JWT with user_id in URL path

**Acceptance Criteria**:
- Users can create new tasks with title, description, and priority
- Users can view their tasks (filtered by user_id from JWT token)
- Users can update task details for their own tasks
- Users can delete their own tasks
- Users can toggle task completion status for their own tasks
- All operations properly validate JWT token and user_id matching
- Proper data validation and error handling

### Phase 4: Search and Filter Functionality
**Priority**: P2
**Dependencies**: Phase 3

**Tasks**:
- **Task 4.1 (RED)**: Implement Backend Integration Tests in `backend/tests/test_search.py` specifically for cross-user isolation and partial-match logic.
- **Task 4.2 (GREEN)**: Implement dynamic filtering in `task_service.py` to satisfy the tests.
- **Task 4.3 (CONTRACT)**: Update the GET route in `tasks.py` to accept and pass optional query parameters.
- **Task 4.4 (FRONTEND)**: Implement `SearchFilter.tsx` using `URLSearchParams` for safe URL construction and a 300ms debounce.

**Acceptance Criteria**:
- Users can search tasks by keywords in title or description
- Users can filter tasks by priority level
- Users can filter tasks by completion status
- Search and filter operations are performant
- All filtered queries maintain user data isolation with `.where(Task.user_id == user_id)` as base condition

**Security Implementation**:
- **Primary Filter Constraint**: Every filtered query MUST have `.where(Task.user_id == user_id)` as the base condition before any search or priority filters are appended.

### Phase 5: Frontend UI Implementation
**Priority**: P2
**Dependencies**: Phase 3

**Tasks**:
- Integrate Better Auth components for login/signup flows
- Create task list page component
- Create task detail/edit page component
- Create reusable UI components (buttons, forms, modals)
- Implement responsive design for mobile and desktop
- Add loading states and error handling UI
- Implement task creation form
- Implement task editing functionality

**Acceptance Criteria**:
- All pages are responsive and work on different screen sizes
- UI components are reusable and consistent
- Better Auth integration works seamlessly
- Form validation works properly
- Loading and error states are handled gracefully
- User interactions are intuitive and smooth

### Phase 6: Frontend-Backend Integration
**Priority**: P2
**Dependencies**: Phase 2, Phase 3, Phase 5

**Tasks**:
- Connect frontend forms to backend API endpoints
- Implement JWT token handling in frontend requests (Authorization: Bearer <token>)
- Set up API client with proper error handling
- Implement real-time updates for task changes
- Add proper error messages for API failures
- Implement optimistic updates where appropriate

**Acceptance Criteria**:
- All frontend actions successfully communicate with backend
- JWT tokens are properly included in API requests
- API errors are handled gracefully in UI
- Data flows correctly between frontend and backend

### Phase 7: Security Validation and Testing
**Priority**: P1
**Dependencies**: All previous phases

**Tasks**:
- Validate that users cannot access other users' tasks
- Test JWT token validation and expiration
- Verify all API endpoints require proper JWT token in Authorization header
- Test input validation and sanitization
- Perform security audit of JWT implementation
- Test edge cases and error conditions

**Acceptance Criteria**:
- Users can only access their own tasks
- JWT tokens are properly validated and handled
- All security requirements are met
- No security vulnerabilities found in audit

### Phase 8: Finalization and Preparation for Implementation
**Priority**: P3
**Dependencies**: All previous phases

**Tasks**:
- Create detailed task list for implementation
- Update all spec.md files with implementation details
- Create version control strategy
- Document deployment process
- Prepare for /sp.implement with linked tasks
- Finalize all configuration files

**Acceptance Criteria**:
- Complete task list created for implementation
- All specifications are detailed and clear
- Configuration files are properly set up
- Deployment process is documented

## Key Entities and Database Schema

### Users Table (managed by Better Auth)
- id (string, primary key)
- email (string, unique)
- created_at (timestamp)

### Tasks Table
- id (integer, primary key, auto-increment)
- user_id (foreign key → users.id)
- title (string, not null)
- description (text, optional)
- completed (boolean, default: false)
- priority (enum: 'low', 'medium', 'high', 'urgent', default: 'medium')
- created_at (timestamp)
- updated_at (timestamp)

## API Specification

### Authentication Integration
- Authentication is handled exclusively by Better Auth
- Backend only validates authenticated requests using Better Auth session context
- No custom auth endpoints will be implemented (signup, signin, etc.)

### Task Endpoints
- GET /api/{user_id}/tasks - List all tasks for the specified user
- POST /api/{user_id}/tasks - Create a new task for the specified user
- GET /api/{user_id}/tasks/{id} - Get specific task (must belong to user)
- PUT /api/{user_id}/tasks/{id} - Update specific task (must belong to user)
- DELETE /api/{user_id}/tasks/{id} - Delete specific task (must belong to user)
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle task completion (must belong to user)

### Security Implementation
- All task endpoints require valid JWT token in Authorization header
- Backend verifies JWT signature using shared secret (BETTER_AUTH_SECRET)
- User ID is extracted from JWT payload and compared with user_id in URL path
- Tasks are filtered by user ID to ensure data isolation
- Requests without valid JWT receive 401 Unauthorized response

## Risk Analysis and Mitigation

### High-Risk Areas
1. **Security**: User data isolation is critical
   - Mitigation: Implement strict user ID validation comparing JWT payload with user_id in URL path
2. **Authentication**: Proper JWT token validation and shared secret management
   - Mitigation: Use industry-standard JWT libraries and secure secret management
3. **Database**: Proper foreign key relationships and data integrity
   - Mitigation: Use SQLModel's validation and database constraints

### Technical Challenges
1. **Frontend-Backend Integration**: Ensuring proper JWT token handling
   - Mitigation: Create clear API contracts and thorough testing
2. **Performance**: Handling large numbers of tasks efficiently
   - Mitigation: Proper database indexing and pagination
3. **JWT Implementation**: Proper token validation and user identity verification
   - Mitigation: Follow JWT best practices and security standards

## Success Criteria

### Technical Success
- All planned features are implemented and working
- Security requirements are fully met
- Application performs well under expected load
- Code follows established patterns and standards

### User Success
- Users can complete account registration and sign-in through Better Auth within 1 minute
- Users can create a new task within 30 seconds of accessing the application
- 95% of user actions (create, read, update, delete) complete successfully without errors
- Users can access their tasks from different devices and see synchronized data
- The application loads and displays the task list within 3 seconds for users with up to 100 tasks
- 90% of users successfully complete primary task management functions (create, update, delete, mark complete) on first attempt

## Next Steps

1. Execute Phase 1: Project Setup and Monorepo Structure
2. Proceed through implementation phases in order
3. Create detailed tasks for each phase
4. Prepare for implementation with /sp.implement