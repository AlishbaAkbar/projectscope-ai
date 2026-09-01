import React, { useState } from 'react';
import {
  Sparkles,
  Users,
  CheckCircle2,
  AlertTriangle,
  Layers,
  ListTodo,
  Clock,
  Download,
  Copy,
  Check,
  RefreshCw,
  Tag,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Cpu,
} from 'lucide-react';
import { ProjectAnalysisResult, Requirement, Feature, Task } from '../types/project';

interface AnalysisResultsProps {
  result: ProjectAnalysisResult;
  onReanalyze: () => Promise<void>;
  isReanalyzing: boolean;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({
  result,
  onReanalyze,
  isReanalyzing,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'requirements' | 'features' | 'tasks' | 'uncertainties'>('overview');
  const [reqFilter, setReqFilter] = useState<string>('all');
  const [copied, setCopied] = useState(false);
  const [expandedFeatures, setExpandedFeatures] = useState<Record<number, boolean>>({});

  const toggleFeatureExpand = (featureId: number) => {
    setExpandedFeatures((prev) => ({
      ...prev,
      [featureId]: !prev[featureId],
    }));
  };

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadJson = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${result.project.name.toLowerCase().replace(/\s+/g, '_')}_analysis.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredRequirements = result.requirements.filter((req) => {
    if (reqFilter === 'all') return true;
    return req.category.toLowerCase() === reqFilter.toLowerCase();
  });

  const getPriorityBadgeClass = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'high':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'medium':
        return 'bg-sky-50 text-sky-700 border-sky-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  const getComplexityBadgeClass = (complexity: string) => {
    switch (complexity.toLowerCase()) {
      case 'high':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'medium':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      default:
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    }
  };

  const getCategoryBadgeClass = (category: string) => {
    switch (category.toLowerCase()) {
      case 'frontend':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'backend':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'database':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200';
      case 'qa':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'integration':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6 mt-8 animate-in fade-in duration-300">
      {/* Header Banner Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="inline-flex items-center rounded-lg bg-sky-100 px-2.5 py-0.5 text-xs font-semibold text-sky-800 uppercase tracking-wider">
                {result.project_type.replace('_', ' ')}
              </span>
              <span className="inline-flex items-center rounded-lg bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700">
                {result.project.platform}
              </span>
              <span className="inline-flex items-center rounded-lg bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700 border border-emerald-200">
                Validated Schema
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              {result.project.name}
            </h1>
            <p className="text-sm text-slate-600 mt-2 max-w-3xl leading-relaxed">
              {result.project.description}
            </p>

            {/* Target Personas */}
            {result.users && result.users.length > 0 && (
              <div className="flex flex-wrap items-center gap-2 mt-4 pt-3 border-t border-slate-100">
                <span className="text-xs font-semibold text-slate-500 flex items-center gap-1">
                  <Users className="h-3.5 w-3.5" /> Target Personas:
                </span>
                {result.users.map((user, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-700"
                  >
                    @{user}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap lg:flex-col gap-2 shrink-0">
            <button
              onClick={onReanalyze}
              disabled={isReanalyzing}
              className="inline-flex items-center justify-center space-x-1.5 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-60 transition"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${isReanalyzing ? 'animate-spin' : ''}`} />
              <span>{isReanalyzing ? 'Re-analyzing...' : 'Re-analyze'}</span>
            </button>

            <button
              onClick={handleCopyJson}
              className="inline-flex items-center justify-center space-x-1.5 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5 text-slate-500" />}
              <span>{copied ? 'Copied JSON' : 'Copy JSON'}</span>
            </button>

            <button
              onClick={handleDownloadJson}
              className="inline-flex items-center justify-center space-x-1.5 rounded-xl bg-slate-900 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-800 transition"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Export Spec</span>
            </button>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-100">
          <div className="rounded-xl bg-slate-50/70 p-3.5 border border-slate-100">
            <div className="text-xs font-medium text-slate-500">Requirements</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">{result.requirements.length}</div>
          </div>
          <div className="rounded-xl bg-slate-50/70 p-3.5 border border-slate-100">
            <div className="text-xs font-medium text-slate-500">Features</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">{result.features.length}</div>
          </div>
          <div className="rounded-xl bg-slate-50/70 p-3.5 border border-slate-100">
            <div className="text-xs font-medium text-slate-500">Development Tasks</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">{result.total_tasks_count}</div>
          </div>
          <div className="rounded-xl bg-sky-50/70 p-3.5 border border-sky-100">
            <div className="text-xs font-medium text-sky-700">Baseline Hours</div>
            <div className="text-xl font-bold text-sky-900 mt-0.5">~{result.total_estimated_hours} hrs</div>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-slate-200 bg-white rounded-xl px-3 pt-2 shadow-sm overflow-x-auto">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex items-center space-x-2 py-3 px-4 text-xs font-semibold border-b-2 whitespace-nowrap transition ${
            activeTab === 'overview'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Cpu className="h-4 w-4" />
          <span>Full Architecture Plan</span>
        </button>

        <button
          onClick={() => setActiveTab('requirements')}
          className={`flex items-center space-x-2 py-3 px-4 text-xs font-semibold border-b-2 whitespace-nowrap transition ${
            activeTab === 'requirements'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <CheckCircle2 className="h-4 w-4" />
          <span>Requirements ({result.requirements.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('features')}
          className={`flex items-center space-x-2 py-3 px-4 text-xs font-semibold border-b-2 whitespace-nowrap transition ${
            activeTab === 'features'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Layers className="h-4 w-4" />
          <span>Features & Normalization ({result.features.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('tasks')}
          className={`flex items-center space-x-2 py-3 px-4 text-xs font-semibold border-b-2 whitespace-nowrap transition ${
            activeTab === 'tasks'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <ListTodo className="h-4 w-4" />
          <span>Baseline Tasks ({result.total_tasks_count})</span>
        </button>

        <button
          onClick={() => setActiveTab('uncertainties')}
          className={`flex items-center space-x-2 py-3 px-4 text-xs font-semibold border-b-2 whitespace-nowrap transition ${
            activeTab === 'uncertainties'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <AlertTriangle className="h-4 w-4" />
          <span>Missing Specs & Assumptions ({result.missing_information.length + result.assumptions.length})</span>
        </button>
      </div>

      {/* Tab Contents */}

      {/* 1. Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Features Grid */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Layers className="h-5 w-5 text-sky-600" />
                <h2 className="text-lg font-bold text-slate-900">Extracted Features & Normalization</h2>
              </div>
              <span className="text-xs text-slate-500">Mapped via Canonical Dictionary</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.features.map((feature) => (
                <div
                  key={feature.id}
                  className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 hover:border-sky-200 hover:bg-white transition"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="text-sm font-bold text-slate-900 capitalize">
                        {feature.name.replace(/_/g, ' ')}
                      </h3>
                      <div className="mt-1 flex flex-wrap items-center gap-1.5">
                        <span className="inline-flex items-center rounded-md bg-slate-200/80 px-2 py-0.5 text-[11px] font-mono font-semibold text-slate-800">
                          {feature.normalized_key}
                        </span>
                        <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-[10px] font-semibold border ${getPriorityBadgeClass(feature.priority)}`}>
                          Priority: {feature.priority}
                        </span>
                        <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-[10px] font-semibold border ${getComplexityBadgeClass(feature.complexity)}`}>
                          Complexity: {feature.complexity}
                        </span>
                      </div>
                    </div>
                    <span className="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded-md border border-slate-200 shrink-0">
                      {Math.round(feature.confidence * 100)}% conf
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 mt-2.5 leading-relaxed">
                    {feature.description}
                  </p>

                  <div className="mt-3 pt-2.5 border-t border-slate-200/60 flex items-center justify-between text-xs text-slate-500">
                    <span>{feature.tasks.length} baseline development tasks</span>
                    <button
                      onClick={() => {
                        setActiveTab('tasks');
                        setExpandedFeatures({ [feature.id]: true });
                      }}
                      className="text-sky-600 hover:text-sky-800 font-medium"
                    >
                      View tasks →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Missing Information & Assumptions Callout */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-6 shadow-sm">
              <div className="flex items-center space-x-2 text-amber-900 font-bold mb-3">
                <AlertTriangle className="h-5 w-5 text-amber-600" />
                <h3>Missing Information / Ambiguities</h3>
              </div>
              <p className="text-xs text-amber-800 mb-3">
                Questions or specifications requiring clarification prior to final timeline estimation:
              </p>
              <ul className="space-y-2">
                {result.missing_information.map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-2 text-xs text-amber-950">
                    <span className="text-amber-500 font-bold mt-0.5">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-2xl border border-sky-200 bg-sky-50/60 p-6 shadow-sm">
              <div className="flex items-center space-x-2 text-sky-900 font-bold mb-3">
                <HelpCircle className="h-5 w-5 text-sky-600" />
                <h3>Architectural Assumptions</h3>
              </div>
              <p className="text-xs text-sky-800 mb-3">
                Baseline architectural and operational assumptions made from the prompt:
              </p>
              <ul className="space-y-2">
                {result.assumptions.map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-2 text-xs text-sky-950">
                    <span className="text-sky-500 font-bold mt-0.5">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* 2. Requirements Tab */}
      {activeTab === 'requirements' && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Extracted Requirements</h2>
              <p className="text-xs text-slate-500">Atomic functional and non-functional specifications with confidence ratings</p>
            </div>

            {/* Category Filter */}
            <div className="flex items-center space-x-1.5 bg-slate-100 p-1 rounded-xl">
              {['all', 'functional', 'non_functional'].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setReqFilter(cat)}
                  className={`px-3 py-1 text-xs font-semibold rounded-lg capitalize transition ${
                    reqFilter === cat
                      ? 'bg-white text-slate-900 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {cat.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            {filteredRequirements.map((req, idx) => (
              <div
                key={req.id || idx}
                className="flex items-start justify-between gap-4 rounded-xl border border-slate-200/80 bg-slate-50/40 p-4 hover:bg-white hover:border-sky-200 transition"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span
                      className={`inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wider border ${
                        req.category.toLowerCase().includes('non')
                          ? 'bg-purple-50 text-purple-700 border-purple-200'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      }`}
                    >
                      {req.category.replace('_', ' ')}
                    </span>
                    <span className="text-[11px] text-slate-400">Source: {req.source}</span>
                  </div>
                  <p className="text-sm text-slate-800 leading-relaxed font-medium">
                    {req.text}
                  </p>
                </div>

                <div className="shrink-0 flex flex-col items-end">
                  <span className="text-xs font-bold text-slate-700">
                    {Math.round(req.confidence * 100)}%
                  </span>
                  <span className="text-[10px] text-slate-400">Confidence</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Features Tab */}
      {activeTab === 'features' && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Feature Taxonomy & Normalization</h2>
            <p className="text-xs text-slate-500">Every identified feature is normalized against standard canonical architecture keys</p>
          </div>

          <div className="space-y-4">
            {result.features.map((feature) => (
              <div
                key={feature.id}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm space-y-3"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-base font-bold text-slate-900 capitalize">
                      {feature.name.replace(/_/g, ' ')}
                    </h3>
                    <span className="inline-flex items-center rounded-lg bg-sky-100 px-2.5 py-0.5 text-xs font-mono font-bold text-sky-900 border border-sky-200">
                      → Canonical: {feature.normalized_key}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className={`inline-flex items-center rounded-md px-2.5 py-0.5 text-xs font-semibold border ${getPriorityBadgeClass(feature.priority)}`}>
                      Priority: {feature.priority}
                    </span>
                    <span className={`inline-flex items-center rounded-md px-2.5 py-0.5 text-xs font-semibold border ${getComplexityBadgeClass(feature.complexity)}`}>
                      Complexity: {feature.complexity}
                    </span>
                  </div>
                </div>

                <p className="text-sm text-slate-700 leading-relaxed">
                  {feature.description}
                </p>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <div className="flex items-center space-x-2">
                    <span>Confidence: <strong>{Math.round(feature.confidence * 100)}%</strong></span>
                    <span>•</span>
                    <span>Decomposed into <strong>{feature.tasks.length} tasks</strong></span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. Tasks Tab */}
      {activeTab === 'tasks' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Deterministic Task Decomposition</h2>
                <p className="text-xs text-slate-500">
                  Development tasks grouped by feature across disciplines (Frontend, Backend, Database, QA, Integration).
                </p>
              </div>

              <div className="flex items-center space-x-3">
                <button
                  onClick={() => {
                    const allExpanded: Record<number, boolean> = {};
                    result.features.forEach((f) => (allExpanded[f.id] = true));
                    setExpandedFeatures(allExpanded);
                  }}
                  className="text-xs font-medium text-slate-600 hover:text-slate-900 underline"
                >
                  Expand All
                </button>
                <span className="text-slate-300">|</span>
                <button
                  onClick={() => setExpandedFeatures({})}
                  className="text-xs font-medium text-slate-600 hover:text-slate-900 underline"
                >
                  Collapse All
                </button>
              </div>
            </div>

            <div className="mt-6 space-y-4">
              {result.features.map((feature) => {
                const isExpanded = expandedFeatures[feature.id] ?? true;
                const featureHours = feature.tasks.reduce((sum, t) => sum + (t.estimated_hours || 0), 0);

                return (
                  <div
                    key={feature.id}
                    className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden"
                  >
                    {/* Feature Accordion Header */}
                    <button
                      onClick={() => toggleFeatureExpand(feature.id)}
                      className="w-full flex items-center justify-between p-4 bg-slate-50/70 hover:bg-slate-100/70 transition text-left"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-100 text-sky-700 font-bold text-xs">
                          {feature.normalized_key.charAt(0)}
                        </div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-bold text-slate-900 capitalize">
                              {feature.name.replace(/_/g, ' ')}
                            </span>
                            <span className="text-xs font-mono text-slate-500">
                              ({feature.normalized_key})
                            </span>
                          </div>
                          <p className="text-xs text-slate-500">
                            {feature.tasks.length} tasks • ~{featureHours} estimated baseline hours
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        {isExpanded ? (
                          <ChevronUp className="h-4 w-4 text-slate-500" />
                        ) : (
                          <ChevronDown className="h-4 w-4 text-slate-500" />
                        )}
                      </div>
                    </button>

                    {/* Tasks List */}
                    {isExpanded && (
                      <div className="p-4 space-y-3 bg-white divide-y divide-slate-100">
                        {feature.tasks.map((task) => (
                          <div
                            key={task.id}
                            className="pt-3 first:pt-0 flex flex-col sm:flex-row sm:items-start justify-between gap-3"
                          >
                            <div className="space-y-1">
                              <div className="flex items-center gap-2">
                                <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-[10px] font-bold border uppercase tracking-wider ${getCategoryBadgeClass(task.category)}`}>
                                  {task.category}
                                </span>
                                <h4 className="text-xs font-bold text-slate-900">
                                  {task.title}
                                </h4>
                              </div>
                              <p className="text-xs text-slate-600 leading-relaxed pl-1">
                                {task.description}
                              </p>
                            </div>

                            {task.estimated_hours && (
                              <div className="shrink-0 flex items-center space-x-1 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700">
                                <Clock className="h-3 w-3 text-slate-500" />
                                <span>{task.estimated_hours}h</span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 5. Uncertainties Tab */}
      {activeTab === 'uncertainties' && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-amber-200 bg-white p-6 shadow-sm">
            <div className="flex items-center space-x-2 text-amber-900 font-bold mb-4">
              <AlertTriangle className="h-5 w-5 text-amber-600" />
              <h2 className="text-lg">Unstated Requirements & Questions ({result.missing_information.length})</h2>
            </div>

            <div className="space-y-3">
              {result.missing_information.map((item, idx) => (
                <div
                  key={idx}
                  className="rounded-xl border border-amber-100 bg-amber-50/40 p-4 text-xs text-amber-950 font-medium leading-relaxed flex items-start space-x-3"
                >
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-amber-200 text-amber-800 font-bold text-[11px]">
                    {idx + 1}
                  </span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-sky-200 bg-white p-6 shadow-sm">
            <div className="flex items-center space-x-2 text-sky-900 font-bold mb-4">
              <HelpCircle className="h-5 w-5 text-sky-600" />
              <h2 className="text-lg">System Assumptions ({result.assumptions.length})</h2>
            </div>

            <div className="space-y-3">
              {result.assumptions.map((item, idx) => (
                <div
                  key={idx}
                  className="rounded-xl border border-sky-100 bg-sky-50/40 p-4 text-xs text-sky-950 font-medium leading-relaxed flex items-start space-x-3"
                >
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-sky-200 text-sky-800 font-bold text-[11px]">
                    {idx + 1}
                  </span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
