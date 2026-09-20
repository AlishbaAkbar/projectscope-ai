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

  console.log('🌐 Request URL:', url);

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  try {
    const response = await fetch(url, { ...options, headers });
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
    if (error instanceof ApiError) {
      throw error;
    }
    console.error('❌ Fetch failed:', error);
    console.error('❌ Failed URL:', url);

    throw new ApiError(
      error.message ||
        'Unable to connect to ProjectScope AI backend server. Please ensure it is running on port 8000.',
      0
    );
  }
}

export const api = {
  /** Create a new project */
  createProject: async (payload: ProjectCreatePayload): Promise<Project> => {
    return request<Project>('/projects', {
      // ✅ No trailing slash
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
    return request<Project[]>('/projects'); // ✅ No trailing slash
  },

  /** Get project by ID */
  getProject: async (projectId: number): Promise<Project> => {
    return request<Project>(`/projects/${projectId}`); // ✅ Added /
  },

  /** Delete project by ID */
  deleteProject: async (projectId: number): Promise<void> => {
    return request<void>(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  },

  /** Run AI Requirement Analysis pipeline on project */
  analyzeProject: async (projectId: number): Promise<ProjectAnalysisResult> => {
    const result = await request<ProjectAnalysisResult>(
      `/projects/${projectId}/analyze`,
      { method: 'POST' }
    );
    try {
      const project = await api.getProject(projectId);
      result.project = project;
    } catch {
      // keep as is
    }
    return result;
  },

  /** Get requirements for project */
  getRequirements: async (projectId: number): Promise<Requirement[]> => {
    return request<Requirement[]>(`/projects/${projectId}/requirements`);
  },

  /** Add a requirement */
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

  /** Get features for project */
  getFeatures: async (projectId: number): Promise<Feature[]> => {
    return request<Feature[]>(`/projects/${projectId}/features`);
  },

  /** Get tasks for project */
  getTasks: async (projectId: number): Promise<Task[]> => {
    return request<Task[]>(`/projects/${projectId}/tasks`);
  },

  /** Send chat message to AI assistant */
  sendChatMessage: async (
    projectId: number,
    message: string,
    history: Array<{ role: string; content: string }> = []
  ): Promise<{
    reply: string;
    citations?: any[];
    suggested_actions?: string[];
  }> => {
    // Backend returns { response, sources, suggestions, confidence }
    const raw = await request<{
      response: string;
      sources?: any[];
      suggestions?: string[];
      confidence?: number;
    }>(`/projects/${projectId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message, history, project_id: projectId }),
    });

    // Map to frontend expected fields
    return {
      reply: raw.response,
      citations: raw.sources,
      suggested_actions: raw.suggestions,
    };
  },

  /** Submit feedback */
  submitFeedback: async (
    projectId: number,
    payload: FeedbackPayload
  ): Promise<any> => {
    return request<any>(`/projects/${projectId}/feedback`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /** Get tech stack recommendations */
  getTechStack: async (projectId: number): Promise<TechStackData> => {
    // Derive from features (backend doesn't have dedicated endpoint)
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

  /** Search RAG knowledge base */
  searchKnowledgeBase: async (query: string): Promise<any> => {
    return request<any>(`/rag/search?query=${encodeURIComponent(query)}`);
  },

  /** Get RAG knowledge base stats */
  getKnowledgeStats: async (): Promise<any> => {
    return request<any>('/rag/stats');
  },
};

// ============================================
// Tech Recommendation Helper
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