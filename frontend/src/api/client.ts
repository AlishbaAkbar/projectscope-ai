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

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

// ============================================
// STORAGE KEYS
// ============================================
const TOKEN_KEY = 'projectscope_access_token';
const REFRESH_KEY = 'projectscope_refresh_token';
const USER_KEY = 'projectscope_user';
const ORG_KEY = 'projectscope_organization';

// ============================================
// API ERROR
// ============================================
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

// ============================================
// TOKEN MANAGEMENT
// ============================================
export const authStorage = {
  getToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(TOKEN_KEY);
  },

  getRefreshToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(REFRESH_KEY);
  },

  getUser: (): any | null => {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  },

  getOrganization: (): any | null => {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem(ORG_KEY);
    return raw ? JSON.parse(raw) : null;
  },

  setSession: (data: {
    access_token: string;
    refresh_token: string;
    user: any;
    organization: any;
  }) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(TOKEN_KEY, data.access_token);
    localStorage.setItem(REFRESH_KEY, data.refresh_token);
    localStorage.setItem(USER_KEY, JSON.stringify(data.user));
    localStorage.setItem(ORG_KEY, JSON.stringify(data.organization));
  },

  clear: () => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(ORG_KEY);
  },

  isAuthenticated: (): boolean => {
    return !!authStorage.getToken();
  },
};

// ============================================
// CORE REQUEST FUNCTION
// ============================================
async function request<T>(
  endpoint: string,
  options: RequestInit = {},
  retryOnAuth: boolean = true
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const token = authStorage.getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, { ...options, headers });

    // Handle 401 — try refresh token once
    if (response.status === 401 && retryOnAuth) {
      const refreshed = await tryRefreshToken();
      if (refreshed) {
        return request<T>(endpoint, options, false);
      }
      // Refresh failed — clear session
      authStorage.clear();
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage =
        data?.message ||
        data?.detail ||
        (Array.isArray(data?.detail) ? data.detail[0]?.msg : null) ||
        `Request failed with status ${response.status}`;

      throw new ApiError(errorMessage, response.status, data?.details || data);
    }

    return data as T;
  } catch (error: any) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(
      error.message ||
        'Unable to connect to ProjectScope AI backend. Ensure it is running on port 8000.',
      0
    );
  }
}

// ============================================
// AUTO TOKEN REFRESH
// ============================================
let refreshPromise: Promise<boolean> | null = null;

async function tryRefreshToken(): Promise<boolean> {
  // Coalesce multiple refresh attempts
  if (refreshPromise) return refreshPromise;

  refreshPromise = (async () => {
    try {
      const refreshToken = authStorage.getRefreshToken();
      if (!refreshToken) return false;

      const response = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!response.ok) return false;

      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem(TOKEN_KEY, data.access_token);
        return true;
      }
      return false;
    } catch {
      return false;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

// ============================================
// MAIN API OBJECT
// ============================================
export const api = {
  // ============================================
  // AUTH
  // ============================================

  register: async (data: {
    email: string;
    password: string;
    full_name: string;
    organization_name?: string;
  }): Promise<any> => {
    const result = await request<any>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    authStorage.setSession(result);
    return result;
  },

  login: async (email: string, password: string): Promise<any> => {
    const result = await request<any>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    authStorage.setSession(result);
    return result;
  },

  logout: async (): Promise<void> => {
    try {
      const refreshToken = authStorage.getRefreshToken();
      if (refreshToken) {
        await request('/auth/logout', {
          method: 'POST',
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      }
    } catch (e) {
      console.warn('Logout API failed:', e);
    } finally {
      authStorage.clear();
    }
  },

  getCurrentUser: async (): Promise<any> => {
    return request<any>('/auth/me');
  },

  isAuthenticated: (): boolean => authStorage.isAuthenticated(),

  // ============================================
  // PROJECTS
  // ============================================

  createProject: async (payload: ProjectCreatePayload): Promise<Project> => {
    return request<Project>('/projects', {
      method: 'POST',
      body: JSON.stringify({
        name: payload.name,
        description: payload.description,
        type: payload.type || payload.platform || 'web',
        platform: payload.platform || 'web',
      }),
    });
  },

  listProjects: async (): Promise<Project[]> => {
    return request<Project[]>('/projects');
  },

  getProject: async (projectId: number): Promise<Project> => {
    return request<Project>(`/projects/${projectId}`);
  },

  deleteProject: async (projectId: number): Promise<void> => {
    return request<void>(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  },

  analyzeProject: async (projectId: number): Promise<ProjectAnalysisResult> => {
    const result = await request<ProjectAnalysisResult>(
      `/projects/${projectId}/analyze`,
      { method: 'POST' }
    );
    try {
      const project = await api.getProject(projectId);
      result.project = project;
    } catch {}
    return result;
  },

  // ============================================
  // REQUIREMENTS
  // ============================================

  getRequirements: async (projectId: number): Promise<Requirement[]> => {
    return request<Requirement[]>(`/projects/${projectId}/requirements`);
  },

  addRequirement: async (
    projectId: number,
    text: string,
    category = 'general'
  ): Promise<any> => {
    return request<any>(
      `/projects/${projectId}/requirements?text=${encodeURIComponent(
        text
      )}&category=${encodeURIComponent(category)}`,
      { method: 'POST' }
    );
  },

  // ============================================
  // FEATURES & TASKS
  // ============================================

  getFeatures: async (projectId: number): Promise<Feature[]> => {
    return request<Feature[]>(`/projects/${projectId}/features`);
  },

  getTasks: async (projectId: number): Promise<Task[]> => {
    return request<Task[]>(`/projects/${projectId}/tasks`);
  },

  // ============================================
  // CHAT
  // ============================================

  sendChatMessage: async (
    projectId: number,
    message: string,
    history: Array<{ role: string; content: string }> = []
  ): Promise<{
    reply: string;
    citations?: any[];
    suggested_actions?: string[];
  }> => {
    const raw = await request<{
      response: string;
      sources?: any[];
      suggestions?: string[];
      confidence?: number;
    }>(`/projects/${projectId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message, history, project_id: projectId }),
    });
    return {
      reply: raw.response,
      citations: raw.sources,
      suggested_actions: raw.suggestions,
    };
  },

  // ============================================
  // FEEDBACK
  // ============================================

  submitFeedback: async (
    projectId: number,
    payload: FeedbackPayload
  ): Promise<any> => {
    return request<any>(`/projects/${projectId}/feedback`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // ============================================
  // TECH STACK
  // ============================================

  getTechStack: async (projectId: number): Promise<TechStackData> => {
    try {
      const features = await api.getFeatures(projectId);
      const featureNames = features.map((f) => f.canonical_name);
      return {
        project_id: projectId,
        platform: 'web',
        recommendations: deriveTechRecommendations(featureNames),
        architectural_notes: [
          'Modular monolith architecture recommended for MVP',
          'Separate AI/ML modules for scalability',
          'Use PostgreSQL as system of record',
        ],
      };
    } catch {
      return {
        project_id: projectId,
        platform: 'web',
        recommendations: [],
        architectural_notes: [],
      };
    }
  },

  // ============================================
  // REPORTS
  // ============================================

  downloadReport: async (
    projectId: number,
    format: 'pdf' | 'docx' | 'markdown' | 'csv'
  ): Promise<void> => {
    const token = authStorage.getToken();
    const response = await fetch(
      `${API_BASE}/projects/${projectId}/report/${format}`,
      {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      }
    );

    if (!response.ok) {
      throw new ApiError('Failed to download report', response.status);
    }

    const blob = await response.blob();
    const contentDisposition = response.headers.get('content-disposition');
    let filename = `report.${format === 'markdown' ? 'md' : format}`;

    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^"]+)"?/);
      if (match) filename = match[1];
    }

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  },

  // ============================================
  // RAG
  // ============================================

  searchKnowledgeBase: async (query: string): Promise<any> => {
    return request<any>(`/rag/search?query=${encodeURIComponent(query)}`);
  },

  getKnowledgeStats: async (): Promise<any> => {
    return request<any>('/rag/stats');
  },
};

// ============================================
// TECH RECOMMENDATION HELPER
// ============================================
function deriveTechRecommendations(
  features: string[]
): Array<{
  name: string;
  category: string;
  role: string;
  rationale: string;
  pros: string[];
  alternatives: string[];
}> {
  const recs = [];

  recs.push({
    name: 'Next.js 14 + TypeScript',
    category: 'Frontend',
    role: 'Primary UI framework',
    rationale: 'App Router, server components, and strong TypeScript support',
    pros: ['SEO-friendly', 'Great DX', 'Large ecosystem'],
    alternatives: ['Vue 3', 'SvelteKit', 'Remix'],
  });

  recs.push({
    name: 'FastAPI + Python',
    category: 'Backend',
    role: 'REST API framework',
    rationale: 'Async performance, Pydantic validation, auto OpenAPI docs',
    pros: ['Fast', 'Type-safe', 'Auto docs'],
    alternatives: ['Node.js + Express', 'NestJS', 'Django'],
  });

  recs.push({
    name: 'PostgreSQL',
    category: 'Database',
    role: 'Primary data store',
    rationale: 'ACID compliance, JSON support, mature tooling',
    pros: ['Reliable', 'Feature-rich', 'Well-supported'],
    alternatives: ['MySQL', 'MongoDB', 'SQLite (dev only)'],
  });

  if (features.includes('AUTHENTICATION')) {
    recs.push({
      name: 'JWT + bcrypt',
      category: 'Authentication',
      role: 'User authentication',
      rationale: 'Stateless auth, secure password hashing',
      pros: ['Scalable', 'Secure', 'Industry-standard'],
      alternatives: ['Auth0', 'Firebase Auth', 'OAuth2 + Passport'],
    });
  }

  if (features.includes('PAYMENT')) {
    recs.push({
      name: 'Stripe',
      category: 'Payments',
      role: 'Payment processing',
      rationale: 'Best-in-class payment API, PCI-compliant',
      pros: ['Great docs', 'Fraud detection', 'Global support'],
      alternatives: ['PayPal', 'Square', 'Braintree'],
    });
  }

  if (features.includes('REAL_TIME')) {
    recs.push({
      name: 'WebSockets + Redis Pub/Sub',
      category: 'Real-time',
      role: 'Live updates',
      rationale: 'Low-latency bidirectional communication',
      pros: ['Fast', 'Scalable', 'Mature'],
      alternatives: ['Socket.io', 'Server-Sent Events', 'Firebase RTDB'],
    });
  }

  if (features.includes('MOBILE_APP')) {
    recs.push({
      name: 'React Native',
      category: 'Mobile',
      role: 'Cross-platform mobile',
      rationale: 'Share code with web, single language',
      pros: ['Code reuse', 'Fast iteration', 'Large community'],
      alternatives: ['Flutter', 'Native iOS/Android'],
    });
  }

  recs.push({
    name: 'Docker + GitHub Actions',
    category: 'DevOps',
    role: 'CI/CD pipeline',
    rationale: 'Reproducible deployments, automated testing',
    pros: ['Portable', 'Automated', 'Free tier'],
    alternatives: ['GitLab CI', 'CircleCI', 'Jenkins'],
  });

  return recs;
}