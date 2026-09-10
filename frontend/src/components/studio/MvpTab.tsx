'use client';

import React, { useState } from 'react';
import { ProjectAnalysisResult, Feature } from '../../types/project';
import {
  Sparkles,
  Rocket,
  CheckCircle2,
  Clock,
  DollarSign,
  Calendar,
  Layers,
  ArrowDownRight,
  Sliders,
  RotateCcw,
} from 'lucide-react';

interface MvpTabProps {
  result: ProjectAnalysisResult;
  onOpenExport: () => void;
}

export const MvpTab: React.FC<MvpTabProps> = ({ result, onOpenExport }) => {
  const features = result.features || [];
  const tasks = result.tasks || [];
  const totalHours = result.total_estimated_hours || 100;
  const totalCost = result.cost?.total?.expected || totalHours * 85;

  // Initialize MVP features: default to HIGH or CRITICAL features
  const [selectedFeatureIds, setSelectedFeatureIds] = useState<number[]>(() => {
    return features
      .filter((f) => {
        const p = (f.priority || '').toUpperCase();
        return p === 'CRITICAL' || p === 'HIGH';
      })
      .map((f) => f.id);
  });

  const toggleFeature = (id: number) => {
    setSelectedFeatureIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const selectAll = () => {
    setSelectedFeatureIds(features.map((f) => f.id));
  };

  const selectRecommended = () => {
    setSelectedFeatureIds(
      features
        .filter((f) => {
          const p = (f.priority || '').toUpperCase();
          return p === 'CRITICAL' || p === 'HIGH';
        })
        .map((f) => f.id)
    );
  };

  // Recalculate MVP Metrics
  const mvpTasks = tasks.filter(
    (t) => t.is_global || (t.feature_id && selectedFeatureIds.includes(t.feature_id))
  );

  const mvpHours = mvpTasks.reduce((sum, t) => sum + (t.estimated_hours || 0), 0);
  const hourRatio = totalHours > 0 ? mvpHours / totalHours : 0.6;
  const mvpCost = Math.round(totalCost * hourRatio);
  const fullWeeks = Math.max(4, Math.round(totalHours / 20));
  const mvpWeeks = Math.max(2, Math.round(mvpHours / 20));
  const timeSavedPercent = Math.max(
    0,
    Math.round(((totalHours - mvpHours) / totalHours) * 100)
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Minimum Viable Product (MVP) Scoping Tool</h2>
          <p className="text-xs text-slate-500">
            Select essential features for early market validation and calculate accelerated time-to-market.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={selectRecommended}
            className="px-3 py-1.5 rounded-xl border border-sky-200 bg-sky-50 hover:bg-sky-100 text-sky-700 text-xs font-bold transition-colors flex items-center space-x-1"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Recommended Preset</span>
          </button>
          <button
            onClick={selectAll}
            className="px-3 py-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold transition-colors"
          >
            Select All
          </button>
        </div>
      </div>

      {/* Comparison Scoreboard */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* MVP Effort */}
        <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-emerald-700 text-xs font-bold uppercase tracking-wider">
            <span>MVP Development Effort</span>
            <Clock className="w-4 h-4" />
          </div>
          <div className="text-3xl font-black text-slate-900">{mvpHours.toFixed(0)} Hours</div>
          <div className="flex items-center space-x-1 text-xs text-emerald-700 font-semibold pt-1">
            <ArrowDownRight className="w-4 h-4 text-emerald-600" />
            <span>-{timeSavedPercent}% effort reduction vs full scope</span>
          </div>
        </div>

        {/* MVP Budget */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider">
            <span>Target MVP Budget</span>
            <DollarSign className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-3xl font-black text-slate-900">${mvpCost.toLocaleString()}</div>
          <p className="text-xs text-slate-500 pt-1">
            Original full scope: <strong>${totalCost.toLocaleString()}</strong>
          </p>
        </div>

        {/* Time to Market */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider">
            <span>Launch Timeline</span>
            <Rocket className="w-4 h-4 text-purple-600" />
          </div>
          <div className="text-3xl font-black text-purple-700">~{mvpWeeks} Weeks</div>
          <p className="text-xs text-slate-500 pt-1">
            vs <strong>{fullWeeks} weeks</strong> for full product release
          </p>
        </div>
      </div>

      {/* Feature Selection Grid */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4 shadow-sm">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-sky-600" />
            <span>Toggle Features (MVP Core vs Phase 2 Backlog)</span>
          </h3>
          <span className="text-xs text-slate-400 font-medium">
            {selectedFeatureIds.length} of {features.length} features included in MVP
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {features.map((feature) => {
            const isIncluded = selectedFeatureIds.includes(feature.id);
            const featureTasks = tasks.filter((t) => t.feature_id === feature.id);
            const hours = featureTasks.reduce((sum, t) => sum + (t.estimated_hours || 0), 0);

            return (
              <div
                key={feature.id}
                onClick={() => toggleFeature(feature.id)}
                className={`p-4 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${
                  isIncluded
                    ? 'border-sky-400 bg-sky-50/40 shadow-sm'
                    : 'border-slate-200 bg-slate-50/40 opacity-70 hover:opacity-100'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    checked={isIncluded}
                    onChange={() => {}}
                    className="mt-1 w-4 h-4 rounded text-sky-600 focus:ring-sky-500 border-slate-300 pointer-events-none"
                  />
                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-bold text-xs text-slate-900">
                        {feature.canonical_name.replace(/_/g, ' ')}
                      </h4>
                      <span className="text-[10px] font-semibold text-slate-500 bg-white px-1.5 py-0.5 rounded border border-slate-200">
                        {feature.priority}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                      {feature.description}
                    </p>
                  </div>
                </div>

                <div className="text-right shrink-0 pl-2">
                  <span className="text-xs font-bold text-slate-800">~{hours.toFixed(0)}h</span>
                  <div className="text-[10px] text-slate-400 font-medium">
                    {isIncluded ? 'MVP Core' : 'Phase 2'}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
