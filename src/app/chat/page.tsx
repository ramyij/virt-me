// src/app/chat/page.tsx
'use client'; // Required if ChatInterface uses client-side hooks

// Assuming your ChatInterface component is in src/components/
// Adjust the import path if necessary
import ChatInterface from '@/components/ChatInterface';
import React from 'react';

export default function ChatPage() {
  return (
    // Add padding and max-width for consistent layout, adjust as needed
    <div className="p-10 md:p-10 max-w-full mx-auto bg-[#4b533c]">
      <ChatInterface />
    </div>
  );
}
