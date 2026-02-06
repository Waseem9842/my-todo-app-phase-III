# Data Model: AI Agent & Stateless Chat API for Todo Management

## Entities

### Conversation
Represents a user's chat session with metadata like start time, status, and user_id.

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Required, references User)
- `started_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, updates on modification)
- `status`: String (Active, Closed, Archived - Default: Active)

**Validation Rules**:
- user_id must exist in the system
- status must be one of the predefined values

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many)

### Message
Represents an individual message in a conversation with content, sender, timestamp, and role (user/assistant).

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `conversation_id`: Integer (Required, references Conversation)
- `role`: String (Required, values: "user", "assistant", "system")
- `content`: String (Required, max length 10000)
- `timestamp`: DateTime (Auto-generated)
- `tool_calls`: JSON (Optional, stores MCP tool calls made during this interaction)
- `tool_results`: JSON (Optional, stores results from MCP tool calls)

**Validation Rules**:
- conversation_id must exist
- role must be one of "user", "assistant", or "system"
- content must not be empty

**Relationships**:
- Belongs to one Conversation (many-to-one)

### User
Represents the authenticated user with user_id from JWT token for access control.
*(Reusing existing User model from the system)*

**Fields**:
- `user_id`: String (Primary Key, Required)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated)

**Validation Rules**:
- user_id must be unique
- user_id cannot be empty

**Relationships**:
- Has many Conversations (one-to-many)

### Task
Represents a user's task with properties like title, description, completion status, and timestamps.
*(Reusing existing Task model from the system)*

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `title`: String (Required, max length 255)
- `description`: String (Optional, max length 1000)
- `completed`: Boolean (Default: False)
- `user_id`: String (Required, references User)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, updates on modification)

**Validation Rules**:
- Title must be between 1-255 characters
- User_id must exist in the system
- Completed status can only be True/False

**Relationships**:
- Belongs to one User (many-to-one)

## State Transitions

### Conversation Status
- Initial state: `status = "active"`
- Transition trigger: Conversation completion or timeout
- Final state: `status = "closed"`

### Task Completion
- Initial state: `completed = False`
- Transition trigger: `complete_task` MCP tool
- Final state: `completed = True`

## Access Control Rules

### User Isolation
- Each conversation must be associated with the authenticated user_id
- Users can only access their own conversations and messages
- Cross-user access attempts result in authorization errors

### Message Access
- Only messages from conversations owned by the user can be accessed
- AI agent responses are tied to specific conversations