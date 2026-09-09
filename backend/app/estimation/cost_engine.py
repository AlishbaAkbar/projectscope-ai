"""
Phase 10: Cost Estimation Engine
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CostResult:
    """Cost estimation result"""
    min_cost: float
    expected_cost: float
    max_cost: float
    currency: str = "USD"
    
    def formatted(self) -> Dict:
        """Return formatted costs"""
        return {
            "min": f"${self.min_cost:,.2f}",
            "expected": f"${self.expected_cost:,.2f}",
            "max": f"${self.max_cost:,.2f}",
            "currency": self.currency
        }


class CostEngine:
    """Calculate costs based on hours and rates"""
    
    # Default hourly rates (if not found in database)
    DEFAULT_RATES = {
        "UI/UX Designer": 45.0,
        "Frontend Developer": 50.0,
        "Backend Developer": 55.0,
        "Full-Stack Developer": 60.0,
        "Mobile Developer": 55.0,
        "QA Engineer": 40.0,
        "DevOps Engineer": 60.0,
        "Security Engineer": 65.0,
        "Product Manager": 50.0,
        "CEO/Business Owner": 75.0,
    }
    
    # Currency settings
    CURRENCY = "USD"
    
    def __init__(self, role_rates: Dict[str, float] = None):
        self.role_rates = role_rates or self.DEFAULT_RATES
    
    def get_rate(self, role_name: str) -> float:
        """Get hourly rate for a role"""
        return self.role_rates.get(role_name, 50.0)
    
    def calculate_role_cost(self, 
                           role_name: str, 
                           hours: float,
                           markup: float = 1.0) -> CostResult:
        """
        Calculate cost for a single role
        
        Args:
            role_name: Name of the role
            hours: Total hours
            markup: Profit/markup multiplier
            
        Returns:
            CostResult with min/expected/max costs
        """
        rate = self.get_rate(role_name)
        
        # 20% variance
        min_hours = hours * 0.8
        max_hours = hours * 1.2
        
        return CostResult(
            min_cost=round(min_hours * rate * markup, 2),
            expected_cost=round(hours * rate * markup, 2),
            max_cost=round(max_hours * rate * markup, 2)
        )
    
    def calculate_project_cost(self,
                               role_hours: Dict[str, float],
                               markup: float = 1.0) -> Dict:
        """
        Calculate total project cost
        
        Args:
            role_hours: Dict of {role_name: total_hours}
            markup: Profit/markup multiplier
            
        Returns:
            Complete cost breakdown
        """
        if not role_hours:
            return {
                "total": {"min": 0, "expected": 0, "max": 0},
                "by_role": {},
                "summary": {}
            }
        
        by_role = {}
        total_min = 0
        total_expected = 0
        total_max = 0
        
        for role_name, hours in role_hours.items():
            cost = self.calculate_role_cost(role_name, hours, markup)
            by_role[role_name] = {
                "hours": hours,
                "rate": self.get_rate(role_name),
                "cost": cost.formatted()
            }
            total_min += cost.min_cost
            total_expected += cost.expected_cost
            total_max += cost.max_cost
        
        return {
            "total": {
                "min": round(total_min, 2),
                "expected": round(total_expected, 2),
                "max": round(total_max, 2),
                "formatted": {
                    "min": f"${total_min:,.2f}",
                    "expected": f"${total_expected:,.2f}",
                    "max": f"${total_max:,.2f}"
                }
            },
            "by_role": by_role,
            "summary": {
                "num_roles": len(role_hours),
                "total_hours": sum(role_hours.values()),
                "avg_rate": round(sum(self.get_rate(r) for r in role_hours.keys()) / len(role_hours), 2),
                "markup": markup,
                "currency": self.CURRENCY
            }
        }
    
    def add_overhead(self, 
                     cost_result: Dict,
                     overhead_percentage: float = 20) -> Dict:
        """
        Add overhead costs
        
        Args:
            cost_result: Result from calculate_project_cost
            overhead_percentage: Overhead percentage (e.g., 20 for 20%)
            
        Returns:
            Cost result with overhead added
        """
        overhead_multiplier = 1 + (overhead_percentage / 100)
        
        result = cost_result.copy()
        result["total"]["min"] = round(result["total"]["min"] * overhead_multiplier, 2)
        result["total"]["expected"] = round(result["total"]["expected"] * overhead_multiplier, 2)
        result["total"]["max"] = round(result["total"]["max"] * overhead_multiplier, 2)
        result["total"]["formatted"]["min"] = f"${result['total']['min']:,.2f}"
        result["total"]["formatted"]["expected"] = f"${result['total']['expected']:,.2f}"
        result["total"]["formatted"]["max"] = f"${result['total']['max']:,.2f}"
        result["overhead"] = f"{overhead_percentage}%"
        
        return result