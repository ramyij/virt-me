// src/app/page.tsx
'use client'; // Keep if HomePage uses client-side features, otherwise remove

import React from 'react';
import Link from 'next/link'; // Import Link for navigation buttons

// --- Placeholder Images (Replace with your actual image URLs) ---
// const BACKGROUND_IMAGE_URL = '/images/background.jpg'; // Example using public folder
const HEADSHOT_IMAGE_URL = '/images/headshot.jpg'; // Example using public folder

// --- Reusable Button Component (Can be moved to its own file) ---
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  href?: string; // Add href for linking
  icon?: React.ReactNode; // Add icon prop
}

const Button: React.FC<ButtonProps> = ({ children, className, variant = 'primary', href, icon, ...props }) => {
  const baseStyle = "inline-block px-6 py-2 rounded-full font-semibold transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 shadow-md text-center";
  const primaryStyle = "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500";
  const secondaryStyle = "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400";

  const combinedClassName = `${baseStyle} inline-flex items-center ${variant === 'primary' ? primaryStyle : secondaryStyle} ${className}`;

  // Check if the link is external
  const isExternal = href && (href.startsWith('http://') || href.startsWith('https://'));

  // If href is provided, render a Next.js Link or a standard <a> tag
  if (href) {
    if (isExternal) {
      // Use a standard <a> tag for external links
      return (
        <a
          href={href}
          className={combinedClassName}
          target="_blank" // Open in new tab
          rel="noopener noreferrer" // Security measure
        >
          {icon} {/* Render icon */}
          {children}
        </a>
      );
    } else {
      // Use Next.js Link for internal navigation
      return (
        <Link href={href} className={combinedClassName}>
          {icon} {/* Render icon */}
          {children}
        </Link>
      );
    }
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
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#4b533c]">
      {/* Background Image - Commented Out
      <div
        className="absolute inset-0 z-0 bg-contain bg-top bg-no-repeat"
        style={{ backgroundImage: `url(${BACKGROUND_IMAGE_URL})` }}
      >
        <div className="absolute inset-0 bg-black opacity-30"></div>
      </div>
      */}

      {/* Content - Adjusted Layout */}
      <div className="relative z-10 flex flex-col items-center p-4 md:p-8 max-w-5xl mx-auto w-full">

        {/* Container for Headshot & Text Block (Flex on Medium+ screens) */}
        <div className="flex flex-col md:flex-row items-center w-full">

          {/* Headshot (Larger, positioned left on md+) */}
          <div className="flex-shrink-0 mb-6 md:mb-0 md:mr-[-5rem] z-0">
            <img
              src={HEADSHOT_IMAGE_URL}
              alt="Ramy Jaber Headshot"
              className="w-96 h-96 md:w-112 md:h-112 rounded-full border-4 border-gray-400 shadow-lg object-cover"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.onerror = null; // Prevent infinite loop
                target.src = 'https://placehold.co/150x150/a3a3a3/ffffff?text=RJ'; // Fallback
              }}
            />
          </div>

          {/* Text Block (Overlaps Headshot on md+) */}
          <div className="relative z-10 bg-gray-800/90 text-white py-4 px-6 md:py-6 md:px-8 rounded-lg shadow-xl flex-grow text-center md:text-left md:mt-20">
            <h1 className="text-3xl md:text-4xl font-bold mb-4">Ramy Jaber</h1>
            <p className="text-base md:text-lg mb-6 text-gray-200 leading-relaxed">
              {/* Replace with your actual blurb */}
              Cloud Solution Architect specializing in Large Language Models (LLMs) and performance engineering. Experienced in technical pre-sales, GTM strategy, team leadership, and driving significant business growth through innovative AI solutions. Passionate about bridging the gap between complex technology and real-world business value.
            </p>
          </div>
        </div>

        {/* Buttons - Use Link component via Button's href prop */}
        {/* Container adjusted for icon placeholders */}
        <div className="flex flex-wrap justify-center items-start gap-8 md:gap-12 mt-[10vh] mb-80">

          {/* Chat Button + Icon */}
          <div className="flex flex-col items-center">
            <img src="/images/icon-chat.svg" alt="Interview Me Icon" className="w-48 h-48 mb-2" /> {/* Placeholder Icon */}
            <Button href="/chat" variant="primary">
              Interview Me (AI Chat)
            </Button>
          </div>

          {/* Photography Button + Icon */}
          <div className="flex flex-col items-center">
            <img src="/images/icon-personal.svg" alt="Photography Icon" className="w-24 h-24 mb-16 mt-10 ml-20 mr-25" /> {/* Placeholder Icon */}
            <Button href="https://photos.ramyjaber.com" variant="secondary">
              Photography
            </Button>
          </div>

          {/* Resume Button + Icon (Formerly Career) */}
          <div className="flex flex-col items-center">
            <img src="/images/icon-career.svg" alt="Resume Icon" className="w-24 h-24 mb-14 mt-10 ml-20 mr-25" />
            <Button href="/resume" variant="secondary">
              Resume
            </Button>
          </div>

        </div>
      </div>
    </div>
  );
};
