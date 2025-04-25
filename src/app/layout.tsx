// src/app/layout.tsx
import React from 'react';
import './globals.css'; // Make sure you have a global CSS file for base styles/Tailwind imports
import Link from 'next/link'; // Use Next.js Link for client-side navigation
import { Inter } from 'next/font/google'; // Import the Inter font

// Instantiate the font
const inter = Inter({ subsets: ['latin'] });

// --- Navigation Bar Component (Defined within Layout) ---
// Note: You could also move Navbar to its own component file and import it
const Navbar: React.FC = () => {
  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Chat', href: '/chat' },
    { name: 'Photography', href: 'https://photos.ramyjaber.com' },
    { name: 'Resume', href: '/resume' },
  ];

  // In a real app router setup, determining active state might use usePathname hook
  // For simplicity here, we won't highlight the active link, but you can add that logic
  const getLinkStyle = () => { // Simplified style logic
    const base = "px-3 py-2 rounded-md text-sm transition duration-150 ease-in-out cursor-pointer";
    // const active = "bg-gray-900 text-white"; // Example active style
    const inactive = "text-white hover:bg-gray-700 hover:text-white font-normal"; // Changed font-medium to font-normal
    // return `${base} ${isActive ? active : inactive}`; // Use this line if you implement active state later
     return `${base} ${inactive}`; // Default to inactive for now
  };

  return (
    <nav className={`${inter.className} bg-gray-800 shadow-lg sticky top-0 z-50`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Adjusted flex container: Nav links left, Social links right */}
        <div className="flex items-center justify-between h-16">
          {/* Navigation Links (Moved Left) */}
          <div className="flex items-center">
            <div className="flex items-baseline space-x-4">
              {navItems.map((item) => {
                const isExternal = item.href.startsWith('http');
                const linkStyle = getLinkStyle();

                if (isExternal) {
                  return (
                    <a
                      key={item.name}
                      href={item.href}
                      className={linkStyle}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {item.name}
                    </a>
                  );
                } else {
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={linkStyle}
                    >
                      {item.name}
                    </Link>
                  );
                }
              })}
            </div>
          </div>

          {/* Social Media Links (Added Right) */}
          <div className="flex items-center space-x-4">
            <a href="https://linkedin.com/in/ramyj" target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white">
              {/* Replace with LinkedIn Icon SVG or Component */}
              <span className="text-sm">LinkedIn</span>
            </a>
            <a href="https://github.com/ramyij" target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white">
              {/* Replace with GitHub Icon SVG or Component */}
              <span className="text-sm">GitHub</span>
            </a>
          </div>

          {/* Mobile Menu Button Placeholder (Keep or implement) */}
          {/* <div className="-mr-2 flex md:hidden"> ... Mobile button ... </div> */}
        </div>
      </div>
    </nav>
  );
};


// --- Root Layout Component ---
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      {/* Ensure no extra whitespace directly within the <head> tags */}
      <head>
        {/* Valid head elements */}
        <title>Ramy Jaber - Virtual Me</title>
        <meta name="description" content="Personal website and AI chat interface for Ramy Jaber" />
        <link rel="icon" href="/favicon.ico" />
        {/* Add other meta/link tags directly adjacent if needed */}
      </head>
      {/* Apply the font className and pale blue background to the body */}
      <body className={`${inter.className} bg-sky-100`}> {/* Changed bg-gray-50 to bg-sky-100 */}
        {/* Navbar will be displayed on all pages */}
        <Navbar />
        {/* Page content will be rendered here */}
        <main>{children}</main>
        {/* You can add a Footer component here if needed */}
      </body>
    </html>
  );
}
