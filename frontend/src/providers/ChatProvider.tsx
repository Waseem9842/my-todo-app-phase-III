// Context provider for chat state management
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ChatMessage, Conversation } from '../types/chat';
import { ChatService } from '../services/chatService';
import { AuthService } from '../services/authService';

interface ChatContextType {
  conversationId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  setConversationId: (id: string | null) => void;
  sendMessage: (content: string) => Promise<void>;
  clearConversation: () => void;
  initializeConversation: (conversationId?: string) => Promise<void>;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize conversation from localStorage or start new one
  useEffect(() => {
    // Check if we're in the browser before accessing localStorage
    if (typeof window !== 'undefined') {
      const savedConversationId = localStorage.getItem('currentConversationId');
      if (savedConversationId) {
        initializeConversation(savedConversationId);
      } else {
        initializeConversation();
      }
    }
  }, []);

  const initializeConversation = async (id?: string) => {
    setIsLoading(true);
    setError(null);

    try {
      if (id) {
        // Load existing conversation
        const token = AuthService.getToken();
        if (token) {
          // Extract user ID from JWT token
          const payload = parseJwtPayload(token);
          const userId = payload.sub || payload.user_id || payload.id;

          if (userId) {
            const conv = await ChatService.getConversation(id, userId);
            if (conv) {
              setConversationId(conv.id);
              setMessages(conv.messages);
              localStorage.setItem('currentConversationId', conv.id);
            } else {
              // Conversation doesn't exist, start new one
              await startNewConversation();
            }
          } else {
            await startNewConversation();
          }
        } else {
          await startNewConversation();
        }
      } else {
        // Start new conversation
        await startNewConversation();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize conversation');
      console.error('Error initializing conversation:', err);
    } finally {
      setIsLoading(false);
    }
  };

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

  const startNewConversation = async () => {
    // Just set up a new conversation ID and empty message list
    const newId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setConversationId(newId);
    setMessages([]);
    
    // Only set localStorage in browser environment
    if (typeof window !== 'undefined') {
      localStorage.setItem('currentConversationId', newId);
    }
  };

  const sendMessage = async (content: string) => {
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
      const response = await ChatService.sendMessage(content, userId, conversationId || undefined);

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
        if (response.conversation_id && !conversationId) {
          setConversationId(response.conversation_id);
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
  };

  const clearConversation = () => {
    const newId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setConversationId(newId);
    setMessages([]);
    
    // Only set localStorage in browser environment
    if (typeof window !== 'undefined') {
      localStorage.setItem('currentConversationId', newId);
    }
  };

  const value = {
    conversationId,
    messages,
    isLoading,
    error,
    setConversationId,
    sendMessage,
    clearConversation,
    initializeConversation
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};