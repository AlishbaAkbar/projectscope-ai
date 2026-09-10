export interface Project {
  id: number;
  name: string;
  description: string;
  type?: string | null;
  platform?: string;
  status?: string;
  organization_id?: number;
  created_at: string;
  updated_at?: string;
}

export interface Requirement {
  id: number;
  project_id: number;
  category: 'functional' | 'non_functional' | 'technical' | 'business' | string;
  text: string;
  source: string;
  confidence: number;
  created_at?: string;
}

export interface Task {
  id: number;
  project_id?: number;
  feature_id?: number | null;
  role_id?: number;
  title: string;
  description: string;
  category?: 'Frontend' | 'Backend' | 'Database' | 'QA' | 'Integration' | 'DevOps' | 'General' | string;
  estimated_hours: number;
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  is_global?: boolean;
  dependencies?: string[];
  created_at?: string;
}

export interface Feature {
  id: number;
  project_id: number;
  name?: string;
  canonical_name: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  complexity: number | string;
  confidence: number;
  tasks?: Task[];
  created_at?: string;
}

export interface Milestone {
  name: string;
  date: string;
  description: string;
}

export interface TimelineData {
  start_date: string;
  end_date: string;
  total_days: number;
  total_working_days: number;
  critical_path: string[];
  milestones: Milestone[];
  weekly_breakdown: Record<string, number>;
  parallelization_opportunities: Array<{
    tasks: string[];
    description: string;
  }>;
  bottlenecks: Array<{
    role: string;
    description: string;
    impact_days: number;
  }>;
}

export interface RoleCostDetail {
  role_name?: string;
  total_hours: number;
  num_tasks: number;
  hourly_rate?: number;
  estimated_cost: number;
  cost?: number;
  percentage?: number;
}

export interface CostData {
  total: {
    expected: number;
    best_case: number;
    worst_case: number;
    currency?: string;
  };
  by_role: Record<string, {
    hours: number;
    rate: number;
    cost: number;
    percentage: number;
  }>;
  summary: {
    total_hours: number;
    blended_rate: number;
    contingency_percent: number;
    contingency_amount: number;
  };
}

export interface RiskItem {
  id: string;
  name: string;
  description: string;
  category: string;
  probability: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  impact: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' | string;
  mitigation: string;
  contingency: string;
  owner: string;
  score: number;
}

export interface RiskSummaryData {
  total_risks: number;
  risk_score: number;
  risk_level: string;
  summary: Record<string, any>;
  risks_by_level: Record<string, number>;
  top_risks: RiskItem[];
  recommendations: string[];
}

export interface HybridEstimateData {
  final_estimate: number;
  range: {
    min: number;
    max: number;
  };
  confidence: number;
  reconciliation_method: string;
  version: string;
  timestamp: string;
  breakdown: {
    rule_based: number;
    ml_prediction: number;
    llm_suggestion: number;
  };
  weights_used: {
    rule: number;
    ml: number;
    llm: number;
  };
}

export interface ExplanationItem {
  category: string;
  title: string;
  explanation: string;
  impact: string;
  factors: string[];
  sources?: string[];
}

export interface ExplanationData {
  summary: string;
  explanations: Record<string, string>;
  detailed_explanations: ExplanationItem[];
  assumptions: string[];
  limitations: string[];
  knowledge_used?: Array<{
    id: string;
    title: string;
    category: string;
    relevance?: number;
  }>;
}

export interface TechRecommendationItem {
  name: string;
  category: string;
  role: string;
  rationale: string;
  pros: string[];
  alternatives: string[];
}

export interface TechStackData {
  project_id: number;
  platform: string;
  recommendations: TechRecommendationItem[];
  architectural_notes: string[];
}

export interface ProjectAnalysisResult {
  project_id: number;
  project?: Project;
  features: Feature[];
  tasks: Task[];
  roles: string[];
  total_estimated_hours: number;
  complexity_score: number;
  risk_level: string;
  summary: Record<string, RoleCostDetail>;
  timeline?: TimelineData;
  cost?: CostData;
  risks?: RiskSummaryData;
  hybrid_estimate?: HybridEstimateData;
  explanation?: ExplanationData;
  tech_stack?: TechStackData;
}

export interface ProjectCreatePayload {
  name: string;
  description: string;
  platform?: string;
  type?: string;
  organization_id?: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  citations?: Array<{
    id?: string;
    title: string;
    category?: string;
    score?: number;
  }>;
  suggested_actions?: string[];
}

export interface FeedbackPayload {
  rating: number;
  category?: string;
  comments?: string;
  tags?: string[];
}

export interface UserSession {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar: string;
  organization: string;
}
