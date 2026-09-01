import React, { useEffect, useState } from 'react';
import { Sparkles, CheckCircle2, Clock, Brain, Check, Database, FileText, Layers, ListChecks } from 'lucide-react';

interface AnalysisProgressProps {
  isLoading: boolean;
}

const STEPS = [
  { id: 1, label: 'Formulating Analysis Prompt', icon: FileText, desc: 'Constructing architect persona & requirements prompt' },
  { id: 2, label: 'Querying LLM Requirement Analyzer', icon: Brain, desc: 'Generating structured project domain breakdown' },
  { id: 3, label: 'Validating Pydantic JSON Schema', icon: Check, desc: 'Verifying data types, requirements, and confidence bounds' },
  { id: 4, label: 'Normalizing Features to Canonical Dictionary', icon: Layers, desc: 'Mapping synonyms to standard architecture keys' },
  { id: 5, label: 'Generating Baseline Engineering Tasks', icon: ListChecks, desc: 'Decomposing into Frontend, Backend, DB & QA work items' },
  { id: 6, label: 'Persisting Scoping Plan to Database', icon: Database, desc: 'Committing atomic transaction & preparing dashboard' },
];

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ isLoading }) => {
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    if (!isLoading) {
      setCurrentStep(1);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length ? prev + 1 : prev));
    }, 450);

    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading) return null;

  return (
    <div className="w-full max-w-4xl mx-auto my-8 rounded-2xl border border-sky-200 bg-gradient-to-b from-sky-50/70 to-white p-6 shadow-sm">
      <div className="flex items-center space-x-3 mb-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-500 text-white animate-pulse">
          <Sparkles className="h-4 w-4" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-900">AI Requirement Pipeline in Progress</h3>
          <p className="text-xs text-slate-500">Executing deterministic extraction and validation phases...</p>
        </div>
      </div>

      <div className="space-y-3">
        {STEPS.map((step) => {
          const isDone = currentStep > step.id;
          const isCurrent = currentStep === step.id;
          const Icon = step.icon;

          return (
            <div
              key={step.id}
              className={`flex items-center justify-between rounded-xl p-3 border transition-all ${
                isCurrent
                  ? 'border-sky-300 bg-sky-50/80 shadow-sm'
                  : isDone
                  ? 'border-emerald-100 bg-emerald-50/40 text-emerald-900'
                  : 'border-slate-100 bg-white/50 text-slate-400 opacity-60'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div
                  className={`flex h-7 w-7 items-center justify-center rounded-lg ${
                    isDone
                      ? 'bg-emerald-500 text-white'
                      : isCurrent
                      ? 'bg-sky-500 text-white animate-spin'
                      : 'bg-slate-100 text-slate-400'
                  }`}
                >
                  {isDone ? <CheckCircle2 className="h-4 w-4" /> : <Icon className="h-3.5 w-3.5" />}
                </div>
                <div>
                  <div className={`text-xs font-semibold ${isCurrent ? 'text-sky-900' : isDone ? 'text-emerald-950' : 'text-slate-500'}`}>
                    {step.label}
                  </div>
                  <div className="text-[11px] text-slate-500">{step.desc}</div>
                </div>
              </div>

              <div>
                {isDone && <span className="text-[11px] font-medium text-emerald-600 bg-emerald-100/70 px-2 py-0.5 rounded-md">Verified</span>}
                {isCurrent && <span className="text-[11px] font-medium text-sky-600 bg-sky-100/70 px-2 py-0.5 rounded-md animate-pulse">Running</span>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
