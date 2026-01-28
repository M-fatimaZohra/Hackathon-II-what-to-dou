/**
 * Search and Filter component for task management
 * Implements search by keyword, filter by priority, and filter by completion status
 */

import React, { useState, useEffect, useCallback } from 'react';

interface SearchFilterProps {
  onFilterChange: (filters: {
    search: string;
    priority: string | null;
    completed: boolean | null;
  }) => void;
}

const SearchFilter: React.FC<SearchFilterProps> = ({ onFilterChange }) => {
  const [search, setSearch] = useState<string>('');
  const [priority, setPriority] = useState<string | null>(null);
  const [completed, setCompleted] = useState<boolean | null>(null);


  // Effect to handle priority and completed changes immediately (without debounce)
  useEffect(() => {
    // Only call immediately for priority/completed changes
    onFilterChange({
      search,
      priority,
      completed
    });
  }, [priority, completed, onFilterChange]);

  // Function to handle search submission
  const handleSearchSubmit = () => {
    onFilterChange({
      search,
      priority,
      completed
    });
  };


  // Handle search input change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  // Handle key press for search input (submit on Enter)
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearchSubmit();
    }
  };

  // Handle priority change
  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value || null; // Convert empty string to null
    setPriority(value);
  };

  // Handle status change
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    if (value === '') {
      setCompleted(null);
    } else {
      setCompleted(value === 'true');
    }
  };

  // Handle clear filters
  const handleClearFilters = () => {
    setSearch('');
    setPriority(null);
    setCompleted(null);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4" data-testid="search-filter-component">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Search Input with Button */}
        <div className="md:col-span-2 flex gap-2">
          <div className="grow">
            <label htmlFor="search-input" className="block text-sm font-medium text-gray-700 mb-1">
              Search Tasks
            </label>
            <input
              id="search-input"
              type="text"
              placeholder="Search by title or description..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={search}
              onChange={handleSearchChange}
              onKeyDown={handleKeyPress}
            />
          </div>
          <div className="self-end pb-1"> {/* Align button with label */}
            <button
              type="button"
              className="px-4 py-2 bg-[#f2d16f] text-[#1B1C1C] rounded hover:bg-[#FFE9A8] transition-colors duration-300"
              onClick={handleSearchSubmit}
            >
              Search
            </button>
          </div>
        </div>

        {/* Priority Filter */}
        <div>
          <label htmlFor="priority-select" className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            id="priority-select"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={priority || ''}
            onChange={handlePriorityChange}
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label htmlFor="status-select" className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            id="status-select"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={completed === null ? '' : completed.toString()}
            onChange={handleStatusChange}
          >
            <option value="">All Statuses</option>
            <option value="true">Completed</option>
            <option value="false">Pending</option>
          </select>
        </div>
      </div>

      {/* Clear Filters Button */}
      {(search || priority || completed !== null) && (
        <div className="mt-3 flex justify-end">
          <button
            type="button"
            className="text-sm text-blue-600 hover:text-blue-800 underline"
            onClick={handleClearFilters}
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
};

export default SearchFilter;