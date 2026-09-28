'use client';

import React, { useState } from 'react';
import { X, Mail, Lock, User, Building, Sparkles, Zap } from 'lucide-react';
import { api } from '../api/client';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [mode, setMode] = useState<'register' | 'login'>('register');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [orgName, setOrgName] = useState('My Organization');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'register') {
        await api.register({
          email,
          password,
          full_name: fullName,
          organization_name: orgName || undefined,
        });
      } else {
        await api.login(email, password);
      }
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async () => {
    setLoading(true);
    setError('');
    try {
      const demoEmail = `demo_${Date.now()}@projectscope.ai`;
      await api.register({
        email: demoEmail,
        password: 'DemoPass123',
        full_name: 'Demo User',
        organization_name: 'Demo Organization',
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Demo login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center overflow-y-auto bg-slate-950/55 p-3 backdrop-blur-sm sm:p-5">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-modal-title"
        className="my-auto w-full max-w-sm overflow-hidden rounded-2xl border border-white/70 bg-white shadow-[0_24px_80px_-24px_rgba(15,23,42,0.55)]"
      >
        <div className="h-1 bg-gradient-to-r from-sky-500 via-cyan-400 to-indigo-500" />
        <div className="px-5 pb-4 pt-5">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-sky-50 text-sky-600">
                <Sparkles size={18} />
              </div>
              <div>
                <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-sky-700">
                  ProjectScope AI
                </p>
                <h2 id="auth-modal-title" className="mt-1 text-lg font-bold tracking-tight text-slate-900">
              {mode === 'register' ? 'Create Account' : 'Welcome Back'}
                </h2>
                <p className="mt-0.5 text-xs text-slate-500">
              {mode === 'register'
                  ? 'Set up your workspace in seconds.'
                  : 'Sign in to pick up where you left off.'}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              aria-label="Close sign in dialog"
              className="rounded-lg p-1.5 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        <div className="mx-5 flex rounded-xl bg-slate-100 p-1">
          {(['login', 'register'] as const).map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => {
                setMode(option);
                setError('');
              }}
              aria-pressed={mode === option}
              className={`flex-1 rounded-lg px-3 py-2 text-xs font-semibold transition ${
                mode === option
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {option === 'login' ? 'Sign in' : 'Create account'}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="space-y-3.5 px-5 pb-5 pt-4">
          <button
            type="button"
            onClick={handleQuickDemo}
            disabled={loading}
            className="flex w-full items-center justify-center gap-2 rounded-xl border border-sky-200 bg-sky-50/80 px-3 py-2.5 text-xs font-semibold text-sky-800 transition hover:border-sky-300 hover:bg-sky-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Zap size={15} className="fill-sky-500 text-sky-500" />
            Try a demo workspace
          </button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-white px-3 text-[11px] text-slate-400">or use your email</span>
            </div>
          </div>

          {error && (
            <div role="alert" className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2.5 text-xs text-rose-700">
              {error}
            </div>
          )}

          {mode === 'register' && (
            <>
              <div>
                <label className="mb-1 block text-xs font-semibold text-slate-700">
                  Full Name
                </label>
                <div className="relative">
                  <User
                    size={16}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    placeholder="Jane Doe"
                    autoComplete="name"
                    className="w-full rounded-lg border border-slate-200 bg-slate-50/70 py-2.5 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-100"
                  />
                </div>
              </div>

              <div>
                <label className="mb-1 block text-xs font-semibold text-slate-700">
                  Organization
                </label>
                <div className="relative">
                  <Building
                    size={16}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                  />
                  <input
                    type="text"
                    value={orgName}
                    onChange={(e) => setOrgName(e.target.value)}
                    placeholder="Acme Inc"
                    autoComplete="organization"
                    className="w-full rounded-lg border border-slate-200 bg-slate-50/70 py-2.5 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-100"
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <label className="mb-1 block text-xs font-semibold text-slate-700">
              Email
            </label>
            <div className="relative">
              <Mail
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                autoComplete="email"
                className="w-full rounded-lg border border-slate-200 bg-slate-50/70 py-2.5 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-100"
              />
            </div>
          </div>

          <div>
            <label className="mb-1 block text-xs font-semibold text-slate-700">
              Password
            </label>
            <div className="relative">
              <Lock
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={mode === 'register' ? 8 : undefined}
                placeholder={mode === 'register' ? 'At least 8 characters' : 'Enter your password'}
                autoComplete={mode === 'register' ? 'new-password' : 'current-password'}
                className="w-full rounded-lg border border-slate-200 bg-slate-50/70 py-2.5 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-sky-400 focus:bg-white focus:ring-4 focus:ring-sky-100"
              />
            </div>
            {mode === 'register' && (
              <p className="mt-1 text-[10px] text-slate-400">
                Use uppercase, lowercase, and at least one digit.
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="flex w-full items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700 focus:outline-none focus:ring-4 focus:ring-sky-100 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : mode === 'register' ? (
              'Create Account'
            ) : (
              'Sign In'
            )}
          </button>

        </form>
      </div>
    </div>
  );
};