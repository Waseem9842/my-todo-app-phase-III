// Main chat interface component with modern UI design
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
    <div className={`flex flex-col h-full bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl shadow-xl border border-gray-200 overflow-hidden ${className}`}>
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 px-6 py-4 border-b border-indigo-500">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="bg-white/20 p-2 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-white">AI Todo Assistant</h2>
          </div>
          <button
            onClick={clearConversation}
            className="px-4 py-2 text-sm bg-white/20 text-white rounded-lg hover:bg-white/30 transition-all duration-200 backdrop-blur-sm border border-white/30"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-gray-100">
        {error && <ErrorDisplay message={error} />}

        <ConversationHistory messages={messages} className="" />

        {isLoading && (
          <div className="flex justify-start animate-fade-in">
            <div className="bg-indigo-50 rounded-2xl p-4 max-w-xs border border-indigo-100 shadow-sm">
              <div className="flex items-center space-x-2">
                <LoadingSpinner />
                <span className="text-sm text-indigo-600 font-medium">Thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white/80 backdrop-blur-sm">
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