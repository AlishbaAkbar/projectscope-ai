"""
Phase 21: Report Service
Central service for all report generation
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ReportService:
    """Central report generation service"""

    def __init__(self, output_dir: str = "reports/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, project_id: int, project_name: str, extension: str) -> str:
        """Generate unique filename"""
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"project_{project_id}_{safe_name}_{timestamp}.{extension}"

    def generate_pdf(self, project_id: int, analysis: Dict[str, Any]) -> str:
        """Generate PDF report"""
        from app.reports.pdf_generator import PDFReportGenerator

        project_name = analysis.get("project", {}).get("name", "Project")
        filename = self._generate_filename(project_id, project_name, "pdf")
        filepath = self.output_dir / filename

        generator = PDFReportGenerator()
        generator.generate(analysis, str(filepath))

        return str(filepath)

    def generate_docx(self, project_id: int, analysis: Dict[str, Any]) -> str:
        """Generate DOCX report"""
        from app.reports.docx_generator import DOCXReportGenerator

        project_name = analysis.get("project", {}).get("name", "Project")
        filename = self._generate_filename(project_id, project_name, "docx")
        filepath = self.output_dir / filename

        generator = DOCXReportGenerator()
        generator.generate(analysis, str(filepath))

        return str(filepath)

    def generate_markdown(self, project_id: int, analysis: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        from app.reports.markdown_generator import MarkdownReportGenerator

        project_name = analysis.get("project", {}).get("name", "Project")
        filename = self._generate_filename(project_id, project_name, "md")
        filepath = self.output_dir / filename

        generator = MarkdownReportGenerator()
        content = generator.generate(analysis)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return str(filepath)

    def generate_csv(self, project_id: int, analysis: Dict[str, Any]) -> str:
        """Generate CSV (Jira-compatible tasks)"""
        from app.reports.csv_generator import CSVReportGenerator

        project_name = analysis.get("project", {}).get("name", "Project")
        filename = self._generate_filename(project_id, project_name, "csv")
        filepath = self.output_dir / filename

        generator = CSVReportGenerator()
        generator.generate(analysis, str(filepath))

        return str(filepath)

    def generate_all(self, project_id: int, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate all report formats"""
        return {
            "pdf": self.generate_pdf(project_id, analysis),
            "docx": self.generate_docx(project_id, analysis),
            "markdown": self.generate_markdown(project_id, analysis),
            "csv": self.generate_csv(project_id, analysis),
        }

    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """Get file metadata"""
        path = Path(filepath)
        if not path.exists():
            return {}

        return {
            "filename": path.name,
            "size": path.stat().st_size,
            "size_kb": round(path.stat().st_size / 1024, 2),
            "extension": path.suffix,
            "created_at": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
        }
