'use client';

import React, { useState, useEffect } from 'react';
import { Requirement, ProjectAnalysisResult } from '../../types/project';
import { api } from '../../api/client';
import {
  CheckCircle2,
  Plus,
  Filter,
  Shield,
  Sparkles,
  RefreshCw,
  Tag,
  AlertCircle,
  Clock,
} from 'lucide-react';

interface RequirementsTabProps {
  result: ProjectAnalysisResult;
  onRefreshProject?: () => Promise<void>;
}

export const RequirementsTab: React.FC<RequirementsTabProps> = ({
  result,
  onRefreshProject,
}) => {
  const [requirements, setRequirements] = useState<Requirement[]>([]);
  const [loading, setLoading] = useState(false);
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newText, setNewText] = useState('');
  const [newCategory, setNewCategory] = useState('functional');
  const [isAdding, setIsAdding] = useState(false);
  const [addSuccess, setAddSuccess] = useState('');

  const fetchRequirements = async () => {
    setLoading(true);
    try {
      const data = await api.getRequirements(result.project_id);
      setRequirements(data);
    } catch (err) {
      console.warn('Could not fetch requirements:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequirements();
  }, [result.project_id]);

  const handleAddRequirement = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newText.trim() || isAdding) return;
    setIsAdding(true);
    try {
      await api.addRequirement(result.project_id, newText.trim(), newCategory);
      setNewText('');
      setShowAddForm(false);
      setAddSuccess('Requirement added! Re-analyze to decompose new tasks.');
      await fetchRequirements();
      if (onRefreshProject) {
        await onRefreshProject();
      }
      setTimeout(() => setAddSuccess(''), 3500);
    } catch (err: any) {
      alert(`Failed to add requirement: ${err.message}`);
    } finally {
      setIsAdding(false);
    }
  };

  const filtered = requirements.filter((req) => {
    if (categoryFilter === 'all') return true;
    return req.category.toLowerCase() === categoryFilter.toLowerCase();
  });

  const getCategoryColor = (cat: string) => {
    switch (cat.toLowerCase()) {
      case 'functional':
        return 'bg-sky-50 text-sky-700 border-sky-200';
      case 'non_functional':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'technical':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'business':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Top Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Project Requirements</h2>
          <p className="text-xs text-slate-500">
            Validated atomic specifications extracted by the prompt engine and user inputs.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold shadow-md shadow-sky-600/20 transition-all"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Requirement</span>
          </button>
        </div>
      </div>

      {addSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{addSuccess}</span>
          </div>
        </div>
      )}

      {/* Add Form Accordion */}
      {showAddForm && (
        <form
          onSubmit={handleAddRequirement}
          className="p-5 rounded-2xl bg-white border border-sky-200 shadow-lg space-y-4 animate-in slide-in-from-top-2 duration-200"
        >
          <h3 className="text-xs font-bold uppercase tracking-wider text-sky-800">
            Add Custom Software Requirement
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="sm:col-span-2">
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Requirement Description
              </label>
              <input
                type="text"
                required
                value={newText}
                onChange={(e) => setNewText(e.target.value)}
                placeholder="e.g. System must support Google and Apple Single Sign-On (SSO)"
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Category
              </label>
              <select
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option value="functional">Functional</option>
                <option value="non_functional">Non-Functional</option>
                <option value="technical">Technical</option>
                <option value="business">Business</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => setShowAddForm(false)}
              className="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-500 hover:bg-slate-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isAdding || !newText.trim()}
              className="px-4 py-1.5 text-xs font-bold rounded-lg bg-sky-600 hover:bg-sky-700 text-white shadow-sm disabled:opacity-50"
            >
              {isAdding ? 'Saving...' : 'Save Requirement'}
            </button>
          </div>
        </form>
      )}

      {/* Filter Tabs */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 border-b border-slate-200 text-xs font-semibold">
        {['all', 'functional', 'non_functional', 'technical', 'business'].map((cat) => (
          <button
            key={cat}
            onClick={() => setCategoryFilter(cat)}
            className={`px-3 py-1.5 rounded-lg capitalize whitespace-nowrap transition-colors ${
              categoryFilter === cat
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {cat.replace('_', ' ')}
          </button>
        ))}
        <span className="text-xs text-slate-400 font-normal ml-auto">
          {filtered.length} of {requirements.length} requirements
        </span>
      </div>

      {/* Requirements List */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-xs space-y-2">
          <RefreshCw className="w-5 h-5 animate-spin mx-auto text-sky-600" />
          <span>Loading requirements...</span>
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 text-xs text-slate-500 space-y-2">
          <AlertCircle className="w-6 h-6 text-slate-300 mx-auto" />
          <p>No requirements matching the "{categoryFilter}" category.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {filtered.map((req) => (
            <div
              key={req.id}
              className="p-4 rounded-xl bg-white border border-slate-200 hover:border-sky-300 hover:shadow-md transition-all space-y-3 flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span
                    className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider border ${getCategoryColor(
                      req.category
                    )}`}
                  >
                    {req.category.replace('_', ' ')}
                  </span>
                  <div className="flex items-center space-x-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    <Shield className="w-3 h-3 text-emerald-600" />
                    <span>{Math.round((req.confidence || 0.9) * 100)}% Confidence</span>
                  </div>
                </div>

                <p className="text-xs text-slate-800 leading-relaxed font-medium">
                  {req.text}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
                <span>Source: {req.source || 'user_input'}</span>
                {req.created_at && (
                  <span>{new Date(req.created_at).toLocaleDateString()}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
