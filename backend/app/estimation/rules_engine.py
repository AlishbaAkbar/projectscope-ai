"""
Phase 9: Deterministic Estimation Engine
Rule-based estimation with complexity and integration factors
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class EstimateResult:
    """Estimation result with min, expected, max values"""
    min_hours: float
    expected_hours: float
    max_hours: float
    confidence: float
    factors_used: Dict[str, float]
    breakdown: Dict[str, float]


class EstimationEngine:
    """
    Deterministic estimation engine with rule-based calculations
    """
    
    # Base complexity levels
    COMPLEXITY_LEVELS = {
        "LOW": 1.0,
        "MEDIUM": 1.5,
        "HIGH": 2.0,
        "VERY_HIGH": 2.5
    }
    
    # Integration complexity multipliers
    INTEGRATION_FACTORS = {
        "none": 1.0,
        "simple_api": 1.2,
        "external_api": 1.5,
        "payment_gateway": 2.0,
        "third_party_sso": 1.8,
        "multiple_integrations": 2.2
    }
    
    # Platform factors
    PLATFORM_FACTORS = {
        "web": 1.0,
        "mobile": 1.5,
        "both": 2.0,
        "desktop": 1.3
    }
    
    # Security factors
    SECURITY_FACTORS = {
        "basic": 1.0,
        "standard": 1.3,
        "high": 1.7,
        "very_high": 2.0
    }
    
    def __init__(self):
        self.task_library = self._load_task_library()
    
    def _load_task_library(self) -> Dict:
        """Load task library with baseline hours"""
        return {
            "AUTHENTICATION": {
                "base_hours": 20,
                "complexity": "MEDIUM",
                "tasks": [
                    {"name": "Design auth flows", "hours": 8},
                    {"name": "Implement JWT", "hours": 12},
                    {"name": "Build auth UI", "hours": 10},
                    {"name": "Security hardening", "hours": 6},
                    {"name": "Testing", "hours": 6}
                ]
            },
            "PRODUCT_CATALOG": {
                "base_hours": 30,
                "complexity": "MEDIUM",
                "tasks": [
                    {"name": "Design catalog", "hours": 12},
                    {"name": "Build product API", "hours": 16},
                    {"name": "Build product UI", "hours": 14},
                    {"name": "Admin panel", "hours": 10},
                    {"name": "Testing", "hours": 8}
                ]
            },
            "CART": {
                "base_hours": 20,
                "complexity": "LOW",
                "tasks": [
                    {"name": "Design cart", "hours": 8},
                    {"name": "Build cart API", "hours": 10},
                    {"name": "Build cart UI", "hours": 10},
                    {"name": "Testing", "hours": 6}
                ]
            },
            "PAYMENT": {
                "base_hours": 35,
                "complexity": "HIGH",
                "tasks": [
                    {"name": "Design payment flows", "hours": 10},
                    {"name": "Select provider", "hours": 4},
                    {"name": "Integrate gateway", "hours": 16},
                    {"name": "Build payment UI", "hours": 10},
                    {"name": "Security", "hours": 8},
                    {"name": "Testing", "hours": 10}
                ]
            },
            "ORDER_MANAGEMENT": {
                "base_hours": 25,
                "complexity": "MEDIUM",
                "tasks": [
                    {"name": "Design order management", "hours": 8},
                    {"name": "Build order API", "hours": 12},
                    {"name": "Build order UI", "hours": 10},
                    {"name": "Testing", "hours": 6}
                ]
            },
            "ADMIN_PANEL": {
                "base_hours": 30,
                "complexity": "HIGH",
                "tasks": [
                    {"name": "Design admin dashboard", "hours": 12},
                    {"name": "Build admin APIs", "hours": 16},
                    {"name": "Build admin UI", "hours": 16},
                    {"name": "Testing", "hours": 8}
                ]
            },
            "MOBILE_APP": {
                "base_hours": 40,
                "complexity": "HIGH",
                "tasks": [
                    {"name": "Architecture", "hours": 8},
                    {"name": "Mobile auth", "hours": 12},
                    {"name": "Mobile UI", "hours": 20},
                    {"name": "API integration", "hours": 16},
                    {"name": "Testing", "hours": 10}
                ]
            },
            "SEARCH": {
                "base_hours": 15,
                "complexity": "LOW",
                "tasks": [
                    {"name": "Implement search", "hours": 12},
                    {"name": "Search UI", "hours": 8},
                    {"name": "Testing", "hours": 4}
                ]
            },
            "REVIEWS": {
                "base_hours": 15,
                "complexity": "LOW",
                "tasks": [
                    {"name": "Design reviews", "hours": 6},
                    {"name": "Build reviews API", "hours": 10},
                    {"name": "Build reviews UI", "hours": 8},
                    {"name": "Testing", "hours": 4}
                ]
            },
            "NOTIFICATIONS": {
                "base_hours": 15,
                "complexity": "LOW",
                "tasks": [
                    {"name": "Build notification system", "hours": 10},
                    {"name": "Notification UI", "hours": 6},
                    {"name": "Testing", "hours": 4}
                ]
            },
            "ANALYTICS": {
                "base_hours": 20,
                "complexity": "MEDIUM",
                "tasks": [
                    {"name": "Build analytics system", "hours": 12},
                    {"name": "Analytics dashboard", "hours": 10},
                    {"name": "Testing", "hours": 4}
                ]
            }
        }
    
    def estimate_feature(self, 
                        feature_name: str, 
                        complexity: int,
                        integrations: List[str] = None,
                        platform: str = "web",
                        security_level: str = "standard") -> EstimateResult:
        """
        Estimate hours for a single feature
        
        Args:
            feature_name: Canonical feature name
            complexity: Complexity score (1-10)
            integrations: List of integration types
            platform: Target platform
            security_level: Security requirement level
            
        Returns:
            EstimateResult with min/expected/max hours
        """
        # Get base hours
        feature_data = self.task_library.get(feature_name, {})
        base_hours = feature_data.get("base_hours", 10)
        base_complexity = feature_data.get("complexity", "MEDIUM")
        
        # Calculate complexity factor (1-10 scale)
        complexity_factor = 1.0 + (complexity - 3) * 0.2
        complexity_factor = max(0.5, min(2.5, complexity_factor))
        
        # Integration factor
        integration_factor = self._calculate_integration_factor(integrations or [])
        
        # Platform factor
        platform_factor = self.PLATFORM_FACTORS.get(platform, 1.0)
        
        # Security factor
        security_factor = self.SECURITY_FACTORS.get(security_level, 1.3)
        
        # Calculate expected hours
        expected_hours = base_hours * complexity_factor * integration_factor * platform_factor * security_factor
        expected_hours = round(expected_hours, 1)
        
        # Calculate min and max (±20% with min 1 hour)
        min_hours = max(1, round(expected_hours * 0.8, 1))
        max_hours = round(expected_hours * 1.2, 1)
        
        # Confidence score based on data quality
        confidence = self._calculate_confidence(complexity, len(integrations or []))
        
        return EstimateResult(
            min_hours=min_hours,
            expected_hours=expected_hours,
            max_hours=max_hours,
            confidence=confidence,
            factors_used={
                "complexity_factor": complexity_factor,
                "integration_factor": integration_factor,
                "platform_factor": platform_factor,
                "security_factor": security_factor
            },
            breakdown={
                "base_hours": base_hours,
                "complexity_impact": round(expected_hours - base_hours, 1)
            }
        )
    
    def estimate_project(self, 
                        features: List[str],
                        complexities: List[int],
                        integrations: List[str] = None,
                        platform: str = "web",
                        security_level: str = "standard") -> Dict:
        """
        Estimate total project hours
        
        Args:
            features: List of feature names
            complexities: List of complexity scores
            integrations: List of integration types
            platform: Target platform
            security_level: Security requirement level
            
        Returns:
            Complete project estimation
        """
        if not features:
            return {
                "total": {"min": 0, "expected": 0, "max": 0},
                "features": [],
                "summary": {}
            }
        
        feature_estimates = []
        total_min = 0
        total_expected = 0
        total_max = 0
        
        for i, feature_name in enumerate(features):
            complexity = complexities[i] if i < len(complexities) else 3
            estimate = self.estimate_feature(
                feature_name=feature_name,
                complexity=complexity,
                integrations=integrations,
                platform=platform,
                security_level=security_level
            )
            
            feature_estimates.append({
                "name": feature_name,
                "min_hours": estimate.min_hours,
                "expected_hours": estimate.expected_hours,
                "max_hours": estimate.max_hours,
                "confidence": estimate.confidence,
                "factors": estimate.factors_used
            })
            
            total_min += estimate.min_hours
            total_expected += estimate.expected_hours
            total_max += estimate.max_hours
        
        # Calculate overall confidence (average)
        avg_confidence = sum(f["confidence"] for f in feature_estimates) / len(feature_estimates)
        
        return {
            "total": {
                "min": round(total_min, 1),
                "expected": round(total_expected, 1),
                "max": round(total_max, 1)
            },
            "features": feature_estimates,
            "summary": {
                "num_features": len(features),
                "avg_confidence": round(avg_confidence, 2),
                "min_per_feature": round(total_min / len(features), 1),
                "max_per_feature": round(total_max / len(features), 1)
            }
        }
    
    def _calculate_integration_factor(self, integrations: List[str]) -> float:
        """Calculate factor based on integrations"""
        if not integrations:
            return 1.0
        
        factor = 1.0
        for integration in integrations:
            factor *= self.INTEGRATION_FACTORS.get(integration, 1.2)
        
        # Cap at 3.0
        return min(3.0, factor)
    
    def _calculate_confidence(self, complexity: int, num_integrations: int) -> float:
        """Calculate confidence score"""
        # Higher complexity = lower confidence
        complexity_penalty = (complexity - 3) * 0.05
        complexity_penalty = max(0, min(0.3, complexity_penalty))
        
        # More integrations = lower confidence
        integration_penalty = num_integrations * 0.03
        integration_penalty = min(0.2, integration_penalty)
        
        confidence = 0.95 - complexity_penalty - integration_penalty
        return round(max(0.5, min(0.95, confidence)), 2)
    
    def get_feature_breakdown(self, feature_name: str, complexity: int) -> Dict:
        """Get detailed task breakdown for a feature"""
        feature_data = self.task_library.get(feature_name, {})
        if not feature_data:
            return {"error": f"Feature '{feature_name}' not found"}
        
        # Calculate factor
        complexity_factor = 1.0 + (complexity - 3) * 0.2
        complexity_factor = max(0.5, min(2.5, complexity_factor))
        
        tasks = []
        total_hours = 0
        
        for task in feature_data.get("tasks", []):
            hours = round(task["hours"] * complexity_factor, 1)
            tasks.append({
                "name": task["name"],
                "base_hours": task["hours"],
                "adjusted_hours": hours
            })
            total_hours += hours
        
        return {
            "feature": feature_name,
            "base_total": feature_data.get("base_hours", 0),
            "adjusted_total": round(total_hours, 1),
            "complexity_factor": complexity_factor,
            "tasks": tasks
        }