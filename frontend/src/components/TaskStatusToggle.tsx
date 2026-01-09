'use client';

import { useState } from 'react';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

interface TaskStatusToggleProps {
  taskId: number;
  completed: boolean;
  onToggle: (taskId: number, completed: boolean) => void;
}

export default function TaskStatusToggle({ taskId, completed, onToggle }: TaskStatusToggleProps) {
  const handleChange = () => {
    const newCompleted = !completed;
    onToggle(taskId, newCompleted);
  };

  return (
    <button
      onClick={handleChange}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-all duration-300 ease-in-out focus:outline-none hover:scale-110 ${
        completed ? 'bg-[#c4eb78]' : 'bg-[#f2d16f]'
      }`}
      aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-all duration-300 ease-in-out ${
          completed ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  );
}