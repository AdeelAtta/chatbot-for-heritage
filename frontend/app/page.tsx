"use client";

import { useState } from "react";
import ChatInterface from "@/components/ChatInterface";
import Sidebar from "@/components/Sidebar";
import MobileNav from "@/components/MobileNav";

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <main className="flex h-screen bg-sand-50 overflow-hidden">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex-1 flex flex-col w-full md:ml-80 transition-all duration-300">
        <header className="bg-white/80 backdrop-blur-md border-b border-sand-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(true)}
                className="md:hidden p-2 hover:bg-sand-100 rounded-lg transition-colors"
              >
                <svg
                  className="w-6 h-6 text-sand-700"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
              <div className="flex items-center gap-3">
                <span className="text-3xl">🏛️</span>
                <div>
                  <h1 className="text-xl font-serif font-bold text-sand-900">
                    Mohenjo-daro AI
                  </h1>
                  <p className="text-xs text-sand-500">Ancient Indus Valley Civilization</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-medium rounded-full">
                <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                Online
              </span>
            </div>
          </div>
        </header>

        <ChatInterface />
      </div>

      <MobileNav onMenuClick={() => setSidebarOpen(true)} />
    </main>
  );
}
