// Service for handling chat API integration with the backend
import {
  ChatResponse,
  ChatMessage,
  Conversation,
  AddTaskRequest,
  ListTasksRequest,
  UpdateTaskRequest,
  CompleteTaskRequest,
  DeleteTaskRequest
} from '../types/chat';

// Base API URL from environment - should be set in .env.local
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Service class for handling communication with the backend chat API
 */
export class ChatService {
  /**
   * Sends a message to the backend chat API
   * @param message The natural language message from the user
   * @param userId The ID of the user sending the message
   * @param conversationId Optional ID of existing conversation to continue
   * @returns Promise resolving to the API response
   */
  static async sendMessage(
    message: string,
    userId: string,
    conversationId?: string
  ): Promise<ChatResponse> {
    try {
      // Convert conversationId to number if it exists, otherwise send undefined
      let numericConversationId: number | undefined;
      if (conversationId) {
        const parsedId = parseInt(conversationId, 10);
        numericConversationId = isNaN(parsedId) ? undefined : parsedId;
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`, // Attach JWT token
        },
        body: JSON.stringify({
          message,
          conversation_id: numericConversationId
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      return {
        success: false,
        response: 'Sorry, I encountered an error processing your request.',
        conversation_id: conversationId || '',
        message_id: '',
        error: {
          type: 'network_error',
          message: error instanceof Error ? error.message : 'Unknown error occurred'
        }
      };
    }
  }

  /**
   * Enhances error handling and status updates for tool actions
   * @param response The API response to validate
   * @param expectedActions Expected actions that should be confirmed
   * @returns Processed response with proper status indicators
   */
  static processApiResponse(response: ChatResponse, expectedActions?: string[]): ChatResponse {
    // Add any additional processing for the response
    if (response.success && response.tool_calls && response.tool_calls.length > 0) {
      // Process tool call results and add any additional status information
      console.log(`Tool calls executed: ${response.tool_calls.map(tc => tc.name).join(', ')}`);
    }

    return response;
  }

  /**
   * Gets the authentication token from localStorage or sessionStorage
   * @returns The JWT token string or null if not found
   */
  private static getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      // Get token from our custom JWT storage (matches AuthProvider and AuthService)
      return localStorage.getItem('jwt_token') ||
             sessionStorage.getItem('jwt_token') ||
             null;
    }
    return null;
  }

  /**
   * Adds a new task via natural language command
   * @param request The request containing the natural language command
   * @returns Promise resolving to the API response
   */
  static async addTask(request: AddTaskRequest): Promise<ChatResponse> {
    return this.sendMessage(request.message, request.user_id, request.conversation_id);
  }

  /**
   * Lists user's tasks via natural language command
   * @param request The request containing user ID and optional conversation ID
   * @returns Promise resolving to the API response
   */
  static async listTasks(request: ListTasksRequest): Promise<ChatResponse> {
    const message = "List my tasks"; // Natural language command to list tasks
    return this.sendMessage(message, request.user_id, request.conversation_id);
  }

  /**
   * Updates an existing task via natural language command
   * @param request The request containing task update details
   * @returns Promise resolving to the API response
   */
  static async updateTask(request: UpdateTaskRequest): Promise<ChatResponse> {
    // Construct a natural language command based on the update request
    let message = `Update task ${request.task_id}`;
    if (request.title) {
      message += ` with title "${request.title}"`;
    }
    if (request.description) {
      message += ` and description "${request.description}"`;
    }

    return this.sendMessage(message, request.user_id, request.conversation_id);
  }

  /**
   * Marks a task as completed via natural language command
   * @param request The request containing task ID and user ID
   * @returns Promise resolving to the API response
   */
  static async completeTask(request: CompleteTaskRequest): Promise<ChatResponse> {
    const message = `Complete task ${request.task_id}`;
    return this.sendMessage(message, request.user_id, request.conversation_id);
  }

  /**
   * Deletes a task via natural language command
   * @param request The request containing task ID and user ID
   * @returns Promise resolving to the API response
   */
  static async deleteTask(request: DeleteTaskRequest): Promise<ChatResponse> {
    const message = `Delete task ${request.task_id}`;
    return this.sendMessage(message, request.user_id, request.conversation_id);
  }

  /**
   * Gets a specific conversation by ID
   * @param conversationId The ID of the conversation to retrieve
   * @param userId The ID of the user requesting the conversation
   * @returns Promise resolving to the conversation data
   */
  static async getConversation(conversationId: string, userId: string): Promise<Conversation | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations/${conversationId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`,
        },
      });

      // Handle 404 and 422 as "not found" cases
      if (response.status === 404 || response.status === 422) {
        return null; // Conversation doesn't exist
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success && data.conversation) {
        // Transform the API response to match our Conversation interface
        return {
          id: data.conversation.id,
          user_id: userId,
          messages: data.conversation.messages.map((msg: any) => ({
            id: msg.id.toString(),
            content: msg.content,
            sender: msg.role === 'assistant' ? 'assistant' : 'user',
            timestamp: new Date(msg.timestamp),
            status: 'received'
          })),
          created_at: new Date(data.conversation.created_at),
          updated_at: new Date(data.conversation.updated_at),
          status: data.conversation.status || 'active'
        };
      }
      return null;
    } catch (error) {
      console.error('Error fetching conversation:', error);
      return null;
    }
  }

  /**
   * Persists conversation ID in local storage for continuity across page refreshes
   * @param conversationId The ID of the conversation to persist
   */
  static persistConversationId(conversationId: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('currentConversationId', conversationId);
    }
  }

  /**
   * Gets the persisted conversation ID from local storage
   * @returns The conversation ID if found, null otherwise
   */
  static getPersistedConversationId(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('currentConversationId');
    }
    return null;
  }
}