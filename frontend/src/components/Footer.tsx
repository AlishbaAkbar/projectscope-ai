import React from 'react';
import { Cpu, CheckCircle2 } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 bg-white py-8 mt-16 text-slate-600 text-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <Cpu className="h-4 w-4 text-sky-600" />
          <span className="font-semibold text-slate-800">ProjectScope AI</span>
          <span className="text-slate-400">|</span>
          <span className="text-xs text-slate-500">
            Pipeline: Natural Language Idea → LLM Analyzer → Pydantic Validation → Feature Normalization → Task Decomposition → Database
          </span>
        </div>

        <div className="flex items-center space-x-4 text-xs text-slate-500">
          <div className="flex items-center space-x-1">
            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
            <span>Deterministic Baseline Engine</span>
          </div>
          <span>•</span>
          <span>Week 1 Milestone Completed</span>
        </div>
      </div>
    </footer>
  );
};
