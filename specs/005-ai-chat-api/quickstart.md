# Quickstart Guide: AI Agent & Stateless Chat API for Todo Management

## Overview
This guide explains how to set up and use the stateless chat API powered by OpenAI Agents SDK that uses MCP tools to manage todo tasks via natural language.

## Prerequisites
- Python 3.13+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- Better Auth for user authentication
- OpenAI API key
- MCP server with todo tools running

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install openai
# Other dependencies should already be in requirements.txt
```

### 2. Configure Environment
Ensure the following environment variables are set:
```bash
OPENAI_API_KEY="your-openai-api-key"
DATABASE_URL="postgresql://..."  # Neon PostgreSQL connection string
MCP_SERVER_URL="http://localhost:8000"  # MCP server endpoint
```

### 3. Database Setup
The system will use the existing database configuration from the backend with new conversation and message tables.

## Using the Chat API

### 1. Send a Request
Send a POST request to the chat endpoint with a valid JWT token:

```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {valid_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a new task to buy groceries"
  }'
```

### 2. Expected Response
The API will return a response with the agent's reply and any tool calls made:

```json
{
  "success": true,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "title": "buy groceries",
        "user_id": "{user_id}"
      },
      "result": {
        "success": true,
        "task_id": 123,
        "message": "Task 'buy groceries' created successfully"
      }
    }
  ],
  "conversation_id": 456
}
```

## API Endpoint
- **Endpoint**: `POST /api/{user_id}/chat`
- **Authentication**: JWT token in Authorization header (Bearer scheme)
- **Request Body**:
  ```json
  {
    "message": "string (required)",
    "conversation_id": "integer (optional, for continuing existing conversation)"
  }
  ```
- **Response**: JSON with agent response, tool calls, and conversation ID

## Configuration Options
- `AGENT_TEMPERATURE`: Controls agent creativity (default: 0.7)
- `AGENT_MODEL`: OpenAI model to use (default: gpt-4)
- `MAX_CONVERSATION_HISTORY`: Number of previous messages to include (default: 10)

## Testing
Run the unit and integration tests to verify the chat API functionality:
```bash
cd backend
pytest tests/unit/test_ai_agent_service.py
pytest tests/integration/test_chat_endpoint.py
```

## Integration with Existing MCP Tools
The AI agent is configured to use the existing MCP tools for todo operations:
- `add_task`: Creates new tasks
- `list_tasks`: Retrieves user's tasks
- `update_task`: Modifies existing tasks
- `complete_task`: Marks tasks as completed
- `delete_task`: Removes tasks