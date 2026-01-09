export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  createdAt: string;
  updatedAt: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
}

// For API responses (same as Task but used to distinguish read operations)
export type TaskRead = Task;