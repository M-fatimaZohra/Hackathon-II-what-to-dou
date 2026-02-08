'use client';

import { ChatKit } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { useChatContext } from '@/components/ChatProvider';

interface ChatAssistantProps {
  conversationId?: string | null;
  onClose?: () => void;
  isOpen?: boolean;
}

// T014-T016: ChatAssistant wrapper component with sidebar overlay
export function ChatAssistant({ conversationId, onClose, isOpen = false }: ChatAssistantProps) {
  const [isExpanded, setIsExpanded] = useState(isOpen);

  // T015: Get control object from ChatProvider context (single shared instance)
  const { control, isReady } = useChatContext();

  // Sync internal state with prop
  useEffect(() => {
    setIsExpanded(isOpen);
  }, [isOpen]);

  // T022: Handle Escape key to close sidebar
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isExpanded) {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isExpanded]);

  const handleClose = () => {
    setIsExpanded(false);
    onClose?.();
  };

  return (
    <>
      {/* Backdrop overlay when expanded */}
      {isExpanded && (
        <div
          className="fixed inset-0 bg-black/20 z-40 transition-opacity duration-300"
          onClick={handleClose}
          aria-hidden="true"
        />
      )}

      {/* T019: Sliding sidebar with fixed positioning and z-index management */}
      {/* T020: Slide-in/slide-out animations (300ms transition) */}
      {/* T021: Responsive design (full screen mobile, 400-500px desktop) */}
      <div
        className={`
          fixed top-0 right-0 h-full bg-white shadow-2xl z-50
          transition-transform duration-300 ease-in-out
          ${isExpanded ? 'translate-x-0' : 'translate-x-full'}
          w-full md:w-[400px] lg:w-[500px]
        `}
        role="dialog"
        aria-modal="true"
        aria-label="AI Assistant Chat"
      >
        {/* T022: Sidebar header with close button */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white">
          <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-md transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* T015: ChatKit component from @openai/chatkit-react SDK with control prop from ChatProvider context */}
        <div className="h-[calc(100%-64px)] overflow-hidden">
          {isReady && control && (
            <ChatKit
              control={control}
              className="h-full"
            />
          )}
        </div>
      </div>
    </>
  );
}

// Export hook for controlling sidebar state (used in tasks page)
export function useChatSidebar() {
  const [isOpen, setIsOpen] = useState(false);

  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);
  const toggle = () => setIsOpen(prev => !prev);

  return { isOpen, open, close, toggle };
}
