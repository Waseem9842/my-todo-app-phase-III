// Create new task page component
// Provides a form for authenticated users to create a new todo task

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { TaskCreate, TaskUpdate } from '@/types/task';
import { TaskForm } from '@/components/tasks/TaskForm';
import { TaskService } from '@/services/task_service';

export default function CreateTaskPage() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuth();
  const router = useRouter();

  // Handle creating a new task
  const handleCreateTask = async (taskData: TaskCreate | TaskUpdate) => {
    if (!user || !user.id) {
      setError('User not authenticated');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Convert user.id to number, handling both string and number formats
      const userId = typeof user.id === 'string' ? parseInt(user.id, 10) : user.id;

      // Ensure we have a TaskCreate object for creation
      const taskCreateData: TaskCreate = {
        title: (taskData as TaskCreate).title,
        description: (taskData as TaskCreate).description,
        completed: (taskData as TaskCreate).completed || false
      };

      const newTask = await TaskService.createTask(userId, taskCreateData);

      // Redirect to tasks page after successful creation
      router.push('/tasks');
      router.refresh(); // Refresh to update the task list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle cancel action
  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Create New Task</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Add a new task to your todo list
        </p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <TaskForm
        onSubmit={handleCreateTask}
        onCancel={handleCancel}
        loading={loading}
        error={error}
      />
    </div>
  );
}