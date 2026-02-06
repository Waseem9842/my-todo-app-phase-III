# Quickstart Guide: MCP Server for Todo Task Operations

## Overview
This guide explains how to set up and run the MCP server for todo task operations.

## Prerequisites
- Python 3.13+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- Better Auth for user authentication

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install python-mcp-sdk  # Official MCP SDK
# Other dependencies should already be in requirements.txt
```

### 2. Configure Environment
Ensure the following environment variables are set:
```bash
DATABASE_URL="postgresql://..."  # Neon PostgreSQL connection string
```

### 3. Database Setup
The system will use the existing database configuration from the backend.

## Running the MCP Server

### 1. Start the Server
The MCP server will run as part of the existing backend application.

### 2. Available Tools
Once running, the following tools will be available:

#### add_task
```json
{
  "title": "String (required)",
  "description": "String (optional)",
  "user_id": "String (required)"
}
```

#### list_tasks
```json
{
  "user_id": "String (required)"
}
```

#### update_task
```json
{
  "task_id": "Integer (required)",
  "title": "String (optional)",
  "description": "String (optional)",
  "user_id": "String (required)"
}
```

#### complete_task
```json
{
  "task_id": "Integer (required)",
  "user_id": "String (required)"
}
```

#### delete_task
```json
{
  "task_id": "Integer (required)",
  "user_id": "String (required)"
}
```

## Testing
Run the integration tests to verify all MCP tools are working correctly:
```bash
cd backend
pytest tests/integration/test_mcp_tools.py
```

## Integration with AI Agents
The tools are designed to be compatible with OpenAI Agents SDK as specified in the requirements.