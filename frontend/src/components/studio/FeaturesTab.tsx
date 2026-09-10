'use client';

import React from 'react';
import { Feature, Task, ProjectAnalysisResult } from '../../types/project';
import {
  Layers,
  Star,
  CheckCircle2,
  AlertCircle,
  Clock,
  ListTodo,
  Tag,
  Shield,
  BarChart,
} from 'lucide-react';

interface FeaturesTabProps {
  result: ProjectAnalysisResult;
}

export const FeaturesTab: React.FC<FeaturesTabProps> = ({ result }) => {
  const features = result.features || [];
  const tasks = result.tasks || [];

  const getPriorityBadge = (priority: string) => {
    switch (priority.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'HIGH':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'MEDIUM':
        return 'bg-sky-50 text-sky-700 border-sky-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  const getFeatureTasks = (featureId: number) => {
    return tasks.filter((t) => t.feature_id === featureId);
  };

  const getFeatureHours = (featureId: number) => {
    return getFeatureTasks(featureId).reduce((sum, t) => sum + (t.estimated_hours || 0), 0);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Extracted Canonical Features</h2>
          <p className="text-xs text-slate-500">
            Modular software units mapped to standard architectural building blocks.
          </p>
        </div>
        <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
          {features.length} Features Defined
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((feature) => {
          const featureTasks = getFeatureTasks(feature.id);
          const totalHours = getFeatureHours(feature.id);
          const complexityNum =
            typeof feature.complexity === 'number'
              ? feature.complexity
              : feature.complexity === 'high'
              ? 5
              : feature.complexity === 'medium'
              ? 3
              : 1;

          return (
            <div
              key={feature.id}
              className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-sky-400 hover:shadow-xl hover:shadow-sky-500/5 transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-3">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200">
                    {feature.canonical_name}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider border ${getPriorityBadge(
                      feature.priority
                    )}`}
                  >
                    {feature.priority}
                  </span>
                </div>

                <h3 className="font-bold text-slate-900 text-sm">
                  {feature.canonical_name.replace(/_/g, ' ')}
                </h3>

                <p className="text-xs text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>

              {/* Stats & Metadata Footer */}
              <div className="space-y-3 pt-3 border-t border-slate-100 text-xs">
                {/* Complexity & Confidence */}
                <div className="flex items-center justify-between text-slate-500">
                  <div className="flex items-center space-x-1">
                    <span className="text-[11px] font-medium">Complexity:</span>
                    <div className="flex items-center space-x-0.5">
                      {[1, 2, 3, 4, 5].map((level) => (
                        <span
                          key={level}
                          className={`w-2 h-2 rounded-full ${
                            level <= complexityNum ? 'bg-purple-600' : 'bg-slate-200'
                          }`}
                        />
                      ))}
                    </div>
                  </div>

                  <span className="text-[11px] text-emerald-700 font-semibold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                    {Math.round((feature.confidence || 0.9) * 100)}% Conf
                  </span>
                </div>

                {/* Subtask and hours badge */}
                <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 text-slate-700">
                  <div className="flex items-center space-x-1.5">
                    <ListTodo className="w-3.5 h-3.5 text-sky-600" />
                    <span className="font-semibold">{featureTasks.length} Tasks</span>
                  </div>
                  <div className="flex items-center space-x-1 font-bold text-slate-900">
                    <Clock className="w-3.5 h-3.5 text-indigo-600" />
                    <span>~{totalHours.toFixed(0)} Hours</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
