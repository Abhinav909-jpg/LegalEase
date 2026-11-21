import React from 'react'
import { ShieldCheck, UploadCloud, MessageSquare, Compass, Home, LayoutDashboard } from 'lucide-react'

export default function Navbar({ activePage, setActivePage, onOpenUpload }) {
  return (
    <nav className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div 
            onClick={() => setActivePage('home')}
            className="flex items-center gap-2.5 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-lg font-extrabold text-slate-900 tracking-tight">Legal<span className="text-brand-600">Ease</span></span>
              </div>
              <p className="text-[10px] text-slate-400 font-medium">National Scheme & Scholarship Navigator</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-1">
            <button
              onClick={() => setActivePage('home')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors ${
                activePage === 'home'
                  ? 'bg-brand-50 text-brand-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Home className="w-4 h-4" />
              <span>Home</span>
            </button>

            <button
              onClick={() => setActivePage('dashboard')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors ${
                activePage === 'dashboard'
                  ? 'bg-brand-50 text-brand-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard & Schemes</span>
            </button>

            <button
              onClick={() => setActivePage('assistant')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors ${
                activePage === 'assistant'
                  ? 'bg-brand-50 text-brand-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <MessageSquare className="w-4 h-4 text-brand-600" />
              <span>AI Assistant</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            </button>

            <button
              onClick={() => setActivePage('eligibility')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors ${
                activePage === 'eligibility'
                  ? 'bg-brand-50 text-brand-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Compass className="w-4 h-4 text-indigo-600" />
              <span>Eligibility Checker</span>
            </button>
          </div>

          {/* Right Action Buttons */}
          <div className="flex items-center gap-2.5">
            <button
              onClick={onOpenUpload}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-brand-700 bg-slate-100 hover:bg-brand-50 rounded-lg border border-slate-200 transition-colors"
              title="Upload new government guideline PDF"
            >
              <UploadCloud className="w-3.5 h-3.5 text-brand-600" />
              <span className="hidden sm:inline">Upload PDF</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
