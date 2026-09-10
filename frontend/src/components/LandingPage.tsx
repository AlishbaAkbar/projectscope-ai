'use client';

import React from 'react';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Layers,
  ListTodo,
  DollarSign,
  Calendar,
  AlertTriangle,
  Cpu,
  Database,
  FileDown,
  MessageSquare,
  Users,
  CheckCircle2,
  Check,
  ChevronRight,
  Zap,
} from 'lucide-react';
import { ProjectCreatePayload } from '../types/project';

interface LandingPageProps {
  onOpenCreate: () => void;
  onSelectPreset: (preset: ProjectCreatePayload) => void;
  onGoToDashboard: () => void;
}

const PRESET_TEMPLATES: Array<{
  title: string;
  platform: string;
  category: string;
  description: string;
  badge: string;
}> = [
  {
    title: 'E-Commerce Marketplace',
    platform: 'Web & Mobile',
    category: 'E-Commerce',
    badge: 'Popular',
    description:
      'Multi-vendor marketplace with product catalog, cart, Stripe checkout, customer order tracking, reviews, and vendor admin dashboard.',
  },
  {
    title: 'Telemedicine & Health App',
    platform: 'Mobile & Web',
    category: 'Healthcare',
    badge: 'High Compliance',
    description:
      'HIPAA-compliant telemedicine platform with patient video consultations, doctor appointment scheduling, prescription tracking, and EHR notes.',
  },
  {
    title: 'University Transit Live Tracker',
    platform: 'Mobile',
    category: 'Logistics',
    badge: 'Real-time GPS',
    description:
      'Live campus bus locator with GPS vehicle telemetry, schedule push notifications, estimated time of arrival (ETA), and transport delay reporting.',
  },
  {
    title: 'B2B SaaS Sales CRM',
    platform: 'Web & Cloud',
    category: 'Enterprise SaaS',
    badge: 'Data-Intensive',
    description:
      'Lead pipeline tracking, automated email integration, deal velocity analytics, role-based team access control, and PDF contract generator.',
  },
];

const CAPABILITIES = [
  {
    icon: Sparkles,
    title: 'AI Requirement Extraction',
    description: 'Converts unstructured product concepts into categorized functional & non-functional requirements with strict Pydantic v2 schemas.',
    color: 'from-sky-500 to-blue-600',
  },
  {
    icon: Layers,
    title: 'Canonical Feature Mapping',
    description: 'Normalizes synonyms (e.g., "sign-in", "user auth") into standardized engineering feature taxonomies.',
    color: 'from-blue-600 to-indigo-600',
  },
  {
    icon: ListTodo,
    title: 'Deterministic Task Breakdown',
    description: 'Decomposes features across 7 engineering disciplines: Frontend, Backend, Database, QA, Integration, DevOps, and PM.',
    color: 'from-indigo-600 to-violet-600',
  },
  {
    icon: Cpu,
    title: 'Hybrid ML Estimation',
    description: 'Combines deterministic rules, regression models (trained on historical software metrics), and LLM suggestions with dynamic weighting.',
    color: 'from-purple-600 to-pink-600',
  },
  {
    icon: Calendar,
    title: 'Timeline & Critical Path',
    description: 'Calculates true working days, detects dependencies, highlights parallelization opportunities, and flags project delivery bottlenecks.',
    color: 'from-emerald-500 to-teal-600',
  },
  {
    icon: DollarSign,
    title: 'Role-Based Cost Modeling',
    description: 'Computes billable hours per engineering role with rates, variance ranges (best vs expected vs worst case), and risk buffers.',
    color: 'from-amber-500 to-orange-600',
  },
  {
    icon: AlertTriangle,
    title: 'Risk Assessment Matrix',
    description: 'Identifies technical, security, and operational hazards with severity scores, mitigation strategies, and assigned owners.',
    color: 'from-rose-500 to-red-600',
  },
  {
    icon: Database,
    title: 'RAG Knowledge Grounding',
    description: 'Retrieves architectural best practices, compliance guidelines, and tech stack benchmarks via vector similarity search.',
    color: 'from-cyan-500 to-blue-600',
  },
];

export const LandingPage: React.FC<LandingPageProps> = ({
  onOpenCreate,
  onSelectPreset,
  onGoToDashboard,
}) => {
  return (
    <div className="space-y-20 pb-16 animate-in fade-in duration-300">
      {/* Hero Section */}
      <section className="relative pt-6 sm:pt-12 text-center max-w-4xl mx-auto space-y-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-sky-50 px-4 py-1.5 text-xs font-semibold text-sky-700 border border-sky-200/80 shadow-sm">
          <Sparkles className="h-4 w-4 text-sky-500 animate-spin-slow" />
          <span>Next-Generation Software Scope & Engineering Architecture Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-[1.15]">
          Turn Rough Software Ideas Into{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 via-blue-600 to-indigo-600">
            Executable Plans
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed font-normal">
          Stop guessing software timelines and budgets. ProjectScope AI extracts requirements, decomposes tasks across 7 disciplines, models hybrid ML costs, calculates critical path timelines, and flags delivery risks in seconds.
        </p>

        {/* Hero CTAs */}
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onOpenCreate}
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-700 hover:to-blue-700 text-white font-bold text-sm shadow-lg shadow-sky-600/25 hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center space-x-2"
          >
            <span>Scope a New Project</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={onGoToDashboard}
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-800 font-bold text-sm shadow-sm transition-all flex items-center justify-center space-x-2"
          >
            <span>View Portfolio Dashboard</span>
          </button>
        </div>

        {/* Live Metrics Trust Banner */}
        <div className="pt-6 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto text-left">
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
            <div className="text-2xl font-black text-slate-900">7 Disciplines</div>
            <div className="text-xs text-slate-500 font-medium">Frontend, Backend, DB, QA, DevOps, Integration, PM</div>
          </div>
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
            <div className="text-2xl font-black text-sky-600">Hybrid ML</div>
            <div className="text-xs text-slate-500 font-medium">Deterministic Rules + ML Regression + LLM Weighting</div>
          </div>
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
            <div className="text-2xl font-black text-emerald-600">Critical Path</div>
            <div className="text-xs text-slate-500 font-medium">Automated Dependency & Bottleneck Graphing</div>
          </div>
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
            <div className="text-2xl font-black text-indigo-600">RAG Grounded</div>
            <div className="text-xs text-slate-500 font-medium">Verified Software Engineering Knowledge Base</div>
          </div>
        </div>
      </section>

      {/* 4 Quick Presets */}
      <section className="max-w-6xl mx-auto space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900">
              Try an Example Project Brief
            </h2>
            <p className="text-xs sm:text-sm text-slate-500">
              Select any pre-configured software scenario to test immediate AI analysis and decomposition.
            </p>
          </div>
          <span className="text-xs font-semibold text-sky-600 hidden sm:inline">1-Click Scoping Ready</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {PRESET_TEMPLATES.map((preset, idx) => (
            <div
              key={idx}
              onClick={() =>
                onSelectPreset({
                  name: preset.title,
                  description: preset.description,
                  platform: preset.platform,
                  type: preset.category.toLowerCase(),
                })
              }
              className="group cursor-pointer p-5 rounded-2xl bg-white border border-slate-200 hover:border-sky-500 hover:shadow-xl hover:shadow-sky-500/10 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-sky-600 bg-sky-50 px-2 py-0.5 rounded-md">
                    {preset.category}
                  </span>
                  <span className="text-[10px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">
                    {preset.badge}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 group-hover:text-sky-600 transition-colors">
                  {preset.title}
                </h3>
                <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed">
                  {preset.description}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-slate-600 group-hover:text-sky-600">
                <span>{preset.platform}</span>
                <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4-Step Pipeline Architecture */}
      <section className="max-w-6xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950 p-8 sm:p-12 text-white space-y-8 shadow-2xl">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-sky-400">Architecture Pipeline</span>
          <h2 className="text-2xl sm:text-4xl font-black tracking-tight">
            How ProjectScope AI Works
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            From natural-language idea to Jira-ready tasks, role allocations, and budget estimates.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 space-y-3">
            <div className="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-sm">
              01
            </div>
            <h3 className="font-bold text-base text-white">Project Idea Ingestion</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Users provide a problem statement or natural brief. The system determines platform constraints and target user personas.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 space-y-3">
            <div className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">
              02
            </div>
            <h3 className="font-bold text-base text-white">Schema Extraction</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              AI extracts functional requirements and maps synonyms to canonical feature keys with strict Pydantic v2 integrity checks.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 space-y-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm">
              03
            </div>
            <h3 className="font-bold text-base text-white">Task Decomposition</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Deterministic rule engines decompose each feature into role-specific subtasks across Frontend, Backend, Database, and QA.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 space-y-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">
              04
            </div>
            <h3 className="font-bold text-base text-white">Hybrid ML & Scoping</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Rules and ML regression combine to output true hours, critical path schedules, risk mitigation cards, and exportable reports.
            </p>
          </div>
        </div>
      </section>

      {/* Core Capabilities Showcase */}
      <section className="max-w-6xl mx-auto space-y-8">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-sky-600">Enterprise Feature Suite</span>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900">
            Complete Scoping & Architecture Capabilities
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Everything your team needs to validate requirements, negotiate budgets, and launch with confidence.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {CAPABILITIES.map((cap, idx) => {
            const Icon = cap.icon;
            return (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-lg transition-all space-y-3"
              >
                <div
                  className={`w-10 h-10 rounded-xl bg-gradient-to-br ${cap.color} text-white flex items-center justify-center shadow-md`}
                >
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-sm text-slate-900">{cap.title}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{cap.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="max-w-5xl mx-auto rounded-2xl bg-gradient-to-r from-sky-600 via-blue-600 to-indigo-600 p-8 sm:p-10 text-white text-center space-y-4 shadow-xl">
        <h2 className="text-2xl sm:text-3xl font-black tracking-tight">
          Ready to Scope Your Next Big Idea?
        </h2>
        <p className="text-xs sm:text-sm text-sky-100 max-w-xl mx-auto leading-relaxed">
          Create your project specification in under 2 minutes. Get instant task breakdowns, accurate cost curves, and actionable architectural blueprints.
        </p>
        <div className="pt-2">
          <button
            onClick={onOpenCreate}
            className="px-6 py-3 rounded-xl bg-white hover:bg-slate-100 text-sky-900 font-bold text-sm shadow-md hover:scale-105 active:scale-95 transition-all"
          >
            Launch Scoping Wizard Now
          </button>
        </div>
      </section>
    </div>
  );
};
