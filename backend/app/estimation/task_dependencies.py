from typing import List, Dict, Set, Tuple
from collections import defaultdict
import networkx as nx  # You'll need to install this: pip install networkx

class TaskDependencyGraph:
    """Manages task dependencies and calculates critical paths"""
    
    def __init__(self, tasks: List[Dict]):
        self.tasks = tasks
        self.graph = nx.DiGraph()
        self._build_graph()
    
    def _build_graph(self):
        """Build dependency graph from tasks"""
        for task in self.tasks:
            self.graph.add_node(task["id"], hours=task.get("hours", 0))
            
            # Add dependencies
            for dep_id in task.get("dependencies", []):
                self.graph.add_edge(dep_id, task["id"])
    
    def get_critical_path(self) -> Tuple[List[str], float]:
        """
        Calculate critical path (longest path through the graph)
        Returns: (path nodes, total hours)
        """
        if not self.graph.nodes():
            return [], 0.0
        
        # Topological sort
        try:
            topo_order = list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            # Handle cycles
            return [], 0.0
        
        # Calculate earliest start times
        earliest_start = {node: 0 for node in self.graph.nodes()}
        
        for node in topo_order:
            for pred in self.graph.predecessors(node):
                pred_hours = self.graph.nodes[pred].get("hours", 0)
                earliest_start[node] = max(
                    earliest_start[node],
                    earliest_start[pred] + pred_hours
                )
        
        # Find critical path
        if not topo_order:
            return [], 0.0
        
        # Find the node with maximum finish time
        end_node = max(topo_order, key=lambda n: earliest_start[n] + self.graph.nodes[n].get("hours", 0))
        total_hours = earliest_start[end_node] + self.graph.nodes[end_node].get("hours", 0)
        
        # Trace back
        critical_path = []
        current = end_node
        
        while current in self.graph.nodes():
            critical_path.append(current)
            predecessors = list(self.graph.predecessors(current))
            
            if not predecessors:
                break
                
            # Find predecessor on critical path
            current = max(
                predecessors,
                key=lambda p: earliest_start[p] + self.graph.nodes[p].get("hours", 0)
            )
        
        critical_path.reverse()
        return critical_path, total_hours
    
    def get_parallelization_opportunities(self) -> Dict:
        """Find tasks that can be parallelized"""
        opportunities = []
        
        # Group tasks by level (tasks that can be done independently)
        levels = defaultdict(list)
        
        for node in self.graph.nodes():
            # Tasks with no dependencies can start immediately
            if len(list(self.graph.predecessors(node))) == 0:
                levels[0].append(node)
            else:
                # Tasks with dependencies go to later levels
                depth = self._get_depth(node)
                levels[depth].append(node)
        
        # Tasks at same level can be parallelized
        for level, tasks in levels.items():
            if len(tasks) > 1:
                opportunities.append({
                    "level": level,
                    "tasks": tasks,
                    "description": f"{len(tasks)} tasks can be done in parallel"
                })
        
        return {"parallelization_opportunities": opportunities}
    
    def _get_depth(self, node: str) -> int:
        """Calculate depth of a node in the graph"""
        if len(list(self.graph.predecessors(node))) == 0:
            return 0
        return 1 + max(self._get_depth(pred) for pred in self.graph.predecessors(node))
    
    def get_bottlenecks(self) -> List[Dict]:
        """Identify bottleneck tasks"""
        bottlenecks = []
        
        for node in self.graph.nodes():
            successors = list(self.graph.successors(node))
            
            # Tasks with many successors are bottlenecks
            if len(successors) > 2:
                bottlenecks.append({
                    "task_id": node,
                    "num_dependents": len(successors),
                    "warning": f"This task blocks {len(successors)} dependent tasks"
                })
        
        return bottlenecks