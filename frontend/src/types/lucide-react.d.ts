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
  export const Code2: LucideIcon;
  export const SlidersHorizontal: LucideIcon;
  export const History: LucideIcon;
  export const ArrowUpRight: LucideIcon;
  export const ShieldCheck: LucideIcon;
  export const ArrowDown: LucideIcon;
}
