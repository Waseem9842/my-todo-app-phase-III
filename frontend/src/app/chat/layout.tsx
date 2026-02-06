// Layout for the chat page
import React from 'react';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Todo Assistant | Chat',
  description: 'Manage your todos using natural language with our AI assistant'
};

interface ChatLayoutProps {
  children: React.ReactNode;
}

const ChatLayout: React.FC<ChatLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
};

export default ChatLayout;