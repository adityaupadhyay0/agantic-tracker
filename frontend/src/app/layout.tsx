import React from 'react';
import './globals.css';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50 min-h-screen">
        <nav className="border-b border-slate-800 p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold tracking-tight text-indigo-400">CORTEX</h1>
            <div className="space-x-6 text-sm font-medium">
              <a href="/" className="hover:text-indigo-400">Dashboard</a>
              <a href="/marketplace" className="hover:text-indigo-400">Marketplace</a>
              <a href="/trends" className="hover:text-indigo-400">Trends</a>
              <a href="/forecast" className="hover:text-indigo-400">Forecast</a>
              <a href="/transparency" className="hover:text-indigo-400">Transparency</a>
              <a href="/onboarding" className="hover:text-indigo-400">Setup</a>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
