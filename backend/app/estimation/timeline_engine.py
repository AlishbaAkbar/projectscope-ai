"""
Phase 11: Timeline Estimation Engine
Calculates project timeline with dependencies, critical path, and milestones
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import networkx as nx


@dataclass
class TaskNode:
    """Task node in dependency graph"""
    id: str
    title: str
    hours: float
    role_id: int
    dependencies: List[str] = field(default_factory=list)
    earliest_start: Optional[datetime] = None
    earliest_finish: Optional[datetime] = None
    latest_start: Optional[datetime] = None
    latest_finish: Optional[datetime] = None
    slack: float = 0.0
    is_critical: bool = False


@dataclass
class Milestone:
    """Project milestone"""
    name: str
    date: datetime
    description: str
    tasks: List[str] = field(default_factory=list)


@dataclass
class TimelineResult:
    """Complete timeline estimation result"""
    start_date: datetime
    end_date: datetime
    total_days: int
    total_working_days: int
    critical_path: List[str]
    milestones: List[Milestone]
    weekly_breakdown: Dict[str, float]
    tasks: List[TaskNode]
    parallelization_opportunities: List[Dict]
    bottlenecks: List[Dict]


class TimelineEngine:
    """
    Calculate project timeline based on:
    - Task dependencies
    - Parallel work opportunities
    - Working days (Monday-Friday)
    - 8 hours per working day
    """
    
    # Working hours per day
    HOURS_PER_DAY = 8
    
    # Working days: Monday=0, Friday=4
    WORKING_DAYS = [0, 1, 2, 3, 4]
    
    def __init__(self, start_date: Optional[datetime] = None):
        self.start_date = start_date or datetime.now().replace(
            hour=9, minute=0, second=0, microsecond=0
        )
        self.graph = nx.DiGraph()
        self.task_nodes: Dict[str, TaskNode] = {}
    
    def add_task(self, task_id: str, title: str, hours: float, 
                 role_id: int, dependencies: List[str] = None):
        """Add a task to the timeline"""
        node = TaskNode(
            id=task_id,
            title=title,
            hours=hours,
            role_id=role_id,
            dependencies=dependencies or []
        )
        self.task_nodes[task_id] = node
        self.graph.add_node(task_id, hours=hours)
        
        for dep in node.dependencies:
            if dep in self.task_nodes:
                self.graph.add_edge(dep, task_id)
    
    def add_tasks_from_list(self, tasks: List[Dict]):
        """Add multiple tasks from a list"""
        for task in tasks:
            self.add_task(
                task_id=task.get("id", f"task_{len(self.task_nodes)}"),
                title=task.get("title", "Task"),
                hours=task.get("estimated_hours", 0),
                role_id=task.get("role_id", 0),
                dependencies=task.get("dependencies", [])
            )
    
    def calculate(self) -> TimelineResult:
        """
        Calculate complete timeline
        
        Returns:
            TimelineResult with dates, critical path, milestones
        """
        if not self.task_nodes:
            return self._empty_result()
        
        # 1. Calculate earliest start/finish (forward pass)
        self._calculate_earliest_times()
        
        # 2. Calculate latest start/finish (backward pass)
        self._calculate_latest_times()
        
        # 3. Calculate slack and identify critical path
        self._calculate_slack_and_critical()
        
        # 4. Get critical path
        critical_path = self._get_critical_path()
        
        # 5. Calculate end date
        end_date = self._calculate_end_date()
        
        # 6. Generate milestones
        milestones = self._generate_milestones()
        
        # 7. Calculate weekly breakdown
        weekly_breakdown = self._calculate_weekly_breakdown()
        
        # 8. Find parallelization opportunities
        parallel_opps = self._find_parallelization_opportunities()
        
        # 9. Find bottlenecks
        bottlenecks = self._find_bottlenecks()
        
        # 10. Calculate total days
        total_days = (end_date - self.start_date).days
        total_working_days = self._count_working_days(self.start_date, end_date)
        
        return TimelineResult(
            start_date=self.start_date,
            end_date=end_date,
            total_days=total_days,
            total_working_days=total_working_days,
            critical_path=critical_path,
            milestones=milestones,
            weekly_breakdown=weekly_breakdown,
            tasks=list(self.task_nodes.values()),
            parallelization_opportunities=parallel_opps,
            bottlenecks=bottlenecks
        )
    
    def _calculate_earliest_times(self):
        """Forward pass: calculate earliest start/finish times"""
        # Topological sort
        try:
            topo_order = list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            # Handle cycles by using all nodes
            topo_order = list(self.graph.nodes())
        
        for node_id in topo_order:
            node = self.task_nodes[node_id]
            if not node.dependencies:
                # No dependencies, start at beginning
                node.earliest_start = self.start_date
            else:
                # Earliest start = max of all dependency finish times
                max_finish = self.start_date
                for dep_id in node.dependencies:
                    if dep_id in self.task_nodes:
                        dep = self.task_nodes[dep_id]
                        if dep.earliest_finish and dep.earliest_finish > max_finish:
                            max_finish = dep.earliest_finish
                node.earliest_start = max_finish
            
            # Earliest finish = earliest start + hours
            node.earliest_finish = self._add_working_hours(
                node.earliest_start, node.hours
            )
    
    def _calculate_latest_times(self):
        """Backward pass: calculate latest start/finish times"""
        # Get all nodes in reverse topological order
        try:
            reverse_order = list(reversed(list(nx.topological_sort(self.graph))))
        except nx.NetworkXUnfeasible:
            reverse_order = list(reversed(list(self.graph.nodes())))
        
        # Get end date
        end_date = self._calculate_end_date()
        
        for node_id in reverse_order:
            node = self.task_nodes[node_id]
            
            # Find successors
            successors = list(self.graph.successors(node_id))
            
            if not successors:
                # No successors, finish at end
                node.latest_finish = end_date
            else:
                # Latest finish = min of all successor latest starts
                min_start = end_date
                for succ_id in successors:
                    if succ_id in self.task_nodes:
                        succ = self.task_nodes[succ_id]
                        if succ.latest_start and succ.latest_start < min_start:
                            min_start = succ.latest_start
                node.latest_finish = min_start
            
            # Latest start = latest finish - hours
            node.latest_start = self._subtract_working_hours(
                node.latest_finish, node.hours
            )
    
    def _calculate_slack_and_critical(self):
        """Calculate slack time and identify critical tasks"""
        for node in self.task_nodes.values():
            if node.earliest_start and node.latest_start:
                slack = (node.latest_start - node.earliest_start).total_seconds() / 3600
                node.slack = slack
                node.is_critical = slack < 1.0  # Less than 1 hour slack = critical
    
    def _get_critical_path(self) -> List[str]:
        """Get critical path (tasks with zero slack)"""
        path = []
        current = None
        
        # Find task with earliest start
        for node in self.task_nodes.values():
            if node.is_critical:
                if not current or node.earliest_start < self.task_nodes[current].earliest_start:
                    current = node.id
        
        if not current:
            return []
        
        # Trace critical path
        while current:
            path.append(current)
            # Find next critical task in path
            next_task = None
            for dep_id in self.graph.successors(current):
                if dep_id in self.task_nodes and self.task_nodes[dep_id].is_critical:
                    next_task = dep_id
                    break
            current = next_task
        
        return path
    
    def _calculate_end_date(self) -> datetime:
        """Calculate project end date based on latest finish"""
        max_finish = self.start_date
        for node in self.task_nodes.values():
            if node.earliest_finish and node.earliest_finish > max_finish:
                max_finish = node.earliest_finish
        
        return max_finish
    
    def _generate_milestones(self) -> List[Milestone]:
        """Generate milestones based on critical path and task completion"""
        milestones = []
        
        # Start milestone
        milestones.append(Milestone(
            name="Project Start",
            date=self.start_date,
            description="Project initiation and planning"
        ))
        
        # Milestones at 25%, 50%, 75%, 100% of critical path
        critical_tasks = [t for t in self.task_nodes.values() if t.is_critical]
        if critical_tasks:
            sorted_tasks = sorted(critical_tasks, key=lambda x: x.earliest_start)
            total = len(sorted_tasks)
            
            milestone_points = [
                (0.25, "25% Complete", "Initial development phase complete"),
                (0.50, "50% Complete", "Core functionality complete"),
                (0.75, "75% Complete", "Feature complete, testing phase"),
                (1.0, "100% Complete", "Project complete, ready for deployment"),
            ]
            
            for i, (pct, name, desc) in enumerate(milestone_points):
                idx = min(int(pct * total), total - 1)
                task = sorted_tasks[idx]
                milestone_date = task.earliest_finish or self.start_date
                
                milestones.append(Milestone(
                    name=name,
                    date=milestone_date,
                    description=desc,
                    tasks=[task.id]
                ))
        
        return milestones
    
    def _calculate_weekly_breakdown(self) -> Dict[str, float]:
        """Calculate hours per week"""
        weekly = defaultdict(float)
        
        for node in self.task_nodes.values():
            if node.earliest_start:
                week_key = node.earliest_start.strftime("%Y-W%W")
                weekly[week_key] += node.hours
        
        return dict(weekly)
    
    def _find_parallelization_opportunities(self) -> List[Dict]:
        """Find tasks that can be done in parallel"""
        opportunities = []
        role_tasks = defaultdict(list)
        
        for node in self.task_nodes.values():
            role_tasks[node.role_id].append(node)
        
        for role_id, tasks in role_tasks.items():
            if len(tasks) > 1:
                # Check if tasks overlap in time
                for i, task1 in enumerate(tasks):
                    for task2 in tasks[i+1:]:
                        if task1.earliest_start and task2.earliest_start:
                            # Check if they can be parallelized
                            if abs((task1.earliest_start - task2.earliest_start).days) < 5:
                                opportunities.append({
                                    "role_id": role_id,
                                    "tasks": [task1.id, task2.id],
                                    "estimated_savings": min(task1.hours, task2.hours)
                                })
        
        return opportunities
    
    def _find_bottlenecks(self) -> List[Dict]:
        """Identify bottleneck tasks"""
        bottlenecks = []
        
        for node in self.task_nodes.values():
            # Tasks with many dependencies are bottlenecks
            successors = list(self.graph.successors(node.id))
            if len(successors) > 3:
                bottlenecks.append({
                    "task_id": node.id,
                    "title": node.title,
                    "num_dependents": len(successors),
                    "slack": node.slack,
                    "warning": f"This task blocks {len(successors)} dependent tasks"
                })
        
        # Sort by number of dependents (highest first)
        bottlenecks.sort(key=lambda x: x["num_dependents"], reverse=True)
        return bottlenecks[:5]
    
    def _add_working_hours(self, start: datetime, hours: float) -> datetime:
        """Add working hours to a date (Monday-Friday, 8 hours/day)"""
        current = start
        remaining_hours = hours
        
        while remaining_hours > 0:
            # Move to next day if needed
            if current.hour >= 17:  # 5 PM
                current = current.replace(hour=9, minute=0) + timedelta(days=1)
                while current.weekday() >= 5:  # Saturday/Sunday
                    current += timedelta(days=1)
            
            # Calculate hours for today
            hours_today = min(remaining_hours, 8)
            current += timedelta(hours=hours_today)
            remaining_hours -= hours_today
            
            # Check if we reached end of day
            if current.hour >= 17:
                current = current.replace(hour=9, minute=0) + timedelta(days=1)
                while current.weekday() >= 5:
                    current += timedelta(days=1)
        
        return current
    
    def _subtract_working_hours(self, end: datetime, hours: float) -> datetime:
        """Subtract working hours from a date"""
        current = end
        remaining_hours = hours
        
        while remaining_hours > 0:
            # Move to previous day if needed
            if current.hour < 9:  # Before 9 AM
                current = current.replace(hour=17, minute=0) - timedelta(days=1)
                while current.weekday() >= 5:
                    current -= timedelta(days=1)
            
            # Calculate hours for today
            hours_today = min(remaining_hours, 8)
            current -= timedelta(hours=hours_today)
            remaining_hours -= hours_today
            
            # Check if we reached start of day
            if current.hour < 9:
                current = current.replace(hour=17, minute=0) - timedelta(days=1)
                while current.weekday() >= 5:
                    current -= timedelta(days=1)
        
        return current
    
    def _count_working_days(self, start: datetime, end: datetime) -> int:
        """Count working days between two dates"""
        days = 0
        current = start
        while current <= end:
            if current.weekday() < 5:
                days += 1
            current += timedelta(days=1)
        return days
    
    def _empty_result(self) -> TimelineResult:
        """Return empty timeline result"""
        return TimelineResult(
            start_date=self.start_date,
            end_date=self.start_date,
            total_days=0,
            total_working_days=0,
            critical_path=[],
            milestones=[],
            weekly_breakdown={},
            tasks=[],
            parallelization_opportunities=[],
            bottlenecks=[]
        )
    
    def get_formatted_timeline(self) -> Dict:
        """Get formatted timeline for API response"""
        result = self.calculate()
        
        return {
            "start_date": result.start_date.isoformat(),
            "end_date": result.end_date.isoformat(),
            "total_days": result.total_days,
            "total_working_days": result.total_working_days,
            "critical_path": result.critical_path,
            "milestones": [
                {
                    "name": m.name,
                    "date": m.date.isoformat(),
                    "description": m.description
                }
                for m in result.milestones
            ],
            "weekly_breakdown": result.weekly_breakdown,
            "parallelization_opportunities": result.parallelization_opportunities,
            "bottlenecks": result.bottlenecks
        }