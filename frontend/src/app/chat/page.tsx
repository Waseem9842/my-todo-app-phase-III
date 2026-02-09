// Chat page component using OpenAI ChatKit UI
'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import { AuthWrapper } from '../../components/auth/AuthWrapper';

// Dynamically import the chat component to avoid SSR issues
const DynamicChatInterface = dynamic(() => import('../../components/chat/DynamicChatComponent'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
    </div>
  ),
});

const ChatPage: React.FC = () => {
  return (
    <AuthWrapper>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Todo Assistant</h1>
          <p className="text-gray-600">
            Manage your tasks using natural language. Just type what you want to do!
          </p>
        </div>
        <div className="h-[600px]">
          <DynamicChatInterface />
        </div>
        <div className="mt-4 text-sm text-gray-500 text-center">
          <p>Examples: "Add a task to buy groceries", "Show me my tasks", "Complete task 1"</p>
        </div>
      </div>
    </AuthWrapper>
  );
};

export default ChatPage;