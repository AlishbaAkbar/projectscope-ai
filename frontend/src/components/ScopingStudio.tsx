'use client';

import React, { useState } from 'react';
import { ProjectAnalysisResult } from '../types/project';
import {
  Sparkles,
  RefreshCw,
  FileDown,
  MessageSquare,
  Layers,
  ListTodo,
  DollarSign,
  Calendar,
  AlertTriangle,
  Cpu,
  Rocket,
  Wand2,
  Users,
  CheckCircle2,
  LayoutGrid,
  Bot,
  Sliders,
} from 'lucide-react';

import { OverviewTab } from './studio/OverviewTab';
import { ChatTab } from './studio/ChatTab';
import { RequirementsTab } from './studio/RequirementsTab';
import { FeaturesTab } from './studio/FeaturesTab';
import { TasksTab } from './studio/TasksTab';
import { TeamTab } from './studio/TeamTab';
import { CostTab } from './studio/CostTab';
import { TimelineTab } from './studio/TimelineTab';
import { RisksTab } from './studio/RisksTab';
import { MvpTab } from './studio/MvpTab';
import { TechStackTab } from './studio/TechStackTab';
import { ExportModal } from './studio/ExportModal';
import { FeedbackModal } from './studio/FeedbackModal';

interface ScopingStudioProps {
  result: ProjectAnalysisResult;
  onReanalyze: () => Promise<void>;
  isReanalyzing: boolean;
  onRefreshProject?: () => Promise<void>;
}

type TabKey =
  | 'overview'
  | 'chat'
  | 'requirements'
  | 'features'
  | 'tasks'
  | 'team'
  | 'cost'
  | 'timeline'
  | 'risks'
  | 'mvp'
  | 'tech-stack';

export const ScopingStudio: React.FC<ScopingStudioProps> = ({
  result,
  onReanalyze,
  isReanalyzing,
  onRefreshProject,
}) => {
  const [activeTab, setActiveTab] = useState<TabKey>('overview');
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);

  const totalHours = result.total_estimated_hours || 0;
  const totalCost = result.cost?.total?.expected || Math.round(totalHours * 85);
  const workingDays = result.timeline?.total_working_days || Math.round(totalHours / 16);
  const riskLevel = result.risk_level || 'HIGH';

  const TABS = [
    { key: 'overview', label: 'Overview', icon: LayoutGrid },
    { key: 'chat', label: 'AI Chat & Refine', icon: Bot, badge: 'RAG' },
    { key: 'requirements', label: 'Requirements', icon: Sparkles, count: result.features.length ? undefined : undefined },
    { key: 'features', label: 'Features', icon: Layers, count: result.features.length },
    { key: 'tasks', label: 'Tasks Breakdown', icon: ListTodo, count: result.tasks.length },
    { key: 'team', label: 'Team Allocation', icon: Users },
    { key: 'cost', label: 'Cost Modeling', icon: DollarSign },
    { key: 'timeline', label: 'Timeline & Critical Path', icon: Calendar },
    { key: 'risks', label: 'Risk Matrix', icon: AlertTriangle },
    { key: 'mvp', label: 'MVP Scoping', icon: Rocket, badge: 'Interactive' },
    { key: 'tech-stack', label: 'Tech Stack', icon: Cpu },
  ] as const;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Project Scope Header */}
      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          {/* Project Identity */}
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold uppercase tracking-wider text-sky-700 bg-sky-50 px-2.5 py-0.5 rounded-md border border-sky-200">
                {result.project?.platform || result.project?.type || 'Web Application'}
              </span>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-200 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Scoped & Verified</span>
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
              {result.project?.name || 'Software Project Scope'}
            </h1>

            <p className="text-xs text-slate-500 max-w-2xl line-clamp-2 leading-relaxed">
              {result.project?.description || 'Natural language project description analyzed into technical specification.'}
            </p>
          </div>

          {/* Action Bar */}
          <div className="flex flex-wrap items-center gap-2 pt-2 lg:pt-0">
            <button
              onClick={() => setActiveTab('chat')}
              className="px-3.5 py-2 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 text-xs font-bold border border-sky-200 shadow-sm transition-all flex items-center space-x-1.5"
            >
              <Bot className="w-4 h-4 text-sky-600" />
              <span>Ask AI Scoper</span>
            </button>

            <button
              onClick={onReanalyze}
              disabled={isReanalyzing}
              className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold border border-slate-200 shadow-sm transition-all flex items-center space-x-1.5 disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${isReanalyzing ? 'animate-spin' : ''}`} />
              <span>{isReanalyzing ? 'Re-analyzing...' : 'Re-Analyze'}</span>
            </button>

            <button
              onClick={() => setIsExportOpen(true)}
              className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-md shadow-slate-900/10 transition-all flex items-center space-x-1.5"
            >
              <FileDown className="w-3.5 h-3.5" />
              <span>Export Scope</span>
            </button>

            <button
              onClick={() => setIsFeedbackOpen(true)}
              className="px-3 py-2 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold border border-amber-200 transition-all flex items-center space-x-1"
            >
              <MessageSquare className="w-3.5 h-3.5 text-amber-600" />
              <span>Feedback</span>
            </button>
          </div>
        </div>

        {/* Quick KPI Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-100 text-xs">
          <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
              Estimated Effort
            </span>
            <span className="text-base font-black text-slate-900">{totalHours.toFixed(0)} Hours</span>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
              Expected Budget
            </span>
            <span className="text-base font-black text-emerald-700">
              ${totalCost.toLocaleString()}
            </span>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
              Working Days
            </span>
            <span className="text-base font-black text-sky-700">{workingDays} Days</span>
          </div>

          <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
              Risk Profile
            </span>
            <span className="text-base font-black text-amber-700">{riskLevel}</span>
          </div>
        </div>
      </div>

      {/* Navigation Tab Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-1.5 shadow-sm overflow-x-auto">
        <div className="flex items-center space-x-1 min-w-max">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as TabKey)}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
                  isActive
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>

                {tab.count !== undefined && (
                  <span
                    className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                      isActive ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'
                    }`}
                  >
                    {tab.count}
                  </span>
                )}

                {tab.badge && (
                  <span
                    className={`px-1.5 py-0.2 rounded text-[9px] font-extrabold uppercase ${
                      isActive ? 'bg-sky-500 text-white' : 'bg-sky-100 text-sky-800'
                    }`}
                  >
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content Display */}
      <div className="transition-all">
        {activeTab === 'overview' && <OverviewTab result={result} />}
        {activeTab === 'chat' && <ChatTab result={result} />}
        {activeTab === 'requirements' && (
          <RequirementsTab result={result} onRefreshProject={onRefreshProject} />
        )}
        {activeTab === 'features' && <FeaturesTab result={result} />}
        {activeTab === 'tasks' && <TasksTab result={result} />}
        {activeTab === 'team' && <TeamTab result={result} />}
        {activeTab === 'cost' && <CostTab result={result} />}
        {activeTab === 'timeline' && <TimelineTab result={result} />}
        {activeTab === 'risks' && <RisksTab result={result} />}
        {activeTab === 'mvp' && (
          <MvpTab result={result} onOpenExport={() => setIsExportOpen(true)} />
        )}
        {activeTab === 'tech-stack' && <TechStackTab result={result} />}
      </div>

      {/* Modals */}
      <ExportModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        result={result}
      />

      <FeedbackModal
        isOpen={isFeedbackOpen}
        onClose={() => setIsFeedbackOpen(false)}
        projectId={result.project_id}
        projectName={result.project?.name || 'Project Scope'}
      />
    </div>
  );
};
