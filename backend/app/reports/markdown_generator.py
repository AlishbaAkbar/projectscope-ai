"""
Phase 21: Markdown Report Generator
"""

from datetime import datetime
from typing import Any, Dict


class MarkdownReportGenerator:
    """Generates Markdown reports"""

    def generate(self, analysis: Dict[str, Any]) -> str:
        """Return markdown string"""
        lines = []

        project = analysis.get("project") or {}

        # Header
        lines.append(f"# Project Scope Report: {project.get('name', 'Project')}\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%B %d, %Y')}  ")
        lines.append(f"**Platform:** {project.get('platform', 'Web')}  ")
        lines.append(f"**Status:** {project.get('status', 'Draft')}\n")

        if project.get("description"):
            lines.append(f"> {project['description'][:400]}\n")

        # Executive Summary
        explanation = analysis.get("explanation") or {}
        if explanation.get("summary"):
            lines.append("## Executive Summary\n")
            lines.append(explanation["summary"] + "\n")

        # Key Metrics
        lines.append("## Key Metrics\n")
        cost = (analysis.get("cost") or {}).get("total", {}) or {}
        timeline = analysis.get("timeline") or {}

        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Hours | {analysis.get('total_estimated_hours', 0):.0f} |")
        lines.append(f"| Expected Cost | ${cost.get('expected', 0):,.2f} |")
        lines.append(f"| Cost Range | ${cost.get('min', 0):,.2f} - ${cost.get('max', 0):,.2f} |")
        lines.append(f"| Timeline | {timeline.get('total_working_days', 0)} working days |")
        lines.append(f"| Complexity | {analysis.get('complexity_score', 0):.1f}/100 |")
        lines.append(f"| Risk Level | {analysis.get('risk_level', 'N/A')} |")
        lines.append(f"| Features | {len(analysis.get('features', []))} |")
        lines.append(f"| Tasks | {len(analysis.get('tasks', []))} |\n")

        # Hybrid
        hybrid = analysis.get("hybrid_estimate") or {}
        if hybrid:
            lines.append("## Hybrid Estimation\n")
            bd = hybrid.get("breakdown", {}) or {}
            lines.append(f"- Rule-Based: **{bd.get('rule_based', 0):.0f} hours**")
            lines.append(f"- ML Prediction: **{bd.get('ml_prediction', 0):.0f} hours**")
            lines.append(f"- LLM Suggestion: **{bd.get('llm_suggestion', 0):.0f} hours**")
            lines.append(f"- **Final: {hybrid.get('final_estimate', 0):.0f} hours**")
            lines.append(f"- Confidence: **{hybrid.get('confidence', 0) * 100:.0f}%**\n")

        # Features
        features = analysis.get("features", []) or []
        if features:
            lines.append("## Features\n")
            lines.append("| Feature | Priority | Complexity |")
            lines.append("|---------|----------|------------|")
            for f in features[:25]:
                lines.append(f"| {f.get('canonical_name', '')} | {f.get('priority', '')} | {f.get('complexity', 0)}/10 |")
            lines.append("")

        # Team
        summary = analysis.get("summary", {}) or {}
        if summary:
            lines.append("## Team Allocation\n")
            lines.append("| Role | Hours | Tasks | Cost |")
            lines.append("|------|-------|-------|------|")
            for role, data in summary.items():
                lines.append(f"| {role} | {data.get('total_hours', 0):.0f} | {data.get('num_tasks', 0)} | ${data.get('estimated_cost', 0):,.2f} |")
            lines.append("")

        # Tasks
        tasks = analysis.get("tasks", []) or []
        if tasks:
            lines.append("## Task Breakdown\n")
            lines.append(f"**Total: {len(tasks)} tasks**\n")
            lines.append("| Task | Role | Hours | Priority |")
            lines.append("|------|------|-------|----------|")
            for t in tasks[:30]:
                lines.append(f"| {(t.get('title') or '')[:50]} | Role {t.get('role_id', 0)} | {t.get('estimated_hours', 0):.0f} | {t.get('priority', '')} |")
            lines.append("")

        # Cost
        cost_data = analysis.get("cost") or {}
        if cost_data:
            lines.append("## Cost Estimation\n")
            lines.append("### Total Cost\n")
            total = cost_data.get("total", {}) or {}
            lines.append(f"- Best Case: **${total.get('min', 0):,.2f}**")
            lines.append(f"- Expected: **${total.get('expected', 0):,.2f}**")
            lines.append(f"- Worst Case: **${total.get('max', 0):,.2f}**\n")

            by_role = cost_data.get("by_role", {}) or {}
            if by_role:
                lines.append("### Cost by Role\n")
                lines.append("| Role | Hours | Rate | Cost |")
                lines.append("|------|-------|------|------|")
                for role, data in by_role.items():
                    cv = data.get("cost", 0)
                    if isinstance(cv, dict):
                        cv = cv.get("expected", 0)
                    lines.append(f"| {role} | {data.get('hours', 0):.0f} | ${data.get('rate', 0):.0f}/hr | ${cv:,.2f} |")
                lines.append("")

        # Timeline
        if timeline:
            lines.append("## Timeline\n")
            lines.append(f"- **Start:** {(timeline.get('start_date') or '')[:10]}")
            lines.append(f"- **End:** {(timeline.get('end_date') or '')[:10]}")
            lines.append(f"- **Working Days:** {timeline.get('total_working_days', 0)}\n")

            milestones = timeline.get("milestones", []) or []
            if milestones:
                lines.append("### Milestones\n")
                for m in milestones:
                    lines.append(f"- **{m.get('name', '')}** — {(m.get('date') or '')[:10]}: {m.get('description', '')}")
                lines.append("")

        # Risks
        risks = analysis.get("risks") or {}
        if risks:
            lines.append("## Risk Assessment\n")
            lines.append(f"**Total Risks:** {risks.get('total_risks', 0)} | **Level:** {risks.get('risk_level', 'N/A')}\n")

            for r in risks.get("top_risks", [])[:5]:
                lines.append(f"### {r.get('name', '')}")
                lines.append(f"- **Level:** {r.get('risk_level', '')}")
                lines.append(f"- **Impact:** {r.get('impact', '')}")
                lines.append(f"- **Mitigation:** {r.get('mitigation', '')}\n")

            recs = risks.get("recommendations", []) or []
            if recs:
                lines.append("### Recommendations\n")
                for rec in recs:
                    lines.append(f"- {rec}")
                lines.append("")

        # MVP
        high = [f for f in features if (f.get("priority") or "").upper() in ["HIGH", "CRITICAL"]]
        if high:
            lines.append("## MVP Recommendation\n")
            lines.append(f"Focus on {len(high)} high-priority features:\n")
            for f in high[:10]:
                lines.append(f"- **{f.get('canonical_name', '')}** — {(f.get('description') or '')[:80]}")
            lines.append("")

        # Tech
        lines.append("## Technology Stack\n")
        lines.append("| Layer | Technology |")
        lines.append("|-------|------------|")
        lines.append("| Frontend | Next.js 14 + TypeScript |")
        lines.append("| Backend | FastAPI + Pydantic |")
        lines.append("| Database | PostgreSQL 16 |")
        lines.append("| Deployment | Docker + GitHub Actions |")

        feature_names = [f.get("canonical_name", "") for f in features]
        if "PAYMENT" in feature_names:
            lines.append("| Payments | Stripe |")
        if "AUTHENTICATION" in feature_names:
            lines.append("| Auth | JWT + bcrypt |")
        lines.append("")

        # Assumptions
        assumptions = explanation.get("assumptions", []) or []
        limitations = explanation.get("limitations", []) or []

        if assumptions or limitations:
            lines.append("## Assumptions & Limitations\n")
            if assumptions:
                lines.append("### Assumptions\n")
                for a in assumptions:
                    lines.append(f"- {a}")
                lines.append("")
            if limitations:
                lines.append("### Limitations\n")
                for limitation in limitations:
                    lines.append(f"- {limitation}")
                lines.append("")

        # Footer
        lines.append("---")
        lines.append(f"*Report generated by ProjectScope AI on {datetime.now().strftime('%B %d, %Y at %H:%M')}*")

        return "\n".join(lines)
