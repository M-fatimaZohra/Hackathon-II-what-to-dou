'use client';

import { useState } from 'react';
import { TaskCreate } from '@/types/task';
import { Inter, Oswald } from 'next/font/google';

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

interface TaskFormProps {
  userId?: string;
  onTaskCreated: (task: TaskCreate, completed: boolean) => void;
}

export default function TaskForm({ userId, onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setError(null);
    setIsSubmitting(true);

    try {
      // Create task object to send to API
      const newTask: TaskCreate = {
        title,
        description,
        priority,
      };

      await onTaskCreated(newTask, false); // New tasks are not completed by default

      // Reset form
      setTitle('');
      setDescription('');
      setPriority('medium');
    } catch (err) {
      console.error('Failed to create task:', err);
      setError('Failed to create task. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full bg-[#FFFDF8] p-6 rounded-lg border border-[#F1F0EB] shadow-lg transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-2xl max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold mb-4 text-[#1B1C1C]" style={oswald.style}>Create New Task</h2>
      {error && <div className="mb-4 p-3 bg-[#FFB5E1] text-[#1B1C1C] rounded" style={inter.style}>{error}</div>}
      <form onSubmit={handleSubmit} style={inter.style}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-[#1B1C1C] font-medium mb-2">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C] transition-all duration-300 ease-in-out hover:scale-105 focus:scale-105"
            disabled={isSubmitting}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="description" className="block text-[#1B1C1C] font-medium mb-2">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C] transition-all duration-300 ease-in-out hover:scale-105 focus:scale-105"
            rows={3}
            disabled={isSubmitting}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="priority" className="block text-[#1B1C1C] font-medium mb-2">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as any)}
            className="w-full px-3 py-2 border border-[#F1F0EB] rounded-md focus:outline-none focus:ring-2 focus:ring-[#f2d16f] bg-[#FFFDF8] text-[#1B1C1C] transition-all duration-300 ease-in-out hover:scale-105 focus:scale-105"
            disabled={isSubmitting}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>
        <button
          type="submit"
          className={`w-full py-2 px-4 rounded-md text-[#1B1C1C] font-medium bg-[#f2d16f] hover:bg-[#FFE9A8] transition-all duration-200 ease-in-out hover:scale-[1.02] ${isSubmitting ? 'opacity-70 cursor-not-allowed' : ''}`}
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Creating Task...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
}