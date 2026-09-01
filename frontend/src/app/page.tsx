'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { ProjectInputForm } from '../components/ProjectInputForm';
import { AnalysisProgress } from '../components/AnalysisProgress';
import { AnalysisResults } from '../components/AnalysisResults';
import { ProjectHistory } from '../components/ProjectHistory';
import { api } from '../api/client';
import { Project, ProjectAnalysisResult, ProjectCreatePayload } from '../types/project';
import { Sparkles, Layers, ListTodo, ShieldCheck, ArrowDown } from 'lucide-react';

export default function HomePage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentResult, setCurrentResult] = useState<ProjectAnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isReanalyzing, setIsReanalyzing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjectList = async () => {
    try {
      const list = await api.listProjects();
      setProjects(list);
    } catch (err) {
      console.warn('Could not fetch project history:', err);
    }
  };

  useEffect(() => {
    fetchProjectList();
  }, []);

  const handleCreateAndAnalyze = async (payload: ProjectCreatePayload) => {
    setIsLoading(true);
    setError(null);
    try {
      // 1. Create project in DB
      const project = await api.createProject(payload);
      
      // 2. Trigger AI analysis pipeline
      const analysisResult = await api.analyzeProject(project.id);
      
      setCurrentResult(analysisResult);
      await fetchProjectList();
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during project analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReanalyze = async () => {
    if (!currentResult) return;
    setIsReanalyzing(true);
    try {
      const result = await api.analyzeProject(currentResult.project.id);
      setCurrentResult(result);
    } catch (err: any) {
      alert(`Re-analysis failed: ${err.message}`);
    } finally {
      setIsReanalyzing(false);
    }
  };

  const handleSelectHistoryProject = async (projectId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.analyzeProject(projectId);
      setCurrentResult(result);
    } catch (err: any) {
      setError(err.message || 'Failed to load project analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-10 max-w-7xl mx-auto w-full">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto mb-10 space-y-3">
          <div className="inline-flex items-center space-x-2 rounded-full bg-sky-50 px-3.5 py-1 text-xs font-semibold text-sky-700 border border-sky-200">
            <Sparkles className="h-3.5 w-3.5 text-sky-500" />
            <span>AI-Driven Software Requirement Engineering</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight leading-tight">
            Turn Rough Software Ideas Into <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 to-blue-600">Structured Plans</span>
          </h1>
          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            ProjectScope AI analyzes your natural language project idea, extracts domain personas & functional requirements, normalizes features, and generates deterministic baseline development tasks.
          </p>

          {/* Core Pipeline Highlights */}
          <div className="pt-3 flex flex-wrap items-center justify-center gap-4 text-xs font-medium text-slate-500">
            <div className="flex items-center space-x-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
              <span>Strict Pydantic Validation</span>
            </div>
            <span className="hidden sm:inline">•</span>
            <div className="flex items-center space-x-1.5">
              <Layers className="h-4 w-4 text-sky-500" />
              <span>Canonical Feature Normalization</span>
            </div>
            <span className="hidden sm:inline">•</span>
            <div className="flex items-center space-x-1.5">
              <ListTodo className="h-4 w-4 text-indigo-500" />
              <span>Baseline Engineering Tasks</span>
            </div>
          </div>
        </div>

        {/* Global Error Banner */}
        {error && (
          <div className="max-w-4xl mx-auto mb-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-xs text-rose-800">
            <strong>Analysis Pipeline Error:</strong> {error}
          </div>
        )}

        {/* Project Input Form */}
        <ProjectInputForm onSubmit={handleCreateAndAnalyze} isLoading={isLoading} />

        {/* Step-by-Step Pipeline Animation */}
        <AnalysisProgress isLoading={isLoading} />

        {/* Structured Results Display */}
        {currentResult && !isLoading && (
          <AnalysisResults
            result={currentResult}
            onReanalyze={handleReanalyze}
            isReanalyzing={isReanalyzing}
          />
        )}

        {/* Project History */}
        {!isLoading && (
          <ProjectHistory
            projects={projects}
            activeProjectId={currentResult?.project.id}
            onSelectProject={handleSelectHistoryProject}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}
