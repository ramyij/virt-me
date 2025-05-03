// src/app/chat/page.tsx
'use client'; // Required if ChatInterface uses client-side hooks

// Assuming your ChatInterface component is in src/components/
// Adjust the import path if necessary
import ChatInterface from '@/components/ChatInterface';
import React from 'react';

export default function ChatPage() {
  return (
    <div className="p-10 md:p-10 max-w-full mx-auto bg-[#4b533c] min-h-screen flex flex-col">
      <ChatInterface />
      {/* Footer */}
      <footer style={{ marginTop: 'auto', textAlign: 'center', fontSize: '0.9rem', color: 'white' }}>
        <p>
          Check out the project on {''}
          <a
            href="https://www.github.com/ramyj"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: 'white', textDecoration: 'underline' }}
          >
            GitHub
          </a>.
        </p>
      </footer>
    </div>
  );
}
