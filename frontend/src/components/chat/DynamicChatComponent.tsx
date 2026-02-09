'use client';

import React from 'react';
import { ChatProvider } from '@/providers/ChatProvider';
import { ChatInterface } from '@/components/chat/ChatInterface';

const DynamicChatComponent = () => {
  return (
    <ChatProvider>
      <ChatInterface />
    </ChatProvider>
  );
};

export default DynamicChatComponent;