// Component for user message input
import React from 'react';

interface InputAreaProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const InputArea: React.FC<InputAreaProps> = ({
  value,
  onChange,
  onSubmit,
  disabled = false,
  placeholder = 'Type your message here...'
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!disabled && value.trim()) {
      onSubmit(e);
    }
  };

  return (
    <div className="flex gap-2">
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        className="flex-1 border border-gray-300 rounded-lg p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        rows={3}
        onKeyDown={(e) => {
          // Submit on Ctrl+Enter or Cmd+Enter
          if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            handleSubmit(e);
          }
        }}
      />
      <button
        onClick={(e) => handleSubmit(e)}
        disabled={disabled || !value.trim()}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Send
      </button>
    </div>
  );
};