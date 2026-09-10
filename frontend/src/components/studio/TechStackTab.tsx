'use client';

import React, { useState, useEffect } from 'react';
import { ProjectAnalysisResult, TechStackData, TechRecommendationItem } from '../../types/project';
import { api } from '../../api/client';
import {
  Cpu,
  Layers,
  Server,
  Database,
  Shield,
  Cloud,
  CheckCircle2,
  ExternalLink,
  Sparkles,
  RefreshCw,
  Zap,
} from 'lucide-react';

interface TechStackTabProps {
  result: ProjectAnalysisResult;
}

const DEFAULT_STACK: TechRecommendationItem[] = [
  {
    name: 'Next.js 14 (App Router) & React 18',
    category: 'Frontend',
    role: 'Primary Client Framework',
    rationale:
      'Server-side rendering (SSR), optimized bundle splitting, built-in SEO capabilities, and vast component ecosystem (Tailwind CSS, Lucide Icons).',
    pros: ['Rapid UI velocity', 'High performance Core Web Vitals', 'Vercel / Docker portable'],
    alternatives: ['Vite + React SPA', 'Remix', 'Nuxt / Vue 3'],
  },
  {
    name: 'FastAPI (Python 3.11+)',
    category: 'Backend',
    role: 'High-Throughput REST API & AI Engine',
    rationale:
      'Native asynchronous I/O with strict Pydantic v2 validation, automatic OpenAPI / Swagger autodoc generation, and seamless integration with ML libraries.',
    pros: ['Auto Swagger UI :8000/docs', 'Zero-overhead async performance', 'Type-safe data contracts'],
    alternatives: ['Go (Gin / Fiber)', 'Node.js / NestJS', 'Django REST Framework'],
  },
  {
    name: 'PostgreSQL 16 + Redis Cache',
    category: 'Database',
    role: 'Relational Store & Low-Latency Cache',
    rationale:
      'Enterprise-grade ACID transactions with JSONB flexibility for flexible schemas, paired with Redis for session states and rate limiting.',
    pros: ['Relational integrity', 'High concurrency connection pooling', 'Fast in-memory caching'],
    alternatives: ['MySQL 8.0', 'MongoDB', 'Supabase Postgres'],
  },
  {
    name: 'JWT + OAuth2 (Auth0 / Supabase)',
    category: 'Security',
    role: 'Identity & Access Control',
    rationale:
      'Stateless bearer token authentication with role-based access control (RBAC), multi-tenant isolation, and social SSO support.',
    pros: ['Standards compliant', 'No server-side session bloat', 'Cross-platform mobile ready'],
    alternatives: ['NextAuth.js', 'Clerk', 'Firebase Auth'],
  },
  {
    name: 'Docker Containers on AWS ECS / GCP Cloud Run',
    category: 'DevOps & Cloud',
    role: 'Continuous Deployment & Orchestration',
    rationale:
      'Containerized micro-services with automatic scaling, zero-downtime rolling updates, and managed SSL certificates.',
    pros: ['Environment parity (Dev/Staging/Prod)', 'Automatic autoscaling', 'Cost-effective serverless billing'],
    alternatives: ['Kubernetes (EKS / GKE)', 'Fly.io', 'AWS App Runner'],
  },
  {
    name: 'Stripe API & Webhooks',
    category: 'Integration',
    role: 'Payment Processing Gateway',
    rationale:
      'Global payment rails handling SCA/3D Secure, recurring billing, webhooks, and PCI-DSS Level 1 compliance.',
    pros: ['Robust test sandbox', 'Developer-friendly SDKs', 'Global currency support'],
    alternatives: ['PayPal / Braintree', 'Adyen', 'Lemon Squeezy'],
  },
];

export const TechStackTab: React.FC<TechStackTabProps> = ({ result }) => {
  const [techStack, setTechStack] = useState<TechStackData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchStack = async () => {
      setLoading(true);
      try {
        const data = await api.getTechStack(result.project_id);
        setTechStack(data);
      } catch (err) {
        console.warn('Could not fetch dynamic tech stack, using architectural defaults:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStack();
  }, [result.project_id]);

  const recommendations =
    techStack?.recommendations && techStack.recommendations.length > 0
      ? techStack.recommendations
      : DEFAULT_STACK;

  const notes = techStack?.architectural_notes || [
    'Architecture optimized for modular monorepo deployment.',
    'Decoupled frontend client state from backend REST contracts.',
    'All secret credentials must reside in environment variable vaults.',
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Recommended Technology Stack</h2>
          <p className="text-xs text-slate-500">
            Tailored architectural blueprint selected based on project domain, platform, and integrations.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-bold text-sky-700 bg-sky-50 px-3 py-1 rounded-xl border border-sky-200">
          <Sparkles className="w-3.5 h-3.5 text-sky-600" />
          <span>Architecture Grounded</span>
        </div>
      </div>

      {/* Architectural Guidelines Card */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
        <span className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
          Engineering Architectural Principles:
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-slate-600">
          {notes.map((note, i) => (
            <div key={i} className="flex items-start space-x-1.5 p-2 bg-white rounded-lg border border-slate-100">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
              <span>{note}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.map((item, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-sky-300 hover:shadow-md transition-all space-y-3 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-sky-50 text-sky-700 border border-sky-200">
                  {item.category}
                </span>
                <span className="text-[11px] font-medium text-slate-400">{item.role}</span>
              </div>

              <h3 className="font-bold text-slate-900 text-sm">{item.name}</h3>

              <p className="text-xs text-slate-600 leading-relaxed">{item.rationale}</p>
            </div>

            <div className="space-y-2 pt-3 border-t border-slate-100 text-xs">
              {/* Pros */}
              <div className="space-y-1">
                <span className="text-[10px] font-bold uppercase text-slate-400">Key Advantages:</span>
                <div className="flex flex-wrap gap-1">
                  {item.pros.map((pro, pIdx) => (
                    <span
                      key={pIdx}
                      className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-emerald-50 text-emerald-800 border border-emerald-200"
                    >
                      ✓ {pro}
                    </span>
                  ))}
                </div>
              </div>

              {/* Alternatives */}
              {item.alternatives && item.alternatives.length > 0 && (
                <div className="pt-1 text-[11px] text-slate-400">
                  <span>Alternatives: </span>
                  <span className="text-slate-600 font-medium">
                    {item.alternatives.join(', ')}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
