// Task service functions
// Handles all API communication for task management operations

import { Task, TaskCreate, TaskUpdate, TaskApiResponse } from '@/types/task';
import { apiClient } from '@/lib/api';

// TaskService class to handle all task-related API operations
class TaskService {
  /**
   * Create a new task for a user
   */
  static async createTask(userId: number, taskCreate: TaskCreate): Promise<Task> {
    try {
      // Ensure userId is properly converted to a number
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const response = await apiClient.post<Task>(`/api/${numericUserId}/tasks`, taskCreate);
      return response;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  /**
   * Get all tasks for a specific user
   */
  static async getTasksByUser(userId: number): Promise<Task[]> {
    try {
      const response = await apiClient.get<Task[]>(`/api/${userId}/tasks`);
      return response || [];
    } catch (error) {
      console.error('Error getting tasks:', error);
      throw error;
    }
  }

  /**
   * Get a specific task by ID for a specific user
   */
  static async getTaskById(userId: number, taskId: number): Promise<Task> {
    try {
      const response = await apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`);
      return response;
    } catch (error) {
      console.error('Error getting task:', error);
      throw error;
    }
  }

  /**
   * Update a specific task for a user
   */
  static async updateTask(userId: number, taskId: number, taskUpdate: TaskUpdate): Promise<Task> {
    try {
      const response = await apiClient.put<Task>(`/api/${userId}/tasks/${taskId}`, taskUpdate);
      return response;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  /**
   * Toggle the completion status of a task for a user
   */
  static async toggleTaskCompletion(userId: number, taskId: number, completed: boolean): Promise<Task> {
    try {
      const response = await apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete?completed=${completed}`, {});
      return response;
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  }

  /**
   * Delete a specific task for a user
   */
  static async deleteTask(userId: number, taskId: number): Promise<void> {
    try {
      await apiClient.delete<void>(`/api/${userId}/tasks/${taskId}`);
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }
}

// Export the task service
export { TaskService };