import { TaskRead, TaskCreate, TaskUpdate } from '@/types/task';
import { authClient } from '@/lib/auth-client';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

class ApiClient {
  private getSessionData = async (): Promise<{ headers: Record<string, string>, userId: string }> => {
    // Get session data using Better Auth client
    const session = await authClient.getSession();

    if (!session || !session.data?.user) {
      throw new Error('No active session found. Please log in.');
    }

    // In browser context, Better Auth stores the JWT in the better-auth.session_data cookie
    // We need to extract this token to send to the FastAPI backend
    if (typeof window === 'undefined') {
      // Server-side rendering context - we can't access cookies
      throw new Error('Cannot make authenticated requests during server-side rendering');
    }

    // Only extract JWT from better-auth.session_data cookie (no fallback logic)
    const token = this.getJwtTokenFromCookie();

    if (!token) {
      throw new Error('Session token not found. Please log in again.');
    }

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    // Ensure userId is extracted as session.data.user.id.
    const userId = session.data.user.id;

    return { headers, userId };
  }

  private getJwtTokenFromCookie(): string | null {
    if (typeof document === 'undefined') {
      // Not in browser context (SSR)
      return null;
    }

    // Extract JWT token - check both possible Better Auth cookie names
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
      cookie = cookie.trim();

      // Use startsWith to properly match the cookie name instead of includes
      if (cookie.startsWith('better-auth.session_data=')) {
        // Extract the cookie value after the equals sign
        const cookieValue = cookie.substring('better-auth.session_data='.length);

        let token = cookieValue;

        // Decode the token if it's URL-encoded
        try {
          token = decodeURIComponent(token);
        } catch (e) {
          continue; // Try next cookie
        }

        // Implement validation loop: verify if it is a 3-part string (split by dots)
        const parts = token.split('.');
        if (parts.length !== 3) {
          continue; // Try next cookie
        }

        // If it has 3 parts, decode the header (handling Base64URL characters - and _) and check if alg === "HS256"
        try {
          let headerPart = parts[0];
          // Handle Base64URL encoding by converting to Base64
          headerPart = headerPart.replace(/-/g, '+').replace(/_/g, '/');

          // Add padding if needed for base64 decoding
          let headerPadded = headerPart;
          while (headerPadded.length % 4 !== 0) {
            headerPadded += '=';
          }

          const headerJson = atob(headerPadded);
          const header = JSON.parse(headerJson);

          // Check if alg === "HS256" - remove strict checks for the typ header field as it may be undefined
          if (header.alg === 'HS256') {
            return token; // Return the token that satisfies the HS256 requirement
          } else {
            continue; // Try next cookie
          }
        } catch (e) {
          continue; // Try next cookie
        }
      }
      // Also check for session_token as a fallback
      else if (cookie.startsWith('better-auth.session_token=')) {
        // Extract the cookie value after the equals sign
        const cookieValue = cookie.substring('better-auth.session_token='.length);

        let token = cookieValue;

        // Decode the token if it's URL-encoded
        try {
          token = decodeURIComponent(token);
        } catch (e) {
          continue; // Try next cookie
        }

        // Implement validation loop: verify if it is a 3-part string (split by dots)
        const parts = token.split('.');
        if (parts.length !== 3) {
          continue; // Try next cookie
        }

        // If it has 3 parts, decode the header (handling Base64URL characters - and _) and check if alg === "HS256"
        try {
          let headerPart = parts[0];
          // Handle Base64URL encoding by converting to Base64
          headerPart = headerPart.replace(/-/g, '+').replace(/_/g, '/');

          // Add padding if needed for base64 decoding
          let headerPadded = headerPart;
          while (headerPadded.length % 4 !== 0) {
            headerPadded += '=';
          }

          const headerJson = atob(headerPadded);
          const header = JSON.parse(headerJson);

          // Check if alg === "HS256" - remove strict checks for the typ header field as it may be undefined
          if (header.alg === 'HS256') {
            return token; // Return the token that satisfies the HS256 requirement
          } else {
            continue; // Try next cookie
          }
        } catch (e) {
          continue; // Try next cookie
        }
      }
    }

    return null;
  }

  // Fetch Refactoring: Use a single helper for fetch to avoid repeating error logic
  private async request(path: string, options: RequestInit = {}, params?: Record<string, any>) {
    const { headers, userId } = await this.getSessionData();

    // Build the URL with parameters if provided
    let url = `${BASE_URL}/${userId}${path}`;

    if (params) {
      // Filter out null, undefined, and empty string values, then construct query string
      const filteredParams = Object.keys(params).reduce((acc, key) => {
        const value = params[key];
        if (value !== null && value !== undefined && value !== '') {
          acc[key] = value;
        }
        return acc;
      }, {} as Record<string, any>);

      const searchParams = new URLSearchParams(filteredParams);
      const paramsString = searchParams.toString();
      if (paramsString) {
        url = `${url}?${paramsString}`;
      }
    }

    const response = await fetch(url, { ...options, headers: { ...headers, ...options.headers } });

    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return response.status === 204 ? null : await response.json();
  }

  // Clean CRUD: Rewrite getTasks, createTask, etc., to just call return this.request('/tasks', { ... }).
  getTasks = async (filters?: { search?: string, priority?: string, completed?: boolean | null }): Promise<TaskRead[]> => {
    return this.request('/tasks', { method: 'GET' }, filters) as Promise<TaskRead[]>;
  }

  createTask = async (task: TaskCreate): Promise<TaskRead> => {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(task)
    }) as Promise<TaskRead>;
  }

  updateTask = async (id: number, task: TaskUpdate): Promise<TaskRead> => {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task)
    }) as Promise<TaskRead>;
  }

  deleteTask = async (id: number): Promise<void> => {
    await this.request(`/tasks/${id}`, { method: 'DELETE' });
  }

  toggleTaskCompletion = async (id: number): Promise<TaskRead> => {
    return this.request(`/tasks/${id}/complete`, { method: 'PATCH' }) as Promise<TaskRead>;
  }
}

export const apiClient = new ApiClient();