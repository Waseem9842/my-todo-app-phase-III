# Quickstart Guide: Final Integration, Security & Readiness for AI Todo Platform

## Overview
This guide explains how to set up and run the complete AI Todo Platform with all integrated components including frontend UI, backend API, MCP server, and database with proper authentication.

## Prerequisites
- Node.js 18+ with npm/yarn
- Python 3.13+ with pip
- PostgreSQL database (Neon Serverless recommended)
- Better Auth account and configuration
- OpenAI API key
- Official MCP SDK

## Environment Setup

### 1. Configure Backend Environment
Create or update `backend/.env`:
```bash
# Database Configuration
DATABASE_URL='postgresql://username:password@host:port/database'

# Authentication Configuration
BETTER_AUTH_SECRET=your-super-secret-key-change-in-production
AUTH_ALGORITHM=HS256
AUTH_AUDIENCE=todo-api
AUTH_ISSUER=better-auth
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=False
LOG_LEVEL=info

# AI/Agent Configuration
OPENAI_API_KEY="your-openai-api-key"
```

### 2. Configure Frontend Environment
Create or update `frontend/.env.local`:
```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# Authentication Configuration
AUTH_SECRET=your-super-secret-key-change-in-production
AUTH_ALGORITHM=HS256
AUTH_AUDIENCE=todo-api
AUTH_ISSUER=better-auth
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Critical**: The AUTH_SECRET and other auth configuration values must be identical between frontend and backend to ensure JWT validation works correctly.

## Installation

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

### 3. Database Setup
```bash
cd backend
alembic upgrade head
```

## Running the Integrated System

### 1. Start Backend Server
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

## Testing the Integration

### 1. Health Checks
Verify all services are running:
- Backend health: `GET http://localhost:8000/health`
- Database connectivity: Check if database queries work
- MCP server status: Verify MCP tools are accessible

### 2. Authentication Flow
1. Visit the frontend application
2. Log in with valid credentials
3. Verify JWT token is properly stored and sent with API requests
4. Check that unauthorized requests are rejected

### 3. End-to-End Flow
1. Log in to the application
2. Navigate to the chat interface
3. Send a natural language command like "Add a task to buy groceries"
4. Verify the AI agent processes the request and creates a task
5. Verify the task appears in the user's task list
6. Test other operations (list, update, complete, delete)

## Monitoring and Logging

### 1. Check Application Logs
- Backend logs: Check console output or configured log files
- Frontend logs: Check browser console
- Database logs: Monitor query performance

### 2. Health Monitoring
Access the health endpoint to check system status:
```bash
curl http://localhost:8000/health
```

### 3. Operation Logging
Monitor operation logs for:
- User authentication events
- Chat interactions and tool calls
- Error occurrences and recovery
- Performance metrics

## Troubleshooting

### Common Issues:
- **JWT Validation Failures**: Verify that AUTH_SECRET is identical in both frontend and backend
- **Database Connectivity**: Check DATABASE_URL configuration and network connectivity
- **MCP Tool Failures**: Verify MCP server is running and tools are properly registered
- **CORS Issues**: Ensure frontend and backend URLs are properly configured in CORS settings

### Debugging Steps:
1. Check environment variables are properly set
2. Verify all services are running
3. Review logs for error messages
4. Test individual components separately before testing integration