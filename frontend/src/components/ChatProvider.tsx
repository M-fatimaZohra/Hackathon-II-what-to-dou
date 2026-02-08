'use client';

import { useChatKit } from '@openai/chatkit-react';
import { authClient } from '@/lib/auth-client';
import { CONFIG } from '@/lib/config';
import { getJwtTokenFromCookie } from '@/lib/jwt-utils';
import { ReactNode, useEffect, useState, createContext, useContext, useRef } from 'react';
import { ChatProviderProps } from '@/types/chat';

// T008: Create context to share control object from useChatKit
interface ChatContextType {
  control: any;
  isReady: boolean;
  token: string;
  userId: string;
}

const ChatContext = createContext<ChatContextType | null>(null);

export function useChatContext() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within ChatProvider');
  }
  return context;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string>('');
  const [userId, setUserId] = useState<string>('');

  // Use refs to access current values in getClientSecret closure
  const userIdRef = useRef(userId);
  const tokenRef = useRef(token);

  // Update refs whenever state changes
  useEffect(() => {
    userIdRef.current = userId;
    tokenRef.current = token;
  }, [userId, token]);

  // T009: Fetch JWT and userId from Better Auth
  useEffect(() => {
    const initAuth = async () => {
      try {
        const session = await authClient.getSession();

        if (!session?.data?.user?.id) {
          throw new Error('No active session or missing user ID');
        }

        // Extract userId from session (this works correctly)
        const extractedUserId = session.data.user.id;

        // Extract JWT from cookie using shared utility (same logic as apiClient)
        const extractedToken = getJwtTokenFromCookie();

        if (!extractedToken) {
          throw new Error('Session token not found in cookies. Please log in again.');
        }

        setUserId(extractedUserId);
        setToken(extractedToken);
        setIsReady(true);
      } catch (err) {
        console.error('Failed to get auth session:', err);
        setError('Authentication failed. Please log in again.');
      }
    };

    initAuth();
  }, []);

  // T008: Use useChatKit hook with Advanced Integration pattern (session exchange)
  const { control } = useChatKit({
    api: {
      // T010: Advanced Integration - Session exchange with backend
      // Remove domainKey for self-hosted backends (security requirement)
      getClientSecret: async () => {
        // Use refs to get current values instead of captured closure values
        const currentUserId = userIdRef.current;
        const currentToken = tokenRef.current;

        // Safety check: Ensure auth is ready before making API call
        if (!currentUserId || !currentToken) {
          throw new Error('Authentication not ready. Please wait for login to complete.');
        }

        try {
          // T011: POST to session endpoint to exchange JWT for client_secret
          const response = await fetch(`${CONFIG.API_BASE_URL}/${currentUserId}/chat/session`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${currentToken}`,
              'Content-Type': 'application/json',
            },
          });

          // T012: Handle authentication errors
          if (response.status === 401) {
            setError('Session expired. Please log in again.');
            throw new Error('Unauthorized: Session expired');
          }

          if (response.status === 403) {
            setError('Access denied. Please check your permissions.');
            throw new Error('Forbidden: Access denied');
          }

          if (!response.ok) {
            const errorText = await response.text();
            setError(`Failed to initialize chat: ${errorText}`);
            throw new Error(`Session exchange failed: ${response.status}`);
          }

          const data = await response.json();

          // T013: Return client_secret from backend response
          if (!data.client_secret) {
            setError('Invalid session response from server');
            throw new Error('Missing client_secret in response');
          }

          return data.client_secret;
        } catch (err) {
          console.error('Session exchange failed:', err);
          // Re-throw to let ChatKit handle the error
          throw err;
        }
      },
    },
    // T012: Error handling callback
    onError: (err) => {
      console.error('ChatKit error:', err);

      if (err.error?.message?.includes('401') || err.error?.message?.includes('Unauthorized')) {
        setError('Session expired. Please log in again.');
      } else if (err.error?.message?.includes('403')) {
        setError('Access denied. Please check your permissions.');
      } else {
        setError(err.error?.message || 'An error occurred with the chat service.');
      }
    },
  });

  // Error state rendering
  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800 font-semibold">ChatKit Configuration Error</p>
        <p className="text-red-600 text-sm">{error}</p>
        <button
          onClick={() => {
            setError(null);
            setIsReady(false);
            window.location.reload();
          }}
          className="mt-2 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  // Loading state while validating environment
  if (!isReady || !token || !userId) {
    return <div className="p-4">Initializing ChatKit...</div>;
  }

  // T008: Provide control object via context to child components
  // T013: SSE connection management handled by useChatKit hook internally
  return (
    <ChatContext.Provider value={{ control, isReady, token, userId }}>
      {children}
    </ChatContext.Provider>
  );
}
