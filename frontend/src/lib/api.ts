import { TaskRead, TaskCreate, TaskUpdate } from '@/types/task';

// Mock in-memory task storage for temporary use without authentication
let mockTasks: TaskRead[] = [
  { id: 1, title: 'Sample Task', description: 'This is a sample task', completed: false, priority: 'medium', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
  { id: 2, title: 'Another Task', description: 'This is another sample task', completed: true, priority: 'high', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() }
];

class ApiClient {
  private mockDelay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  async getTasks(): Promise<TaskRead[]> {
    // Simulate network delay
    await this.mockDelay(200);
    return [...mockTasks]; // Return a copy to prevent direct mutation
  }

  async createTask(task: TaskCreate): Promise<TaskRead> {
    await this.mockDelay(300);
    const newTask: TaskRead = {
      ...task,
      id: Math.max(...mockTasks.map(t => t.id), 0) + 1,
      completed: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    mockTasks.push(newTask);
    return newTask;
  }

  async updateTask(id: number, task: TaskUpdate): Promise<TaskRead> {
    await this.mockDelay(300);
    const index = mockTasks.findIndex(t => t.id === id);
    if (index === -1) {
      throw new Error('Task not found');
    }
    const updatedTask = {
      ...mockTasks[index],
      ...task,
      id,
      updatedAt: new Date().toISOString()
    };
    mockTasks[index] = updatedTask;
    return updatedTask;
  }

  async deleteTask(id: number): Promise<void> {
    await this.mockDelay(300);
    mockTasks = mockTasks.filter(task => task.id !== id);
  }

  async toggleTaskCompletion(id: number): Promise<TaskRead> {
    await this.mockDelay(300);
    const index = mockTasks.findIndex(t => t.id === id);
    if (index === -1) {
      throw new Error('Task not found');
    }
    const task = mockTasks[index];
    const updatedTask = {
      ...task,
      completed: !task.completed,
      updatedAt: new Date().toISOString()
    };
    mockTasks[index] = updatedTask;
    return updatedTask;
  }
}

export const apiClient = new ApiClient();