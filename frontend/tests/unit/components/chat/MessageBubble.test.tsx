// Unit tests for MessageBubble component
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MessageBubble } from '../../../../src/components/chat/MessageBubble';
import { ChatMessage } from '../../../../src/types/chat';

describe('MessageBubble', () => {
  const mockMessage: ChatMessage = {
    id: '1',
    content: 'Test message',
    sender: 'user',
    timestamp: new Date(),
    status: 'sent'
  };

  it('renders user message correctly', () => {
    render(<MessageBubble message={mockMessage} />);
    expect(screen.getByText('Test message')).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    const assistantMessage: ChatMessage = {
      ...mockMessage,
      sender: 'assistant'
    };
    render(<MessageBubble message={assistantMessage} />);
    expect(screen.getByText('Test message')).toBeInTheDocument();
  });
});