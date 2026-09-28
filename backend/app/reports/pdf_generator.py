"""
Phase 21: PDF Report Generator
Uses ReportLab for professional PDF output
"""

from altair import value
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any, List
from datetime import datetime

from traitlets import default


class PDFReportGenerator:
    """Generates professional PDF reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _safe_float(self, value, default: float = 0.0) -> float:
        """Safely convert any value to float"""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _setup_styles(self):
        """Custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceBefore=16,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            spaceBefore=10,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=6,
            leading=14
        ))
    
    def generate(self, analysis: Dict[str, Any], output_path: str):
        """Generate PDF report"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title=f"Project Report - {analysis.get('project', {}).get('name', 'Project')}",
            author="ProjectScope AI"
        )
        
        story = []
        
        # Cover Page
        story.extend(self._build_cover_page(analysis))
        story.append(PageBreak())
        
        # Executive Summary
        story.extend(self._build_executive_summary(analysis))
        story.append(PageBreak())
        
        # Requirements & Features
        story.extend(self._build_requirements_features(analysis))
        
        # Team Allocation
        story.extend(self._build_team(analysis))
        
        # Tasks
        story.extend(self._build_tasks(analysis))
        
        # Cost
        story.extend(self._build_cost(analysis))
        
        # Timeline
        story.extend(self._build_timeline(analysis))
        
        # Risks
        story.extend(self._build_risks(analysis))
        
        # MVP
        story.extend(self._build_mvp(analysis))
        
        # Technology
        story.extend(self._build_technology(analysis))
        
        # Assumptions & Limitations
        story.extend(self._build_assumptions(analysis))
        
        doc.build(story)
    
    def _build_cover_page(self, analysis: Dict) -> List:
        """Cover page"""
        story = []
        
        project = analysis.get("project", {}) or {}
        name = project.get("name", "Project")
        description = project.get("description", "")
        
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("PROJECT SCOPE REPORT", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Project name
        name_style = ParagraphStyle(
            name='ProjectName',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(name, name_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Meta table
        total_hours = self._safe_float(analysis.get('total_estimated_hours', 0))
        total_cost = self._safe_float(
            (analysis.get('cost') or {}).get('total', {}).get('expected', 0)
        )

        meta_data = [
            ["Generated", datetime.now().strftime("%B %d, %Y")],
            ["Platform", str(project.get("platform", "Web"))],
            ["Status", str(project.get("status", "Draft"))],
            ["Total Hours", f"{total_hours:.0f}"],
            ["Total Cost", f"${total_cost:,.2f}"],
            ["Risk Level", str(analysis.get('risk_level', 'MEDIUM'))],
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 3*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Description
        if description:
            story.append(Paragraph("<b>Project Description</b>", self.styles['SubHeading']))
            story.append(Paragraph(description[:500], self.styles['CustomBody']))
        
        return story
    
    def _build_executive_summary(self, analysis: Dict) -> List:
        """Executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeading']))
        
        # Summary from explanation
        explanation = analysis.get("explanation", {}) or {}
        summary_text = explanation.get("summary", "")
        
        if summary_text:
            story.append(Paragraph(summary_text, self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Key metrics table
        story.append(Paragraph("Key Metrics", self.styles['SubHeading']))
        
        total_hours = self._safe_float(analysis.get("total_estimated_hours", 0))
        cost = (analysis.get("cost") or {}).get("total", {}) or {}
        timeline = analysis.get("timeline") or {}
        complexity = self._safe_float(analysis.get('complexity_score', 0))

        metrics_data = [
            ["Metric", "Value"],
            ["Total Estimated Hours", f"{total_hours:.0f} hours"],
            ["Total Cost (Expected)", f"${self._safe_float(cost.get('expected', 0)):,.2f}"],
            ["Total Cost Range", f"${self._safe_float(cost.get('min', 0)):,.2f} - ${self._safe_float(cost.get('max', 0)):,.2f}"],
            ["Timeline", f"{timeline.get('total_working_days', 0)} working days"],
            ["Complexity Score", f"{complexity:.1f}/100"],
            ["Risk Level", str(analysis.get('risk_level', 'N/A'))],
            ["Features", f"{len(analysis.get('features', []))}"],
            ["Tasks", f"{len(analysis.get('tasks', []))}"],
            ["Roles", f"{len(analysis.get('roles', []))}"],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Hybrid estimate
        hybrid = analysis.get("hybrid_estimate") or {}
        if hybrid:
            story.append(Paragraph("Hybrid Estimation Breakdown", self.styles['SubHeading']))
            breakdown = hybrid.get("breakdown", {}) or {}
            weights = hybrid.get("weights_used", {}) or {}

            breakdown_data = [
                ["Source", "Hours", "Weight"],
                ["Rule-Based Estimate", f"{self._safe_float(breakdown.get('rule_based', 0)):.0f}", f"{self._safe_float(weights.get('rule', 0))*100:.0f}%"],
                ["ML Prediction", f"{self._safe_float(breakdown.get('ml_prediction', 0)):.0f}", f"{self._safe_float(weights.get('ml', 0))*100:.0f}%"],
                ["LLM Suggestion", f"{self._safe_float(breakdown.get('llm_suggestion', 0)):.0f}", f"{self._safe_float(weights.get('llm', 0))*100:.0f}%"],
                ["Final Estimate", f"{self._safe_float(hybrid.get('final_estimate', 0)):.0f}", "100%"],
            ]
            
            bd_table = Table(breakdown_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            bd_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dbeafe')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(bd_table)
        
        return story
    
    def _build_requirements_features(self, analysis: Dict) -> List:
        """Requirements and features section"""
        story = []
        
        story.append(Paragraph("Requirements & Features", self.styles['SectionHeading']))
        
        # Features
        features = analysis.get("features", []) or []
        if features:
            story.append(Paragraph(f"Extracted Features ({len(features)})", self.styles['SubHeading']))
            
            feature_data = [["Feature", "Priority", "Complexity"]]
            for f in features[:20]:
                feature_data.append([
                    f.get("canonical_name", "N/A"),
                    f.get("priority", "MEDIUM"),
                    f"{f.get('complexity', 0)}/10"
                ])
            
            feature_table = Table(feature_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            feature_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(feature_table)
            story.append(Spacer(1, 0.3*inch))
        
        return story
    
    def _build_team(self, analysis: Dict) -> List:
        """Team allocation section"""
        story = []
        
        story.append(Paragraph("Team Allocation", self.styles['SectionHeading']))
        
        summary = analysis.get("summary", {}) or {}
        if summary:
            team_data = [["Role", "Hours", "Tasks", "Cost"]]
            for role, data in summary.items():
                hours = self._safe_float(data.get('total_hours', 0))
                tasks = data.get('num_tasks', 0)
                cost = self._safe_float(data.get('estimated_cost', 0))
                team_data.append([
                    str(role),
                    f"{hours:.0f}",
                    str(tasks),
                    f"${cost:,.2f}"
                ])
            
            team_table = Table(team_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.6*inch])
            team_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(team_table)
        
        story.append(Spacer(1, 0.3*inch))
        return story
        
    
    def _build_tasks(self, analysis: Dict) -> List:
        """Task breakdown section"""
        story = []
        
        story.append(Paragraph("Task Breakdown", self.styles['SectionHeading']))
        
        tasks = analysis.get("tasks", []) or []
        if tasks:
            story.append(Paragraph(f"Total Tasks: {len(tasks)}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))
            
            task_data = [["Task", "Role", "Hours", "Priority"]]
            for task in tasks[:30]:
                hours = self._safe_float(task.get('estimated_hours', 0))
                task_data.append([
                    str(task.get("title", ""))[:50],
                    f"Role {task.get('role_id', 0)}",
                    f"{hours:.0f}",
                    str(task.get("priority", "MEDIUM"))
                ])
            
            task_table = Table(task_data, colWidths=[3.5*inch, 1*inch, 0.8*inch, 1*inch])
            task_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(task_table)
        
        story.append(PageBreak())
        return story
    
    def _build_cost(self, analysis: Dict) -> List:
        """Cost breakdown section"""
        story = []
        
        story.append(Paragraph("Cost Estimation", self.styles['SectionHeading']))
        
        cost = analysis.get("cost") or {}
        total = cost.get("total", {}) or {}
        
        # Safe float conversion
        min_cost = self._safe_float(total.get('min', 0))
        expected_cost = self._safe_float(total.get('expected', 0))
        max_cost = self._safe_float(total.get('max', 0))
        
        story.append(Paragraph("Total Project Cost", self.styles['SubHeading']))
        
        cost_data = [
            ["Scenario", "Amount"],
            ["Best Case (Min)", f"${min_cost:,.2f}"],
            ["Expected", f"${expected_cost:,.2f}"],
            ["Worst Case (Max)", f"${max_cost:,.2f}"],
        ]
        
        cost_table = Table(cost_data, colWidths=[3*inch, 3*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#dbeafe')),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(cost_table)
        story.append(Spacer(1, 0.3*inch))
        
        # By role
        by_role = cost.get("by_role", {}) or {}
        if by_role:
            story.append(Paragraph("Cost by Role", self.styles['SubHeading']))
            
            role_data = [["Role", "Hours", "Rate", "Cost"]]
            for role, data in by_role.items():
                cost_val = data.get("cost", 0)
                if isinstance(cost_val, dict):
                    cost_val = cost_val.get("expected", 0)
                cost_val = self._safe_float(cost_val)
                hours = self._safe_float(data.get('hours', 0))
                rate = self._safe_float(data.get('rate', 0))
                
                role_data.append([
                    str(role),
                    f"{hours:.0f}",
                    f"${rate:.0f}/hr",
                    f"${cost_val:,.2f}"
                ])
            
            role_table = Table(role_data, colWidths=[2.2*inch, 1*inch, 1.2*inch, 1.6*inch])
            role_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(role_table)
        
        return story
    
    def _build_timeline(self, analysis: Dict) -> List:
        """Timeline section"""
        story = []
        
        story.append(Paragraph("Timeline & Critical Path", self.styles['SectionHeading']))
        
        timeline = analysis.get("timeline") or {}
        
        if timeline:
            start = (timeline.get('start_date') or 'N/A')[:10]
            end = (timeline.get('end_date') or 'N/A')[:10]
            story.append(Paragraph(
                f"<b>Start:</b> {start} &nbsp;&nbsp; "
                f"<b>End:</b> {end} &nbsp;&nbsp; "
                f"<b>Duration:</b> {timeline.get('total_working_days', 0)} working days",
                self.styles['CustomBody']
            ))
            story.append(Spacer(1, 0.2*inch))
            
            # Milestones
            milestones = timeline.get("milestones", []) or []
            if milestones:
                story.append(Paragraph("Milestones", self.styles['SubHeading']))
                
                ms_data = [["Milestone", "Date", "Description"]]
                for m in milestones:
                    ms_data.append([
                        m.get("name", ""),
                        (m.get("date") or "")[:10],
                        (m.get("description") or "")[:50]
                    ])
                
                ms_table = Table(ms_data, colWidths=[1.5*inch, 1.2*inch, 3.3*inch])
                ms_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(ms_table)
        
        story.append(PageBreak())
        return story
    
    def _build_risks(self, analysis: Dict) -> List:
        """Risk section"""
        story = []
        
        story.append(Paragraph("Risk Assessment", self.styles['SectionHeading']))
        
        risks = analysis.get("risks") or {}
        
        if risks:
            story.append(Paragraph(
                f"<b>Total Risks:</b> {risks.get('total_risks', 0)} &nbsp;&nbsp; "
                f"<b>Overall Risk Level:</b> {risks.get('risk_level', 'N/A')} &nbsp;&nbsp; "
                f"<b>Risk Score:</b> {risks.get('risk_score', 0):.1f}",
                self.styles['CustomBody']
            ))
            story.append(Spacer(1, 0.2*inch))
            
            # Top risks
            top_risks = risks.get("top_risks", []) or []
            if top_risks:
                story.append(Paragraph("Top Risks", self.styles['SubHeading']))
                
                risk_data = [["Risk", "Level", "Impact", "Mitigation"]]
                for r in top_risks:
                    risk_data.append([
                        (r.get("name") or "")[:30],
                        r.get("risk_level", ""),
                        r.get("impact", ""),
                        (r.get("mitigation") or "")[:40]
                    ])
                
                risk_table = Table(risk_data, colWidths=[1.8*inch, 0.8*inch, 0.8*inch, 2.6*inch])
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(risk_table)
                story.append(Spacer(1, 0.2*inch))
            
            # Recommendations
            recommendations = risks.get("recommendations", []) or []
            if recommendations:
                story.append(Paragraph("Recommendations", self.styles['SubHeading']))
                for rec in recommendations:
                    story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        return story
    
    def _build_mvp(self, analysis: Dict) -> List:
        """MVP recommendation section"""
        story = []
        
        story.append(Paragraph("MVP Recommendation", self.styles['SectionHeading']))
        
        features = analysis.get("features", []) or []
        high_priority = [
            f for f in features
            if (f.get("priority") or "").upper() in ["HIGH", "CRITICAL"]
        ]
        
        story.append(Paragraph(
            f"Based on our analysis, the MVP should focus on {len(high_priority)} high-priority features "
            f"to deliver core value quickly. The remaining {len(features) - len(high_priority)} features "
            f"can be added in Phase 2.",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.15*inch))
        
        if high_priority:
            story.append(Paragraph("MVP Core Features", self.styles['SubHeading']))
            for f in high_priority[:10]:
                story.append(Paragraph(
                    f"• <b>{f.get('canonical_name', '')}</b> — {(f.get('description') or '')[:80]}",
                    self.styles['CustomBody']
                ))
        
        return story
    
    def _build_technology(self, analysis: Dict) -> List:
        """Technology recommendations"""
        story = []
        
        story.append(Paragraph("Technology Recommendations", self.styles['SectionHeading']))
        
        # Derived from features
        features = [f.get("canonical_name", "") for f in analysis.get("features", []) or []]
        
        tech_stack = [
            ("Frontend", "Next.js 14 + TypeScript + Tailwind CSS"),
            ("Backend", "Python FastAPI + Pydantic v2"),
            ("Database", "PostgreSQL 16"),
            ("Cache/Queue", "Redis + Celery"),
            ("Deployment", "Docker + GitHub Actions"),
        ]
        
        if "AUTHENTICATION" in features:
            tech_stack.append(("Auth", "JWT + bcrypt/argon2"))
        if "PAYMENT" in features:
            tech_stack.append(("Payments", "Stripe / PayPal"))
        if "REAL_TIME" in features:
            tech_stack.append(("Real-time", "WebSockets + Redis Pub/Sub"))
        if "MOBILE_APP" in features:
            tech_stack.append(("Mobile", "React Native / Flutter"))
        
        tech_data = [["Layer", "Recommended Technology"]] + tech_stack
        
        tech_table = Table(tech_data, colWidths=[2*inch, 4*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tech_table)
        story.append(PageBreak())
        
        return story
    
    def _build_assumptions(self, analysis: Dict) -> List:
        """Assumptions & limitations"""
        story = []
        
        explanation = analysis.get("explanation") or {}
        
        # Assumptions
        assumptions = explanation.get("assumptions", []) or []
        if assumptions:
            story.append(Paragraph("Assumptions", self.styles['SectionHeading']))
            for a in assumptions:
                story.append(Paragraph(f"• {a}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Limitations
        limitations = explanation.get("limitations", []) or []
        if limitations:
            story.append(Paragraph("Limitations", self.styles['SectionHeading']))
            for l in limitations:
                story.append(Paragraph(f"• {l}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Confidence
        hybrid = analysis.get("hybrid_estimate") or {}
        confidence = hybrid.get("confidence", 0)
        story.append(Paragraph("Confidence Level", self.styles['SectionHeading']))
        story.append(Paragraph(
            f"Overall confidence: <b>{confidence * 100:.0f}%</b>. "
            f"This confidence is based on data quality, model performance, and project complexity.",
            self.styles['CustomBody']
        ))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        line_style = ParagraphStyle(
            name='Line',
            alignment=TA_CENTER,
            textColor=colors.HexColor('#cbd5e1')
        )
        story.append(Paragraph("─" * 50, line_style))
        story.append(Paragraph(
            f"Report generated by ProjectScope AI on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
            line_style
        ))
        
        return story