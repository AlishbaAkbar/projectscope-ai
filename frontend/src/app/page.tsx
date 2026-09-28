'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { LandingPage } from '../components/LandingPage';
import { DashboardView } from '../components/DashboardView';
import { ScopingStudio } from '../components/ScopingStudio';
import { CreateProjectModal } from '../components/CreateProjectModal';
import { AuthModal } from '../components/AuthModal';
import { LoginModal } from '../components/LoginModal';
import { api, authStorage } from '../api/client';
import {
  Project,
  ProjectAnalysisResult,
  ProjectCreatePayload,
  UserSession,
} from '../types/project';
import { Sparkles, AlertCircle, Layers } from 'lucide-react';

export default function HomePage() {
  const [activeView, setActiveView] = useState<
    'landing' | 'dashboard' | 'studio' | 'knowledge'
  >('landing');
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentResult, setCurrentResult] = useState<ProjectAnalysisResult | null>(null);
  const [currentSession, setCurrentSession] = useState<UserSession | null>(null);

  // Modals & form state
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [createPreset, setCreatePreset] = useState<ProjectCreatePayload | null>(null);

  // Loading & error state
  const [isLoading, setIsLoading] = useState(false);
  const [isReanalyzing, setIsReanalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // ============================================
  // LOAD SESSION FROM LOCALSTORAGE
  // ============================================
  useEffect(() => {
    const user = authStorage.getUser();
    if (user) {
      setCurrentSession({
        id: String(user.id),
        name: user.full_name,
        email: user.email,
        role: user.role,
        avatar: '',
        organization: authStorage.getOrganization()?.name || 'Org',
      });
    }
  }, []);

  // ============================================
  // FETCH PROJECTS
  // ============================================
  const fetchProjectList = async () => {
    // If not authenticated → show login modal
    if (!api.isAuthenticated()) {
      setIsLoginOpen(true);
      return;
    }

    try {
      const list = await api.listProjects();
      setProjects(list);
    } catch (err: any) {
      console.warn('Could not fetch project list:', err);
      if (err.status === 401) {
        setIsLoginOpen(true);
      }
    }
  };

  useEffect(() => {
    fetchProjectList();
  }, []);

  // ============================================
  // AUTH HANDLERS
  // ============================================
  const handleLoginSuccess = () => {
    const user = authStorage.getUser();
    if (user) {
      setCurrentSession({
        id: String(user.id),
        name: user.full_name,
        email: user.email,
        role: user.role,
        avatar: '',
        organization: authStorage.getOrganization()?.name || 'Org',
      });
    }
    fetchProjectList();
  };

  const handleLogout = async () => {
    await api.logout();
    setCurrentSession(null);
    setProjects([]);
    setCurrentResult(null);
    setIsLoginOpen(true);
  };

  // ============================================
  // PROJECT CREATION
  // ============================================
  const handleCreateProject = async (
    payload: ProjectCreatePayload,
    autoAnalyze: boolean
  ) => {
    setIsLoading(true);
    setError(null);

    try {
      const project = await api.createProject(payload);

      if (autoAnalyze) {
        const analysis = await api.analyzeProject(project.id);
        setCurrentResult(analysis);
        setActiveView('studio');
      } else {
        setActiveView('dashboard');
      }

      await fetchProjectList();
      setIsCreateOpen(false);
      setCreatePreset(null);
    } catch (err: any) {
      setError(err.message || 'Failed to create and analyze project.');
    } finally {
      setIsLoading(false);
    }
  };

  // ============================================
  // PROJECT SELECTION
  // ============================================
  const handleSelectProject = async (projectId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const analysis = await api.analyzeProject(projectId);
      setCurrentResult(analysis);
      setActiveView('studio');
    } catch (err: any) {
      setError(err.message || 'Failed to load project analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReanalyze = async () => {
    if (!currentResult) return;
    setIsReanalyzing(true);
    try {
      const analysis = await api.analyzeProject(currentResult.project_id);
      setCurrentResult(analysis);
    } catch (err: any) {
      alert(`Re-analysis failed: ${err.message}`);
    } finally {
      setIsReanalyzing(false);
    }
  };

  const handleDeleteProject = async (projectId: number) => {
    try {
      await api.deleteProject(projectId);
      if (currentResult?.project_id === projectId) {
        setCurrentResult(null);
      }
      await fetchProjectList();
    } catch (err: any) {
      alert(`Failed to delete project: ${err.message}`);
    }
  };

  // ============================================
  // PRESET TEMPLATE
  // ============================================
  const handlePresetSelect = (preset: ProjectCreatePayload) => {
    setCreatePreset(preset);
    setIsCreateOpen(true);
  };

  // ============================================
  // RENDER
  // ============================================
  return (
    <div className="flex flex-col min-h-screen bg-slate-50/50">
      {/* Top Navbar */}
      <Navbar
        activeView={activeView}
        onNavigate={(view) => setActiveView(view)}
        activeProjectName={currentResult?.project?.name}
        currentSession={currentSession}
        onOpenAuth={() => setIsLoginOpen(true)}
        onLogout={handleLogout}
      />

      {/* Main App Container */}
      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-8 max-w-7xl mx-auto w-full">
        {/* Global Error Alert */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl border border-rose-200 bg-rose-50 text-xs text-rose-800 flex items-center justify-between shadow-sm">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>
                <strong>System Notice:</strong> {error}
              </span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-rose-600 hover:text-rose-800 font-bold ml-4"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Loading Overlay */}
        {isLoading && (
          <div className="py-24 text-center space-y-4">
            <div className="w-14 h-14 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto shadow-md">
              <Sparkles className="w-7 h-7 animate-spin" />
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              Executing AI Requirement Analysis & Decomposition...
            </h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto leading-relaxed">
              Invoking Requirement Analyzer, normalizing canonical features, calculating hybrid ML effort curves, and constructing critical path timelines.
            </p>
          </div>
        )}

        {/* Landing */}
        {!isLoading && activeView === 'landing' && (
          <LandingPage
            onOpenCreate={() => {
              setCreatePreset(null);
              setIsCreateOpen(true);
            }}
            onSelectPreset={handlePresetSelect}
            onGoToDashboard={() => setActiveView('dashboard')}
          />
        )}

        {/* Dashboard */}
        {!isLoading && activeView === 'dashboard' && (
          <DashboardView
            projects={projects}
            onSelectProject={handleSelectProject}
            onOpenCreate={() => {
              setCreatePreset(null);
              setIsCreateOpen(true);
            }}
            onDeleteProject={handleDeleteProject}
            currentResult={currentResult}
          />
        )}

        {/* Scoping Studio */}
        {!isLoading && activeView === 'studio' && (
          <>
            {currentResult ? (
              <ScopingStudio
                result={currentResult}
                onReanalyze={handleReanalyze}
                isReanalyzing={isReanalyzing}
                onRefreshProject={() =>
                  handleSelectProject(currentResult.project_id)
                }
              />
            ) : (
              <div className="p-12 text-center bg-white rounded-3xl border border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto my-12">
                <div className="w-12 h-12 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto">
                  <Layers className="w-6 h-6" />
                </div>
                <h3 className="text-base font-bold text-slate-900">
                  No Project Currently Selected
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Select an existing project from your portfolio dashboard or create a new scope brief.
                </p>
                <div className="flex items-center justify-center gap-2 pt-2">
                  <button
                    onClick={() => setActiveView('dashboard')}
                    className="px-4 py-2 text-xs font-semibold rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700"
                  >
                    Open Dashboard
                  </button>
                  <button
                    onClick={() => {
                      setCreatePreset(null);
                      setIsCreateOpen(true);
                    }}
                    className="px-4 py-2 text-xs font-bold rounded-xl bg-sky-600 hover:bg-sky-700 text-white shadow-md"
                  >
                    Create New Project
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Modals */}
      <CreateProjectModal
        isOpen={isCreateOpen}
        onClose={() => {
          setIsCreateOpen(false);
          setCreatePreset(null);
        }}
        onSubmit={handleCreateProject}
        isLoading={isLoading}
        initialData={createPreset}
      />

      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onLoginSuccess={handleLoginSuccess}
        currentSession={currentSession}
        onLogout={handleLogout}
      />

      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onSuccess={handleLoginSuccess}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}