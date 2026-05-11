"use client";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const topics = [
    { name: "History of Mohenjo-daro", icon: "📜" },
    { name: "City Architecture", icon: "🏗️" },
    { name: "Discovery & Excavations", icon: "🔍" },
    { name: "Daily Life & Culture", icon: "👥" },
    { name: "Famous Artifacts", icon: "🏺" },
    { name: "Drainage System", icon: "💧" },
    { name: "Decline & Abandonment", icon: "📉" },
    { name: "Preservation Efforts", icon: "🛡️" },
    { name: "Tourism Information", icon: "🗺️" },
  ];

  return (
    <>
      <div
        className={`fixed inset-0 bg-black/50 z-40 md:hidden transition-opacity duration-300 ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
      />

      <aside
        className={`fixed md:left-0 top-0 h-full w-80 bg-white border-r border-sand-200 z-50 transform transition-transform duration-300 ease-out ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0 overflow-y-auto`}
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-serif font-bold text-sand-800">About</h2>
              <p className="text-xs text-sand-500 mt-1">Mohenjo-daro AI Chatbot</p>
            </div>
            <button
              onClick={onClose}
              className="md:hidden p-2 hover:bg-sand-100 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5 text-sand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="bg-gradient-to-br from-sand-100 to-sand-50 rounded-xl p-4 mb-6 border border-sand-200">
            <div className="flex items-start gap-3">
              <img src="/logo.png" alt="logo" className="w-10 h-10 object-contain flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-sand-800 text-sm">Mohenjo-daro</h3>
                <p className="text-xs text-sand-600 leading-relaxed mt-1">
                  Mound of the Dead Men was one of the largest urban settlements of the ancient 
                  Indus Valley Civilization, flourishing from approximately 2500-1900 BCE.
                </p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-sand-700 mb-3">Topics You Can Ask About</h3>
            <div className="space-y-1">
              {topics.map((topic) => (
                <button
                  key={topic.name}
                  className="w-full text-left px-3 py-2.5 rounded-lg text-sm text-sand-600 hover:bg-sand-50 hover:text-sand-800 transition-all duration-200 flex items-center gap-2"
                >
                  <span>{topic.icon}</span>
                  <span>{topic.name}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-sand-200">
            <div className="flex items-center gap-2 text-xs text-sand-400">
              <span className="w-2 h-2 bg-emerald-500 rounded-full" />
              <span>Powered by Hugging Face API</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
