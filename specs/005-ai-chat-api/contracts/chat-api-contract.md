# API Contract: AI Agent & Stateless Chat API for Todo Management

## Overview
This document defines the contract for the stateless chat API that enables natural language interaction with todo management tools. The API integrates with OpenAI Agents SDK to process user requests and invoke appropriate MCP tools.

## Endpoint: Chat API

### POST /api/{user_id}/chat
Process natural language requests and return AI agent responses with tool call information.

**Path Parameter**:
```json
{
  "user_id": {
    "type": "string",
    "required": true,
    "description": "The ID of the user making the request, from JWT token"
  }
}
```

**Headers**:
```json
{
  "Authorization": {
    "type": "string",
    "required": true,
    "description": "Bearer token with valid JWT from Better Auth"
  },
  "Content-Type": {
    "type": "string",
    "required": true,
    "description": "application/json"
  }
}
```

**Request Body**:
```json
{
  "message": {
    "type": "string",
    "required": true,
    "description": "Natural language message from the user (max 10000 characters)"
  },
  "conversation_id": {
    "type": "integer",
    "required": false,
    "description": "ID of existing conversation to continue, if omitted starts new conversation"
  }
}
```

**Success Response** (200 OK):
```json
{
  "success": {
    "type": "boolean",
    "description": "Always true for successful requests"
  },
  "response": {
    "type": "string",
    "description": "AI agent's natural language response to the user"
  },
  "tool_calls": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "name": {"type": "string", "description": "Name of the MCP tool called"},
        "arguments": {"type": "object", "description": "Arguments passed to the tool"},
        "result": {"type": "object", "description": "Result from the tool execution"}
      }
    },
    "description": "Array of MCP tools called during processing and their results"
  },
  "conversation_id": {
    "type": "integer",
    "description": "ID of the conversation, new if not provided in request"
  },
  "message_id": {
    "type": "integer",
    "description": "ID of the message created in the conversation"
  }
}
```

**Error Response** (400, 401, 403, 500):
```json
{
  "success": {
    "type": "boolean",
    "description": "Always false for error responses"
  },
  "error": {
    "type": "string",
    "description": "Type of error (e.g., 'validation_error', 'auth_error', 'tool_error', 'internal_error')"
  },
  "message": {
    "type": "string",
    "description": "Human-readable error message"
  }
}
```

### Common Error Cases:
- **400 Bad Request**: Invalid request body or parameters
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: JWT token valid but user doesn't have access to the specified user_id
- **500 Internal Server Error**: Unexpected server error during processing

## Data Models

### Conversation Object
```json
{
  "id": {"type": "integer"},
  "user_id": {"type": "string"},
  "started_at": {"type": "string", "format": "datetime"},
  "updated_at": {"type": "string", "format": "datetime"},
  "status": {"type": "string", "enum": ["active", "closed", "archived"]}
}
```

### Message Object
```json
{
  "id": {"type": "integer"},
  "conversation_id": {"type": "integer"},
  "role": {"type": "string", "enum": ["user", "assistant", "system"]},
  "content": {"type": "string"},
  "timestamp": {"type": "string", "format": "datetime"},
  "tool_calls": {"type": "object"},
  "tool_results": {"type": "object"}
}
```

## Security Requirements
1. All requests must include a valid JWT token in the Authorization header
2. The user_id in the path must match the user_id in the JWT token
3. Users can only access their own conversations
4. All inputs must be sanitized to prevent injection attacks
5. Rate limiting should be applied to prevent abuse of the AI agent

## Performance Requirements
1. API responses should be returned within 10 seconds for typical requests
2. The system should handle concurrent requests from multiple users
3. Large message content should be processed efficiently
4. Conversation history should be managed to prevent performance degradation

## Integration Requirements
1. The AI agent must be able to invoke existing MCP tools for todo operations
2. Conversation state must be persisted in the database between requests
3. Tool call results must be returned to the user in the response
4. The system must maintain user isolation across all operations