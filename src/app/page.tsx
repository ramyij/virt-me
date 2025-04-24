// src/app/page.tsx
'use client'; // Keep if HomePage uses client-side features, otherwise remove

import React from 'react';
import Link from 'next/link'; // Import Link for navigation buttons

// --- Placeholder Images (Replace with your actual image URLs) ---
const BACKGROUND_IMAGE_URL = '/images/background.jpg'; // Example using public folder
const HEADSHOT_IMAGE_URL = '/images/headshot.jpg'; // Example using public folder

// --- Reusable Button Component (Can be moved to its own file) ---
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  href?: string; // Add href for linking
}

const Button: React.FC<ButtonProps> = ({ children, className, variant = 'primary', href, ...props }) => {
  const baseStyle = "inline-block px-6 py-2 rounded-full font-semibold transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 shadow-md text-center";
  const primaryStyle = "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500";
  const secondaryStyle = "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400";

  // Combine base, variant, and any additional classes
  const combinedClassName = `${baseStyle} ${variant === 'primary' ? primaryStyle : secondaryStyle} ${className}`;

  // If href is provided, render a Next.js Link component
  if (href) {
    return (
      // Remove legacyBehavior. Link now renders its own <a> tag.
      // Apply the combined styles directly to the Link component.
      <Link href={href} className={combinedClassName}>
        {children}
      </Link>
    );
  }

  // Fallback to regular button if no href
  return (
    <button
      className={combinedClassName}
      {...props} // Pass other button props like onClick, disabled, etc.
    >
      {children}
    </button>
  );
};


// --- Home Page Component Definition ---
// This is the main component exported from src/app/page.tsx
export default function HomePage() {
  return (
    // Using min-h-screen ensures it takes at least the full viewport height
    <div className="relative min-h-screen flex items-center justify-center text-white overflow-hidden">
      {/* Background Image */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${BACKGROUND_IMAGE_URL})` }}
      >
        {/* Overlay for better text readability */}
        <div className="absolute inset-0 bg-black opacity-30"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center p-8 max-w-3xl mx-auto">
        {/* Headshot */}
        <img
          src={HEADSHOT_IMAGE_URL}
          alt="Ramy Jaber Headshot"
          className="w-36 h-36 rounded-full mb-6 border-4 border-gray-400 shadow-lg object-cover" 
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.onerror = null; // Prevent infinite loop
            target.src = 'https://placehold.co/150x150/a3a3a3/ffffff?text=RJ'; // Fallback
          }}
        />

        {/* Blurb */}
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Ramy Jaber</h1>
        <p className="text-lg md:text-xl mb-8 text-gray-200 leading-relaxed">
          {/* Replace with your actual blurb */}
          Cloud Solution Architect specializing in Large Language Models (LLMs) and performance engineering. Experienced in technical pre-sales, GTM strategy, team leadership, and driving significant business growth through innovative AI solutions. Passionate about bridging the gap between complex technology and real-world business value.
        </p>

        {/* Buttons - Use Link component via Button's href prop */}
        <div className="flex flex-wrap justify-center gap-4">
          <Button href="/chat" variant="primary">
            Interview Me (AI Chat)
          </Button>
          <Button href="/personal" variant="secondary">
            Personal
          </Button>
          <Button href="/career" variant="secondary">
            Career
          </Button>
        </div>
      </div>
    </div>
  );
};
