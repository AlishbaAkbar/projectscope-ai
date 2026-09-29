"""
Phase 21: CSV Report Generator
Jira-compatible task export
"""

import csv
from datetime import datetime
from typing import Any, Dict


class CSVReportGenerator:
    """Generates Jira-compatible CSV exports"""

    def generate(self, analysis: Dict[str, Any], output_path: str):
        """Generate CSV with Jira-compatible columns"""
        tasks = analysis.get("tasks", []) or []

        # Jira-compatible headers
        headers = [
            "Issue Key",
            "Issue Type",
            "Summary",
            "Description",
            "Priority",
            "Story Points",
            "Original Estimate",
            "Component",
            "Assignee",
            "Labels",
        ]

        project = analysis.get("project") or {}
        project_name = project.get("name", "Project")

        # Priority mapping
        priority_map = {
            "HIGH": "High",
            "CRITICAL": "Highest",
            "MEDIUM": "Medium",
            "LOW": "Low",
        }

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for i, task in enumerate(tasks, start=1):
                issue_key = f"PROJ-{i}"
                hours = task.get("estimated_hours", 0)
                story_points = max(1, round(hours / 4))  # 4 hours per point

                row = [
                    issue_key,
                    "Task",
                    (task.get("title") or "")[:100],
                    (task.get("description") or "")[:200],
                    priority_map.get((task.get("priority") or "MEDIUM").upper(), "Medium"),
                    story_points,
                    f"{hours}h",
                    f"Role-{task.get('role_id', 0)}",
                    "",  # Unassigned
                    f"{project_name},AI-Scoped",
                ]
                writer.writerow(row)

        return output_path
