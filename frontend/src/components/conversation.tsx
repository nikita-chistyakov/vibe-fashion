import { useConversationStore } from '@/libs/zustand/conversation';
import { Roles } from '@/constants';
import { useRef, useEffect, useCallback } from 'react';

const Buble = ({ text, role }: { text: string; role: string }) => {
  if (role === Roles.USER) {
    return (
      <div
        className={`rounded-lg p-4 py-2 max-w-xs break-words ${'bg-blue-500 text-white self-end rounded-br-none'}`}
      >
        {text}
      </div>
    );
  }
  return (
    <div
      className={`rounded-lg p-4 py-2 max-w-xs break-words ${'bg-gray-200 text-gray-800 self-start rounded-bl-none'}`}
    >
      {text}
    </div>
  );
};

export const Conversation = () => {
  const { conversation } = useConversationStore();
  const bottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [conversation, scrollToBottom]);

  return (
    <div className="flex flex-col gap-4 h-60 overflow-y-auto border border-gray-600 rounded-md p-4 w-full">
      {conversation.map((msg, idx) => (
        <Buble key={idx} text={msg.content} role={msg.role} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
};
