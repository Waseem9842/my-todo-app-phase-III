# Quickstart Guide: Chat UI for AI-Powered Todo Chatbot

## Overview
This guide explains how to set up and use the Chat UI for AI-Powered Todo Chatbot using OpenAI ChatKit that allows users to manage todos via natural language.

## Prerequisites
- Node.js 18+ with npm or yarn
- Better Auth account and configuration
- Access to the backend chat API endpoint
- OpenAI ChatKit installed as a dependency

## Setup

### 1. Install Dependencies
```bash
cd frontend
npm install openai-chatkit better-auth react-query
# Other dependencies should already be in package.json
```

### 2. Configure Environment
Ensure the following environment variables are set in your `.env.local`:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"  # Better Auth backend URL
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"   # Backend API URL
NEXT_PUBLIC_JWT_SECRET="your-jwt-secret"           # JWT verification secret
```

### 3. Authentication Setup
Configure Better Auth in your frontend app to handle user authentication and JWT token management.

## Using the Chat UI

### 1. Navigate to the Chat Page
Visit the chat page at `/chat` where the OpenAI ChatKit interface is implemented.

### 2. Authenticate User
The user must be authenticated via Better Auth to access the chat functionality. The JWT token will be automatically attached to API requests.

### 3. Send a Message
Type a natural language message in the chat input like "Add a new task to buy groceries" and press Enter.

### 4. Expected Response
The UI will display the AI assistant's response with appropriate feedback about the task operation performed.

## API Integration
- **Endpoint**: `POST /api/{user_id}/chat`
- **Authentication**: JWT token automatically attached in Authorization header
- **Request Body**:
  ```json
  {
    "message": "string (required)",
    "conversation_id": "integer (optional, for continuing existing conversation)"
  }
  ```
- **Response**: JSON with AI response, tool calls, and conversation ID

## Component Structure
- `components/ChatInterface.tsx`: Main chat UI component using OpenAI ChatKit
- `services/chatService.ts`: API integration for chat endpoint
- `hooks/useChat.ts`: Custom hook for chat state management
- `types/chat.ts`: TypeScript types for chat messages and conversations

## Testing
Run the frontend tests to verify the chat UI functionality:
```bash
cd frontend
npm test
```

## Troubleshooting
- If JWT tokens expire during a conversation, the user will need to re-authenticate
- Network connectivity issues will show appropriate error messages in the chat interface
- Invalid requests will return error responses that are displayed in the UI