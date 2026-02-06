# Data Model: Chat UI for AI-Powered Todo Chatbot

## Entities

### ChatMessage
Represents a message in the conversation with content, sender (user/assistant), timestamp, and status (sent, received, error).

**Fields**:
- `id`: String or Number (Unique identifier for the message)
- `content`: String (Required, the text content of the message)
- `sender`: String (Required, values: "user" or "assistant")
- `timestamp`: Date (Auto-generated, when the message was sent/received)
- `status`: String (Optional, values: "sent", "received", "error" - for UI feedback)
- `tool_calls`: Array (Optional, any tool calls made as part of this message)
- `tool_results`: Array (Optional, results from tool calls)

**Validation Rules**:
- Content must not be empty
- Sender must be either "user" or "assistant"
- Timestamp must be a valid date/time

**Relationships**:
- Belongs to one Conversation (many-to-one)

### Conversation
Represents a chat session with metadata like conversation_id, user_id, and message history.

**Fields**:
- `id`: String or Number (Unique identifier for the conversation)
- `user_id`: String (Required, ID of the user who owns this conversation)
- `messages`: Array (Array of ChatMessage objects)
- `created_at`: Date (Auto-generated, when conversation started)
- `updated_at`: Date (Auto-generated, when last message was added)
- `status`: String (Values: "active", "closed" - Default: "active")

**Validation Rules**:
- user_id must exist and be valid
- messages must be an array of valid ChatMessage objects
- status must be one of the allowed values

**Relationships**:
- Belongs to one User (many-to-one)
- Has many ChatMessages (one-to-many)

### User
Represents the authenticated user with user_id from Better Auth JWT token.

**Fields**:
- `user_id`: String (Primary identifier from JWT token)
- `name`: String (Optional, user's display name)
- `jwt_token`: String (Current JWT token for API requests)

**Validation Rules**:
- user_id must be unique and valid
- jwt_token must be a valid JWT format

**Relationships**:
- Has many Conversations (one-to-many)

## State Transitions

### Message Status
- Initial state: `status = "sent"` (when user sends message)
- Transition trigger: API response received
- Final state: `status = "received"` (for assistant messages) or `status = "error"` (if API call fails)

### Conversation Status
- Initial state: `status = "active"` (when conversation starts)
- Transition trigger: Conversation completion or timeout
- Final state: `status = "closed"` (when conversation ends)

## Access Control Rules

### User Isolation
- Each conversation must be associated with the authenticated user_id
- Users can only access their own conversations and messages
- Cross-user access attempts result in authorization errors