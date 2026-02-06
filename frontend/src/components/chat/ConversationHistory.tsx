// Component for displaying conversation history
import React from 'react';
import { ChatMessage } from '../../types/chat';
import { MessageBubble } from './MessageBubble';

interface ConversationHistoryProps {
  messages: ChatMessage[];
  className?: string;
}

export const ConversationHistory: React.FC<ConversationHistoryProps> = ({
  messages,
  className = ''
}) => {
  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <p>No messages yet. Start a conversation by typing a message.</p>
      </div>
    );
  }

  return (
    <div className={`overflow-y-auto flex-1 space-y-4 ${className}`}>
      {messages.map((message) => (
        <div key={message.id} className="flex justify-start">
          <MessageBubble message={message} />
        </div>
      ))}
    </div>
  );
};