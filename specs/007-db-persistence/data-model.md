# Data Model: Database Models, Migrations & Persistence for AI Todo Chatbot

## Entities

### Task
Represents a user's todo item with properties like title, description, completion status, and timestamps.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `title`: String (Required, min 1 char, max 255 chars)
- `description`: String (Optional, max 1000 chars)
- `completed`: Boolean (Default: False)
- `user_id`: String (Required, identifies the user who owns this task)
- `created_at`: DateTime (Auto-generated, when task was created)
- `updated_at`: DateTime (Auto-generated, updates when task is modified)

**Validation Rules**:
- Title must be between 1-255 characters
- User_id must not be empty
- Completed status can only be True/False

**Relationships**:
- Belongs to one User (many-to-one via user_id)

### Conversation
Represents a chat session with metadata like user_id, creation time, status, and relationship to associated messages.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Required, identifies the user who owns this conversation)
- `started_at`: DateTime (Auto-generated, when conversation was initiated)
- `updated_at`: DateTime (Auto-generated, updates when new messages are added)
- `status`: String (Default: "active", values: "active", "closed", "archived")

**Validation Rules**:
- user_id must not be empty
- status must be one of the allowed values

**Relationships**:
- Belongs to one User (many-to-one via user_id)
- Has many Messages (one-to-many)

### Message
Represents an individual message in a conversation with content, sender, timestamp, and optional tool call data.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `conversation_id`: Integer (Required, references the parent conversation)
- `role`: String (Required, values: "user", "assistant", "system")
- `content`: String (Required, max 10000 chars)
- `timestamp`: DateTime (Auto-generated, when message was created)
- `tool_calls`: JSON (Optional, stores MCP tool calls made during this interaction)
- `tool_results`: JSON (Optional, stores results from MCP tool calls)

**Validation Rules**:
- content must not be empty
- role must be one of the allowed values
- conversation_id must reference an existing conversation

**Relationships**:
- Belongs to one Conversation (many-to-one via conversation_id)

### User
Represents the authenticated user identity referenced by user_id in other entities for data isolation.

**Fields**:
- `user_id`: String (Primary Key, Required)
- `name`: String (Optional, user's display name)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, updates on modification)

**Validation Rules**:
- user_id must be unique
- user_id cannot be empty

**Relationships**:
- Has many Tasks (one-to-many)
- Has many Conversations (one-to-many)
- Has many Messages through Conversations (one-to-many-through)

## State Transitions

### Task Completion
- Initial state: `completed = False`
- Transition trigger: complete_task operation
- Final state: `completed = True`

### Conversation Status
- Initial state: `status = "active"`
- Transition triggers:
  - Conversation completion: `status = "closed"`
  - Archiving: `status = "archived"`
- Final states: "closed" or "archived"

## Access Control Rules

### User Isolation
- Each entity (Task, Conversation, Message) must be associated with the authenticated user_id
- Users can only access their own entities
- Cross-user access attempts must be prevented at both service and database levels
- All queries must filter by user_id to ensure proper isolation