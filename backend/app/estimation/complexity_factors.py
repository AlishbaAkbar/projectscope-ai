"""
Complexity factor calculations
"""

from typing import Dict, List, Tuple


class ComplexityFactors:
    """Calculate complexity factors for estimation"""
    
    # Feature complexity weights (1-10 scale)
    FEATURE_WEIGHTS = {
        "AUTHENTICATION": 3,
        "USER_MANAGEMENT": 2,
        "PRODUCT_CATALOG": 4,
        "SEARCH": 4,
        "CART": 3,
        "PAYMENT": 5,
        "ORDER_MANAGEMENT": 3,
        "ADMIN_PANEL": 5,
        "MOBILE_APP": 6,
        "REAL_TIME": 5,
        "REVIEWS": 3,
        "NOTIFICATIONS": 4,
        "ANALYTICS": 4,
    }
    
    # Dependency complexity multipliers
    DEPENDENCY_MULTIPLIERS = {
        0: 1.0,
        1: 1.1,
        2: 1.2,
        3: 1.35,
        4: 1.5,
    }
    
    @classmethod
    def get_base_complexity(cls, feature_name: str) -> int:
        """Get base complexity for a feature"""
        return cls.FEATURE_WEIGHTS.get(feature_name, 3)
    
    @classmethod
    def calculate_complexity_score(cls, 
                                   features: List[str],
                                   dependencies: Dict[str, List[str]] = None) -> Tuple[int, Dict]:
        """
        Calculate overall complexity score
        
        Returns:
            Tuple of (total_score, breakdown)
        """
        if not features:
            return 0, {}
        
        dependencies = dependencies or {}
        total_score = 0
        breakdown = {}
        
        for feature in features:
            base = cls.get_base_complexity(feature)
            dep_count = len(dependencies.get(feature, []))
            dep_multiplier = cls.DEPENDENCY_MULTIPLIERS.get(
                min(dep_count, 4), 
                1.5
            )
            
            score = round(base * dep_multiplier, 1)
            total_score += score
            
            breakdown[feature] = {
                "base": base,
                "dependencies": dep_count,
                "multiplier": dep_multiplier,
                "score": score
            }
        
        return round(total_score, 1), breakdown
    
    @classmethod
    def get_complexity_level(cls, score: float) -> str:
        """Get complexity level from score"""
        if score <= 10:
            return "LOW"
        elif score <= 20:
            return "MEDIUM"
        elif score <= 30:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    @classmethod
    def get_risk_level(cls, score: float, num_integrations: int) -> str:
        """Get risk level from complexity and integrations"""
        risk_score = score + (num_integrations * 2)
        
        if risk_score <= 15:
            return "LOW"
        elif risk_score <= 25:
            return "MEDIUM"
        elif risk_score <= 35:
            return "HIGH"
        else:
            return "CRITICAL"