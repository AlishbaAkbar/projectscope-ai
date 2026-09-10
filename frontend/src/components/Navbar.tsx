'use client';

import React from 'react';
import { Sparkles, Terminal, Layers, LayoutDashboard, Compass, Database, User, LogOut, ChevronDown } from 'lucide-react';
import { UserSession } from '../types/project';

interface NavbarProps {
  activeView: 'landing' | 'dashboard' | 'studio' | 'knowledge';
  onNavigate: (view: 'landing' | 'dashboard' | 'studio' | 'knowledge') => void;
  activeProjectName?: string | null;
  currentSession: UserSession | null;
  onOpenAuth: () => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeView,
  onNavigate,
  activeProjectName,
  currentSession,
  onOpenAuth,
  onLogout,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/85 backdrop-blur-md transition-all">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center space-x-6">
          <button
            onClick={() => onNavigate('landing')}
            className="flex items-center space-x-3 text-left group cursor-pointer"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 via-blue-600 to-indigo-700 text-white shadow-md shadow-sky-500/25 group-hover:scale-105 transition-transform">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-black tracking-tight text-slate-900">
                  ProjectScope <span className="text-sky-600">AI</span>
                </span>
                <span className="inline-flex items-center rounded-md bg-sky-50 px-2 py-0.5 text-[11px] font-semibold text-sky-700 border border-sky-200">
                  v2.0
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">AI Architecture & Software Scoping Engine</p>
            </div>
          </button>

          {/* Primary Navigation Pills */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-100/80 p-1 rounded-xl border border-slate-200/60 text-xs font-semibold">
            <button
              onClick={() => onNavigate('landing')}
              className={`px-3.5 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 ${
                activeView === 'landing'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <Compass className="w-3.5 h-3.5 text-sky-600" />
              <span>Explore</span>
            </button>

            <button
              onClick={() => onNavigate('dashboard')}
              className={`px-3.5 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 ${
                activeView === 'dashboard'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5 text-indigo-600" />
              <span>Dashboard</span>
            </button>

            <button
              onClick={() => onNavigate('studio')}
              className={`px-3.5 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 ${
                activeView === 'studio'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-blue-600" />
              <span>Scoping Studio</span>
              {activeProjectName && (
                <span className="max-w-[120px] truncate text-[10px] font-medium bg-sky-100 text-sky-800 px-1.5 py-0.5 rounded ml-1">
                  {activeProjectName}
                </span>
              )}
            </button>
          </nav>
        </div>

        {/* Right Side / Actions & Auth */}
        <div className="flex items-center space-x-3">
          {/* API Status Indicator */}
          <div className="hidden lg:flex items-center space-x-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 border border-emerald-200">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>API Online :8000</span>
          </div>

          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="hidden sm:inline-flex items-center space-x-1.5 rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-sm"
          >
            <Terminal className="h-3.5 w-3.5 text-slate-500" />
            <span>FastAPI Docs</span>
          </a>

          {/* User Account / Profile Badge */}
          {currentSession ? (
            <div className="flex items-center space-x-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl p-1.5 transition-all">
              <img
                src={currentSession.avatar}
                alt={currentSession.name}
                className="w-7 h-7 rounded-lg object-cover border border-slate-200"
              />
              <div className="hidden sm:block text-left text-xs pr-1">
                <div className="font-semibold text-slate-900 leading-tight truncate max-w-[120px]">
                  {currentSession.name}
                </div>
                <div className="text-[10px] text-slate-500 truncate max-w-[120px]">{currentSession.role}</div>
              </div>
              <button
                onClick={onOpenAuth}
                title="Switch Profile"
                className="p-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-200/60"
              >
                <ChevronDown className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="inline-flex items-center space-x-1.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-700 hover:to-blue-700 px-3.5 py-1.5 text-xs font-semibold text-white shadow-md shadow-sky-600/20 transition-all"
            >
              <User className="h-3.5 w-3.5" />
              <span>Sign In / Demo</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
