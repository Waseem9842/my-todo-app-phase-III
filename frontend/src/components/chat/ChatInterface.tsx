// Main chat interface component using OpenAI ChatKit patterns
'use client';

import React, { useState } from 'react';
import { useChat } from '../../providers/ChatProvider';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { ConversationHistory } from './ConversationHistory';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { ErrorDisplay } from '../ui/ErrorDisplay';

interface ChatInterfaceProps {
  className?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  className = ''
}) => {
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    clearConversation
  } = useChat();
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      await sendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className={`flex flex-col h-full bg-white rounded-lg shadow-md ${className}`}>
      {/* Chat Header */}
      <div className="bg-gray-100 px-4 py-3 border-b border-gray-200 rounded-t-lg">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-800">AI Todo Assistant</h2>
          <button
            onClick={clearConversation}
            className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {error && <ErrorDisplay message={error} />}

        <ConversationHistory messages={messages} className="" />

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-lg p-3 max-w-xs">
              <LoadingSpinner />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <InputArea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onSubmit={handleSubmit}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};