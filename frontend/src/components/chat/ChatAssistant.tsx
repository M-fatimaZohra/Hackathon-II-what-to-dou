'use client';

import { ChatKit } from '@openai/chatkit-react';
import { useState, useEffect, useRef } from 'react';
import { X, MessageCircle, Clock } from 'lucide-react';
import { useChatContext } from '@/components/ChatProvider';

interface ChatAssistantProps {
  conversationId?: string | null;
  onClose?: () => void;
  isOpen?: boolean;
}

// T014-T016: ChatAssistant wrapper component with sidebar overlay
export function ChatAssistant({ conversationId, onClose, isOpen = false }: ChatAssistantProps) {
  const [isExpanded, setIsExpanded] = useState(isOpen);
  const [viewMode, setViewMode] = useState<'chat' | 'history'>('chat');

  // T015: Get control object and fallback messages from ChatProvider context
  const { control, isReady, messages } = useChatContext();
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

  // Diagnostic: Check web component initialization
  useEffect(() => {
    const checkWebComponent = async () => {
      try {
        await customElements.whenDefined('openai-chatkit');
        console.log('[ChatKit] Web component ready');
      } catch (error) {
        console.error('[ChatKit] Web component failed to initialize:', error);
      }
    };
    checkWebComponent();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

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

        {/* T015: ChatKit full-height with view mode toggle */}
        <div className="h-[calc(100%-64px)] relative overflow-hidden">
          {/* ChatKit SDK: full height background layer (always rendered) */}
          {isReady && control && (
            <ChatKit
              control={control}
              className="h-full"
            />
          )}

          {/* View mode toggle strip: Chat / History */}
          {messages.length > 0 && (
            <div
              className="absolute left-0 right-0 z-20 flex bg-white border-b border-gray-100"
              style={{ top: '52px' }}
            >
              <button
                onClick={() => setViewMode('chat')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 text-[13px] font-medium transition-colors ${
                  viewMode === 'chat'
                    ? 'text-[#0D0D0D] border-b-2 border-[#0D0D0D]'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <MessageCircle className="w-3.5 h-3.5" />
                Chat
              </button>
              <button
                onClick={() => setViewMode('history')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2 text-[13px] font-medium transition-colors ${
                  viewMode === 'history'
                    ? 'text-[#0D0D0D] border-b-2 border-[#0D0D0D]'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <Clock className="w-3.5 h-3.5" />
                History
              </button>
            </div>
          )}

          {/* Custom message overlay: only visible in chat mode */}
          {viewMode === 'chat' && messages.length > 0 && (
            <div
              className="absolute left-0 right-0 z-10 bg-white overflow-y-auto pointer-events-auto"
              style={{ top: '88px', bottom: '118px' }}
            >
              <div className="px-5 py-4 space-y-5">
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {msg.role === 'user' ? (
                      <div className="max-w-[85%] bg-[#F3F3F3] text-[#0D0D0D] rounded-[20px] rounded-br-[4px] py-2.5 px-4 text-[15px] leading-relaxed whitespace-pre-wrap">
                        {msg.content}
                      </div>
                    ) : (
                      <div className="max-w-[90%] text-[#0D0D0D] text-[15px] leading-relaxed whitespace-pre-wrap">
                        {msg.content}
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
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
