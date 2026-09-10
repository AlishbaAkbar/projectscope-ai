import {
  Project,
  ProjectAnalysisResult,
  ProjectCreatePayload,
  Feature,
  Task,
  Requirement,
  TechStackData,
  ChatMessage,
  FeedbackPayload,
} from '../types/project';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export class ApiError extends Error {
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
      const errorMessage = data?.message || data?.detail || `Request failed with status ${response.status}`;
      throw new ApiError(errorMessage, response.status, data?.details || data);
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
      body: JSON.stringify({
        name: payload.name,
        description: payload.description,
        type: payload.type || payload.platform || 'web',
        platform: payload.platform || 'web',
        organization_id: payload.organization_id || 1,
      }),
    });
  },

  /** List all projects */
  listProjects: async (): Promise<Project[]> => {
    return request<Project[]>('/projects');
  },

  /** Get project by ID */
  getProject: async (projectId: number): Promise<Project> => {
    return request<Project>(`/projects/${projectId}`);
  },

  /** Delete project by ID */
  deleteProject: async (projectId: number): Promise<void> => {
    return request<void>(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  },

  /** Run AI Requirement Analysis pipeline on project */
  analyzeProject: async (projectId: number): Promise<ProjectAnalysisResult> => {
    const result = await request<ProjectAnalysisResult>(`/projects/${projectId}/analyze`, {
      method: 'POST',
    });
    // Fetch project details to accompany result if needed
    try {
      const project = await api.getProject(projectId);
      result.project = project;
    } catch {
      // Keep result as is
    }
    return result;
  },

  /** Get requirements for project */
  getRequirements: async (projectId: number): Promise<Requirement[]> => {
    return request<Requirement[]>(`/projects/${projectId}/requirements`);
  },

  /** Add a requirement */
  addRequirement: async (projectId: number, text: string, category = 'general'): Promise<any> => {
    return request<any>(`/projects/${projectId}/requirements?text=${encodeURIComponent(text)}&category=${encodeURIComponent(category)}`, {
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

  /** Send chat message to AI assistant */
  sendChatMessage: async (projectId: number, message: string, history: Array<{ role: string; content: string }> = []): Promise<{
    reply: string;
    citations?: any[];
    suggested_actions?: string[];
  }> => {
    return request<{ reply: string; citations?: any[]; suggested_actions?: string[] }>(`/projects/${projectId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message, history }),
    });
  },

  /** Submit feedback */
  submitFeedback: async (projectId: number, payload: FeedbackPayload): Promise<any> => {
    return request<any>(`/projects/${projectId}/feedback`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /** Get tech stack recommendations */
  getTechStack: async (projectId: number): Promise<TechStackData> => {
    return request<TechStackData>(`/projects/${projectId}/tech-stack`);
  },

  /** Search RAG knowledge base */
  searchKnowledgeBase: async (query: string): Promise<any> => {
    return request<any>(`/rag/search?query=${encodeURIComponent(query)}`);
  },

  /** Get RAG knowledge base stats */
  getKnowledgeStats: async (): Promise<any> => {
    return request<any>('/rag/stats');
  },
};

