# Data Model: MCP Server for Todo Task Operations

## Entities

### Todo Task
Represents a user's task with properties like title, description, completion status, and timestamps.

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

### User
Represents the owner of tasks with user_id as the primary identifier for access control.

**Fields**:
- `user_id`: String (Primary Key, Required)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated)

**Validation Rules**:
- user_id must be unique
- user_id cannot be empty

**Relationships**:
- Has many Todo Tasks (one-to-many)

## State Transitions

### Task Completion
- Initial state: `completed = False`
- Transition trigger: `complete_task` MCP tool
- Final state: `completed = True`

### Task Update
- Can update: title, description
- Cannot update: user_id, id
- Updated_at timestamp automatically updated

## Access Control Rules

### User Isolation
- Each tool must validate that the requesting user_id matches the task's user_id
- Users can only access their own tasks
- Cross-user access attempts result in authorization errors