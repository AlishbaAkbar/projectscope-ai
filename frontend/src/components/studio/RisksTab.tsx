'use client';

import React from 'react';
import { ProjectAnalysisResult, RiskItem } from '../../types/project';
import {
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  HelpCircle,
  User,
  Zap,
} from 'lucide-react';

interface RisksTabProps {
  result: ProjectAnalysisResult;
}

const DEFAULT_RISKS: RiskItem[] = [
  {
    id: 'risk-1',
    name: '3rd-Party Gateway Integration & Latency',
    description: 'External API service rate limits, webhook delivery dropouts, or protocol changes could disrupt checkout and notifications.',
    category: 'Technical / Integration',
    probability: 'HIGH',
    impact: 'HIGH',
    risk_level: 'HIGH',
    mitigation: 'Implement idempotent retry queues, exponential backoff, and asynchronous background worker processing.',
    contingency: 'Fallback to circuit breakers and cached responses to prevent cascading service downtime.',
    owner: 'Senior Backend Engineer',
    score: 8.5,
  },
  {
    id: 'risk-2',
    name: 'User Data Protection & Compliance (PCI / GDPR)',
    description: 'Handling sensitive customer credentials and payment tokens creates regulatory audit requirements.',
    category: 'Security / Compliance',
    probability: 'MEDIUM',
    impact: 'HIGH',
    risk_level: 'HIGH',
    mitigation: 'Delegate tokenization to PCI-DSS Level 1 certified gateways (e.g. Stripe Elements). Never log PANs.',
    contingency: 'Execute quarterly third-party vulnerability scans and enable automated database encryption at rest.',
    owner: 'Security / DevOps Engineer',
    score: 7.8,
  },
  {
    id: 'risk-3',
    name: 'Requirement Volatility & Feature Creep',
    description: 'Adding dynamic modifications to checkout flows during mid-sprint cycles causes delivery slippage.',
    category: 'Project Management',
    probability: 'HIGH',
    impact: 'MEDIUM',
    risk_level: 'MEDIUM',
    mitigation: 'Establish a strict Change Control Process and freeze sprint scope post-grooming.',
    contingency: 'Defer non-essential enhancements to Phase 2 backlog.',
    owner: 'Technical Project Manager',
    score: 6.4,
  },
  {
    id: 'risk-4',
    name: 'Database Query Bottlenecks Under High Load',
    description: 'Unindexed relational queries on product listings or telemetry can degrade response times past 1.5s.',
    category: 'Performance',
    probability: 'MEDIUM',
    impact: 'MEDIUM',
    risk_level: 'MEDIUM',
    mitigation: 'Implement Redis caching layer for read-heavy operations and compose composite B-tree indexes.',
    contingency: 'Enable automated database read replicas and query optimization monitors.',
    owner: 'Database Administrator',
    score: 5.9,
  },
];

export const RisksTab: React.FC<RisksTabProps> = ({ result }) => {
  const riskSummary = result.risks;
  const overallRisk = result.risk_level || riskSummary?.risk_level || 'HIGH';
  const topRisks = riskSummary?.top_risks && riskSummary.top_risks.length > 0 ? riskSummary.top_risks : DEFAULT_RISKS;

  const recommendations = riskSummary?.recommendations || [
    'Enforce rigorous automated contract testing between Frontend and Backend.',
    'Isolate third-party payment and telemetry integrations behind defensive adapter layers.',
    'Reserve a 15% budget buffer for unexpected operational and cloud infrastructure overhead.',
    'Set up continuous deployment with canary testing to minimize regression blast radius.',
  ];

  const getRiskBadge = (level: string) => {
    switch (level.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-rose-100 text-rose-800 border-rose-300';
      case 'HIGH':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'MEDIUM':
        return 'bg-sky-100 text-sky-800 border-sky-300';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Risk Assessment & Mitigation Matrix</h2>
          <p className="text-xs text-slate-500">
            Systemic technical, compliance, operational, and delivery risk evaluation.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold text-slate-500">Overall Project Posture:</span>
          <span
            className={`px-3 py-1 rounded-xl text-xs font-black uppercase tracking-wider border ${getRiskBadge(
              overallRisk
            )}`}
          >
            {overallRisk} Risk
          </span>
        </div>
      </div>

      {/* Recommendations Banner */}
      <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Strategic Risk Mitigation Guidelines</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-600">
          {recommendations.map((rec, i) => (
            <div key={i} className="flex items-start space-x-2 p-2 rounded-lg bg-slate-50 border border-slate-100">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Cards */}
      <div className="space-y-4">
        {topRisks.map((risk) => (
          <div
            key={risk.id}
            className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-md transition-all space-y-4"
          >
            {/* Card Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200">
                  {risk.category}
                </span>
                <span
                  className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider border ${getRiskBadge(
                    risk.risk_level || 'HIGH'
                  )}`}
                >
                  {risk.risk_level || 'HIGH'} Severity
                </span>
              </div>

              <div className="flex items-center space-x-4 text-xs text-slate-500">
                <span>
                  Probability: <strong className="text-slate-800">{risk.probability}</strong>
                </span>
                <span>•</span>
                <span>
                  Impact: <strong className="text-slate-800">{risk.impact}</strong>
                </span>
              </div>
            </div>

            {/* Title & Description */}
            <div className="space-y-1">
              <h4 className="font-bold text-sm text-slate-900">{risk.name}</h4>
              <p className="text-xs text-slate-600 leading-relaxed">{risk.description}</p>
            </div>

            {/* Mitigations Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-slate-100 text-xs">
              <div className="p-3 rounded-xl bg-emerald-50/50 border border-emerald-100 space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 flex items-center space-x-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Preventative Mitigation</span>
                </span>
                <p className="text-[11px] text-emerald-950 leading-relaxed">{risk.mitigation}</p>
              </div>

              <div className="p-3 rounded-xl bg-sky-50/50 border border-sky-100 space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-sky-800 flex items-center space-x-1">
                  <Zap className="w-3.5 h-3.5 text-sky-600" />
                  <span>Contingency Fallback</span>
                </span>
                <p className="text-[11px] text-sky-950 leading-relaxed">{risk.contingency}</p>
              </div>
            </div>

            {/* Owner Footer */}
            <div className="pt-2 flex items-center justify-between text-[11px] text-slate-400">
              <div className="flex items-center space-x-1.5">
                <User className="w-3.5 h-3.5 text-slate-400" />
                <span>Risk Owner: <strong className="text-slate-700 font-semibold">{risk.owner}</strong></span>
              </div>
              <span>Calculated Risk Weight: {risk.score || 7.5}/10</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
