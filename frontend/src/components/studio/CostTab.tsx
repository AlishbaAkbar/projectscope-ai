'use client';

import React, { useState } from 'react';
import { ProjectAnalysisResult } from '../../types/project';
import {
  DollarSign,
  TrendingDown,
  TrendingUp,
  ShieldCheck,
  Percent,
  Sliders,
  PieChart,
  HelpCircle,
} from 'lucide-react';

interface CostTabProps {
  result: ProjectAnalysisResult;
}

export const CostTab: React.FC<CostTabProps> = ({ result }) => {
  const [rateMultiplier, setRateMultiplier] = useState(1.0);

  const costData = result.cost;
  const summary = result.summary || {};
  const totalHours = result.total_estimated_hours || 100;

  // Calculate baseline amounts
  const expectedBase = costData?.total?.expected || totalHours * 75;
  const bestCase = costData?.total?.best_case || Math.round(expectedBase * 0.85);
  const worstCase = costData?.total?.worst_case || Math.round(expectedBase * 1.35);

  const adjustedExpected = Math.round(expectedBase * rateMultiplier);
  const adjustedBest = Math.round(bestCase * rateMultiplier);
  const adjustedWorst = Math.round(worstCase * rateMultiplier);

  const contingencyAmount = Math.round(adjustedExpected * 0.15);

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Financial Effort & Cost Modeling</h2>
          <p className="text-xs text-slate-500">
            Three-point financial projections calibrated against discipline rates and scope volatility.
          </p>
        </div>

        {/* Rate Multiplier Slider */}
        <div className="flex items-center space-x-2 bg-slate-100 p-2 rounded-xl border border-slate-200 text-xs">
          <Sliders className="w-3.5 h-3.5 text-slate-500" />
          <span className="font-semibold text-slate-600">Rate Tier:</span>
          <select
            value={rateMultiplier}
            onChange={(e) => setRateMultiplier(parseFloat(e.target.value))}
            className="bg-white px-2 py-1 rounded-lg border border-slate-200 font-bold text-slate-800 text-xs focus:outline-none"
          >
            <option value="0.75">Nearshore / Regional (0.75x)</option>
            <option value="1.0">Standard Market (1.0x)</option>
            <option value="1.35">Tier-1 Enterprise / Specialist (1.35x)</option>
          </select>
        </div>
      </div>

      {/* 3-Point Estimate Hero Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Best Case */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-emerald-300 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-emerald-600">
            <span className="text-xs font-bold uppercase tracking-wider">Best-Case Budget</span>
            <TrendingDown className="w-4 h-4" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            ${adjustedBest.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Optimal path with zero requirement volatility and clean 3rd-party integrations.
          </p>
        </div>

        {/* Expected Case */}
        <div className="p-5 rounded-2xl bg-gradient-to-br from-sky-50 to-indigo-50 border border-sky-300 shadow-md space-y-2 relative overflow-hidden">
          <div className="absolute top-2 right-2 text-[10px] font-bold uppercase tracking-wider bg-sky-600 text-white px-2 py-0.5 rounded-full">
            Recommended
          </div>
          <div className="flex items-center justify-between text-sky-700">
            <span className="text-xs font-bold uppercase tracking-wider">Expected Investment</span>
            <DollarSign className="w-4 h-4" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            ${adjustedExpected.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed">
            Calibrated baseline incorporating standard QA cycles, iterations, and sprint ceremonies.
          </p>
        </div>

        {/* Worst Case */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-amber-300 shadow-sm space-y-2">
          <div className="flex items-center justify-between text-amber-600">
            <span className="text-xs font-bold uppercase tracking-wider">Worst-Case Ceiling</span>
            <TrendingUp className="w-4 h-4" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            ${adjustedWorst.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Conservative upper bound accounting for external API delays and edge-case testing.
          </p>
        </div>
      </div>

      {/* Contingency Buffer Summary */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-2 text-slate-700">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>
            Recommended <strong>15% Risk Contingency Buffer</strong>:{' '}
            <span className="font-bold text-slate-900">${contingencyAmount.toLocaleString()}</span>
          </span>
        </div>
        <span className="text-[11px] text-slate-500">
          Average Blended Rate: <strong>${Math.round((adjustedExpected / totalHours))} / hour</strong>
        </span>
      </div>

      {/* Cost by Role Table */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="px-6 py-4 border-b border-slate-100 font-bold text-sm text-slate-900">
          Budget Allocation by Discipline & Role
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
              <tr>
                <th className="px-6 py-3">Engineering Discipline</th>
                <th className="px-6 py-3">Allocated Hours</th>
                <th className="px-6 py-3">Hourly Rate</th>
                <th className="px-6 py-3">Estimated Investment</th>
                <th className="px-6 py-3">% of Project Budget</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {Object.entries(summary).map(([role, data]) => {
                const hours = data.total_hours || 0;
                const pct = Math.round((hours / totalHours) * 100);
                const roleCost = Math.round((data.estimated_cost || hours * 85) * rateMultiplier);

                return (
                  <tr key={role} className="hover:bg-slate-50/70 transition-colors">
                    <td className="px-6 py-3.5 font-bold text-slate-900">{role}</td>
                    <td className="px-6 py-3.5 text-slate-600 font-medium">{hours.toFixed(0)} hrs</td>
                    <td className="px-6 py-3.5 text-slate-600 font-medium">
                      ${Math.round(85 * rateMultiplier)}/hr
                    </td>
                    <td className="px-6 py-3.5 font-bold text-slate-900">
                      ${roleCost.toLocaleString()}
                    </td>
                    <td className="px-6 py-3.5">
                      <div className="flex items-center space-x-2">
                        <span className="text-slate-600 font-medium w-8">{pct}%</span>
                        <div className="w-20 h-1.5 rounded-full bg-slate-100 overflow-hidden">
                          <div
                            className="h-full bg-sky-600 rounded-full"
                            style={{ width: `${Math.min(100, pct)}%` }}
                          />
                        </div>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
