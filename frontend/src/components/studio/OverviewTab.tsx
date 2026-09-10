'use client';

import React from 'react';
import { ProjectAnalysisResult } from '../../types/project';
import {
  Sparkles,
  Clock,
  DollarSign,
  Calendar,
  AlertTriangle,
  Cpu,
  Layers,
  BookOpen,
  CheckCircle2,
  HelpCircle,
  TrendingUp,
  Percent,
} from 'lucide-react';

interface OverviewTabProps {
  result: ProjectAnalysisResult;
}

export const OverviewTab: React.FC<OverviewTabProps> = ({ result }) => {
  const hybrid = result.hybrid_estimate;
  const explanation = result.explanation;
  const totalHours = result.total_estimated_hours || 100;
  const totalCost = result.cost?.total?.expected || Math.round(totalHours * 85);
  const workingDays = result.timeline?.total_working_days || Math.round(totalHours / 16);
  const riskLevel = result.risk_level || 'HIGH';

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Executive Summary Card */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-sky-900 via-indigo-950 to-slate-900 text-white shadow-xl space-y-4">
        <div className="flex items-center space-x-2 text-sky-400 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Executive Project Scope Dossier</span>
        </div>

        <h2 className="text-xl sm:text-2xl font-black tracking-tight">
          {result.project?.name || 'Project Overview'}
        </h2>

        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-3xl">
          {explanation?.summary ||
            `This software project encompasses ${result.features.length} core functional features decomposed into ${result.tasks.length} atomic engineering tasks. The estimated baseline requires ${totalHours.toFixed(0)} hours across frontend, backend, database, QA, and cloud disciplines.`}
        </p>

        {/* 4 Metrics in Hero */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-white/10 text-xs">
          <div>
            <div className="text-[11px] text-slate-400 font-medium">Estimated Effort</div>
            <div className="text-lg sm:text-xl font-black text-white">{totalHours.toFixed(0)} Hours</div>
          </div>
          <div>
            <div className="text-[11px] text-slate-400 font-medium">Projected Budget</div>
            <div className="text-lg sm:text-xl font-black text-emerald-400">
              ${totalCost.toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-[11px] text-slate-400 font-medium">Target Schedule</div>
            <div className="text-lg sm:text-xl font-black text-sky-400">{workingDays} Working Days</div>
          </div>
          <div>
            <div className="text-[11px] text-slate-400 font-medium">Risk Level</div>
            <div className="text-lg sm:text-xl font-black text-amber-400">{riskLevel}</div>
          </div>
        </div>
      </div>

      {/* Phase 17 Hybrid ML Estimation Breakdown */}
      {hybrid && (
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2.5">
              <div className="p-2 rounded-xl bg-purple-50 text-purple-700">
                <Cpu className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
                  <span>Hybrid ML Estimation Engine</span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-100 text-purple-800">
                    Phase 17
                  </span>
                </h3>
                <p className="text-[11px] text-slate-500">
                  Reconciled output combining rule-based heuristics and trained regression models
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <span className="text-xs font-semibold text-slate-500">Method:</span>
              <span className="text-xs font-bold text-purple-800 bg-purple-50 border border-purple-200 px-2.5 py-1 rounded-lg">
                {hybrid.reconciliation_method || 'Balanced'}
              </span>
              <span className="text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-lg">
                {Math.round(hybrid.confidence * 100)}% Confidence
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            {/* Rule Based */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-[11px] text-slate-500 font-bold uppercase">Rule-Based Engine</div>
              <div className="text-xl font-black text-slate-900">
                {hybrid.breakdown?.rule_based?.toFixed(1) || '--'} hrs
              </div>
              <p className="text-[11px] text-slate-500">
                Weight: <strong>{Math.round((hybrid.weights_used?.rule || 0.5) * 100)}%</strong>
              </p>
            </div>

            {/* ML Prediction */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-[11px] text-slate-500 font-bold uppercase">ML Regression Model</div>
              <div className="text-xl font-black text-purple-700">
                {hybrid.breakdown?.ml_prediction?.toFixed(1) || '--'} hrs
              </div>
              <p className="text-[11px] text-slate-500">
                Weight: <strong>{Math.round((hybrid.weights_used?.ml || 0.5) * 100)}%</strong>
              </p>
            </div>

            {/* Final Hybrid */}
            <div className="p-4 rounded-xl bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-200 space-y-1">
              <div className="text-[11px] text-purple-700 font-bold uppercase">Reconciled Final Effort</div>
              <div className="text-xl font-black text-indigo-900">
                {hybrid.final_estimate?.toFixed(1)} hrs
              </div>
              <p className="text-[11px] text-purple-700 font-medium">
                Range: {hybrid.range?.min?.toFixed(0)}h – {hybrid.range?.max?.toFixed(0)}h
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Phase 18 Explainable AI Breakdown */}
      {explanation && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-5 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-sm text-slate-900 flex items-center space-x-2">
              <BookOpen className="w-4 h-4 text-sky-600" />
              <span>Explainable AI Scoping Factors</span>
            </h3>
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Audit Transparency
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {Object.entries(explanation.explanations || {}).map(([key, value]) => (
              <div key={key} className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold capitalize text-slate-800 text-[11px] block">
                  {key} Analysis
                </span>
                <p className="text-slate-600 leading-relaxed text-[11px]">{value}</p>
              </div>
            ))}
          </div>

          {/* Assumptions and Limitations */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-slate-100 text-xs">
            <div className="space-y-2">
              <span className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
                Stated Assumptions:
              </span>
              <ul className="space-y-1 text-slate-600 list-disc pl-4 text-[11px]">
                {(explanation.assumptions || []).slice(0, 4).map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </div>

            <div className="space-y-2">
              <span className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
                Scope Boundaries & Limitations:
              </span>
              <ul className="space-y-1 text-slate-600 list-disc pl-4 text-[11px]">
                {(explanation.limitations || []).slice(0, 4).map((l, i) => (
                  <li key={i}>{l}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
