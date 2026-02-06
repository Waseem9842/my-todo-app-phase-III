# Quickstart Guide: Database Models, Migrations & Persistence for AI Todo Chatbot

## Overview
This guide explains how to set up and use the database persistence layer for the AI Todo Chatbot using SQLModel and Neon PostgreSQL.

## Prerequisites
- Python 3.13+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- Better Auth for user authentication

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install alembic
# Other dependencies should already be in requirements.txt
```

### 2. Configure Database Connection
Ensure the following environment variables are set in your .env file:
```bash
DATABASE_URL="postgresql://..."  # Neon PostgreSQL connection string
NEON_DB_NAME="..."               # Database name
NEON_DB_USER="..."               # Database user
NEON_DB_PASSWORD="..."           # Database password
```

### 3. Initialize Alembic Migrations
```bash
cd backend
alembic init alembic
```

## Using the Persistence Layer

### 1. Define Models
The persistence layer includes three main models:
- Task: For todo management with user isolation
- Conversation: For chat session management
- Message: For individual chat messages with tool call logging

### 2. Create Database Tables
Run migrations to create the required tables:
```bash
cd backend
alembic revision --autogenerate -m "create task, conversation, message tables"
alembic upgrade head
```

### 3. Use the Services
The service layer provides methods for all CRUD operations with proper user validation:

#### Task Operations
```python
from backend.src.services.task_service import TaskService
from sqlmodel import Session

# Create a task
task = TaskService.create_task(task_data, db_session)

# Get user's tasks
tasks = TaskService.get_tasks_by_user(user_id, db_session)

# Update a task
updated_task = TaskService.update_task(task_id, user_id, task_update, db_session)

# Delete a task
success = TaskService.delete_task(task_id, user_id, db_session)
```

#### Conversation Operations
```python
from backend.src.services.conversation_service import ConversationService

# Create a conversation
conversation = ConversationService.create_conversation(conversation_data, db_session)

# Get user's conversations
conversations = ConversationService.get_conversations_by_user(user_id, db_session)
```

#### Message Operations
```python
from backend.src.services.message_service import MessageService

# Create a message
message = MessageService.create_message(message_data, db_session)

# Get conversation messages
messages = MessageService.get_messages_by_conversation(conversation_id, db_session)
```

## Testing
Run the unit tests to verify the database persistence functionality:
```bash
cd backend
pytest tests/unit/models/
pytest tests/unit/services/
```

Run integration tests:
```bash
pytest tests/integration/test_db_persistence.py
```

## Migration Management
- Create new migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`
- Check migration status: `alembic current`
- Rollback migration: `alembic downgrade -1`

## User Isolation
All operations enforce user isolation by validating that the user_id matches the entity's owner. This ensures that users can only access their own data.