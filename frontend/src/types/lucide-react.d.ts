declare module 'lucide-react' {
  import * as React from 'react';

  export interface LucideProps extends React.SVGProps<SVGSVGElement> {
    size?: string | number;
    color?: string;
    strokeWidth?: string | number;
  }

  export type LucideIcon = React.ForwardRefExoticComponent<
    LucideProps & React.RefAttributes<SVGSVGElement>
  >;

  export const Sparkles: LucideIcon;
  export const Terminal: LucideIcon;
  export const Layers: LucideIcon;
  export const Cpu: LucideIcon;
  export const CheckCircle2: LucideIcon;
  export const ArrowRight: LucideIcon;
  export const Lightbulb: LucideIcon;
  export const Compass: LucideIcon;
  export const Globe: LucideIcon;
  export const Smartphone: LucideIcon;
  export const Laptop: LucideIcon;
  export const Server: LucideIcon;
  export const Clock: LucideIcon;
  export const Brain: LucideIcon;
  export const Check: LucideIcon;
  export const Database: LucideIcon;
  export const FileText: LucideIcon;
  export const ListChecks: LucideIcon;
  export const Users: LucideIcon;
  export const AlertTriangle: LucideIcon;
  export const AlertCircle: LucideIcon;
  export const ListTodo: LucideIcon;
  export const Download: LucideIcon;
  export const Copy: LucideIcon;
  export const RefreshCw: LucideIcon;
  export const Tag: LucideIcon;
  export const ShieldAlert: LucideIcon;
  export const HelpCircle: LucideIcon;
  export const FolderGit2: LucideIcon;
  export const ChevronDown: LucideIcon;
  export const ChevronUp: LucideIcon;
  export const ChevronRight: LucideIcon;
  export const Code2: LucideIcon;
  export const SlidersHorizontal: LucideIcon;
  export const History: LucideIcon;
  export const ArrowUpRight: LucideIcon;
  export const ShieldCheck: LucideIcon;
  export const ArrowDown: LucideIcon;
  export const LayoutDashboard: LucideIcon;
  export const LayoutGrid: LucideIcon;
  export const FileDown: LucideIcon;
  export const Plus: LucideIcon;
  export const TrendingUp: LucideIcon;
  export const TrendingDown: LucideIcon;
  export const Rocket: LucideIcon;
  export const BarChart: LucideIcon;
  export const BarChart2: LucideIcon;
  export const BarChart3: LucideIcon;
  export const Bot: LucideIcon;
  export const UserCheck: LucideIcon;
  export const Building: LucideIcon;
  export const Wand2: LucideIcon;
  export const FolderOpen: LucideIcon;
  export const GitCommit: LucideIcon;
  export const GitBranch: LucideIcon;
  export const Milestone: LucideIcon;
  export const Zap: LucideIcon;
  export const Star: LucideIcon;
  export const Sliders: LucideIcon;
  export const ArrowDownRight: LucideIcon;
  export const RotateCcw: LucideIcon;
  export const Printer: LucideIcon;
  export const Table: LucideIcon;
  export const Code: LucideIcon;
  export const ThumbsUp: LucideIcon;
  export const ArrowLeft: LucideIcon;
  export const Briefcase: LucideIcon;
  export const Percent: LucideIcon;
  export const Award: LucideIcon;
  export const ExternalLink: LucideIcon;
  export const Lock: LucideIcon;
  export const Mail: LucideIcon;
  export const User: LucideIcon;
  export const LogOut: LucideIcon;
  export const X: LucideIcon;
  export const Trash2: LucideIcon;
  export const Filter: LucideIcon;
  export const Send: LucideIcon;
  export const Search: LucideIcon;
  export const Shield: LucideIcon;
  export const DollarSign: LucideIcon;
  export const Calendar: LucideIcon;
  export const BookOpen: LucideIcon;
  export const MessageSquare: LucideIcon;
}
