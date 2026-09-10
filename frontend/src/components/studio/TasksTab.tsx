'use client';

import React, { useState } from 'react';
import { Task, ProjectAnalysisResult } from '../../types/project';
import {
  ListTodo,
  Clock,
  Search,
  Filter,
  Layers,
  CheckCircle2,
  AlertCircle,
  GitBranch,
  User,
} from 'lucide-react';

interface TasksTabProps {
  result: ProjectAnalysisResult;
}

const ROLE_MAP: Record<number, string> = {
  1: 'UI/UX Designer',
  2: 'Frontend Engineer',
  3: 'Backend Engineer',
  4: 'Full Stack Engineer',
  5: 'Database Administrator',
  6: 'QA Automation Engineer',
  7: 'DevOps / Cloud Engineer',
  8: 'Security Engineer',
  9: 'Technical Project Manager',
  10: 'Solutions Architect',
};

export const TasksTab: React.FC<TasksTabProps> = ({ result }) => {
  const [disciplineFilter, setDisciplineFilter] = useState('all');
  const [search, setSearch] = useState('');

  const tasks = result.tasks || [];

  const getDiscipline = (task: Task) => {
    if (task.category) return task.category;
    const title = task.title.toLowerCase();
    if (title.includes('design') || title.includes('ui') || title.includes('page') || title.includes('interface'))
      return 'Frontend';
    if (title.includes('api') || title.includes('jwt') || title.includes('backend') || title.includes('gateway'))
      return 'Backend';
    if (title.includes('database') || title.includes('model') || title.includes('schema')) return 'Database';
    if (title.includes('test') || title.includes('qa')) return 'QA';
    if (title.includes('cloud') || title.includes('ci/cd') || title.includes('infra') || title.includes('devops'))
      return 'DevOps';
    return 'Engineering';
  };

  const filteredTasks = tasks.filter((task) => {
    const disc = getDiscipline(task).toLowerCase();
    const matchesFilter = disciplineFilter === 'all' || disc === disciplineFilter.toLowerCase();
    const matchesSearch =
      task.title.toLowerCase().includes(search.toLowerCase()) ||
      (task.description && task.description.toLowerCase().includes(search.toLowerCase()));
    return matchesFilter && matchesSearch;
  });

  const getDisciplineBadge = (disc: string) => {
    switch (disc.toLowerCase()) {
      case 'frontend':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'backend':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'database':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200';
      case 'qa':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'devops':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Deterministic Task Breakdown</h2>
          <p className="text-xs text-slate-500">
            Atomic engineering subtasks classified by discipline, role allocation, and estimated effort.
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search subtasks..."
            className="w-full pl-8 pr-3 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
        </div>
      </div>

      {/* Discipline Filter Pills */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 border-b border-slate-200 text-xs font-semibold">
        {['all', 'frontend', 'backend', 'database', 'qa', 'devops'].map((disc) => (
          <button
            key={disc}
            onClick={() => setDisciplineFilter(disc)}
            className={`px-3 py-1.5 rounded-lg capitalize whitespace-nowrap transition-colors ${
              disciplineFilter === disc
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {disc === 'all' ? 'All Disciplines' : disc}
          </button>
        ))}
        <span className="text-xs text-slate-400 font-normal ml-auto">
          {filteredTasks.length} of {tasks.length} tasks
        </span>
      </div>

      {/* Tasks List */}
      <div className="space-y-3">
        {filteredTasks.map((task) => {
          const discipline = getDiscipline(task);
          const roleName = task.role_id ? ROLE_MAP[task.role_id] : 'Software Engineer';

          return (
            <div
              key={task.id}
              className="p-4 rounded-xl bg-white border border-slate-200 hover:border-sky-300 hover:shadow-md transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span
                    className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider border ${getDisciplineBadge(
                      discipline
                    )}`}
                  >
                    {discipline}
                  </span>

                  {task.is_global && (
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-purple-50 text-purple-700 border border-purple-200">
                      Global System Task
                    </span>
                  )}

                  <span className="text-[11px] font-medium text-slate-500 flex items-center space-x-1">
                    <User className="w-3 h-3 text-slate-400" />
                    <span>{roleName}</span>
                  </span>
                </div>

                <h4 className="font-bold text-sm text-slate-900 leading-snug">{task.title}</h4>
                <p className="text-xs text-slate-500 leading-relaxed">{task.description}</p>
              </div>

              {/* Hours and Meta */}
              <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-100 gap-1 shrink-0">
                <div className="flex items-center space-x-1.5 px-3 py-1 rounded-xl bg-slate-100 text-slate-900 font-bold text-xs">
                  <Clock className="w-3.5 h-3.5 text-sky-600" />
                  <span>{task.estimated_hours}h</span>
                </div>
                <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">
                  Est. Effort
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
