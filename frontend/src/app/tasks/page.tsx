'use client';

import TaskList from '@/components/TaskList';
import { ChatProvider } from '@/components/ChatProvider';
import { ChatAssistant, useChatSidebar } from '@/components/chat/ChatAssistant';
import { MessageSquare } from 'lucide-react';

export default function TasksPage() {
  const { isOpen, open, close } = useChatSidebar();

  return (
    // T018: Wrap content with ChatProvider
    <ChatProvider>
      <div className="min-h-screen bg-[#FFFBED]">
        {/* T017: Toggle button for opening chat sidebar */}
        <div className="fixed bottom-6 right-6 z-30">
          <button
            onClick={open}
            className="flex items-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors"
            aria-label="Open AI Assistant"
          >
            <MessageSquare className="w-5 h-5" />
            <span className="font-medium">AI Assistant</span>
          </button>
        </div>

        <TaskList />

        {/* T016: Conditionally render ChatAssistant sidebar */}
        <ChatAssistant isOpen={isOpen} onClose={close} />
      </div>
    </ChatProvider>
  );
}