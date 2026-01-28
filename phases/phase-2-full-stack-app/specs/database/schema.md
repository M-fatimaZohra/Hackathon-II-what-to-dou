# Database Schema: AI Native Todo Application

## Overview
This document defines the database schema for the AI Native Todo Application. The application uses Neon Serverless PostgreSQL for persistent storage. The schema includes tables for users (managed by Better Auth) and tasks, with proper relationships and constraints to ensure data integrity and security.

## Database Configuration
- **Database Type**: PostgreSQL (Neon Serverless)
- **Connection Pooling**: Enabled for optimal performance
- **SSL**: Required for all connections
- **Backup Strategy**: Automated daily backups with point-in-time recovery

## Schema Diagram
```
+----------------+          +------------------+
|    users       |          |     tasks        |
|----------------|          |------------------|
| id (PK)        |<---------| user_id (FK)     |
| email          |          | id (PK)          |
| email_verified |          | title            |
| created_at     |          | description      |
| updated_at     |          | completed        |
+----------------+          | priority         |
                           | created_at       |
                           | updated_at       |
                           +------------------+
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

## Security Considerations

### Data Isolation
- Row-level security ensures users can only access their own tasks
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
-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT ck_tasks_priority CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    CONSTRAINT ck_tasks_title_not_empty CHECK (LENGTH(TRIM(title)) > 0),
    CONSTRAINT ck_tasks_description_length CHECK (LENGTH(description) <= 1000)
);

-- Create indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_title_text ON tasks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')));
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
-- Get all tasks for a specific user
SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;

-- Get tasks filtered by priority
SELECT * FROM tasks WHERE user_id = $1 AND priority = $2;

-- Get completed tasks
SELECT * FROM tasks WHERE user_id = $1 AND completed = true;

-- Search tasks by title/description
SELECT * FROM tasks
WHERE user_id = $1
AND to_tsvector('english', title || ' ' || COALESCE(description, ''))
@@ plainto_tsquery('english', $2);
```

### Security Queries
```sql
-- Ensure user can only access their own tasks
SELECT * FROM tasks
WHERE user_id = $1 AND id = $2;  -- $1 is extracted from JWT, $2 is requested task ID
```

## Schema Evolution
- Add new columns with appropriate default values
- Use NOT NULL constraints with defaults when possible
- Consider backward compatibility when modifying existing columns
- Plan for deprecation of old columns/tables
- Document all schema changes in the change log