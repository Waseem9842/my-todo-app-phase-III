// Component for displaying individual chat messages with status indicators
import React from 'react';
import { ChatMessage } from '../../types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  // Determine styling based on message sender and status
  const bubbleStyle = isUser
    ? 'bg-blue-500 text-white ml-auto'  // User messages on the right
    : 'bg-gray-200 text-gray-800 mr-auto'; // Assistant messages on the left

  // Additional styling based on message status
  const statusStyle = message.status === 'error'
    ? 'bg-red-200 text-red-800 border border-red-400'
    : message.status === 'sent'
      ? 'bg-blue-400'  // Different shade for sent messages
      : message.status === 'received'
        ? 'bg-blue-600'  // Different shade for received messages
        : '';

  // Format timestamp for display
  const formattedTime = message.timestamp.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`max-w-[80%] rounded-lg p-3 ${bubbleStyle} ${statusStyle}`}>
      <div className="whitespace-pre-wrap break-words">
        {message.content}
      </div>
      <div className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'} text-right`}>
        {formattedTime}
        {message.status && (
          <span className="ml-1">
            {message.status === 'sent' ? '✓' :
             message.status === 'received' ? '✓✓' :
             message.status === 'error' ? '⚠️' : ''}
          </span>
        )}
      </div>

      {/* Display tool calls if present */}
      {message.tool_calls && message.tool_calls.length > 0 && (
        <div className="mt-2 pt-2 border-t border-gray-300 text-xs">
          <div className="font-medium text-gray-600">Tools used:</div>
          {message.tool_calls.map((call: any, index: number) => (
            <div key={index} className="mt-1 bg-gray-100 p-2 rounded">
              <div className="font-mono">{call.name}({JSON.stringify(call.arguments)})</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};