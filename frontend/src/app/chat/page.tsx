// Chat page component using OpenAI ChatKit UI
'use client';

import React from 'react';
import { ChatProvider } from '../../providers/ChatProvider';
import { AuthWrapper } from '../../components/auth/AuthWrapper';
import { ChatInterface } from '../../components/chat/ChatInterface';

const ChatPage: React.FC = () => {
  return (
    <AuthWrapper>
      <ChatProvider>
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="mb-6 text-center">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Todo Assistant</h1>
            <p className="text-gray-600">
              Manage your tasks using natural language. Just type what you want to do!
            </p>
          </div>
          <div className="h-[600px]">
            <ChatInterface />
          </div>
          <div className="mt-4 text-sm text-gray-500 text-center">
            <p>Examples: "Add a task to buy groceries", "Show me my tasks", "Complete task 1"</p>
          </div>
        </div>
      </ChatProvider>
    </AuthWrapper>
  );
};

export default ChatPage;