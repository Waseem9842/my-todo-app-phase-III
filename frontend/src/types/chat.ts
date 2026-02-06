// Types for chat entities in the AI-powered todo chatbot

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant'; // Determines if message is from user or AI assistant
  timestamp: Date;
  status?: 'sent' | 'received' | 'error'; // For UI feedback on message status
  tool_calls?: any[]; // Stores any tool calls made as part of this message
  tool_results?: any[]; // Stores results from tool calls
}

export interface Conversation {
  id: string; // Unique identifier for the conversation
  user_id: string; // ID of the user who owns this conversation
  messages: ChatMessage[]; // Array of messages in chronological order
  created_at: Date; // When the conversation was started
  updated_at: Date; // When the last message was added
  status: 'active' | 'closed' | 'archived'; // Current status of the conversation
}

export interface User {
  user_id: string; // Primary identifier from JWT token
  name?: string; // Optional display name
  jwt_token?: string; // Current JWT token for API requests
}

// Request types for API communication
export interface AddTaskRequest {
  message: string; // Natural language command to add a task
  user_id: string; // ID of the user making the request
  conversation_id?: string; // Optional ID of existing conversation to continue
}

export interface ListTasksRequest {
  user_id: string; // ID of the user whose tasks to retrieve
  conversation_id?: string; // Optional ID of existing conversation to continue
}

export interface UpdateTaskRequest {
  task_id: number; // ID of the task to update
  user_id: string; // ID of the user making the request
  title?: string; // New title for the task (optional)
  description?: string; // New description for the task (optional)
  conversation_id?: string; // Optional ID of existing conversation to continue
}

export interface CompleteTaskRequest {
  task_id: number; // ID of the task to mark as completed
  user_id: string; // ID of the user making the request
  conversation_id?: string; // Optional ID of existing conversation to continue
}

export interface DeleteTaskRequest {
  task_id: number; // ID of the task to delete
  user_id: string; // ID of the user making the request
  conversation_id?: string; // Optional ID of existing conversation to continue
}

// Response types from API
export interface ChatResponse {
  success: boolean;
  response: string; // AI agent's response to the user's request
  tool_calls?: Array<{
    name: string;
    arguments: Record<string, any>;
    result: any;
  }>; // Tool calls made during processing and their results
  conversation_id: string; // ID of the conversation (new if not provided in request)
  message_id: string; // ID of the message created in the conversation
  error?: {
    type: string;
    message: string;
  }; // Error details if success is false
}