// Component for displaying individual chat messages with modern design
import React from 'react';
import { ChatMessage } from '../../types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  // Determine styling based on message sender and status
  const bubbleStyle = isUser
    ? 'bg-gradient-to-r from-indigo-500 to-indigo-600 text-white ml-auto rounded-br-none'  // User messages on the right
    : 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 mr-auto rounded-bl-none border border-gray-200'; // Assistant messages on the left

  // Additional styling based on message status
  const statusStyle = message.status === 'error'
    ? 'bg-gradient-to-r from-red-100 to-red-200 text-red-800 border border-red-300'
    : message.status === 'sent'
      ? 'from-indigo-400 to-indigo-500'  // Different gradient for sent messages
      : message.status === 'received'
        ? 'from-indigo-600 to-indigo-700'  // Different gradient for received messages
        : '';

  // Format timestamp for display
  const formattedTime = message.timestamp.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`max-w-[85%] rounded-2xl p-4 shadow-sm transition-all duration-200 ease-in-out transform hover:scale-[1.02] ${bubbleStyle} ${statusStyle}`}>
      <div className="whitespace-pre-wrap break-words">
        {message.content}
      </div>
      <div className={`text-xs mt-2 opacity-80 ${isUser ? 'text-indigo-100' : 'text-gray-500'} text-right flex justify-end items-center`}>
        <span>{formattedTime}</span>
        {message.status && (
          <span className="ml-1 inline-flex items-center justify-center">
            {message.status === 'sent' ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : message.status === 'received' ? (
              <div className="flex space-x-0.5">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            ) : message.status === 'error' ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : null}
          </span>
        )}
      </div>

      {/* Display tool calls if present */}
      {message.tool_calls && message.tool_calls.length > 0 && (
        <div className={`mt-3 pt-3 border-t ${isUser ? 'border-indigo-400/30' : 'border-gray-300'} text-xs`}>
          <div className={`font-medium ${isUser ? 'text-indigo-200' : 'text-gray-600'}`}>Tools used:</div>
          {message.tool_calls.map((call: any, index: number) => (
            <div 
              key={index} 
              className={`mt-1 p-2 rounded-lg text-xs font-mono ${
                isUser 
                  ? 'bg-indigo-400/20 text-indigo-100' 
                  : 'bg-gray-300/30 text-gray-700'
              }`}
            >
              <div className="truncate">{call.name}({JSON.stringify(call.arguments)})</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};