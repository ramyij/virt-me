// src/app/chat/page.tsx
'use client'; // Required if ChatInterface uses client-side hooks

// Assuming your ChatInterface component is in src/components/
// Adjust the import path if necessary
import ChatInterface from '@/components/ChatInterface';
import React from 'react';

export default function ChatPage() {
  return (
    // Add padding and max-width for consistent layout, adjust as needed
    // The overall background color will likely be handled by the layout/global styles
    <div className="p-0 md:p-0 max-w-full mx-auto">
      {/*
        Removed the outer container with bg-white/shadow from the previous version,
        as the ChatInterface component likely handles its own container styling.
        Adjust if your ChatInterface needs an outer wrapper here.
      */}
      <ChatInterface />
    </div>
  );
}

// Placeholder for ChatInterface if you don't have the file yet
// You should replace this with the actual import above once you have the component
/*
const ChatInterface = () => {
  // Your actual useChat hook and UI logic would go here
  return (
    <div className="flex flex-col h-screen max-h-[90vh] w-full max-w-2xl mx-auto bg-white rounded-lg shadow-xl overflow-hidden">
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        <p>Chat messages will appear here...</p>
      </div>
      <div className="border-t border-gray-200 p-4 bg-white">
        <form className="flex items-center space-x-2">
          <input
            className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask me anything..."
          />
          <button
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};
*/
