'use client';

import React from 'react';
import { ProjectAnalysisResult } from '../../types/project';
import {
  Calendar,
  Clock,
  Milestone as MilestoneIcon,
  GitCommit,
  AlertTriangle,
  Zap,
  CheckCircle2,
  ArrowRight,
  Sparkles,
} from 'lucide-react';

interface TimelineTabProps {
  result: ProjectAnalysisResult;
}

export const TimelineTab: React.FC<TimelineTabProps> = ({ result }) => {
  const timeline = result.timeline;
  const totalHours = result.total_estimated_hours || 100;

  // Approximate working days and milestones if not populated
  const workingDays = timeline?.total_working_days || Math.max(12, Math.round(totalHours / 16));
  const calendarDays = timeline?.total_days || Math.round(workingDays * 1.4);
  const criticalPath = timeline?.critical_path || [
    'Database Architecture & Schema Definition',
    'JWT Authentication & Access Control',
    'Core Business Logic & API Endpoints',
    'Frontend Client Integration & State Management',
    'Payment / External Gateway Testing',
    'End-to-End QA Automation & Security Audit',
  ];

  const milestones = timeline?.milestones || [
    {
      name: 'Sprint 1: Architecture & Data Foundations',
      date: 'Day 1 – 5',
      description: 'Setup database models, CI/CD pipeline, and authentication middleware.',
    },
    {
      name: 'Sprint 2: Core Domain APIs & Services',
      date: 'Day 6 – 12',
      description: 'CRUD endpoints, business logic validation, and third-party integrations.',
    },
    {
      name: 'Sprint 3: Frontend Views & Interactive UI',
      date: 'Day 13 – 19',
      description: 'User interfaces, responsive layouts, client-side caching, and API binding.',
    },
    {
      name: 'Sprint 4: Verification, Security & Production Prep',
      date: 'Day 20 – 25',
      description: 'Integration tests, PCI/Security auditing, load testing, and production deployment.',
    },
  ];

  const parallelization = timeline?.parallelization_opportunities || [
    {
      tasks: ['Frontend UI Development', 'Backend Business Logic'],
      description: 'Can run concurrently once API schemas and contract interfaces are agreed upon.',
    },
    {
      tasks: ['QA Test Script Authoring', 'API Implementation'],
      description: 'QA engineers can construct integration suites alongside feature PRs using mock data.',
    },
  ];

  const bottlenecks = timeline?.bottlenecks || [
    {
      role: 'Backend & Data Modeling',
      description: 'Frontend state binding cannot complete until authentication and core APIs stabilize.',
      impact_days: 3,
    },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Timeline & Critical Path Roadmap</h2>
        <p className="text-xs text-slate-500">
          Dependency scheduling, milestone projections, and parallel execution tracks.
        </p>
      </div>

      {/* KPI Timeline Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Working Days</span>
            <Clock className="w-4 h-4 text-sky-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">{workingDays} Days</div>
          <p className="text-[11px] text-slate-500">Excluding weekends & holidays</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Calendar Span</span>
            <Calendar className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">{calendarDays} Days</div>
          <p className="text-[11px] text-slate-500">~{Math.ceil(calendarDays / 7)} weeks to launch</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Critical Path</span>
            <GitCommit className="w-4 h-4 text-rose-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">{criticalPath.length} Tasks</div>
          <p className="text-[11px] text-slate-500">Zero-slack delivery sequence</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Milestones</span>
            <MilestoneIcon className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">{milestones.length} Phases</div>
          <p className="text-[11px] text-slate-500">Structured release gates</p>
        </div>
      </div>

      {/* Structured Sprint Milestones */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-6 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
          <MilestoneIcon className="w-4 h-4 text-sky-600" />
          <span>Delivery Sprints & Release Gates</span>
        </h3>

        <div className="space-y-4">
          {milestones.map((m, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl border border-slate-100 hover:border-slate-300 bg-slate-50/50 hover:bg-white transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div className="flex items-start space-x-3">
                <div className="w-7 h-7 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center font-black text-xs shrink-0 mt-0.5">
                  {idx + 1}
                </div>
                <div>
                  <h4 className="font-bold text-xs sm:text-sm text-slate-900">{m.name}</h4>
                  <p className="text-xs text-slate-500 leading-relaxed mt-0.5">{m.description}</p>
                </div>
              </div>

              <div className="text-right shrink-0">
                <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-white border border-slate-200 text-slate-700">
                  {m.date}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Critical Path & Parallelization Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Critical Path Sequence */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-rose-700 font-bold text-xs uppercase tracking-wider">
            <GitCommit className="w-4 h-4 text-rose-600" />
            <span>Critical Path Dependencies</span>
          </div>
          <p className="text-xs text-slate-500">
            Delays in these specific tasks directly push the release date:
          </p>
          <div className="space-y-2">
            {criticalPath.map((item, i) => (
              <div
                key={i}
                className="p-2.5 rounded-lg bg-rose-50/60 border border-rose-100 text-xs text-rose-900 flex items-center space-x-2 font-medium"
              >
                <span className="w-5 h-5 rounded-full bg-rose-200/80 text-rose-800 text-[10px] flex items-center justify-center font-bold">
                  {i + 1}
                </span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Parallel Tracks & Bottlenecks */}
        <div className="space-y-4">
          {/* Parallel Opportunities */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 text-emerald-700 font-bold text-xs uppercase tracking-wider">
              <Zap className="w-4 h-4 text-emerald-600" />
              <span>Parallelization Opportunities</span>
            </div>
            <div className="space-y-2">
              {parallelization.map((p, i) => (
                <div key={i} className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-100 text-xs text-emerald-900 space-y-1">
                  <div className="font-bold flex items-center space-x-1">
                    <span>{p.tasks.join(' ↔ ')}</span>
                  </div>
                  <p className="text-[11px] text-emerald-800">{p.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Bottlenecks */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-3">
            <div className="flex items-center space-x-2 text-amber-700 font-bold text-xs uppercase tracking-wider">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Potential Bottlenecks</span>
            </div>
            <div className="space-y-2">
              {bottlenecks.map((b, i) => (
                <div key={i} className="p-3 rounded-xl bg-amber-50/60 border border-amber-100 text-xs text-amber-900 space-y-1">
                  <div className="font-bold">{b.role}</div>
                  <p className="text-[11px] text-amber-800">{b.description}</p>
                  <div className="text-[10px] text-amber-700 font-semibold">
                    Risk Buffer: +{b.impact_days} days
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
