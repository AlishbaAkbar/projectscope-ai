'use client';

import React, { useState } from 'react';
import { Project, ProjectAnalysisResult } from '../types/project';
import {
  LayoutDashboard,
  Plus,
  Search,
  Layers,
  Clock,
  DollarSign,
  AlertTriangle,
  ChevronRight,
  Trash2,
  Sparkles,
  Smartphone,
  Globe,
  Server,
  FolderOpen,
  Calendar,
  BarChart3,
} from 'lucide-react';

interface DashboardViewProps {
  projects: Project[];
  onSelectProject: (projectId: number) => void;
  onOpenCreate: () => void;
  onDeleteProject: (projectId: number) => Promise<void>;
  currentResult: ProjectAnalysisResult | null;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  projects,
  onSelectProject,
  onOpenCreate,
  onDeleteProject,
  currentResult,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [platformFilter, setPlatformFilter] = useState('all');
  const [isDeleting, setIsDeleting] = useState<number | null>(null);

  // Compute portfolio metrics
  const totalProjects = projects.length;
  const filteredProjects = projects.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (p.description && p.description.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesPlatform =
      platformFilter === 'all' ||
      (p.type && p.type.toLowerCase().includes(platformFilter.toLowerCase())) ||
      (p.platform && p.platform.toLowerCase().includes(platformFilter.toLowerCase()));
    return matchesSearch && matchesPlatform;
  });

  const getPlatformIcon = (platformStr?: string) => {
    const s = (platformStr || '').toLowerCase();
    if (s.includes('mobile')) return <Smartphone className="w-4 h-4 text-purple-600" />;
    if (s.includes('cloud') || s.includes('api')) return <Server className="w-4 h-4 text-emerald-600" />;
    return <Globe className="w-4 h-4 text-sky-600" />;
  };

  const handleDelete = async (e: React.MouseEvent, projectId: number) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this project and its scoped data?')) return;
    setIsDeleting(projectId);
    try {
      await onDeleteProject(projectId);
    } finally {
      setIsDeleting(null);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Top Header & Quick Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            Portfolio Dashboard
          </h1>
          <p className="text-xs sm:text-sm text-slate-500">
            Overview of all scoped software initiatives, estimated velocity, and engineering telemetry.
          </p>
        </div>

        <button
          onClick={onOpenCreate}
          className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-700 hover:to-blue-700 text-white text-xs font-bold shadow-md shadow-sky-600/20 hover:shadow-lg transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>New Project Scope</span>
        </button>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Projects</span>
            <FolderOpen className="w-4 h-4 text-sky-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">{totalProjects}</div>
          <p className="text-[11px] text-slate-500">Active software briefs</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Latest Project Effort</span>
            <Clock className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {currentResult?.total_estimated_hours ? `${currentResult.total_estimated_hours.toFixed(0)}h` : '--'}
          </div>
          <p className="text-[11px] text-slate-500">Hybrid ML estimate</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Projected Value</span>
            <DollarSign className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {currentResult?.cost?.total?.expected
              ? `$${currentResult.cost.total.expected.toLocaleString()}`
              : '$25,000+'}
          </div>
          <p className="text-[11px] text-slate-500">Industry blended cost baseline</p>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Active Risk Profile</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {currentResult?.risk_level || 'BALANCED'}
          </div>
          <p className="text-[11px] text-slate-500">Calculated risk level</p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search projects by name or keywords..."
            className="w-full pl-9 pr-4 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
        </div>

        <div className="flex items-center space-x-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          {['all', 'web', 'mobile', 'saas', 'healthcare'].map((plat) => (
            <button
              key={plat}
              onClick={() => setPlatformFilter(plat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize whitespace-nowrap transition-colors ${
                platformFilter === plat
                  ? 'bg-sky-100 text-sky-800'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {plat === 'all' ? 'All Platforms' : plat}
            </button>
          ))}
        </div>
      </div>

      {/* Projects Grid */}
      {filteredProjects.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-white border border-dashed border-slate-300 space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto">
            <Sparkles className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">No matching projects found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Get started by scoping your first software idea or apply an enterprise template.
          </p>
          <button
            onClick={onOpenCreate}
            className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold shadow-md transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Create First Project</span>
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredProjects.map((project) => (
            <div
              key={project.id}
              onClick={() => onSelectProject(project.id)}
              className="group cursor-pointer p-5 rounded-2xl bg-white border border-slate-200 hover:border-sky-500 hover:shadow-xl hover:shadow-sky-500/10 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2.5">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 rounded-lg bg-slate-100 group-hover:bg-sky-50 transition-colors">
                      {getPlatformIcon(project.type || project.platform)}
                    </div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
                      {project.type || project.platform || 'Web'}
                    </span>
                  </div>

                  <button
                    onClick={(e) => handleDelete(e, project.id)}
                    disabled={isDeleting === project.id}
                    title="Delete Project"
                    className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <h3 className="font-bold text-slate-900 text-base group-hover:text-sky-600 transition-colors leading-snug">
                  {project.name}
                </h3>

                <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed">
                  {project.description || 'No description provided.'}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <div className="flex items-center space-x-1 text-slate-400 text-[11px]">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>{new Date(project.created_at).toLocaleDateString()}</span>
                </div>

                <div className="inline-flex items-center space-x-1 text-sky-600 font-bold group-hover:translate-x-1 transition-transform">
                  <span>Open Studio</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
