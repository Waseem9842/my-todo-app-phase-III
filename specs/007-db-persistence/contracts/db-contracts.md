# API Contracts: Database Models, Migrations & Persistence for AI Todo Chatbot

## Overview
This document defines the database contracts and access patterns for the persistence layer of the AI Todo Chatbot. These contracts ensure proper data isolation, consistency, and access patterns between the application services and the database layer.

## Entity Contracts

### Task Entity Contract

**Schema Definition**:
```sql
Table: tasks
- id: INTEGER (PRIMARY KEY, AUTO_INCREMENT)
- title: VARCHAR(255) (NOT NULL, length 1-255)
- description: TEXT (NULL, max length 1000)
- completed: BOOLEAN (NOT NULL, DEFAULT FALSE)
- user_id: VARCHAR (NOT NULL, identifies the owner)
- created_at: TIMESTAMP (NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- updated_at: TIMESTAMP (NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
```

**Access Contract**:
- All read/write operations must include user_id validation
- Queries must filter by user_id to ensure isolation
- Creation requires valid user_id
- Updates/deletes require user_id match validation

**Validation Contract**:
- Title: Required, 1-255 characters
- Description: Optional, max 1000 characters
- user_id: Required, non-empty string

### Conversation Entity Contract

**Schema Definition**:
```sql
Table: conversations
- id: INTEGER (PRIMARY KEY, AUTO_INCREMENT)
- user_id: VARCHAR (NOT NULL, identifies the owner)
- started_at: TIMESTAMP (NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- updated_at: TIMESTAMP (NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
- status: VARCHAR (NOT NULL, DEFAULT 'active', values: 'active', 'closed', 'archived')
```

**Access Contract**:
- All operations require user_id validation
- Only conversations belonging to the user can be accessed
- Creation requires valid user_id
- Status updates must follow valid state transitions

**Validation Contract**:
- user_id: Required, non-empty string
- status: Required, one of allowed values

### Message Entity Contract

**Schema Definition**:
```sql
Table: messages
- id: INTEGER (PRIMARY KEY, AUTO_INCREMENT)
- conversation_id: INTEGER (NOT NULL, FOREIGN KEY to conversations.id)
- role: VARCHAR (NOT NULL, values: 'user', 'assistant', 'system')
- content: TEXT (NOT NULL, max length 10000)
- timestamp: TIMESTAMP (NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- tool_calls: JSON (NULL, stores MCP tool calls)
- tool_results: JSON (NULL, stores results from tool calls)
```

**Access Contract**:
- Messages can only be accessed through valid conversation owned by the user
- Creation requires valid conversation_id and user_id validation
- All queries must validate conversation ownership via user

**Validation Contract**:
- conversation_id: Required, must reference existing conversation
- role: Required, one of allowed values
- content: Required, non-empty
- tool_calls/tool_results: Optional JSON objects

## Service Layer Contracts

### Task Service Contract

**Method**: `create_task(task_data, db_session)`
- Input: TaskCreate object with valid user_id
- Output: Created Task object or exception
- Contract: Validates user_id, creates task with provided data, enforces user isolation

**Method**: `get_tasks_by_user(user_id, db_session)`
- Input: user_id string
- Output: List of Task objects belonging to user
- Contract: Returns only tasks owned by specified user

**Method**: `update_task(task_id, user_id, task_update, db_session)`
- Input: task_id, user_id, TaskUpdate object
- Output: Updated Task object or None if not found/authorized
- Contract: Validates user owns task before updating

**Method**: `delete_task(task_id, user_id, db_session)`
- Input: task_id, user_id
- Output: Boolean success indicator
- Contract: Validates user owns task before deletion

### Conversation Service Contract

**Method**: `create_conversation(conversation_data, db_session)`
- Input: ConversationCreate object with valid user_id
- Output: Created Conversation object
- Contract: Creates conversation associated with user_id

**Method**: `get_conversations_by_user(user_id, db_session)`
- Input: user_id string
- Output: List of Conversation objects belonging to user
- Contract: Returns only conversations owned by specified user

### Message Service Contract

**Method**: `create_message(message_data, db_session)`
- Input: MessageCreate object with valid conversation_id
- Output: Created Message object
- Contract: Validates conversation exists and belongs to user before creating message

**Method**: `get_messages_by_conversation(conversation_id, user_id, db_session)`
- Input: conversation_id, user_id
- Output: List of Message objects in conversation
- Contract: Validates user owns the conversation before returning messages

## Migration Contract

**Migration Requirements**:
- All schema changes must be implemented through Alembic migrations
- Migrations must be backward compatible where possible
- Migration scripts must be idempotent
- Migration testing must verify data integrity

**Deployment Contract**:
- Migrations must run successfully on Neon PostgreSQL
- Zero-downtime deployments preferred
- Rollback scripts must be provided for non-trivial changes
- Migration validation must occur before applying to production

## Error Handling Contract

**Database Errors**:
- Connection failures: Return appropriate service errors
- Constraint violations: Validate before database insertion
- Isolation violations: Reject with clear authorization errors
- Transaction failures: Implement proper rollback procedures

**User Isolation Errors**:
- All unauthorized access attempts must be logged
- Clear error messages without revealing sensitive information
- Proper HTTP status codes (403 for authorization failures)