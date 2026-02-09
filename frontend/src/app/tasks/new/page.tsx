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
    <div className="max-w-3xl mx-auto p-4 md:p-6">
      <div className="mb-8">
        <div className="flex items-center">
          <div className="mr-4 p-3 rounded-xl bg-indigo-100">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
              Create New Task
            </h1>
            <p className="mt-2 text-gray-600">
              Add a new task to your todo list
            </p>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-r-lg mb-6" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="bg-white rounded-2xl border-0 shadow-lg p-6">
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={handleCancel}
          loading={loading}
          error={error}
        />
      </div>
    </div>
  );
}