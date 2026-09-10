'use client';

import React, { useState } from 'react';
import {
  X,
  Sparkles,
  Layers,
  Smartphone,
  Globe,
  Server,
  Monitor,
  CheckCircle2,
  DollarSign,
  Calendar,
  Tag,
  Wand2,
} from 'lucide-react';
import { ProjectCreatePayload } from '../types/project';

interface CreateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (payload: ProjectCreatePayload, runAnalyzeImmediately: boolean) => Promise<void>;
  isLoading: boolean;
  initialData?: ProjectCreatePayload | null;
}

const TEMPLATES = [
  {
    name: 'E-Commerce Marketplace',
    platform: 'web',
    type: 'e-commerce',
    desc: 'Multi-vendor e-commerce platform where customers can browse catalogs, add items to cart, pay with credit card/Stripe, and track orders. Vendors manage their product inventory and sales analytics.',
  },
  {
    name: 'Telemedicine Consultation Platform',
    platform: 'mobile',
    type: 'healthcare',
    desc: 'HIPAA-compliant mobile healthcare app where patients book appointments, conduct encrypted video calls with certified doctors, view e-prescriptions, and securely manage health records.',
  },
  {
    name: 'Live Campus Transit & Bus Tracker',
    platform: 'mobile',
    type: 'transportation',
    desc: 'Live transit application where university students view real-time bus locations on a map, receive route delay alerts, see dynamic arrival ETAs, and report service issues to dispatchers.',
  },
  {
    name: 'B2B Workflow & Sales CRM',
    platform: 'web',
    type: 'saas',
    desc: 'Cloud-based sales pipeline CRM featuring lead tracking, automated deal progression, team task management, email notifications, role-based permissions, and PDF export reports.',
  },
];

export const CreateProjectModal: React.FC<CreateProjectModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  isLoading,
  initialData,
}) => {
  const [name, setName] = useState(initialData?.name || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [platform, setPlatform] = useState(initialData?.platform || 'web');
  const [projectType, setProjectType] = useState(initialData?.type || 'e-commerce');
  const [targetUsers, setTargetUsers] = useState('Customer, Admin');
  const [budget, setBudget] = useState('25000');
  const [timelineWeeks, setTimelineWeeks] = useState('8');
  const [constraints, setConstraints] = useState('Cloud-native, PostgreSQL database');
  const [autoAnalyze, setAutoAnalyze] = useState(true);

  if (!isOpen) return null;

  const handleApplyTemplate = (tpl: (typeof TEMPLATES)[0]) => {
    setName(tpl.name);
    setDescription(tpl.desc);
    setPlatform(tpl.platform);
    setProjectType(tpl.type);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !description.trim()) return;

    // Combine user hints into description to enrich AI prompt engine
    const richDescription = `${description.trim()}\n\n[Project Metadata]\nPlatform: ${platform}\nCategory: ${projectType}\nTarget Personas: ${targetUsers}\nEstimated Budget Target: $${budget}\nTarget Delivery Window: ${timelineWeeks} weeks\nTechnical Preferences: ${constraints}`;

    await onSubmit(
      {
        name: name.trim(),
        description: richDescription,
        platform,
        type: projectType,
      },
      autoAnalyze
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl my-8 bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-sky-600 via-blue-600 to-indigo-700 p-6 text-white flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-white/10 backdrop-blur-sm">
              <Wand2 className="w-5 h-5 text-sky-200" />
            </div>
            <div>
              <h3 className="text-lg font-bold">New Project Scope Brief</h3>
              <p className="text-xs text-sky-100">
                Define your software specifications for instant AI requirement decomposition
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            disabled={isLoading}
            className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Container */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5 max-h-[80vh] overflow-y-auto">
          {/* Quick template bar */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-1">
              <Sparkles className="w-3.5 h-3.5 text-sky-500" />
              <span>Quick-Start Presets (Click to autofill)</span>
            </label>
            <div className="flex flex-wrap gap-2">
              {TEMPLATES.map((tpl, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => handleApplyTemplate(tpl)}
                  className="px-2.5 py-1 text-xs rounded-lg border border-slate-200 bg-slate-50 hover:bg-sky-50 hover:border-sky-300 text-slate-700 hover:text-sky-700 font-medium transition-colors"
                >
                  {tpl.name}
                </button>
              ))}
            </div>
          </div>

          {/* Project Name */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Project Name <span className="text-rose-500">*</span>
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. NextGen Telehealth Mobile App"
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition-all"
            />
          </div>

          {/* Platform & Domain Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Target Platform
              </label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option value="web">Web Application (Next.js / React)</option>
                <option value="mobile">Mobile Application (iOS / Android)</option>
                <option value="cross-platform">Cross-Platform (Web & Mobile)</option>
                <option value="cloud">Cloud Backend / REST API</option>
                <option value="desktop">Desktop Software (Electron)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Domain / Industry Category
              </label>
              <select
                value={projectType}
                onChange={(e) => setProjectType(e.target.value)}
                className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option value="e-commerce">E-Commerce & Retail</option>
                <option value="healthcare">Healthcare & Life Sciences</option>
                <option value="fintech">FinTech & Banking</option>
                <option value="transportation">Logistics & Transportation</option>
                <option value="saas">Enterprise B2B SaaS</option>
                <option value="social">Social Media & Community</option>
                <option value="edtech">EdTech & Learning</option>
              </select>
            </div>
          </div>

          {/* Detailed Problem Statement / Idea Description */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                Detailed Project Description & Problem Statement <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-slate-400">{description.length} characters</span>
            </div>
            <textarea
              required
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your software idea in natural language. Mention what users will do, required integrations (e.g. Stripe, Maps, Twilio), admin workflows, and business goals..."
              className="w-full p-3 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent leading-relaxed"
            />
          </div>

          {/* Secondary Parameters (Personas, Budget, Timeline) */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div>
              <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">
                Target Personas
              </label>
              <input
                type="text"
                value={targetUsers}
                onChange={(e) => setTargetUsers(e.target.value)}
                placeholder="User, Admin, Manager"
                className="w-full px-2.5 py-1.5 text-xs rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">
                Target Budget ($)
              </label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder="25000"
                className="w-full px-2.5 py-1.5 text-xs rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">
                Timeline Target (Weeks)
              </label>
              <input
                type="number"
                value={timelineWeeks}
                onChange={(e) => setTimelineWeeks(e.target.value)}
                placeholder="8"
                className="w-full px-2.5 py-1.5 text-xs rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
          </div>

          {/* Technical Preferences / Constraints */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
              Technical Constraints / Preferences
            </label>
            <input
              type="text"
              value={constraints}
              onChange={(e) => setConstraints(e.target.value)}
              placeholder="e.g. AWS Cloud, PostgreSQL, HIPAA Compliance, WebSockets"
              className="w-full px-3.5 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>

          {/* Auto-analyze checkbox */}
          <div className="flex items-center space-x-2.5 pt-1">
            <input
              type="checkbox"
              id="autoAnalyze"
              checked={autoAnalyze}
              onChange={(e) => setAutoAnalyze(e.target.checked)}
              className="w-4 h-4 rounded text-sky-600 focus:ring-sky-500 border-slate-300 cursor-pointer"
            />
            <label htmlFor="autoAnalyze" className="text-xs font-medium text-slate-700 cursor-pointer">
              Automatically trigger AI analysis, task decomposition & ML estimation upon creation
            </label>
          </div>

          {/* Footer Actions */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2.5 text-xs font-semibold rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={isLoading || !name.trim() || !description.trim()}
              className="px-6 py-2.5 text-xs font-bold rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-700 hover:to-blue-700 text-white shadow-md shadow-sky-600/20 disabled:opacity-50 flex items-center space-x-2 transition-all"
            >
              {isLoading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Scoping Project...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>{autoAnalyze ? 'Create & Run AI Analysis' : 'Save Project Draft'}</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
