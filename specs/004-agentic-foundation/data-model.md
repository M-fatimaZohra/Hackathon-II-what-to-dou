# Data Model: Phase III – Backend Agentic Foundation

## Overview
This document defines the database schema extensions for the AI Chatbot functionality, building upon the existing Todo application schema.

## Extended Schema Diagram
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

## New Table Definitions

### Conversation Table
This table stores chat session information with proper relationships to users:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Auto-incrementing conversation identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to users table (from JWT) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_conversations_user_id`: Index on user_id for fast user-based queries
- `idx_conversations_created_at`: Index on created_at for chronological ordering

**Constraints**:
- `pk_conversations_id`: Primary key constraint on id
- `fk_conversations_user_id`: Foreign key constraint linking to users table
- `ck_conversations_user_id_not_empty`: Check constraint ensuring user_id is not empty

### Message Table
This table stores individual chat messages with proper relationships to conversations and users:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Auto-incrementing message identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to users table (from JWT) |
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

## Updated Relationships

### Foreign Key Constraints
- `fk_messages_user_id`: REFERENCES users(id) ON DELETE CASCADE
- `fk_messages_conversation_id`: REFERENCES conversations(id) ON DELETE CASCADE
- `fk_conversations_user_id`: REFERENCES users(id) ON DELETE CASCADE

### Security Considerations
- All queries must filter by user_id to enforce data isolation
- Conversation and message access is restricted to the owning user
- Proper JOINs must be used to verify user ownership before operations

## Integration with Existing Schema
The new tables integrate with the existing schema through the user_id foreign key that connects to the Better Auth managed users table. This maintains the existing security model where users can only access their own data.

## Performance Optimizations
- Proper indexing on user_id, conversation_id, and timestamps for fast queries
- Consider composite indexes for common query patterns (e.g., user_id + conversation_id)
- Full-text search indexes on message content if needed for search functionality
- Partitioning by user_id or date range for large-scale deployments

## Migration Strategy
1. Add conversations table with proper constraints
2. Add messages table with proper constraints and foreign keys
3. Update existing application code to use new schema
4. Add indexes for optimal performance
5. Test user isolation and security measures

## Sample Queries
```sql
-- Get all conversations for a specific user
SELECT * FROM conversations WHERE user_id = $1 ORDER BY created_at DESC;

-- Get all messages for a specific conversation
SELECT * FROM messages WHERE conversation_id = $1 ORDER BY created_at ASC;

-- Get messages for a user with conversation context
SELECT m.*, c.created_at as conversation_start
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE m.user_id = $1 AND c.id = $2
ORDER BY m.created_at ASC;
```