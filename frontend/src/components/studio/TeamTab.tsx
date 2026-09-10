'use client';

import React from 'react';
import { ProjectAnalysisResult } from '../../types/project';
import { Users, Clock, DollarSign, Award, Briefcase, BarChart2, ShieldCheck } from 'lucide-react';

interface TeamTabProps {
  result: ProjectAnalysisResult;
}

const DEFAULT_HOURLY_RATES: Record<string, number> = {
  'UI/UX Designer': 75,
  'Frontend Engineer': 85,
  'Backend Engineer': 95,
  'Full Stack Engineer': 90,
  'Database Administrator': 95,
  'QA Automation Engineer': 65,
  'DevOps / Cloud Engineer': 105,
  'Security Engineer': 115,
  'Technical Project Manager': 80,
  'Solutions Architect': 125,
};

export const TeamTab: React.FC<TeamTabProps> = ({ result }) => {
  const summary = result.summary || {};
  const totalHours = result.total_estimated_hours || 1;

  const roleEntries = Object.entries(summary);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Team Allocation & Resource Workload</h2>
        <p className="text-xs text-slate-500">
          Discipline breakdown, effort distribution, and recommended staffing composition.
        </p>
      </div>

      {/* Team Composition Recommendations Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-sky-50 via-indigo-50 to-purple-50 border border-sky-100 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-2 text-sky-800 font-bold text-xs uppercase tracking-wider">
            <Award className="w-4 h-4 text-sky-600" />
            <span>Recommended Engineering Squad</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed max-w-xl">
            Based on the {totalHours.toFixed(0)} total hour baseline and required competencies, this initiative requires a cross-functional squad of 3-4 specialized team members.
          </p>
        </div>
        <div className="px-4 py-2 rounded-xl bg-white shadow-sm border border-sky-200 text-center shrink-0">
          <span className="text-[10px] font-bold text-slate-400 uppercase">Squad Size</span>
          <div className="text-xl font-black text-sky-700">3 – 4 FTEs</div>
        </div>
      </div>

      {/* Role Workload Distribution Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {roleEntries.map(([roleName, data]) => {
          const hours = data.total_hours || 0;
          const percentage = Math.round((hours / totalHours) * 100);
          const rate = DEFAULT_HOURLY_RATES[roleName] || 85;
          const cost = data.estimated_cost || hours * rate;

          return (
            <div
              key={roleName}
              className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all space-y-3"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold text-xs">
                    <Briefcase className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-slate-900">{roleName}</h4>
                    <span className="text-[11px] text-slate-400 font-medium">
                      {data.num_tasks} Assigned Tasks
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-sm font-black text-slate-900">{hours.toFixed(0)}h</span>
                  <div className="text-[11px] text-slate-500 font-medium">{percentage}% of Effort</div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1">
                <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-sky-500 to-indigo-600 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, Math.max(5, percentage))}%` }}
                  />
                </div>
              </div>

              {/* Financial Rate and Allocation */}
              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span className="flex items-center space-x-1">
                  <span>Standard Rate:</span>
                  <strong className="text-slate-800">${rate}/hr</strong>
                </span>
                <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                  Est. Cost: ${cost.toLocaleString()}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
