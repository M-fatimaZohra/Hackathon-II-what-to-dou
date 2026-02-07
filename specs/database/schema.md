# Database Schema: AI Native Todo Application

## Overview
This document defines the database schema for the AI Native Todo Application. The application uses Neon Serverless PostgreSQL for persistent storage. The schema includes tables for users (managed by Better Auth), tasks, and new tables for AI chatbot functionality (conversations and messages), with proper relationships and constraints to ensure data integrity and security.

## Database Configuration
- **Database Type**: PostgreSQL (Neon Serverless)
- **Connection Pooling**: Enabled for optimal performance
- **SSL**: Required for all connections
- **Backup Strategy**: Automated daily backups with point-in-time recovery

## Schema Diagram
```
+----------------+          +------------------+          +---------------+
|    users       |          |  conversations   |          |    messages   |
|----------------|          |------------------|          |---------------|
| id (PK)        |<---------| user_id (FK)     |<---------| conversation_ |
| email          |          | id (PK)          |          | id (FK)       |
| email_verified |          | created_at       |          | id (PK)       |
| created_at     |          | updated_at       |          | user_id (FK)  |
| updated_at     |          +------------------+          | role          |
+----------------+                                         | content       |
                                                          | created_at    |
                                                                 |
                                                    +------------+-------------+
                                                    |                          |
                                      +-------------------+    +-------------------+
                                      |      tasks        |    |   task updates    |
                                      |-------------------|    |-------------------|
                                      | id (PK)           |    | id (PK)           |
                                      | user_id (FK)      |    | conversation_id   |
                                      | title             |    | task_id (FK)      |
                                      | description       |    | update_type       |
                                      | completed         |    | content           |
                                      | priority          |    | created_at        |
                                      | created_at        |    +-------------------+
                                      | updated_at        |
                                      +-------------------+
```

## Table Definitions

### Users Table (Managed by Better Auth)
This table is primarily managed by Better Auth, with the following structure:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| email_verified | BOOLEAN | DEFAULT FALSE | Whether the email has been verified |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_users_email`: Unique index on email column for fast lookups and uniqueness enforcement
- `idx_users_created_at`: Index on created_at for chronological queries

**Constraints**:
- `pk_users_id`: Primary key constraint on id
- `uk_users_email`: Unique constraint on email
- `ck_users_email_format`: Check constraint to ensure email format (via application logic)

### Tasks Table
This table stores all user tasks with proper relationships to users:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY, NOT NULL | Auto-incrementing task identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to users table |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Task description (optional) |
| completed | BOOLEAN | DEFAULT FALSE | Task completion status |
| priority | VARCHAR(20) | DEFAULT 'medium', CHECK | Priority level: 'low', 'medium', 'high', 'urgent' |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_tasks_user_id`: Index on user_id for fast user-based queries
- `idx_tasks_priority`: Index on priority for priority-based filtering
- `idx_tasks_completed`: Index on completed for status-based queries
- `idx_tasks_created_at`: Index on created_at for chronological ordering
- `idx_tasks_title_text`: Full-text search index on title and description

**Constraints**:
- `pk_tasks_id`: Primary key constraint on id
- `fk_tasks_user_id`: Foreign key constraint linking to users table
- `ck_tasks_priority`: Check constraint ensuring priority is one of allowed values
- `ck_tasks_title_not_empty`: Check constraint ensuring title is not empty or just whitespace
- `ck_tasks_description_length`: Check constraint limiting description to 1000 characters

**Foreign Keys**:
- `fk_tasks_user_id`: References users(id) with CASCADE on DELETE to remove tasks when user is deleted

### Conversations Table
This table stores chat session information for the AI chatbot functionality:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY, NOT NULL | Auto-incrementing conversation identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to users table |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_conversations_user_id`: Index on user_id for fast user-based queries
- `idx_conversations_created_at`: Index on created_at for chronological ordering

**Constraints**:
- `pk_conversations_id`: Primary key constraint on id
- `fk_conversations_user_id`: Foreign key constraint linking to users table
- `ck_conversations_user_id_not_empty`: Check constraint ensuring user_id is not empty

**Foreign Keys**:
- `fk_conversations_user_id`: References users(id) with CASCADE on DELETE to remove conversations when user is deleted

### Messages Table
This table stores individual chat messages for the AI chatbot functionality:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY, NOT NULL | Auto-incrementing message identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to users table |
| conversation_id | INTEGER | NOT NULL, FOREIGN KEY | Reference to conversations table |
| role | VARCHAR(20) | NOT NULL, CHECK | Role: 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message creation timestamp |

**Indexes**:
- `idx_messages_user_id`: Index on user_id for fast user-based queries
- `idx_messages_conversation_id`: Index on conversation_id for conversation-based queries
- `idx_messages_created_at`: Index on created_at for chronological ordering
- `idx_messages_role`: Index on role for filtering by message type

**Constraints**:
- `pk_messages_id`: Primary key constraint on id
- `fk_messages_user_id`: Foreign key constraint linking to users table
- `fk_messages_conversation_id`: Foreign key constraint linking to conversations table
- `ck_messages_role`: Check constraint ensuring role is 'user' or 'assistant'
- `ck_messages_content_not_empty`: Check constraint ensuring content is not empty or just whitespace

**Foreign Keys**:
- `fk_messages_user_id`: References users(id) with CASCADE on DELETE
- `fk_messages_conversation_id`: References conversations(id) with CASCADE on DELETE

## Security Considerations

### Data Isolation
- Row-level security ensures users can only access their own tasks, conversations, and messages
- All queries must filter by user_id to enforce data isolation
- Database views or security policies can be implemented to enforce this at the database level

### Indexing Strategy
- Proper indexing on user_id for fast filtering by user
- Indexing on priority and completion status for filtering
- Full-text search index for title/description search functionality
- Timestamp indexes for chronological operations

### Constraints
- Check constraints ensure data integrity for priority values
- Foreign key constraints maintain referential integrity
- NOT NULL constraints ensure required fields are always populated

## Performance Optimizations

### Query Optimization
- Composite indexes for common query patterns (e.g., user_id + priority)
- Proper indexing for search functionality
- Consider partial indexes for frequently filtered values

### Partitioning
- For large datasets, consider partitioning by user_id or created_at
- Horizontal sharding by user_id for very large applications

### Caching Strategy
- Cache frequently accessed user data
- Cache user-specific task lists with appropriate invalidation
- Implement application-level caching for complex queries

## Migration Strategy

### Initial Setup
```sql
-- Create conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT ck_messages_role CHECK (role IN ('user', 'assistant')),
    CONSTRAINT ck_messages_content_not_empty CHECK (LENGTH(TRIM(content)) > 0)
);

-- Create indexes for conversations
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);

-- Create indexes for messages
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_role ON messages(role);
```

### Future Migrations
- Use migration framework (like Alembic for Python) to manage schema changes
- Always test migrations on a copy of production data
- Plan for zero-downtime migrations where possible
- Maintain backward compatibility during migrations

## Backup and Recovery

### Backup Strategy
- Automated daily backups of the entire database
- Point-in-time recovery capability
- Off-site backup storage for disaster recovery
- Regular backup verification and restoration testing

### Recovery Procedures
- Documented procedures for restoring from backups
- Regular testing of recovery procedures
- Procedures for restoring individual tables if needed
- Rollback procedures for failed migrations

## Monitoring and Maintenance

### Database Monitoring
- Monitor query performance and execution times
- Track database connection usage
- Monitor disk space and growth
- Alerting for slow queries or high resource usage

### Maintenance Tasks
- Regular index optimization and rebuilding
- Vacuuming and analyzing tables for performance
- Monitoring for dead tuples and bloat
- Regular integrity checks

## Sample Queries

### Common Operations
```sql
-- Get all conversations for a specific user
SELECT * FROM conversations WHERE user_id = $1 ORDER BY created_at DESC;

-- Get messages for a specific conversation
SELECT * FROM messages WHERE conversation_id = $1 ORDER BY created_at ASC;

-- Get messages for a user with conversation context
SELECT m.*, c.created_at as conversation_start
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE m.user_id = $1 AND c.id = $2
ORDER BY m.created_at ASC;
```

### Security Queries
```sql
-- Ensure user can only access their own conversations and messages
SELECT * FROM conversations
WHERE user_id = $1 AND id = $2;  -- $1 is extracted from JWT, $2 is requested conversation ID

SELECT * FROM messages
WHERE user_id = $1 AND conversation_id = $2;  -- Verify user access to specific conversation
```

## Schema Evolution
- Add new columns with appropriate default values
- Use NOT NULL constraints with defaults when possible
- Consider backward compatibility when modifying existing columns
- Plan for deprecation of old columns/tables
- Document all schema changes in the change log