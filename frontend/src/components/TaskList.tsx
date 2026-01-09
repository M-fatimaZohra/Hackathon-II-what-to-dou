'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import { Inter, Oswald } from 'next/font/google';
import TaskForm from './TaskForm';
import TaskStatusToggle from './TaskStatusToggle';
import { apiClient } from '@/lib/api';

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const oswald = Oswald({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editForm, setEditForm] = useState({ title: '', description: '', priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent' });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await apiClient.getTasks();
      setTasks(tasksData);
      setError(null);
    } catch (err: any) {
      console.error('Failed to load tasks:', err);
      setError('Failed to load tasks. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = async (newTask: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt' | 'completed'>, completed: boolean) => {
    try {
      const createdTask = await apiClient.createTask(newTask);
      setTasks([createdTask, ...tasks]);
    } catch (err: any) {
      console.error('Failed to create task:', err);
      setError('Failed to create task. Please try again.');
    }
  };

  const handleTaskUpdated = async (updatedTask: Task) => {
    try {
      const updatedTaskResult = await apiClient.updateTask(updatedTask.id, {
        title: updatedTask.title,
        description: updatedTask.description,
        priority: updatedTask.priority
      });

      setTasks(tasks.map(task =>
        task.id === updatedTask.id ? updatedTaskResult : task
      ));
      setEditingTask(null);
    } catch (err: any) {
      console.error('Failed to update task:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  const handleTaskDeleted = async (taskId: number) => {
    try {
      await apiClient.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task. Please try again.');
    }
  };

  const handleStatusToggle = async (taskId: number, completed: boolean) => {
    try {
      const updatedTask = await apiClient.toggleTaskCompletion(taskId);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      console.error('Failed to toggle task status:', err);
      setError('Failed to update task status. Please try again.');
    }
  };

  const startEditing = (task: Task) => {
    setEditingTask(task);
    setEditForm({
      title: task.title,
      description: task.description || '',
      priority: task.priority
    });
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (editingTask) {
      const updatedTask = {
        ...editingTask,
        title: editForm.title,
        description: editForm.description,
        priority: editForm.priority,
      };

      await handleTaskUpdated(updatedTask);
    }
  };

  const cancelEdit = () => {
    setEditingTask(null);
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">
      <p className="text-lg text-[#1B1C1C] font-inter">Loading tasks...</p>
    </div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-64">
      <p className="text-red-500 text-lg">{error}</p>
      <button
        onClick={loadTasks}
        className="ml-4 px-4 py-2 bg-[#f2d16f] text-[#1B1C1C] rounded hover:bg-[#FFE9A8]"
      >
        Retry
      </button>
    </div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 w-full" style={inter.style}>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-[#1B1C1C] mb-6" style={oswald.style}>My Tasks</h1>
        <TaskForm onTaskCreated={handleTaskCreated} />
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <h2 className="text-xl font-medium text-[#1B1C1C]" style={inter.style}>No tasks yet</h2>
          <p className="text-[#1B1C1C] mt-2" style={inter.style}>Create your first task to get started</p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            editingTask && editingTask.id === task.id ? (
              // Edit form for the task being edited
              <div key={task.id} className="p-4 rounded-lg border bg-[#FFFDF8] border-[#F1F0EB] shadow-lg transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-2xl">
                <form onSubmit={handleEditSubmit} style={inter.style}>
                  <div className="mb-2">
                    <input
                      type="text"
                      value={editForm.title}
                      onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                      className="w-full px-3 py-1 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C]"
                      required
                    />
                  </div>
                  <div className="mb-2">
                    <textarea
                      value={editForm.description}
                      onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                      className="w-full px-3 py-1 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C]"
                      rows={2}
                    />
                  </div>
                  <div className="mb-2 flex flex-col sm:flex-row sm:items-center gap-2">
                    <select
                      value={editForm.priority}
                      onChange={(e) => setEditForm({...editForm, priority: e.target.value as any})}
                      className="px-2 py-1 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C]"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      editForm.priority === 'low' ? 'bg-[#FFE9A8] text-[#1B1C1C]' :
                      editForm.priority === 'medium' ? 'bg-[#ECFFC6] text-[#1B1C1C]' :
                      editForm.priority === 'high' ? 'bg-[#FFB5E1] text-[#1B1C1C]' :
                      'bg-[#F1D6FF] text-[#1B1C1C]'
                    }`} style={inter.style}>
                      {editForm.priority.charAt(0).toUpperCase() + editForm.priority.slice(1)}
                    </span>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0 mt-2">
                    <button
                      type="submit"
                      className="px-3 py-1 bg-[#f2d16f] text-[#1B1C1C] rounded hover:bg-[#FFE9A8] transition-all duration-300 ease-in-out hover:scale-105 text-xs sm:text-sm"
                      style={inter.style}
                    >
                      Save
                    </button>
                    <button
                      type="button"
                      onClick={cancelEdit}
                      className="px-3 py-1 bg-[#ed72bb] text-white rounded hover:bg-[#FFB5E1] transition-all duration-300 ease-in-out hover:scale-105 text-xs sm:text-sm"
                      style={inter.style}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              // Display task normally
              <div
                key={task.id}
                className={`p-4 rounded-lg border transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-2xl ${
                  task.completed
                    ? 'bg-[#F1F0EB] border-[#F1F0EB] shadow-md'
                    : 'bg-[#FFFDF8] border-[#F1F0EB] shadow-lg'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 sm:gap-0">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center">
                      <TaskStatusToggle
                        taskId={task.id}
                        completed={task.completed}
                        onToggle={handleStatusToggle}
                      />
                      <h3 className={`ml-3 text-lg font-medium wrap-break-word ${
                        task.completed ? 'line-through text-[#1B1C1C]' : 'text-[#1B1C1C]'
                      }`} style={inter.style}>
                        {task.title}
                      </h3>
                    </div>
                    {task.description && (
                      <p className={`ml-10 mt-1 text-[#1B1C1C] wrap-break-word ${
                        task.completed ? 'text-opacity-60' : ''
                      }`} style={inter.style}>
                        {task.description}
                      </p>
                    )}
                    <div className="ml-10 mt-2 flex flex-wrap items-center gap-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        task.priority === 'low' ? 'bg-[#FFE9A8] text-[#1B1C1C]' :
                        task.priority === 'medium' ? 'bg-[#ECFFC6] text-[#1B1C1C]' :
                        task.priority === 'high' ? 'bg-[#FFB5E1] text-[#1B1C1C]' :
                        'bg-[#F1D6FF] text-[#1B1C1C]'
                      }`} style={inter.style}>
                        {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                      </span>
                      <span className="text-xs text-[#1B1C1C]" style={inter.style}>
                        Created: {new Date(task.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0">
                    <button
                      onClick={() => startEditing(task)}
                      className="px-3 py-1 bg-[#f2d16f] text-[#1B1C1C] rounded hover:bg-[#FFE9A8] transition-all duration-300 ease-in-out hover:scale-105 text-xs sm:text-sm"
                      style={inter.style}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleTaskDeleted(task.id)}
                      className="px-3 py-1 bg-[#ed72bb] text-white rounded hover:bg-[#FFB5E1] transition-all duration-300 ease-in-out hover:scale-105 text-xs sm:text-sm"
                      style={inter.style}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            )
          ))}
        </div>
      )}
    </div>
  );
}