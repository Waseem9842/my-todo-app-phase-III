// Component for displaying conversation history with improved layout
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
      <div className="flex flex-col items-center justify-center h-full text-gray-500 p-8">
        <div className="bg-indigo-100 p-4 rounded-full mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </div>
        <p className="text-lg font-medium text-gray-700">No messages yet</p>
        <p className="text-gray-500 mt-1">Start a conversation by typing a message below</p>
      </div>
    );
  }

  return (
    <div className={`overflow-y-auto flex-1 space-y-4 ${className}`}>
      {messages.map((message) => (
        <div 
          key={message.id} 
          className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <MessageBubble message={message} />
        </div>
      ))}
    </div>
  );
};