import React from 'react';
import Link from 'next/link'; // Optional: If needed for other links

// Updated function name
export default function ResumePage() {
  return (
    <div className="container mx-auto px-4 py-8 bg-[#4b533c] text-white min-h-screen">
      {/* Updated title */}
      <h1 className="text-3xl font-bold mb-6">Resume</h1>

      <p className="mb-4">
        You can view or download my resume below.
      </p>

      <div className="w-full h-[200vh] border rounded-lg overflow-hidden shadow-md bg-white">
        <iframe
          src="/images/resume.pdf#view=FitH"
          title="Ramy Jaber Resume" // Title attribute remains relevant
          width="100%"
          height="100%"
          style={{ border: 'none' }}
        />
      </div>
      <p className="mt-4 text-sm text-gray-300">
        Having trouble viewing the resume? <a href="/images/resume.pdf" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">Download it directly</a>.
      </p>

      {/* Placeholder for any future additional content */}

    </div>
  );
} 