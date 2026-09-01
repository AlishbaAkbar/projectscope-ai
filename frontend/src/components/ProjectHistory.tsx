import React from 'react';
import { History, FolderGit2, Clock, ArrowUpRight } from 'lucide-react';
import { Project } from '../types/project';

interface ProjectHistoryProps {
  projects: Project[];
  activeProjectId?: number;
  onSelectProject: (projectId: number) => void;
}

export const ProjectHistory: React.FC<ProjectHistoryProps> = ({
  projects,
  activeProjectId,
  onSelectProject,
}) => {
  if (!projects || projects.length === 0) return null;

  return (
    <div className="w-full max-w-4xl mx-auto mt-10 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center space-x-2 mb-4">
        <History className="h-4 w-4 text-slate-500" />
        <h3 className="text-sm font-bold text-slate-900">Recent Scoped Projects</h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
        {projects.map((proj) => {
          const isActive = proj.id === activeProjectId;
          return (
            <button
              key={proj.id}
              onClick={() => onSelectProject(proj.id)}
              className={`p-3.5 rounded-xl border text-left transition flex flex-col justify-between ${
                isActive
                  ? 'border-sky-500 bg-sky-50/60 ring-2 ring-sky-500/20'
                  : 'border-slate-200 bg-slate-50/40 hover:border-sky-300 hover:bg-white'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 truncate max-w-[170px]">
                    {proj.name}
                  </span>
                  <ArrowUpRight className="h-3.5 w-3.5 text-slate-400" />
                </div>
                <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed">
                  {proj.description}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
                <span className="capitalize">{proj.platform}</span>
                <span>{new Date(proj.created_at).toLocaleDateString()}</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
