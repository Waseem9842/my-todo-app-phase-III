# MCP Tools Contract: Todo Task Operations

## Overview
This document defines the contract for MCP (Model Context Protocol) tools that provide todo task operations. These tools are designed to be consumed by AI agents through the Official MCP SDK.

## Tool Definitions

### 1. add_task
**Purpose**: Create a new todo task for a specific user.

**Input Parameters**:
```json
{
  "title": {
    "type": "string",
    "required": true,
    "description": "The title of the task (1-255 characters)"
  },
  "description": {
    "type": "string",
    "required": false,
    "description": "Optional description of the task (max 1000 characters)"
  },
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user creating the task"
  }
}
```

**Output**:
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the operation was successful"
  },
  "task_id": {
    "type": "integer",
    "description": "The ID of the newly created task"
  },
  "message": {
    "type": "string",
    "description": "Human-readable message about the operation"
  }
}
```

**Error Cases**:
- Invalid user_id: Returns error with message
- Invalid title: Returns error with message
- Database error: Returns error with message

### 2. list_tasks
**Purpose**: Retrieve all tasks for a specific user.

**Input Parameters**:
```json
{
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user whose tasks to retrieve"
  }
}
```

**Output**:
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the operation was successful"
  },
  "tasks": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "completed": {"type": "boolean"},
        "created_at": {"type": "string", "format": "datetime"},
        "updated_at": {"type": "string", "format": "datetime"}
      }
    },
    "description": "Array of tasks belonging to the user"
  },
  "message": {
    "type": "string",
    "description": "Human-readable message about the operation"
  }
}
```

**Error Cases**:
- Invalid user_id: Returns error with message
- Database error: Returns error with message

### 3. update_task
**Purpose**: Update an existing task for a specific user.

**Input Parameters**:
```json
{
  "task_id": {
    "type": "integer",
    "required": true,
    "description": "The ID of the task to update"
  },
  "title": {
    "type": "string",
    "required": false,
    "description": "New title for the task (1-255 characters)"
  },
  "description": {
    "type": "string",
    "required": false,
    "description": "New description for the task (max 1000 characters)"
  },
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user who owns the task"
  }
}
```

**Output**:
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the operation was successful"
  },
  "task": {
    "type": "object",
    "properties": {
      "id": {"type": "integer"},
      "title": {"type": "string"},
      "description": {"type": "string"},
      "completed": {"type": "boolean"},
      "created_at": {"type": "string", "format": "datetime"},
      "updated_at": {"type": "string", "format": "datetime"}
    },
    "description": "Updated task object"
  },
  "message": {
    "type": "string",
    "description": "Human-readable message about the operation"
  }
}
```

**Error Cases**:
- Invalid user_id: Returns error with message
- Invalid task_id: Returns error with message
- Task doesn't belong to user: Returns error with message
- Invalid parameters: Returns error with message

### 4. complete_task
**Purpose**: Mark a task as completed for a specific user.

**Input Parameters**:
```json
{
  "task_id": {
    "type": "integer",
    "required": true,
    "description": "The ID of the task to mark as completed"
  },
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user who owns the task"
  }
}
```

**Output**:
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the operation was successful"
  },
  "task": {
    "type": "object",
    "properties": {
      "id": {"type": "integer"},
      "title": {"type": "string"},
      "description": {"type": "string"},
      "completed": {"type": "boolean"},
      "created_at": {"type": "string", "format": "datetime"},
      "updated_at": {"type": "string", "format": "datetime"}
    },
    "description": "Updated task object with completed status"
  },
  "message": {
    "type": "string",
    "description": "Human-readable message about the operation"
  }
}
```

**Error Cases**:
- Invalid user_id: Returns error with message
- Invalid task_id: Returns error with message
- Task doesn't belong to user: Returns error with message

### 5. delete_task
**Purpose**: Delete a task for a specific user.

**Input Parameters**:
```json
{
  "task_id": {
    "type": "integer",
    "required": true,
    "description": "The ID of the task to delete"
  },
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user who owns the task"
  }
}
```

**Output**:
```json
{
  "success": {
    "type": "boolean",
    "description": "Indicates if the operation was successful"
  },
  "message": {
    "type": "string",
    "description": "Human-readable message about the operation"
  }
}
```

**Error Cases**:
- Invalid user_id: Returns error with message
- Invalid task_id: Returns error with message
- Task doesn't belong to user: Returns error with message
- Database error: Returns error with message

## Common Error Responses
All tools follow the same error response pattern:
```json
{
  "success": false,
  "error": {
    "type": "string",
    "description": "Type of error (e.g., 'validation_error', 'authorization_error', 'database_error')"
  },
  "message": {
    "type": "string",
    "description": "Detailed error message for debugging"
  }
}
```

## Security Requirements
1. All operations must validate that user_id matches the task owner
2. No cross-user access is allowed
3. All inputs must be validated before processing
4. Error messages should not reveal sensitive information