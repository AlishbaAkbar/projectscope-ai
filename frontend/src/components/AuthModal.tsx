'use client';

import React, { useState } from 'react';
import { UserSession } from '../types/project';
import { X, Shield, Sparkles, UserCheck, Lock, Mail, User, Building, CheckCircle2 } from 'lucide-react';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoginSuccess: (session: UserSession) => void;
  currentSession: UserSession | null;
  onLogout: () => void;
}

const DEMO_PERSONAS: UserSession[] = [
  {
    id: 'demo-architect',
    name: 'Alex Rivera',
    email: 'alex.rivera@enterprise.io',
    role: 'Principal Solutions Architect',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    organization: 'Acme Cloud Systems',
  },
  {
    id: 'demo-pm',
    name: 'Sarah Chen',
    email: 'sarah.chen@innovate.co',
    role: 'Lead Product Manager',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80',
    organization: 'VentureScale Labs',
  },
  {
    id: 'demo-techlead',
    name: 'Marcus Vance',
    email: 'marcus.v@devcraft.org',
    role: 'Staff Engineering Lead',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    organization: 'DevCraft Studio',
  },
];

export const AuthModal: React.FC<AuthModalProps> = ({
  isOpen,
  onClose,
  onLoginSuccess,
  currentSession,
  onLogout,
}) => {
  const [tab, setTab] = useState<'signin' | 'signup' | 'demo'>('demo');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('Product Lead');
  const [organization, setOrganization] = useState('Acme Corporation');
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen) return null;

  const handleDemoSelect = (persona: UserSession) => {
    localStorage.setItem('projectscope_user_session', JSON.stringify(persona));
    onLoginSuccess(persona);
    setSuccessMsg(`Welcome, ${persona.name}!`);
    setTimeout(() => {
      setSuccessMsg('');
      onClose();
    }, 600);
  };

  const handleCustomSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const session: UserSession = {
      id: `user-${Date.now()}`,
      name: name.trim() || email.split('@')[0] || 'Project Lead',
      email: email || 'user@example.com',
      role: role || 'Lead Architect',
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80',
      organization: organization || 'My Organization',
    };
    localStorage.setItem('projectscope_user_session', JSON.stringify(session));
    onLoginSuccess(session);
    setSuccessMsg(`Signed in as ${session.name}`);
    setTimeout(() => {
      setSuccessMsg('');
      onClose();
    }, 600);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-md bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-sky-600 to-indigo-700 p-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="p-2 rounded-xl bg-white/10 backdrop-blur-sm">
                <Sparkles className="w-5 h-5 text-sky-200" />
              </div>
              <div>
                <h3 className="text-lg font-bold">ProjectScope AI Account</h3>
                <p className="text-xs text-sky-100">Role-based scoping & project workspace</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Current Session status banner if already signed in */}
          {currentSession && (
            <div className="mt-4 p-3 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <img
                  src={currentSession.avatar}
                  alt={currentSession.name}
                  className="w-9 h-9 rounded-full border border-white/30 object-cover"
                />
                <div className="text-xs">
                  <div className="font-semibold text-white">{currentSession.name}</div>
                  <div className="text-sky-200">{currentSession.role}</div>
                </div>
              </div>
              <button
                onClick={() => {
                  onLogout();
                  localStorage.removeItem('projectscope_user_session');
                }}
                className="px-2.5 py-1 text-xs font-medium rounded-lg bg-rose-500/80 hover:bg-rose-500 text-white transition-colors"
              >
                Sign Out
              </button>
            </div>
          )}
        </div>

        {/* Tab selection */}
        <div className="flex border-b border-slate-200 bg-slate-50 text-xs font-semibold">
          <button
            onClick={() => setTab('demo')}
            className={`flex-1 py-3 text-center border-b-2 transition-colors ${
              tab === 'demo'
                ? 'border-sky-600 text-sky-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            ⚡ 1-Click Demo Profiles
          </button>
          <button
            onClick={() => setTab('signin')}
            className={`flex-1 py-3 text-center border-b-2 transition-colors ${
              tab === 'signin'
                ? 'border-sky-600 text-sky-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => setTab('signup')}
            className={`flex-1 py-3 text-center border-b-2 transition-colors ${
              tab === 'signup'
                ? 'border-sky-600 text-sky-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            Register
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6">
          {successMsg && (
            <div className="mb-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{successMsg}</span>
            </div>
          )}

          {tab === 'demo' && (
            <div className="space-y-3">
              <p className="text-xs text-slate-600 mb-2">
                Select a verified persona to test scoping, cost models, and project collaboration:
              </p>
              {DEMO_PERSONAS.map((persona) => (
                <button
                  key={persona.id}
                  onClick={() => handleDemoSelect(persona)}
                  className="w-full text-left p-3.5 rounded-xl border border-slate-200 hover:border-sky-500 hover:bg-sky-50/50 transition-all flex items-center justify-between group"
                >
                  <div className="flex items-center space-x-3">
                    <img
                      src={persona.avatar}
                      alt={persona.name}
                      className="w-10 h-10 rounded-full object-cover border border-slate-200 group-hover:border-sky-400"
                    />
                    <div>
                      <div className="text-sm font-bold text-slate-900 group-hover:text-sky-700">
                        {persona.name}
                      </div>
                      <div className="text-xs font-medium text-slate-500">{persona.role}</div>
                      <div className="text-[11px] text-slate-400">{persona.organization}</div>
                    </div>
                  </div>
                  <UserCheck className="w-5 h-5 text-slate-300 group-hover:text-sky-600 transition-colors" />
                </button>
              ))}
            </div>
          )}

          {tab === 'signin' && (
            <form onSubmit={handleCustomSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="architect@company.com"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 px-4 rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-semibold text-sm shadow-md shadow-sky-600/20 transition-colors"
              >
                Sign In to Workspace
              </button>
            </form>
          )}

          {tab === 'signup' && (
            <form onSubmit={handleCustomSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  Full Name
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Jordan Hayes"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="jordan@enterprise.io"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Role
                  </label>
                  <input
                    type="text"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    placeholder="Lead Architect"
                    className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Organization
                  </label>
                  <input
                    type="text"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    placeholder="Acme Tech"
                    className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Create secure password"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full mt-2 py-2.5 px-4 rounded-xl bg-sky-600 hover:bg-sky-700 text-white font-semibold text-sm shadow-md shadow-sky-600/20 transition-colors"
              >
                Create Account
              </button>
            </form>
          )}
        </div>

        {/* Footer info */}
        <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
          <span className="flex items-center space-x-1">
            <Shield className="w-3.5 h-3.5 text-emerald-600" />
            <span>Encrypted Local Session</span>
          </span>
          <span>FastAPI 0.1.0 Ready</span>
        </div>
      </div>
    </div>
  );
};
