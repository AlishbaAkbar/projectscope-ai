"""
Phase 12: Risk Engine
Identifies, analyzes, and mitigates project risks
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ImpactLevel(Enum):
    CATASTROPHIC = "CATASTROPHIC"
    MAJOR = "MAJOR"
    MODERATE = "MODERATE"
    MINOR = "MINOR"
    NEGLIGIBLE = "NEGLIGIBLE"


class ProbabilityLevel(Enum):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"


@dataclass
class Risk:
    id: str
    name: str
    description: str
    category: str
    probability: str
    impact: str
    risk_level: str
    mitigation: str
    contingency: str
    owner: str
    score: float = 0.0
    status: str = "IDENTIFIED"


@dataclass
class RiskResult:
    risks: List[Risk]
    total_risks: int
    critical_risks: int
    high_risks: int
    medium_risks: int
    low_risks: int
    risk_score: float
    risk_level: str
    summary: Dict
    recommendations: List[str]


class RiskEngine:
    """Comprehensive risk assessment engine"""
    
    def __init__(self):
        pass
    
    def assess_project(self, 
                       features: List[str],
                       complexities: List[int],
                       integrations: List[str],
                       platform: str = "web",
                       security_level: str = "standard",
                       budget: float = None,
                       timeline: int = None) -> RiskResult:
        """Assess all risks for a project"""
        risks = []
        total_score = 0
        
        # 1. Technical Risk
        if complexities and sum(complexities) / len(complexities) > 5:
            risk = Risk(
                id="RISK-001",
                name="Technical Complexity Risk",
                description=f"Project complexity may exceed team capabilities",
                category="TECHNICAL",
                probability="MEDIUM",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Break down complex features, use proof-of-concepts",
                contingency="Bring in external consultants",
                owner="Tech Lead",
                score=50.0
            )
            risks.append(risk)
            total_score += 50.0
        
        # 2. Schedule Risk
        if len(features) > 10:
            risk = Risk(
                id="RISK-002",
                name="Schedule Risk",
                description=f"Project may not meet planned deadlines ({len(features)} features)",
                category="SCHEDULE",
                probability="MEDIUM",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Buffer time in estimates, daily stand-ups",
                contingency="Reduce scope or extend timeline",
                owner="Project Manager",
                score=55.0
            )
            risks.append(risk)
            total_score += 55.0
        
        # 3. Resource Risk
        if len(features) > 15:
            risk = Risk(
                id="RISK-003",
                name="Resource Risk",
                description="Insufficient or unavailable resources",
                category="RESOURCE",
                probability="MEDIUM",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Cross-train team members",
                contingency="Hire contractors",
                owner="Project Manager",
                score=45.0
            )
            risks.append(risk)
            total_score += 45.0
        
        # 4. Budget Risk
        if len(features) > 12:
            risk = Risk(
                id="RISK-004",
                name="Budget Risk",
                description="Project may exceed allocated budget",
                category="BUDGET",
                probability="LOW",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Track actuals vs estimates weekly",
                contingency="Cut non-essential features",
                owner="CEO",
                score=40.0
            )
            risks.append(risk)
            total_score += 40.0
        
        # 5. Security Risk
        has_payment = any("PAYMENT" in f for f in features)
        if has_payment or security_level in ["high", "very_high"]:
            risk = Risk(
                id="RISK-005",
                name="Security Risk",
                description="Potential security vulnerabilities",
                category="SECURITY",
                probability="MEDIUM",
                impact="MAJOR",
                risk_level="HIGH",
                mitigation="Security review, penetration testing",
                contingency="Implement additional security measures",
                owner="Security Engineer",
                score=65.0
            )
            risks.append(risk)
            total_score += 65.0
        
        # 6. Integration Risk
        if integrations and len(integrations) > 2:
            risk = Risk(
                id="RISK-006",
                name="Integration Risk",
                description=f"Third-party integration may fail ({len(integrations)} integrations)",
                category="INTEGRATION",
                probability="MEDIUM",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Thorough testing, error handling",
                contingency="Alternative provider",
                owner="Backend Developer",
                score=50.0
            )
            risks.append(risk)
            total_score += 50.0
        
        # 7. Compliance Risk
        has_user_data = any("AUTH" in f or "USER" in f for f in features)
        if has_user_data or has_payment:
            risk = Risk(
                id="RISK-007",
                name="Compliance Risk",
                description="Regulatory or legal compliance issues",
                category="COMPLIANCE",
                probability="LOW",
                impact="MAJOR",
                risk_level="HIGH",
                mitigation="Legal review, compliance checklist",
                contingency="Implement additional controls",
                owner="CEO",
                score=60.0
            )
            risks.append(risk)
            total_score += 60.0
        
        # 8. Scalability Risk
        has_realtime = any("REAL_TIME" in f for f in features)
        if has_realtime or platform in ["mobile", "both"]:
            risk = Risk(
                id="RISK-008",
                name="Scalability Risk",
                description="System may not handle expected load",
                category="SCALABILITY",
                probability="LOW",
                impact="MODERATE",
                risk_level="MEDIUM",
                mitigation="Load testing, performance optimization",
                contingency="Auto-scaling, infrastructure upgrade",
                owner="DevOps Engineer",
                score="35.0"
            )
            risks.append(risk)
            total_score += 35.0
        
        # 9. Data Risk
        if len(features) > 8:
            risk = Risk(
                id="RISK-009",
                name="Data Risk",
                description="Data loss or corruption",
                category="DATA",
                probability="LOW",
                impact="MODERATE",
                risk_level="LOW",
                mitigation="Regular backups, data validation",
                contingency="Restore from backup",
                owner="Backend Developer",
                score=30.0
            )
            risks.append(risk)
            total_score += 30.0
        
        # 10. Dependency Risk
        if len(features) > 6:
            risk = Risk(
                id="RISK-010",
                name="Dependency Risk",
                description="External dependencies may cause delays",
                category="DEPENDENCY",
                probability="LOW",
                impact="MINOR",
                risk_level="LOW",
                mitigation="Version locking, fallback packages",
                contingency="Alternative solutions",
                owner="Tech Lead",
                score=25.0
            )
            risks.append(risk)
            total_score += 25.0
        
        # Calculate risk level
        avg_score = total_score / len(risks) if risks else 0
        
        if avg_score >= 70:
            risk_level = "CRITICAL"
        elif avg_score >= 50:
            risk_level = "HIGH"
        elif avg_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Count risks by level
        critical = sum(1 for r in risks if r.risk_level == "CRITICAL")
        high = sum(1 for r in risks if r.risk_level == "HIGH")
        medium = sum(1 for r in risks if r.risk_level == "MEDIUM")
        low = sum(1 for r in risks if r.risk_level == "LOW")
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risks)
        
        return RiskResult(
            risks=risks,
            total_risks=len(risks),
            critical_risks=critical,
            high_risks=high,
            medium_risks=medium,
            low_risks=low,
            risk_score=round(total_score, 2),
            risk_level=risk_level,
            summary={
                "total_score": round(total_score, 2),
                "avg_score": round(avg_score, 2),
                "risk_level": risk_level,
                "critical_risks": critical,
                "high_risks": high,
                "medium_risks": medium,
                "low_risks": low
            },
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, risks: List[Risk]) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        critical = [r for r in risks if r.risk_level == "CRITICAL"]
        high = [r for r in risks if r.risk_level == "HIGH"]
        
        if critical:
            recommendations.append(f"⚠️ CRITICAL: Address {len(critical)} critical risks immediately")
        
        if high:
            recommendations.append(f"🔴 HIGH: Mitigate {len(high)} high risks in the next sprint")
        
        recommendations.append("📋 Create a risk register and review it weekly")
        recommendations.append("🔄 Implement regular status reporting and risk tracking")
        
        # Specific recommendations
        tech_risks = [r for r in risks if r.category == "TECHNICAL" and r.risk_level in ["CRITICAL", "HIGH"]]
        if tech_risks:
            recommendations.append("👨‍💻 Schedule technical design reviews for complex components")
        
        security_risks = [r for r in risks if r.category == "SECURITY" and r.risk_level in ["CRITICAL", "HIGH"]]
        if security_risks:
            recommendations.append("🔒 Perform security audit and penetration testing")
        
        schedule_risks = [r for r in risks if r.category == "SCHEDULE" and r.risk_level in ["CRITICAL", "HIGH"]]
        if schedule_risks:
            recommendations.append("📅 Implement buffer time in project schedule (20-30%)")
        
        return recommendations
    
    def get_risk_summary(self, risk_result: RiskResult) -> Dict:
        """Get formatted risk summary for API response"""
        return {
            "total_risks": risk_result.total_risks,
            "risk_score": risk_result.risk_score,
            "risk_level": risk_result.risk_level,
            "summary": risk_result.summary,
            "risks_by_level": {
                "critical": risk_result.critical_risks,
                "high": risk_result.high_risks,
                "medium": risk_result.medium_risks,
                "low": risk_result.low_risks
            },
            "top_risks": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "category": r.category,
                    "probability": r.probability,
                    "impact": r.impact,
                    "risk_level": r.risk_level,
                    "mitigation": r.mitigation,
                    "contingency": r.contingency,
                    "owner": r.owner,
                    "score": r.score
                }
                for r in risk_result.risks[:5]
            ],
            "recommendations": risk_result.recommendations
        }