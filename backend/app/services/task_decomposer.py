import json
from typing import List, Dict, Optional, Set
from pathlib import Path
from collections import defaultdict

from app.models.feature import Feature
from app.models.task import Task
from app.models.role import Role
from app.schemas.tasks import TaskCreate
from app.services.role_service import RoleService


class TaskDecomposer:
    """
    Phase 7: Task Decomposition Engine
    Now with role name support
    """
    
    def __init__(self, db=None):
        self.db = db
        self.library_path = Path(__file__).parent.parent / "data" / "task_library.json"
        self.task_library = self._load_library()
        self.role_service = RoleService(db) if db else None
    
    def _load_library(self) -> Dict:
        """Load task library from JSON file"""
        if self.library_path.exists():
            with open(self.library_path) as f:
                return json.load(f)
        else:
            # Fallback task library
            return {
                "tasks": {
                    "AUTHENTICATION": {
                        "baseline_tasks": [
                            {"id": "auth_design", "title": "Design authentication flows", "role": "UI/UX Designer", "base_hours": 8},
                            {"id": "auth_backend", "title": "Implement JWT authentication", "role": "Backend Developer", "base_hours": 12},
                            {"id": "auth_frontend", "title": "Build authentication UI", "role": "Frontend Developer", "base_hours": 10},
                            {"id": "auth_security", "title": "Implement security best practices", "role": "Security Engineer", "base_hours": 6},
                            {"id": "auth_testing", "title": "Test authentication flows", "role": "QA Engineer", "base_hours": 6},
                        ]
                    },
                    "PRODUCT_CATALOG": {
                        "baseline_tasks": [
                            {"id": "product_design", "title": "Design product catalog", "role": "UI/UX Designer", "base_hours": 12},
                            {"id": "product_backend", "title": "Build product API", "role": "Backend Developer", "base_hours": 16},
                            {"id": "product_frontend", "title": "Build product pages", "role": "Frontend Developer", "base_hours": 14},
                            {"id": "product_admin", "title": "Build admin product management", "role": "Full-Stack Developer", "base_hours": 10},
                            {"id": "product_testing", "title": "Test product catalog", "role": "QA Engineer", "base_hours": 8},
                        ]
                    },
                    "CART": {
                        "baseline_tasks": [
                            {"id": "cart_design", "title": "Design shopping cart", "role": "UI/UX Designer", "base_hours": 8},
                            {"id": "cart_backend", "title": "Build cart API", "role": "Backend Developer", "base_hours": 10},
                            {"id": "cart_frontend", "title": "Build cart interface", "role": "Frontend Developer", "base_hours": 10},
                            {"id": "cart_testing", "title": "Test cart functionality", "role": "QA Engineer", "base_hours": 6},
                        ]
                    },
                    "PAYMENT": {
                        "baseline_tasks": [
                            {"id": "payment_design", "title": "Design payment flows", "role": "UI/UX Designer", "base_hours": 10},
                            {"id": "payment_business", "title": "Select payment provider", "role": "CEO/Business Owner", "base_hours": 4},
                            {"id": "payment_backend", "title": "Integrate payment gateway", "role": "Backend Developer", "base_hours": 16},
                            {"id": "payment_frontend", "title": "Build payment UI", "role": "Frontend Developer", "base_hours": 10},
                            {"id": "payment_security", "title": "Implement payment security", "role": "Security Engineer", "base_hours": 8},
                            {"id": "payment_testing", "title": "Test payment processing", "role": "QA Engineer", "base_hours": 10},
                        ]
                    },
                    "ORDER_MANAGEMENT": {
                        "baseline_tasks": [
                            {"id": "order_design", "title": "Design order management", "role": "UI/UX Designer", "base_hours": 8},
                            {"id": "order_backend", "title": "Build order management API", "role": "Backend Developer", "base_hours": 12},
                            {"id": "order_frontend", "title": "Build order interface", "role": "Frontend Developer", "base_hours": 10},
                            {"id": "order_testing", "title": "Test order management", "role": "QA Engineer", "base_hours": 6},
                        ]
                    },
                    "ADMIN_PANEL": {
                        "baseline_tasks": [
                            {"id": "admin_design", "title": "Design admin dashboard", "role": "UI/UX Designer", "base_hours": 12},
                            {"id": "admin_backend", "title": "Build admin APIs", "role": "Backend Developer", "base_hours": 16},
                            {"id": "admin_frontend", "title": "Build admin dashboard", "role": "Frontend Developer", "base_hours": 16},
                            {"id": "admin_testing", "title": "Test admin panel", "role": "QA Engineer", "base_hours": 8},
                        ]
                    },
                    "SEARCH": {
                        "baseline_tasks": [
                            {"id": "search_backend", "title": "Implement search functionality", "role": "Backend Developer", "base_hours": 12},
                            {"id": "search_frontend", "title": "Build search interface", "role": "Frontend Developer", "base_hours": 8},
                            {"id": "search_testing", "title": "Test search", "role": "QA Engineer", "base_hours": 4},
                        ]
                    }
                },
                "global_tasks": {
                    "devops": [
                        {"id": "devops_setup", "title": "Set up cloud infrastructure", "role": "DevOps Engineer", "base_hours": 8},
                        {"id": "devops_ci_cd", "title": "Set up CI/CD pipeline", "role": "DevOps Engineer", "base_hours": 8},
                    ],
                    "testing": [
                        {"id": "test_strategy", "title": "Define testing strategy", "role": "QA Engineer", "base_hours": 4},
                        {"id": "test_automation", "title": "Set up test automation", "role": "QA Engineer", "base_hours": 8},
                    ],
                    "project_management": [
                        {"id": "pm_planning", "title": "Project planning", "role": "Product Manager", "base_hours": 4},
                        {"id": "pm_requirements", "title": "Document requirements", "role": "Product Manager", "base_hours": 6},
                    ]
                }
            }
    
    def _get_role_id(self, role_name: str) -> int:
        """Get role ID from role name"""
        role_mapping = {
            "UI/UX Designer": 1,
            "Frontend Developer": 2,
            "Backend Developer": 3,
            "Full-Stack Developer": 4,
            "Mobile Developer": 5,
            "QA Engineer": 6,
            "DevOps Engineer": 7,
            "Security Engineer": 8,
            "Product Manager": 9,
            "CEO/Business Owner": 10,
        }
        return role_mapping.get(role_name, 0)
    
    def _get_role_name(self, role_id: int) -> str:
        """Get role name from role ID"""
        role_mapping = {
            1: "UI/UX Designer",
            2: "Frontend Developer",
            3: "Backend Developer",
            4: "Full-Stack Developer",
            5: "Mobile Developer",
            6: "QA Engineer",
            7: "DevOps Engineer",
            8: "Security Engineer",
            9: "Product Manager",
            10: "CEO/Business Owner",
        }
        return role_mapping.get(role_id, f"Role {role_id}")
    
    def decompose_features(self, features: List[Feature]) -> List[Task]:
        """Decompose features into tasks with role names"""
        all_tasks = []
        
        for feature in features:
            feature_tasks = self._decompose_feature(feature)
            all_tasks.extend(feature_tasks)
        
        if len(features) > 3:
            global_tasks = self._add_global_tasks(features)
            all_tasks.extend(global_tasks)
        
        all_tasks = self._calculate_dependencies(all_tasks)
        all_tasks = self._estimate_durations(all_tasks)
        
        return all_tasks
    
    def _decompose_feature(self, feature: Feature) -> List[Task]:
        """Decompose a single feature into tasks"""
        feature_id = feature.canonical_name
        tasks = []
        
        if feature_id in self.task_library["tasks"]:
            baseline_tasks = self.task_library["tasks"][feature_id]["baseline_tasks"]
            
            for task_data in baseline_tasks:
                complexity_factor = 1.0 + (feature.complexity - 3) * 0.2
                adjusted_hours = round(task_data["base_hours"] * complexity_factor)
                
                role_id = self._get_role_id(task_data["role"])
                role_name = self._get_role_name(role_id)
                
                task = Task(
                    feature_id=feature.id,
                    role_id=role_id,
                    title=task_data["title"],
                    description=task_data.get("description", f"Task: {task_data['title']}"),
                    estimated_hours=adjusted_hours,
                    base_hours=task_data["base_hours"],
                    complexity_factor=complexity_factor,
                    priority=self._calculate_task_priority(feature.priority),
                    project_id=0
                )
                tasks.append(task)
        
        return tasks
    
    def _add_global_tasks(self, features: List[Feature]) -> List[Task]:
        """Add global tasks based on project complexity"""
        tasks = []
        
        for task_data in self.task_library.get("global_tasks", {}).get("devops", []):
            task = Task(
                feature_id=None,
                role_id=self._get_role_id(task_data["role"]),
                title=task_data["title"],
                description=task_data.get("description", ""),
                estimated_hours=task_data["base_hours"],
                base_hours=task_data["base_hours"],
                complexity_factor=1.0,
                priority="HIGH",
                is_global=True,
                project_id=0
            )
            tasks.append(task)
        
        for task_data in self.task_library.get("global_tasks", {}).get("testing", []):
            task = Task(
                feature_id=None,
                role_id=self._get_role_id(task_data["role"]),
                title=task_data["title"],
                description=task_data.get("description", ""),
                estimated_hours=task_data["base_hours"],
                base_hours=task_data["base_hours"],
                complexity_factor=1.0,
                priority="MEDIUM",
                is_global=True,
                project_id=0
            )
            tasks.append(task)
        
        for task_data in self.task_library.get("global_tasks", {}).get("project_management", []):
            task = Task(
                feature_id=None,
                role_id=self._get_role_id(task_data["role"]),
                title=task_data["title"],
                description=task_data.get("description", ""),
                estimated_hours=task_data["base_hours"],
                base_hours=task_data["base_hours"],
                complexity_factor=1.0,
                priority="HIGH",
                is_global=True,
                project_id=0
            )
            tasks.append(task)
        
        return tasks
    
    def _calculate_task_priority(self, feature_priority: str) -> str:
        """Calculate task priority from feature priority"""
        if feature_priority == "HIGH":
            return "HIGH"
        elif feature_priority == "MEDIUM":
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Calculate task dependencies based on roles and order"""
        role_tasks = defaultdict(list)
        for task in tasks:
            role_tasks[task.role_id].append(task)
        
        for role_id, role_task_list in role_tasks.items():
            for idx, task in enumerate(role_task_list):
                if idx > 0:
                    task.dependencies = [role_task_list[idx - 1].id]
        
        return tasks
    
    def _estimate_durations(self, tasks: List[Task]) -> List[Task]:
        """Estimate min, expected, and max hours for each task"""
        for task in tasks:
            task.min_hours = max(1, round(task.estimated_hours * 0.8))
            task.max_hours = round(task.estimated_hours * 1.2)
            task.confidence = 0.8
        return tasks
    
    def get_task_summary(self, tasks: List[Task]) -> Dict:
        """Get summary of tasks by role with role names"""
        summary = {}
        
        for task in tasks:
            role_id = task.role_id
            role_name = self._get_role_name(role_id)
            
            if role_name not in summary:
                summary[role_name] = {
                    "role_id": role_id,
                    "total_hours": 0,
                    "num_tasks": 0,
                    "tasks": []
                }
            
            summary[role_name]["total_hours"] += task.estimated_hours
            summary[role_name]["num_tasks"] += 1
            summary[role_name]["tasks"].append({
                "id": task.id,
                "title": task.title,
                "hours": task.estimated_hours,
                "priority": task.priority
            })
        
        return summary