export interface Project {
  id: number;
  name: string;
  description: string;
  platform: string;
  project_type?: string | null;
  target_users?: string[];
  created_at: string;
  updated_at: string;
}

export interface Requirement {
  id: number;
  project_id: number;
  category: 'functional' | 'non_functional' | 'technical' | 'business';
  text: string;
  source: string;
  confidence: number;
  created_at: string;
}

export interface Task {
  id: number;
  feature_id: number;
  title: string;
  description: string;
  category: 'Frontend' | 'Backend' | 'Database' | 'QA' | 'Integration' | 'DevOps' | 'General';
  estimated_hours?: number | null;
  created_at: string;
}

export interface Feature {
  id: number;
  project_id: number;
  name: string;
  normalized_key: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  complexity: 'low' | 'medium' | 'high';
  confidence: number;
  created_at: string;
  tasks: Task[];
}

export interface ProjectAnalysisResult {
  project: Project;
  project_type: string;
  users: string[];
  requirements: Requirement[];
  features: Feature[];
  missing_information: string[];
  assumptions: string[];
  total_tasks_count: number;
  total_estimated_hours: number;
}

export interface ProjectCreatePayload {
  name: string;
  description: string;
  platform: string;
}
