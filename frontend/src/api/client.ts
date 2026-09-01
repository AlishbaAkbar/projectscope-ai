import { Project, ProjectAnalysisResult, ProjectCreatePayload, Feature, Task } from '../types/project';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  status: number;
  details?: any;

  constructor(message: string, status: number, details?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  try {
    const response = await fetch(url, { ...options, headers });
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage = data?.message || `Request failed with status ${response.status}`;
      throw new ApiError(errorMessage, response.status, data?.details);
    }

    return data as T;
  } catch (error: any) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Handle network or connection failures
    throw new ApiError(
      error.message || 'Unable to connect to ProjectScope AI backend server. Please ensure it is running on port 8000.',
      0
    );
  }
}

export const api = {
  /** Create a new project */
  createProject: async (payload: ProjectCreatePayload): Promise<Project> => {
    return request<Project>('/projects', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /** List all projects */
  listProjects: async (skip = 0, limit = 50): Promise<Project[]> => {
    return request<Project[]>(`/projects?skip=${skip}&limit=${limit}`);
  },

  /** Get project by ID */
  getProject: async (projectId: number): Promise<Project> => {
    return request<Project>(`/projects/${projectId}`);
  },

  /** Run AI Requirement Analysis pipeline on project */
  analyzeProject: async (projectId: number): Promise<ProjectAnalysisResult> => {
    return request<ProjectAnalysisResult>(`/projects/${projectId}/analyze`, {
      method: 'POST',
    });
  },

  /** Get features for project */
  getFeatures: async (projectId: number): Promise<Feature[]> => {
    return request<Feature[]>(`/projects/${projectId}/features`);
  },

  /** Get tasks for project */
  getTasks: async (projectId: number): Promise<Task[]> => {
    return request<Task[]>(`/projects/${projectId}/tasks`);
  },
};
