// src/components/ChatInterface.tsx
'use client'; // Required for components using hooks like useState, useEffect, useChat

import React from 'react';
// Import the useChat hook from the Vercel AI SDK (ensure you have @ai-sdk/react installed)
// npm install @ai-sdk/react or yarn add @ai-sdk/react
import { useChat } from '@ai-sdk/react';

export default function ChatInterface() {
  // Configure the useChat hook
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    // Point the hook to your backend API route
    api: '/api/chat',
    maxSteps: 3,
    // Optional: Initial messages or other configurations
    // initialMessages: [ { id: 'initial', role: 'system', content: 'Ask me about my experience!' } ],
    // onError: (err) => { console.error("Chat error:", err); /* Handle errors */ }
  });

  return (
    <div className="flex flex-col h-screen max-h-[90vh] w-full max-w-2xl mx-auto bg-gray-500 rounded-lg shadow-xl overflow-hidden">
      {/* Message display area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#dbdfd3]">
        {messages.length > 0 ? (
          messages.map(m => (
            <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow ${
                  m.role === 'user'
                    ? 'bg-[#4f8f24] text-white'
                    : 'bg-[#f1faeb] text-gray-800'
                }`}
              >
                <span className="font-semibold capitalize mr-2">
                  {m.role === 'assistant' ? 'Ramy' : m.role}:
                </span>
                {/* Handle potential line breaks in messages */}
                {m.content.split('\n').map((line, index) => (
                    <React.Fragment key={index}>
                        {line}
                        <br />
                    </React.Fragment>
                ))}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-l text-gray-800">
            Start the interview by asking me a question about my professional or personal background!
          </div>
        )}
        {/* Display loading indicator */}
        {isLoading && (
            <div className="flex justify-start">
                 <div className="px-4 py-2 rounded-lg shadow bg-gray-200 text-gray-800 animate-pulse">
                    Thinking...
                 </div>
            </div>
        )}
        {/* Display error messages */}
        {error && (
             <div className="flex justify-start">
                 <div className="px-4 py-2 rounded-lg shadow bg-red-100 text-red-700">
                    <span className="font-semibold">Error:</span> {error.message || "An unknown error occurred."}
                 </div>
             </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={input}
            placeholder="Hi, how are you doing today?"
            onChange={handleInputChange}
            disabled={isLoading} // Disable input while loading
          />
          <button
            type="submit"
            className="px-6 py-2 bg-[#4f8f24] text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            disabled={isLoading || !input.trim()} // Disable if loading or input is empty/whitespace
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}