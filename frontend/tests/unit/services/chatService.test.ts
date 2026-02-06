// Unit tests for ChatService
import { ChatService } from '../../../src/services/chatService';
import { ChatMessage } from '../../../src/types/chat';

describe('ChatService', () => {
  // Mock the fetch API
  global.fetch = jest.fn();

  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  it('should send a message successfully', async () => {
    const mockResponse = {
      success: true,
      response: 'Task created successfully',
      conversation_id: '123',
      message_id: '456'
    };

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse)
    });

    const result = await ChatService.sendMessage('Add a new task', 'user123');

    expect(result).toEqual(mockResponse);
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/user123/chat'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    );
  });

  it('should handle errors gracefully', async () => {
    (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

    const result = await ChatService.sendMessage('Add a new task', 'user123');

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });
});