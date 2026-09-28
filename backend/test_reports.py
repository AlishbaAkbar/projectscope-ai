"""
Test Phase 21 report generation directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.project import Project
from app.models.feature import Feature
from app.models.task import Task
from app.reports.report_service import ReportService


def build_analysis_dict(project_id: int):
    """Build a simple analysis dict from DB"""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            print(f"❌ Project {project_id} not found")
            return None
        
        features = db.query(Feature).filter(Feature.project_id == project_id).all()
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # Build minimal analysis dict
        total_hours = sum(t.estimated_hours for t in tasks)
        
        # Role summary
        summary = {}
        for task in tasks:
            role_key = f"Role {task.role_id}"
            if role_key not in summary:
                summary[role_key] = {"total_hours": 0, "num_tasks": 0, "estimated_cost": 0}
            summary[role_key]["total_hours"] += task.estimated_hours
            summary[role_key]["num_tasks"] += 1
            summary[role_key]["estimated_cost"] += task.estimated_hours * 50
        
        analysis = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "platform": project.platform or "Web",
                "status": project.status or "draft",
                "type": project.type,
            },
            "features": [
                {
                    "id": f.id,
                    "canonical_name": f.canonical_name,
                    "description": f.description,
                    "priority": f.priority,
                    "complexity": f.complexity,
                }
                for f in features
            ],
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "role_id": t.role_id,
                    "estimated_hours": t.estimated_hours,
                    "priority": t.priority,
                }
                for t in tasks
            ],
            "roles": list(summary.keys()),
            "total_estimated_hours": total_hours,
            "complexity_score": sum(f.complexity for f in features),
            "risk_level": "MEDIUM",
            "summary": summary,
            "timeline": {
                "start_date": "2026-09-22T09:00:00",
                "end_date": "2026-10-15T17:00:00",
                "total_days": 23,
                "total_working_days": 17,
                "critical_path": [],
                "milestones": [
                    {"name": "Project Start", "date": "2026-09-22T09:00:00", "description": "Kickoff"},
                    {"name": "50% Complete", "date": "2026-10-03T17:00:00", "description": "Mid-point"},
                    {"name": "100% Complete", "date": "2026-10-15T17:00:00", "description": "Launch"},
                ],
                "weekly_breakdown": {},
                "parallelization_opportunities": [],
                "bottlenecks": [],
            },
            "cost": {
                "total": {
                    "min": round(total_hours * 50 * 0.8, 2),
                    "expected": round(total_hours * 50, 2),
                    "max": round(total_hours * 50 * 1.2, 2),
                    "formatted": {
                        "min": f"${total_hours * 50 * 0.8:,.2f}",
                        "expected": f"${total_hours * 50:,.2f}",
                        "max": f"${total_hours * 50 * 1.2:,.2f}",
                    }
                },
                "by_role": {
                    role: {
                        "hours": data["total_hours"],
                        "rate": 50,
                        "cost": {"expected": data["estimated_cost"]},
                    }
                    for role, data in summary.items()
                },
                "summary": {"num_roles": len(summary), "total_hours": total_hours},
            },
            "risks": {
                "total_risks": 5,
                "risk_score": 45,
                "risk_level": "MEDIUM",
                "risks_by_level": {"critical": 0, "high": 1, "medium": 3, "low": 1},
                "top_risks": [
                    {
                        "id": "RISK-001",
                        "name": "Technical Complexity",
                        "risk_level": "HIGH",
                        "impact": "MAJOR",
                        "mitigation": "Break down complex features",
                    },
                ],
                "recommendations": ["Create risk register", "Weekly reviews"],
            },
            "hybrid_estimate": {
                "final_estimate": total_hours,
                "range": {"min": total_hours * 0.85, "max": total_hours * 1.2},
                "confidence": 0.75,
                "reconciliation_method": "Rule-Dominant",
                "breakdown": {
                    "rule_based": total_hours,
                    "ml_prediction": total_hours * 0.95,
                    "llm_suggestion": total_hours,
                },
                "weights_used": {"rule": 0.5, "ml": 0.25, "llm": 0.25},
            },
            "explanation": {
                "summary": f"This project involves {len(features)} features and {len(tasks)} tasks.",
                "explanations": {},
                "detailed_explanations": [],
                "assumptions": [
                    "Scope remains stable",
                    "Resources available",
                ],
                "limitations": [
                    "Estimates based on similar projects",
                ],
                "knowledge_used": [],
            },
        }
        
        return analysis
    finally:
        db.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_reports.py <project_id>")
        return
    
    project_id = int(sys.argv[1])
    print(f"🔄 Testing reports for project {project_id}...")
    
    analysis = build_analysis_dict(project_id)
    if not analysis:
        return
    
    service = ReportService()
    
    print("\n📄 Generating PDF...")
    try:
        pdf_path = service.generate_pdf(project_id, analysis)
        print(f"✅ PDF: {pdf_path}")
    except Exception as e:
        print(f"❌ PDF failed: {e}")
    
    print("\n📝 Generating DOCX...")
    try:
        docx_path = service.generate_docx(project_id, analysis)
        print(f"✅ DOCX: {docx_path}")
    except Exception as e:
        print(f"❌ DOCX failed: {e}")
    
    print("\n📋 Generating Markdown...")
    try:
        md_path = service.generate_markdown(project_id, analysis)
        print(f"✅ Markdown: {md_path}")
    except Exception as e:
        print(f"❌ Markdown failed: {e}")
    
    print("\n📊 Generating CSV...")
    try:
        csv_path = service.generate_csv(project_id, analysis)
        print(f"✅ CSV: {csv_path}")
    except Exception as e:
        print(f"❌ CSV failed: {e}")
    
    print("\n🎉 Done! Check reports/generated/")


if __name__ == "__main__":
    main()