"""
Phase 17: Hybrid Estimation Engine
Combines Rules + ML + LLM estimates with reconciliation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime
import json


@dataclass
class HybridEstimate:
    """Complete hybrid estimation result"""
    rule_estimate: float
    ml_estimate: float
    llm_estimate: float
    final_estimate: float
    min_range: float
    max_range: float
    confidence: float
    weights_used: Dict[str, float]
    reconciliation_method: str
    version: str
    timestamp: str


class HybridEngine:
    """
    Hybrid estimation engine with reconciliation policy
    """
    
    # Version tracking
    VERSION = "1.0.0"
    
    # Default weights (can be tuned based on historical data)
    DEFAULT_WEIGHTS = {
        "rule": 0.40,      # 40% weight to rule-based
        "ml": 0.35,        # 35% weight to ML
        "llm": 0.25        # 25% weight to LLM
    }
    
    # Confidence thresholds
    CONFIDENCE_THRESHOLDS = {
        "high": 0.80,
        "medium": 0.60,
        "low": 0.40
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize hybrid engine with weights
        
        Args:
            weights: Custom weights for rule/ml/llm
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self._normalize_weights()
        self.history = []
    
    def _normalize_weights(self):
        """Ensure weights sum to 1.0"""
        total = sum(self.weights.values())
        if total != 1.0:
            for key in self.weights:
                self.weights[key] = self.weights[key] / total
    
    def estimate(self, 
                 rule_estimate: float,
                 ml_estimate: Optional[float],
                 llm_estimate: Optional[float],
                 ml_confidence: float = 0.5,
                 data_quality: str = "medium") -> HybridEstimate:
        """
        Generate hybrid estimate from multiple sources
        
        Args:
            rule_estimate: Rule-based estimate in hours
            ml_estimate: ML prediction in hours (None if unavailable)
            llm_estimate: LLM suggestion in hours (None if unavailable)
            ml_confidence: Confidence of ML model (0-1)
            data_quality: "high", "medium", or "low"
            
        Returns:
            HybridEstimate with final estimate and confidence
        """
        # Handle missing estimates
        ml_estimate = ml_estimate or rule_estimate
        llm_estimate = llm_estimate or rule_estimate
        
        # Calculate dynamic weights based on data quality and confidence
        weights = self._calculate_dynamic_weights(
            ml_confidence=ml_confidence,
            data_quality=data_quality,
            has_ml=ml_estimate != rule_estimate,
            has_llm=llm_estimate != rule_estimate
        )
        
        # Calculate weighted average
        final_estimate = (
            weights["rule"] * rule_estimate +
            weights["ml"] * ml_estimate +
            weights["llm"] * llm_estimate
        )
        
        # Calculate range based on spread
        estimates = [rule_estimate, ml_estimate, llm_estimate]
        spread = max(estimates) - min(estimates)
        
        # Range = final ± (spread * 0.5) or ±20% whichever is larger
        range_margin = max(spread * 0.5, final_estimate * 0.15)
        min_range = max(0, final_estimate - range_margin)
        max_range = final_estimate + range_margin
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            estimates=estimates,
            ml_confidence=ml_confidence,
            data_quality=data_quality,
            spread=spread
        )
        
        # Determine reconciliation method
        method = self._determine_method(weights)
        
        # Create result
        result = HybridEstimate(
            rule_estimate=round(rule_estimate, 1),
            ml_estimate=round(ml_estimate, 1),
            llm_estimate=round(llm_estimate, 1),
            final_estimate=round(final_estimate, 1),
            min_range=round(min_range, 1),
            max_range=round(max_range, 1),
            confidence=round(confidence, 2),
            weights_used={k: round(v, 2) for k, v in weights.items()},
            reconciliation_method=method,
            version=self.VERSION,
            timestamp=datetime.now().isoformat()
        )
        
        # Store history
        self.history.append(result)
        
        return result
    
    def _calculate_dynamic_weights(self,
                                   ml_confidence: float,
                                   data_quality: str,
                                   has_ml: bool,
                                   has_llm: bool) -> Dict[str, float]:
        """
        Calculate dynamic weights based on confidence and data quality
        """
        weights = self.DEFAULT_WEIGHTS.copy()
        
        # Adjust based on ML confidence
        if has_ml:
            if ml_confidence >= 0.8:
                weights["ml"] = 0.45
                weights["rule"] = 0.30
                weights["llm"] = 0.25
            elif ml_confidence >= 0.6:
                weights["ml"] = 0.35
                weights["rule"] = 0.35
                weights["llm"] = 0.30
            else:
                weights["ml"] = 0.20
                weights["rule"] = 0.50
                weights["llm"] = 0.30
        
        # Adjust based on data quality
        if data_quality == "high":
            weights["rule"] += 0.05
            weights["ml"] += 0.05
        elif data_quality == "low":
            weights["rule"] -= 0.10
            weights["llm"] += 0.10
        
        # If no ML available, distribute weight
        if not has_ml:
            weights["ml"] = 0
            weights["rule"] += 0.20
            weights["llm"] += 0.15
        
        # If no LLM available, distribute weight
        if not has_llm:
            weights["llm"] = 0
            weights["rule"] += 0.15
            weights["ml"] += 0.10
        
        # Normalize
        total = sum(weights.values())
        if total > 0:
            for key in weights:
                weights[key] = weights[key] / total
        
        return weights
    
    def _calculate_confidence(self,
                             estimates: List[float],
                             ml_confidence: float,
                             data_quality: str,
                             spread: float) -> float:
        """
        Calculate overall confidence score (0-1)
        """
        # Base confidence
        confidence = 0.70
        
        # Adjust based on spread (smaller spread = higher confidence)
        avg_estimate = sum(estimates) / len(estimates)
        if avg_estimate > 0:
            spread_ratio = spread / avg_estimate
            if spread_ratio < 0.1:
                confidence += 0.15
            elif spread_ratio < 0.2:
                confidence += 0.10
            elif spread_ratio < 0.3:
                confidence += 0.05
            else:
                confidence -= 0.10
        
        # Adjust based on ML confidence
        confidence = confidence * 0.7 + ml_confidence * 0.3
        
        # Adjust based on data quality
        quality_multipliers = {
            "high": 1.1,
            "medium": 1.0,
            "low": 0.85
        }
        confidence *= quality_multipliers.get(data_quality, 1.0)
        
        # Ensure within 0-1 range
        return max(0.1, min(0.95, confidence))
    
    def _determine_method(self, weights: Dict[str, float]) -> str:
        """
        Determine reconciliation method used
        """
        if weights["rule"] > weights["ml"] and weights["rule"] > weights["llm"]:
            return "Rule-Dominant"
        elif weights["ml"] > weights["rule"] and weights["ml"] > weights["llm"]:
            return "ML-Dominant"
        elif weights["llm"] > weights["rule"] and weights["llm"] > weights["ml"]:
            return "LLM-Dominant"
        else:
            return "Balanced"
    
    def get_formatted_result(self, result: HybridEstimate) -> Dict:
        """
        Format hybrid estimate for API response
        """
        return {
            "hybrid_estimate": {
                "final_estimate": result.final_estimate,
                "range": {
                    "min": result.min_range,
                    "max": result.max_range
                },
                "confidence": result.confidence,
                "reconciliation_method": result.reconciliation_method,
                "version": result.version,
                "timestamp": result.timestamp,
                "breakdown": {
                    "rule_based": result.rule_estimate,
                    "ml_prediction": result.ml_estimate,
                    "llm_suggestion": result.llm_estimate
                },
                "weights_used": result.weights_used
            }
        }
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get estimation history
        """
        return [
            {
                "final_estimate": h.final_estimate,
                "confidence": h.confidence,
                "method": h.reconciliation_method,
                "timestamp": h.timestamp
            }
            for h in self.history[-limit:]
        ]
    
    def validate_on_history(self, historical_projects: List[Dict]) -> Dict:
        """
        Validate hybrid engine on historical data
        
        Args:
            historical_projects: List of dicts with actual hours
            
        Returns:
            Validation metrics
        """
        if not historical_projects:
            return {"error": "No historical data provided"}
        
        errors = []
        for project in historical_projects:
            rule_est = project.get("rule_estimate", 0)
            ml_est = project.get("ml_estimate", rule_est)
            llm_est = project.get("llm_estimate", rule_est)
            actual = project.get("actual_hours", 0)
            
            result = self.estimate(
                rule_estimate=rule_est,
                ml_estimate=ml_est,
                llm_estimate=llm_est,
                ml_confidence=project.get("ml_confidence", 0.5),
                data_quality=project.get("data_quality", "medium")
            )
            
            error = abs(result.final_estimate - actual) / actual if actual > 0 else 0
            errors.append(error)
        
        return {
            "total_projects": len(historical_projects),
            "mean_absolute_error_pct": round(np.mean(errors) * 100, 2),
            "median_error_pct": round(np.median(errors) * 100, 2),
            "max_error_pct": round(max(errors) * 100, 2),
            "min_error_pct": round(min(errors) * 100, 2),
            "validation_date": datetime.now().isoformat(),
            "engine_version": self.VERSION
        }