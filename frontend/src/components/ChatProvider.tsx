'use client';

import { useChatKit } from '@openai/chatkit-react';
import { authClient } from '@/lib/auth-client';
import { CONFIG } from '@/lib/config';
import { getJwtTokenFromCookie } from '@/lib/jwt-utils';
import { ReactNode, useEffect, useState, createContext, useContext, useRef } from 'react';
import { ChatProviderProps } from '@/types/chat';

// Message type for fallback rendering when ChatKit SDK fails to display
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

// T008: Create context to share control object from useChatKit
interface ChatContextType {
  control: any;
  isReady: boolean;
  token: string;
  userId: string;
  messages: ChatMessage[];
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
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // Use refs to access current values in fetch closure
  const userIdRef = useRef(userId);
  const tokenRef = useRef(token);
  // Track the last user message text for pairing with response.done
  const pendingUserMessageRef = useRef<string>('');

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

  // T008: Use useChatKit hook with CustomApiConfig for pass-through to custom SSE backend
  // Destructure both control AND top-level methods (setThreadId, ref, etc.)
  const { control, ref, setThreadId } = useChatKit({
    api: {
      // CustomApiConfig: domainKey identifies the domain for ChatKit
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || 'localhost-dev',

      // Point ChatKit to our custom FastAPI backend streaming endpoint
      url: `${CONFIG.API_BASE_URL}/${userId}/chat`,

      // Custom fetch function to inject JWT Authorization header and transform request
      fetch: async (input: RequestInfo | URL, init?: RequestInit) => {
        // Get current token from ref (avoids closure issues)
        const currentToken = tokenRef.current;

        if (!currentToken) {
          throw new Error('Authentication token not available');
        }

        // Transform request body to match backend ChatRequest schema
        let transformedBody: any = {};

        if (init?.body) {
          try {
            const originalBody = JSON.parse(init.body as string);

            // 🔍 DEBUG: Log ALL requests to understand ChatKit's behavior
            console.log('[ChatProvider] ===== REQUEST START =====');
            console.log('[ChatProvider] Request type:', originalBody.type || 'NO TYPE');
            console.log('[ChatProvider] Full request body:', JSON.stringify(originalBody, null, 2));
            console.log('[ChatProvider] ===== REQUEST END =====');

            // T063-T064: CRITICAL FIX - Intercept threads.list requests (FR-017)
            // ChatKit sends threads.list on mount to load conversation history
            // Backend doesn't implement thread listing endpoint, so we mock the response
            // Without this, threads.list gets transformed to {message: ''} and corrupts ChatKit state
            if (originalBody.type === 'threads.list') {
              console.log('[ChatProvider] ✅ INTERCEPTING threads.list - returning mock response');
              return new Response(JSON.stringify({
                data: [],
                has_more: false
              }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
              });
            }

            console.log('[ChatProvider] ⚠️ NOT threads.list - proceeding to transform for backend');

            // Extract message from various possible formats
            let message = "";

            // ChatKit SDK actual format: {params: {input: {content: [{type: "input_text", text: "..."}]}}}
            if (originalBody.params?.input?.content && Array.isArray(originalBody.params.input.content)) {
              const textContent = originalBody.params.input.content.find(
                (item: any) => item.type === "input_text"
              );
              message = textContent?.text || "";
            } else if (originalBody.messages && Array.isArray(originalBody.messages)) {
              // Fallback: {messages: [{role: "user", content: "..."}]}
              const lastMessage = originalBody.messages[originalBody.messages.length - 1];
              message = lastMessage?.content || "";
            } else if (originalBody.message) {
              // Fallback: {message: "..."}
              message = originalBody.message;
            } else if (originalBody.input) {
              // Fallback: {input: "..."}
              message = originalBody.input;
            }

            // Extract thread_id if present and map to conversation_id
            let conversationId: number | undefined = undefined;
            if (originalBody.params?.thread_id) {
              // ChatKit sends thread_id as string, convert to number for backend
              conversationId = parseInt(originalBody.params.thread_id, 10);
              console.log('[ChatProvider] Thread ID from request:', conversationId);
            }

            // Create request matching ChatRequest schema: {message: string, conversation_id?: number}
            transformedBody = {
              message: message,
              conversation_id: conversationId,
            };

            // Immediately show user message in custom UI (don't wait for response.done)
            if (message) {
              setMessages(prev => [...prev, { role: 'user' as const, content: message }]);
              console.log('[ChatProvider] 💬 User message added immediately:', message.slice(0, 60));
            }
            pendingUserMessageRef.current = message;

            console.log('[ChatProvider] Transformed request:', transformedBody);
          } catch (e) {
            console.error('[ChatProvider] Failed to parse request body:', e);
            // If parsing fails, pass through original body
            transformedBody = init.body;
          }
        }

        // Inject Authorization header with JWT token
        const response = await fetch(input, {
          ...init,
          body: JSON.stringify(transformedBody),
          headers: {
            ...init?.headers,
            'Authorization': `Bearer ${currentToken}`,
            'Content-Type': 'application/json',
          },
        });

        // Parse SSE stream for response.done fallback + thread sync
        const contentType = response.headers.get('content-type');
        if (contentType?.includes('text/event-stream') && response.body) {
          const [stream1, stream2] = response.body.tee();

          // Non-blocking: parse stream2 for thread.created and response.done only
          (async () => {
            const reader = stream2.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            try {
              while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                  if (!line.startsWith('data: ')) continue;
                  try {
                    const evt = JSON.parse(line.slice(6));

                    // Sync thread ID from backend
                    if (evt.type === 'thread.created' && evt.thread?.id) {
                      console.log('[ChatProvider] 🔗 Thread synced:', evt.thread.id);
                      setThreadId(evt.thread.id);
                    }

                    // Capture final assistant text from response.done
                    // (User message already added immediately on send)
                    if (evt.type === 'response.done') {
                      const assistantText =
                        evt.response?.output?.[0]?.content?.[0]?.text || '';

                      if (assistantText) {
                        console.log('[ChatProvider] ✅ response.done captured:', assistantText.slice(0, 80));
                        setMessages(prev => [
                          ...prev,
                          { role: 'assistant' as const, content: assistantText },
                        ]);
                        pendingUserMessageRef.current = '';
                      }

                      // Final thread sync
                      const threadId = evt.response?.output?.[0]?.id?.split('_')[1];
                      if (evt.response?.id) {
                        console.log('[ChatProvider] 🔗 Final response ID:', evt.response.id);
                      }
                    }
                  } catch {
                    // Skip non-JSON lines
                  }
                }
              }
            } catch (err) {
              console.error('[ChatProvider] Stream parse error:', err);
            } finally {
              reader.releaseLock();
            }
          })();

          // Return stream1 to ChatKit SDK for its own processing
          return new Response(stream1, {
            status: response.status,
            statusText: response.statusText,
            headers: response.headers,
          });
        }

        return response;
      },
    },
    // Thread change callback — event payload is { threadId: string | null }
    onThreadChange: (event) => {
      console.log('[ChatProvider] Thread change event:', event);
      if (event?.threadId) {
        console.log('[ChatProvider] Syncing thread ID:', event.threadId);
        setThreadId(event.threadId);
      }
    },
    // T012: Error handling callback
    onError: (err) => {
      console.error('[ChatKit Error]:', {
        error: err,
        message: err.error?.message,
        timestamp: new Date().toISOString()
      });

      if (err.error?.message?.includes('401') || err.error?.message?.includes('Unauthorized')) {
        setError('Session expired. Please log in again.');
      } else if (err.error?.message?.includes('403')) {
        setError('Access denied. Please check your permissions.');
      } else {
        setError(err.error?.message || 'An error occurred with the chat service.');
      }
    },
  });

  // Monitor thread ID changes for debugging
  useEffect(() => {
    if (ref?.current) {
      // Note: threadId might not be directly accessible on ref.current
      // This is for debugging purposes only
      console.log('[ChatProvider] ChatKit ref available:', !!ref.current);
    }
  }, [ref]);

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
    <ChatContext.Provider value={{ control, isReady, token, userId, messages }}>
      {children}
    </ChatContext.Provider>
  );
}
