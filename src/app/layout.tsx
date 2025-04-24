// src/app/layout.tsx
import React from 'react';
import './globals.css'; // Make sure you have a global CSS file for base styles/Tailwind imports
import Link from 'next/link'; // Use Next.js Link for client-side navigation

// --- Navigation Bar Component (Defined within Layout) ---
// Note: You could also move Navbar to its own component file and import it
const Navbar: React.FC = () => {
  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Chat', href: '/chat' },
    { name: 'Personal', href: '/personal' },
    { name: 'Career', href: '/career' },
  ];

  // In a real app router setup, determining active state might use usePathname hook
  // For simplicity here, we won't highlight the active link, but you can add that logic
  // const getLinkStyle = () => { // Simplified style logic
  //   const base = "px-3 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out cursor-pointer";
  //   // const active = "bg-gray-900 text-white"; // Example active style
  //   const inactive = "text-gray-300 hover:bg-gray-700 hover:text-white";
  //   // return `${base} ${isActive ? active : inactive}`; // Use this line if you implement active state later
  //    return `${base} ${inactive}`; // Default to inactive for now
  // };

  return (
    <nav className="bg-gray-800 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
             {/* Link the name back to the homepage */}
             <Link href="/" className="text-white font-bold text-xl mr-6">
                Ramy Jaber
             </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  // className={getLinkStyle()} // Pass active state logic here if needed
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
          {/* TODO: Add mobile menu button here if needed */}
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
      <body className="bg-gray-50"> {/* Apply default background to body */}
        {/* Navbar will be displayed on all pages */}
        <Navbar />
        {/* Page content will be rendered here */}
        <main>{children}</main>
        {/* You can add a Footer component here if needed */}
      </body>
    </html>
  );
}
