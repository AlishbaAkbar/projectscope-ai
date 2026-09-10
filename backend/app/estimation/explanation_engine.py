"""
Phase 18: Explainable AI Engine
Provides human-readable explanations for all estimates
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Explanation:
    """Single explanation item"""
    category: str
    title: str
    explanation: str
    impact: str
    factors: List[str] = field(default_factory=list)


@dataclass
class ExplanationResult:
    """Complete explanation result"""
    summary: str
    complexity_explanation: str
    cost_explanation: str
    timeline_explanation: str
    risk_explanation: str
    estimate_explanation: str
    detailed_explanations: List[Explanation]
    assumptions: List[str]
    limitations: List[str]


class ExplanationEngine:
    """
    Generates human-readable explanations for all project estimates
    """
    
    def __init__(self):
        self.explanations = []
    
    def explain_project(self,
                       features: List[str],
                       complexities: List[int],
                       total_hours: float,
                       total_cost: float,
                       timeline_days: int,
                       risks: Dict,
                       complexity_score: float,
                       hybrid_estimate: Dict = None) -> ExplanationResult:
        """
        Generate complete explanation for project
        
        Args:
            features: List of feature names
            complexities: List of complexity scores
            total_hours: Total estimated hours
            total_cost: Total estimated cost
            timeline_days: Timeline in days
            risks: Risk summary
            complexity_score: Complexity score
            hybrid_estimate: Hybrid estimation result
            
        Returns:
            ExplanationResult with all explanations
        """
        explanations = []
        
        # 1. Complexity Explanation
        complexity_exp = self._explain_complexity(features, complexities, complexity_score)
        explanations.append(complexity_exp)
        
        # 2. Cost Explanation
        cost_exp = self._explain_cost(total_hours, total_cost)
        explanations.append(cost_exp)
        
        # 3. Timeline Explanation
        timeline_exp = self._explain_timeline(timeline_days, total_hours)
        explanations.append(timeline_exp)
        
        # 4. Risk Explanation
        risk_exp = self._explain_risks(risks)
        explanations.append(risk_exp)
        
        # 5. Estimate Explanation
        estimate_exp = self._explain_estimate(total_hours, hybrid_estimate)
        explanations.append(estimate_exp)
        
        # Generate summary
        summary = self._generate_summary(
            features, total_hours, total_cost, timeline_days, risks
        )
        
        # Generate assumptions
        assumptions = self._generate_assumptions(features)
        
        # Generate limitations
        limitations = self._generate_limitations()
        
        return ExplanationResult(
            summary=summary,
            complexity_explanation=complexity_exp.explanation,
            cost_explanation=cost_exp.explanation,
            timeline_explanation=timeline_exp.explanation,
            risk_explanation=risk_exp.explanation,
            estimate_explanation=estimate_exp.explanation,
            detailed_explanations=explanations,
            assumptions=assumptions,
            limitations=limitations
        )
    
    def _explain_complexity(self, features: List[str], complexities: List[int], score: float) -> Explanation:
        """Explain complexity score"""
        reasons = []
        
        # Check for specific features
        if "PAYMENT" in features:
            reasons.append("payment integration (high complexity)")
        if "ADMIN_PANEL" in features:
            reasons.append("admin dashboard (multiple roles and permissions)")
        if "AUTHENTICATION" in features:
            reasons.append("user authentication and account management")
        if "REAL_TIME" in features:
            reasons.append("real-time functionality")
        if "MOBILE_APP" in features:
            reasons.append("mobile application support")
        if "ORDER_MANAGEMENT" in features:
            reasons.append("order tracking and management")
        
        # Check complexity levels
        high_complexity_features = [
            f for f, c in zip(features, complexities) if c >= 5
        ]
        if high_complexity_features:
            reasons.append(f"high complexity in: {', '.join(high_complexity_features)}")
        
        # Generate explanation
        if score >= 30:
            level = "high"
            explanation = (
                f"Complexity is {level} ({score:.0f}/100). "
                f"This is because the project contains {len(features)} features including "
                f"{', '.join(reasons)}. The high number of features and their interdependencies "
                f"increase the overall complexity."
            )
        elif score >= 15:
            level = "medium"
            explanation = (
                f"Complexity is {level} ({score:.0f}/100). "
                f"The project has {len(features)} features with moderate complexity. "
                f"Key complexity drivers: {', '.join(reasons[:3]) if reasons else 'standard features'}."
            )
        else:
            level = "low"
            explanation = (
                f"Complexity is {level} ({score:.0f}/100). "
                f"The project has {len(features)} features with relatively simple requirements. "
                f"This should be manageable for a standard development team."
            )
        
        return Explanation(
            category="COMPLEXITY",
            title=f"Complexity Score: {score:.0f}/100 ({level.upper()})",
            explanation=explanation,
            impact=level.upper(),
            factors=reasons
        )
    
    def _explain_cost(self, total_hours: float, total_cost: float) -> Explanation:
        """Explain cost estimate"""
        # Calculate average rate
        avg_rate = total_cost / total_hours if total_hours > 0 else 0
        
        explanation = (
            f"Total estimated cost is ${total_cost:,.2f}. "
            f"This is based on {total_hours:,.1f} hours of work at an average rate of ${avg_rate:.2f}/hour. "
            f"The cost includes all roles (design, development, QA, DevOps) required for the project."
        )
        
        # Add range explanation
        if total_cost > 0:
            min_cost = total_cost * 0.8
            max_cost = total_cost * 1.2
            explanation += (
                f" The cost range is ${min_cost:,.2f} - ${max_cost:,.2f} "
                f"depending on actual implementation complexity and resource availability."
            )
        
        return Explanation(
            category="COST",
            title=f"Estimated Cost: ${total_cost:,.2f}",
            explanation=explanation,
            impact="HIGH" if total_cost > 50000 else "MEDIUM" if total_cost > 20000 else "LOW"
        )
    
    def _explain_timeline(self, timeline_days: int, total_hours: float) -> Explanation:
        """Explain timeline estimate"""
        # Calculate weeks
        weeks = timeline_days / 5 if timeline_days > 0 else 0
        
        explanation = (
            f"Estimated timeline is {timeline_days} working days ({weeks:.1f} weeks). "
            f"With {total_hours:,.1f} total hours and a team working in parallel, "
            f"the project can be completed in this timeframe. "
        )
        
        if timeline_days > 60:
            explanation += "This is a long-term project requiring careful planning and regular milestones."
        elif timeline_days > 30:
            explanation += "This is a medium-term project with multiple phases."
        else:
            explanation += "This is a relatively short project that can be completed quickly."
        
        return Explanation(
            category="TIMELINE",
            title=f"Timeline: {timeline_days} working days",
            explanation=explanation,
            impact="HIGH" if timeline_days > 60 else "MEDIUM" if timeline_days > 30 else "LOW"
        )
    
    def _explain_risks(self, risks: Dict) -> Explanation:
        """Explain risks"""
        total = risks.get("total_risks", 0)
        level = risks.get("risk_level", "UNKNOWN")
        
        # Get top risks
        top_risks = risks.get("top_risks", [])
        risk_names = [r.get("name", "") for r in top_risks[:3]]
        
        explanation = (
            f"Risk assessment identified {total} risks with overall risk level: {level}. "
        )
        
        if risk_names:
            explanation += f"Top risks include: {', '.join(risk_names)}. "
        
        if level in ["CRITICAL", "HIGH"]:
            explanation += (
                "These risks require immediate attention and mitigation strategies. "
                "Consider adding buffer time and resources to address them."
            )
        elif level == "MEDIUM":
            explanation += (
                "These risks should be monitored regularly and mitigation plans should be prepared. "
                "Regular risk reviews are recommended."
            )
        else:
            explanation += (
                "Risk levels are manageable with standard project management practices. "
                "Continue regular monitoring."
            )
        
        return Explanation(
            category="RISK",
            title=f"Risk Level: {level} ({total} risks)",
            explanation=explanation,
            impact=level,
            factors=risk_names
        )
    
    def _explain_estimate(self, total_hours: float, hybrid_estimate: Dict = None) -> Explanation:
        """Explain the estimate calculation"""
        explanation = (
            f"The final estimate of {total_hours:,.1f} hours is calculated using a hybrid approach: "
        )
        
        if hybrid_estimate:
            breakdown = hybrid_estimate.get("breakdown", {})
            weights = hybrid_estimate.get("weights_used", {})
            confidence = hybrid_estimate.get("confidence", 0)
            method = hybrid_estimate.get("reconciliation_method", "Balanced")
            
            explanation += (
                f"Rule-based estimate: {breakdown.get('rule_based', 0):,.1f} hours, "
                f"ML prediction: {breakdown.get('ml_prediction', 0):,.1f} hours, "
                f"LLM suggestion: {breakdown.get('llm_suggestion', 0):,.1f} hours. "
                f"These are combined using {method} reconciliation with weights: "
                f"Rules {weights.get('rule', 0)*100:.0f}%, ML {weights.get('ml', 0)*100:.0f}%, "
                f"LLM {weights.get('llm', 0)*100:.0f}%. "
                f"Confidence level: {confidence*100:.0f}%."
            )
        else:
            explanation += (
                "This estimate is based on a deterministic rule-based engine "
                "using historical task data and complexity factors."
            )
        
        return Explanation(
            category="ESTIMATE",
            title=f"Estimate: {total_hours:,.1f} hours",
            explanation=explanation,
            impact="HIGH"
        )
    
    def _generate_summary(self, features: List[str], total_hours: float,
                          total_cost: float, timeline_days: int, risks: Dict) -> str:
        """Generate executive summary"""
        risk_level = risks.get("risk_level", "UNKNOWN")
        
        summary = (
            f"This project involves {len(features)} key features and is estimated to require "
            f"{total_hours:,.1f} hours of development effort, costing approximately "
            f"${total_cost:,.2f}. The estimated timeline is {timeline_days} working days. "
        )
        
        if risk_level in ["CRITICAL", "HIGH"]:
            summary += (
                f"⚠️ The project has {risk_level} risk level and requires careful attention "
                f"to security, compliance, and technical challenges."
            )
        elif risk_level == "MEDIUM":
            summary += (
                f"The project has {risk_level} risk level. Regular monitoring and "
                f"mitigation strategies are recommended."
            )
        else:
            summary += (
                f"The project has {risk_level} risk level and should proceed smoothly "
                f"with standard development practices."
            )
        
        return summary
    
    def _generate_assumptions(self, features: List[str]) -> List[str]:
        """Generate list of assumptions"""
        assumptions = [
            "The project scope remains stable throughout development",
            "Required resources (developers, designers, QA) are available",
            "No major technical blockers or unexpected dependencies",
            "Client provides timely feedback and approvals",
            "Third-party services (if any) remain available and functional"
        ]
        
        if "PAYMENT" in features:
            assumptions.append("Payment provider account will be set up and approved")
        
        if "MOBILE_APP" in features:
            assumptions.append("App store approval processes will be completed on time")
        
        if "REAL_TIME" in features:
            assumptions.append("Infrastructure can support real-time connections")
        
        return assumptions
    
    def _generate_limitations(self) -> List[str]:
        """Generate list of limitations"""
        return [
            "Estimates are based on similar historical projects and may vary",
            "Actual effort depends on team experience and skill level",
            "Changes in requirements will affect estimates",
            "External factors (market, technology) may impact timeline",
            "ML predictions are based on limited historical data and may improve over time"
        ]
    
    def get_formatted_explanation(self, result: ExplanationResult) -> Dict:
        """Format explanation for API response"""
        return {
            "summary": result.summary,
            "explanations": {
                "complexity": result.complexity_explanation,
                "cost": result.cost_explanation,
                "timeline": result.timeline_explanation,
                "risks": result.risk_explanation,
                "estimate": result.estimate_explanation
            },
            "detailed_explanations": [
                {
                    "category": exp.category,
                    "title": exp.title,
                    "explanation": exp.explanation,
                    "impact": exp.impact,
                    "factors": exp.factors
                }
                for exp in result.detailed_explanations
            ],
            "assumptions": result.assumptions,
            "limitations": result.limitations
        }