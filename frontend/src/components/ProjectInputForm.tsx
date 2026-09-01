import React, { useState } from 'react';
import { Sparkles, ArrowRight, Lightbulb, Compass, Globe, Smartphone, Laptop, Server } from 'lucide-react';
import { ProjectCreatePayload } from '../types/project';

interface ProjectInputFormProps {
  onSubmit: (payload: ProjectCreatePayload) => Promise<void>;
  isLoading: boolean;
}

const SAMPLE_PROJECTS = [
  {
    label: '🚌 University Transport App',
    name: 'Campus Transit Go',
    platform: 'Mobile',
    description:
      'I want to build a university transport app where students can view buses, track their bus live, receive notifications and report transport issues.',
  },
  {
    label: '🛍️ E-Commerce Store',
    name: 'NovaMart Storefront',
    platform: 'Web',
    description:
      'An online store where customers can browse catalog, add items to cart, checkout with Stripe, and track orders.',
  },
  {
    label: '🍔 Food Delivery Platform',
    name: 'QuickBite Delivery',
    platform: 'Full-stack',
    description:
      'A food delivery application where users can discover local restaurants, order food, and track courier on a live GPS map.',
  },
  {
    label: '🏥 Healthcare Clinic Scheduler',
    name: 'CarePoint Clinic Portal',
    platform: 'Web',
    description:
      'A healthcare appointment system where patients can search doctors, book consultation slots, and review medical history.',
  },
];

export const ProjectInputForm: React.FC<ProjectInputFormProps> = ({ onSubmit, isLoading }) => {
  const [name, setName] = useState('');
  const [platform, setPlatform] = useState('Web');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleApplySample = (sample: typeof SAMPLE_PROJECTS[0]) => {
    setName(sample.name);
    setPlatform(sample.platform);
    setDescription(sample.description);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Please provide a project name.');
      return;
    }
    if (!description.trim() || description.trim().length < 5) {
      setError('Please provide a project description of at least 5 characters.');
      return;
    }

    setError(null);
    try {
      await onSubmit({
        name: name.trim(),
        platform: platform.trim(),
        description: description.trim(),
      });
    } catch (err: any) {
      setError(err.message || 'Failed to analyze project.');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
      <div className="flex items-center space-x-3 mb-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-100 text-sky-700">
          <Compass className="h-5 w-5" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-900">Define Software Project Scope</h2>
          <p className="text-sm text-slate-500">
            Enter your natural-language project idea to generate structured requirements, normalized features, and development tasks.
          </p>
        </div>
      </div>

      {/* Quick Sample Presets */}
      <div className="mb-6">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-slate-600 mb-2">
          <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
          <span>Quick Sample Presets:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {SAMPLE_PROJECTS.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplySample(sample)}
              className="inline-flex items-center rounded-lg border border-slate-200 bg-slate-50/80 px-3 py-1.5 text-xs font-medium text-slate-700 hover:border-sky-300 hover:bg-sky-50 hover:text-sky-800 transition-colors"
            >
              {sample.label}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="sm:col-span-2">
            <label htmlFor="project-name" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Project Name <span className="text-rose-500">*</span>
            </label>
            <input
              id="project-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. University Transport App"
              disabled={isLoading}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 disabled:opacity-60 transition"
            />
          </div>

          <div>
            <label htmlFor="project-platform" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Target Platform
            </label>
            <select
              id="project-platform"
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              disabled={isLoading}
              className="w-full rounded-xl border border-slate-200 bg-slate-50/50 px-3.5 py-2.5 text-sm text-slate-900 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 disabled:opacity-60 transition"
            >
              <option value="Web">Web Application</option>
              <option value="Mobile">Mobile App (iOS / Android)</option>
              <option value="Full-stack">Full-Stack (Web + Mobile)</option>
              <option value="API">Backend / API Service</option>
              <option value="Desktop">Desktop App</option>
            </select>
          </div>
        </div>

        <div>
          <label htmlFor="project-description" className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            Project Idea / Natural Language Description <span className="text-rose-500">*</span>
          </label>
          <textarea
            id="project-description"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe what you want to build, user workflows, desired features, or technical goals..."
            disabled={isLoading}
            className="w-full rounded-xl border border-slate-200 bg-slate-50/50 p-4 text-sm text-slate-900 placeholder:text-slate-400 focus:border-sky-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 disabled:opacity-60 transition resize-y"
          />
        </div>

        {error && (
          <div className="rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs text-rose-700">
            {error}
          </div>
        )}

        <div className="flex items-center justify-end pt-2">
          <button
            type="submit"
            disabled={isLoading || !name.trim() || !description.trim()}
            className="inline-flex items-center space-x-2 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-md shadow-sky-600/20 hover:from-sky-500 hover:to-blue-500 focus:outline-none focus:ring-2 focus:ring-sky-500/40 disabled:cursor-not-allowed disabled:opacity-50 transition-all"
          >
            {isLoading ? (
              <>
                <span className="h-4 w-4 rounded-full border-2 border-white/30 border-t-white animate-spin"></span>
                <span>Analyzing Project Scope...</span>
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                <span>Analyze Project</span>
                <ArrowRight className="h-4 w-4 ml-1" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
