// End-to-end tests for chat flow functionality
import { test, expect, describe } from '@jest/globals';
import { ChatService } from '../../../src/services/chatService';

// Mock the fetch API for testing
global.fetch = jest.fn();

describe('Chat Flow Integration Tests', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  test('should maintain conversation across page refreshes', async () => {
    // Mock successful API responses
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        success: true,
        response: 'Task added successfully',
        conversation_id: 'test-conversation-id',
        message_id: 'test-message-id'
      })
    });

    // Test conversation persistence
    const mockMessage = 'Add a new task';
    const mockUserId = 'user123';

    const result = await ChatService.sendMessage(mockMessage, mockUserId);

    expect(result.success).toBe(true);
    expect(result.conversation_id).toBe('test-conversation-id');

    // Verify that conversation ID was persisted
    expect(localStorage.getItem('currentConversationId')).toBe('test-conversation-id');
  });

  test('should handle multi-turn conversation correctly', async () => {
    // Mock successful API responses for multiple requests
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          success: true,
          response: 'Task added successfully',
          conversation_id: 'test-conversation-id',
          message_id: 'msg1'
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          success: true,
          response: 'Here are your tasks',
          conversation_id: 'test-conversation-id', // Same conversation ID
          message_id: 'msg2'
        })
      });

    // First message
    const result1 = await ChatService.sendMessage('Add task', 'user123');
    expect(result1.conversation_id).toBe('test-conversation-id');

    // Second message in same conversation
    const result2 = await ChatService.sendMessage('List tasks', 'user123');
    expect(result2.conversation_id).toBe('test-conversation-id');
  });
});