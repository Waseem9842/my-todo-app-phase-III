// Tasks page component
// Displays all tasks for the authenticated user with CRUD functionality

'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/providers/AuthProvider';
import { Task } from '@/types/task';
import { TaskList } from '@/components/tasks/TaskList';
import { TaskService } from '@/services/task_service';

// Tasks page component implementation
export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuth();

  // Load tasks when component mounts or user changes
  useEffect(() => {
    if (user && user.isAuthenticated && user.id) {
      loadTasks();
    }
  }, [user]);

  // Load tasks for the authenticated user
  const loadTasks = async () => {
    if (!user || !user.id) return;

    try {
      setLoading(true);
      setError(null);
      const userTasks = await TaskService.getTasksByUser(parseInt(user.id));
      setTasks(userTasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle updating a task
  const handleUpdateTask = async (updatedTask: Task) => {
    if (!user || !user.id) return;

    try {
      setLoading(true);
      const updated = await TaskService.updateTask(
        parseInt(user.id),
        updatedTask.id,
        {
          title: updatedTask.title,
          description: updatedTask.description,
          completed: updatedTask.completed
        }
      );

      setTasks(tasks.map(task => task.id === updated.id ? updated : task));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle toggling task completion
  const handleToggleTaskCompletion = async (taskId: number, completed: boolean) => {
    if (!user || !user.id) return;

    try {
      setLoading(true);
      const updatedTask = await TaskService.toggleTaskCompletion(
        parseInt(user.id),
        taskId,
        completed
      );

      setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task completion');
      console.error('Error toggling task completion:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle deleting a task
  const handleDeleteTask = async (taskId: number) => {
    if (!user || !user.id) return;

    try {
      setLoading(true);
      await TaskService.deleteTask(parseInt(user.id), taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-6">
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
              My Tasks
            </h1>
            <p className="mt-2 text-gray-600">
              Manage your todo items efficiently
            </p>
          </div>
          <div className="flex space-x-3">
            <div className="bg-indigo-50 px-4 py-2 rounded-lg flex items-center">
              <span className="text-sm font-medium text-indigo-700">
                Total: {tasks.length} tasks
              </span>
            </div>
            <div className="bg-green-50 px-4 py-2 rounded-lg flex items-center">
              <span className="text-sm font-medium text-green-700">
                Completed: {tasks.filter(t => t.completed).length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-r-lg mb-6" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="bg-white rounded-2xl border-0 shadow-lg overflow-hidden">
        <TaskList
          tasks={tasks}
          loading={loading}
          error={error}
          onTaskUpdate={handleUpdateTask}
          onTaskDelete={handleDeleteTask}
          onTaskToggleCompletion={handleToggleTaskCompletion}
        />
      </div>
    </div>
  );
}