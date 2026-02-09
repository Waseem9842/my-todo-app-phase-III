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
import dynamic from 'next/dynamic';

// Dynamically import the chat component to avoid SSR issues
const DynamicChatInterface = dynamic(() => import('@/components/chat/DynamicChatComponent'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
    </div>
  ),
});

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
    <div className="max-w-7xl mx-auto p-4 md:p-6">
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
              Dashboard
            </h1>
            <p className="mt-2 text-gray-600">
              Welcome back, {user?.name || user?.email || 'User'}. Manage your tasks and account settings efficiently.
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-indigo-50 px-4 py-2 rounded-lg">
              <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-sm font-medium text-indigo-700">Online</span>
            </div>
            <Button
              variant="outline"
              onClick={() => {
                logout();
                router.push('/signin');
              }}
              className="border-red-200 text-red-600 hover:bg-red-50"
            >
              Sign Out
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gradient-to-br from-indigo-50 to-white p-6 rounded-2xl border border-indigo-100 shadow-sm">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-indigo-100">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-600">Total Tasks</h3>
              <p className="text-2xl font-bold text-gray-900">{tasks.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-white p-6 rounded-2xl border border-green-100 shadow-sm">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-100">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-600">Completed</h3>
              <p className="text-2xl font-bold text-gray-900">{tasks.filter(t => t.completed).length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-amber-50 to-white p-6 rounded-2xl border border-amber-100 shadow-sm">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-amber-100">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-600">Pending</h3>
              <p className="text-2xl font-bold text-gray-900">{tasks.filter(t => !t.completed).length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tasks section - Show up to 5 tasks */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">Your Tasks</h2>
          <Button
            onClick={() => router.push('/tasks')}
            className="bg-indigo-600 hover:bg-indigo-700"
          >
            View All
          </Button>
        </div>
        <Card className="rounded-2xl border-0 shadow-lg bg-white">
          <CardContent className="p-6">
            <TaskList
              tasks={tasks.slice(0, 5)} // Show only first 5 tasks
              loading={tasksLoading}
              error={tasksError}
              onTaskUpdate={handleUpdateTask}
              onTaskDelete={handleDeleteTask}
              onTaskToggleCompletion={handleToggleTaskCompletion}
            />
            {tasks.length === 0 && !tasksLoading && (
              <div className="text-center py-12">
                <div className="mx-auto h-16 w-16 rounded-full bg-indigo-100 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <p className="text-gray-600 text-lg mb-4">
                  No tasks yet. Get started by creating your first task!
                </p>
                <Button
                  onClick={() => router.push('/tasks/new')}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                >
                  Create Your First Task
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="rounded-2xl border-0 shadow-lg bg-gradient-to-br from-white to-indigo-50">
          <CardHeader>
            <CardTitle className="flex items-center">
              <div className="p-2 rounded-lg bg-indigo-100 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <span>Create New Task</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-6">
              Add a new task to stay organized and boost your productivity
            </p>
            <Button
              onClick={() => router.push('/tasks/new')}
              className="w-full bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800"
            >
              Create Task
            </Button>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-0 shadow-lg bg-gradient-to-br from-white to-purple-50">
          <CardHeader>
            <CardTitle className="flex items-center">
              <div className="p-2 rounded-lg bg-purple-100 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <span>Manage Account</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-6">
              Update your account settings and preferences
            </p>
            <Button
              onClick={() => router.push('/profile')}
              variant="outline"
              className="w-full border-purple-200 text-purple-700 hover:bg-purple-50"
            >
              Profile Settings
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Chatbot Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">AI Todo Assistant</h2>
        </div>
        <Card className="rounded-2xl border-0 shadow-lg overflow-hidden">
          <CardContent className="p-0">
            <div className="h-[400px]">
              <DynamicChatInterface />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="text-center text-sm text-gray-500 mt-12">
        <p>Designed and developed by Muhammad Waseem</p>
      </div>
    </div>
  );
}
