// Individual task page component
// Displays and allows editing of a specific task for the authenticated user

'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { apiClient } from '@/lib/api';
import { Task, TaskUpdate } from '@/types/task';
import { TaskForm } from '@/components/tasks/TaskForm';

export default function TaskDetailPage() {
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();

  // Load the specific task when component mounts or user changes
  useEffect(() => {
    if (user && user.id && params.id) {
      loadTask();
    }
  }, [user, params.id]);

  // Load the specific task
  const loadTask = async () => {
    if (!user || !user.id || !params.id) return;

    try {
      setLoading(true);
      setError(null);
      const taskId = parseInt(params.id as string);
      const loadedTask = await apiClient.get<Task>(`/${parseInt(user.id)}/tasks/${taskId}`);
      setTask(loadedTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load task');
      console.error('Error loading task:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle updating the task
  const handleUpdateTask = async (updatedTask: TaskUpdate) => {
    if (!user || !user.id || !task) return;

    try {
      setLoading(true);
      setError(null);

      const response = await apiClient.put<Task>(
        `/${parseInt(user.id)}/tasks/${task.id}`,
        {
          title: updatedTask.title ?? task.title,
          description: updatedTask.description ?? task.description,
          completed: updatedTask.completed ?? task.completed
        }
      );

      setTask(response);
      router.push('/tasks'); // Redirect back to tasks list after update
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle deleting the task
  const handleDeleteTask = async () => {
    if (!user || !user.id || !task) return;

    if (confirm('Are you sure you want to delete this task?')) {
      try {
        setLoading(true);
        setError(null);

        await apiClient.delete(`/${parseInt(user.id)}/tasks/${task.id}`);
        router.push('/tasks'); // Redirect back to tasks list after deletion
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to delete task');
        console.error('Error deleting task:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  // Handle toggling task completion
  const handleToggleCompletion = async () => {
    if (!user || !user.id || !task) return;

    try {
      setLoading(true);
      setError(null);

      const response = await apiClient.patch<Task>(
        `/${parseInt(user.id)}/tasks/${task.id}/complete`,
        { completed: !task.completed }
      );

      setTask(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task completion');
      console.error('Error toggling task completion:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle cancel action
  const handleCancel = () => {
    router.push('/tasks');
  };

  // Render loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
        <button
          onClick={() => router.back()}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Go Back
        </button>
      </div>
    );
  }

  // Render task not found
  if (!task) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4" role="alert">
          <span className="block sm:inline">Task not found or does not belong to the current user</span>
        </div>
        <button
          onClick={() => router.push('/tasks')}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Back to Tasks
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Task Details</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Edit or manage your task
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h2 className={`text-xl font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900 dark:text-white'}`}>
              {task.title}
            </h2>
            {task.description && (
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                {task.description}
              </p>
            )}
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleToggleCompletion}
              className={`inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md ${
                task.completed
                  ? 'text-white bg-green-600 hover:bg-green-700'
                  : 'text-white bg-yellow-600 hover:bg-yellow-700'
              }`}
            >
              {task.completed ? 'Mark Incomplete' : 'Mark Complete'}
            </button>
          </div>
        </div>

        <div className="mt-4 flex items-center text-xs text-gray-500 dark:text-gray-400">
          <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
          <span className="mx-2">•</span>
          <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
        </div>

        <div className="mt-6 flex space-x-4">
          <button
            onClick={handleDeleteTask}
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete Task
          </button>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Edit Task</h2>
        <TaskForm
          task={task}
          onSubmit={handleUpdateTask}
          onCancel={handleCancel}
          loading={loading}
          error={error}
        />
      </div>
    </div>
  );
}