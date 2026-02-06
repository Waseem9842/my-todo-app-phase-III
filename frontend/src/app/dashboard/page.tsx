// Dashboard page component
// Shows authenticated user's overview and navigation to tasks

'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Task } from '@/types/task';
import { TaskService } from '@/services/task_service';
import { TaskList } from '@/components/tasks/TaskList';
import { ChatProvider } from '@/providers/ChatProvider';
import { ChatInterface } from '@/components/chat/ChatInterface';

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [tasksLoading, setTasksLoading] = useState<boolean>(true);
  const [tasksError, setTasksError] = useState<string | null>(null);

  useEffect(() => {
    // If user is not authenticated, redirect to sign in
    if (!loading && (!user || !user.isAuthenticated)) {
      router.push('/signin');
    }
  }, [user, loading, router]);

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
      setTasksLoading(true);
      setTasksError(null);
      const userTasks = await TaskService.getTasksByUser(parseInt(user.id));
      setTasks(userTasks);
    } catch (err) {
      setTasksError(err instanceof Error ? err.message : 'Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setTasksLoading(false);
    }
  };

  // Handle updating a task
  const handleUpdateTask = async (updatedTask: Task) => {
    if (!user || !user.id) return;

    try {
      setTasksLoading(true);
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
      setTasksError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setTasksLoading(false);
    }
  };

  // Handle toggling task completion
  const handleToggleTaskCompletion = async (taskId: number, completed: boolean) => {
    if (!user || !user.id) return;

    try {
      setTasksLoading(true);
      const updatedTask = await TaskService.toggleTaskCompletion(
        parseInt(user.id),
        taskId,
        completed
      );

      setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    } catch (err) {
      setTasksError(err instanceof Error ? err.message : 'Failed to update task completion');
      console.error('Error toggling task completion:', err);
    } finally {
      setTasksLoading(false);
    }
  };

  // Handle deleting a task
  const handleDeleteTask = async (taskId: number) => {
    if (!user || !user.id) return;

    try {
      setTasksLoading(true);
      await TaskService.deleteTask(parseInt(user.id), taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setTasksError(err instanceof Error ? err.message : 'Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setTasksLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user || !user.isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
         Welcome back. Manage your tasks and account settings efficiently.
         Designed and developed by Muhammad Waseem.
        </p>
      </div>

      {/* Tasks section - Show up to 5 tasks */}
      <div className="mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-xl font-semibold">Your Tasks</CardTitle>
            <Button
              onClick={() => router.push('/tasks')}
              variant="outline"
              size="sm"
              className="text-sm"
            >
              View All
            </Button>
          </CardHeader>
          <CardContent>
            <TaskList
              tasks={tasks.slice(0, 5)} // Show only first 5 tasks
              loading={tasksLoading}
              error={tasksError}
              onTaskUpdate={handleUpdateTask}
              onTaskDelete={handleDeleteTask}
              onTaskToggleCompletion={handleToggleTaskCompletion}
            />
            {tasks.length === 0 && !tasksLoading && (
              <div className="text-center py-8">
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  No tasks yet.
                </p>
                <Button
                  onClick={() => router.push('/tasks/new')}
                  variant="default"
                >
                  Create Your First Task
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Add New Task</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Create a new task to stay organized
            </p>
            <Button
              onClick={() => router.push('/tasks/new')}
              className="w-full"
            >
              Create Task
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Manage Account</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Update your account settings and preferences
            </p>
            <Button
              onClick={() => router.push('/profile')}
              variant="outline"
              className="w-full"
            >
              Profile Settings
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Chatbot Section */}
      <div className="mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-semibold">AI Todo Assistant</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              <ChatProvider>
                <ChatInterface />
              </ChatProvider>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end">
        <Button
          variant="outline"
          onClick={() => {
            logout();
            router.push('/signin');
          }}
        >
          Sign Out
        </Button>
      </div>
    </div>
  );
}
