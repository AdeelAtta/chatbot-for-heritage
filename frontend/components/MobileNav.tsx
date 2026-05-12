"use client";

import { Home, MessageCircle, Menu } from "lucide-react";

interface MobileNavProps {
  onMenuClick: () => void;
}

export default function MobileNav({ onMenuClick }: MobileNavProps) {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 glass border-t border-sand-200/50 z-40">
      <div className="flex items-center justify-around py-3">
        <button className="flex flex-col items-center gap-1 text-primary-600">
          <Home className="w-5 h-5" />
          <span className="text-xs font-medium">Home</span>
        </button>
        <button className="flex flex-col items-center gap-1 text-sand-400">
          <MessageCircle className="w-5 h-5" />
          <span className="text-xs">Chat</span>
        </button>
        <button
          onClick={onMenuClick}
          className="flex flex-col items-center gap-1 text-sand-400"
        >
          <Menu className="w-5 h-5" />
          <span className="text-xs">Menu</span>
        </button>
      </div>
    </nav>
  );
}
