/**
 * Chat Type Definitions
 *
 * Type definitions for ChatKit integration with Better Auth
 */

/**
 * ChatKit SDK Configuration
 */
export interface ChatKitConfig {
  baseUrl: string | (() => Promise<string>);
  headers: Record<string, string> | (() => Promise<Record<string, string>>);
  domainKey: string;
  onError?: (error: ChatError) => void;
}

/**
 * ChatProvider Component Props
 */
export interface ChatProviderProps {
  children: React.ReactNode;
}

/**
 * Chat Error Types
 */
export interface ChatError {
  message: string;
  code?: string;
  status?: number;
  details?: unknown;
}

/**
 * Chat Session Data
 */
export interface ChatSession {
  userId: string;
  accessToken: string;
}

/**
 * ChatKit Message Types
 */
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

/**
 * Conversation Metadata
 */
export interface ConversationMetadata {
  id?: string | null;
  title?: string;
  createdAt?: Date;
  updatedAt?: Date;
}
