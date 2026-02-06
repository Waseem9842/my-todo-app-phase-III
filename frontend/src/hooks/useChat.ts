// Custom hook for chat state management
import { useState, useEffect, useCallback } from 'react';
import { ChatMessage } from '../types/chat';
import { ChatService } from '../services/chatService';
import { AuthService } from '../services/authService';

interface UseChatReturn {
  messages: ChatMessage[];
  sendMessage: (content: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  clearMessages: () => void;
}

export const useChat = (): UseChatReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load initial messages if there's an existing conversation
  useEffect(() => {
    const initializeChat = async () => {
      const savedConversationId = localStorage.getItem('currentConversationId');
      if (savedConversationId) {
        const token = AuthService.getToken();
        if (token) {
          try {
            // Extract user ID from JWT token
            const payload = parseJwtPayload(token);
            const userId = payload.sub || payload.user_id || payload.id;

            if (userId) {
              const conv = await ChatService.getConversation(savedConversationId, userId);
              if (conv) {
                setMessages(conv.messages);
              }
            }
          } catch (err) {
            console.error('Error loading conversation:', err);
          }
        }
      }
    };

    initializeChat();
  }, []);

  // Handle page refresh by restoring conversation from storage
  useEffect(() => {
    const handlePageRefresh = () => {
      const storedConversationId = localStorage.getItem('currentConversationId');
      if (storedConversationId) {
        // Conversation ID is already handled by the first effect
        // This effect can be used for additional refresh handling if needed
      }
    };

    // Check for stored conversation on mount
    handlePageRefresh();
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userId = AuthService.getUserId();
    if (!userId) {
      setError('User not authenticated');
      return;
    }

    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      content,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await ChatService.sendMessage(content, userId);

      if (response.success) {
        // Add assistant response to messages
        const assistantMessage: ChatMessage = {
          id: `msg_${Date.now() + 1}`,
          content: response.response,
          sender: 'assistant',
          timestamp: new Date(),
          status: 'received',
          tool_calls: response.tool_calls
        };

        setMessages(prev => [...prev, assistantMessage]);

        // Update conversation ID if it was returned (for new conversations)
        if (response.conversation_id) {
          localStorage.setItem('currentConversationId', response.conversation_id);
        }
      } else {
        // Show error as a message from assistant
        const errorMessage: ChatMessage = {
          id: `msg_${Date.now() + 1}`,
          content: response.error?.message || 'Sorry, I encountered an error processing your request.',
          sender: 'assistant',
          timestamp: new Date(),
          status: 'error'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      console.error('Error sending message:', err);

      // Show error as a message from assistant
      const errorMessage: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        content: 'Sorry, I encountered an error processing your request.',
        sender: 'assistant',
        timestamp: new Date(),
        status: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    localStorage.removeItem('currentConversationId');

    // Start a new conversation
    const newId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('currentConversationId', newId);
  }, []);

  // Helper function to parse JWT payload
  const parseJwtPayload = (token: string): { [key: string]: any } => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  };

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    clearMessages
  };
};