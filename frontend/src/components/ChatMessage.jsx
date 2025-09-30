import React from 'react';
import { Bot, User } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`flex gap-2 ${isAssistant ? '' : 'flex-row-reverse'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isAssistant ? 'bg-primary-100' : 'bg-gray-200'
      }`}>
        {isAssistant ? (
          <Bot className="w-4 h-4 text-primary-600" />
        ) : (
          <User className="w-4 h-4 text-gray-600" />
        )}
      </div>
      <div className={`flex-1 ${isAssistant ? 'text-left' : 'text-right'}`}>
        <div className={`inline-block px-3 py-2 rounded-lg text-sm ${
          isAssistant ? 'bg-gray-100 text-gray-900' : 'bg-primary-600 text-white'
        }`}>
          {message.content}
        </div>
        <div className="text-xs text-gray-400 mt-1">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;