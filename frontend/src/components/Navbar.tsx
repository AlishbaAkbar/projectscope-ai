import React from 'react';
import { Sparkles, Terminal, Layers } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-blue-700 text-white shadow-md shadow-sky-500/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-bold tracking-tight text-slate-900">
                ProjectScope <span className="text-sky-600">AI</span>
              </span>
              <span className="inline-flex items-center rounded-md bg-sky-50 px-2 py-0.5 text-xs font-semibold text-sky-700 border border-sky-200">
                Week 1 Prototype
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">AI Requirement Analysis & Scoping Engine</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="hidden md:flex items-center space-x-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 border border-emerald-200">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>API Online :8000</span>
          </div>

          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center space-x-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <Terminal className="h-3.5 w-3.5 text-slate-500" />
            <span>FastAPI Docs</span>
          </a>
        </div>
      </div>
    </header>
  );
};
