# """
# Phase 24: Structured Output Schemas for LLM Responses
# Validates all LLM output using Pydantic v2 before processing.
# """

# from pydantic import BaseModel, Field, field_validator, model_validator
# from typing import List, Optional, Union


# class RawRequirement(BaseModel):
#     """A single extracted requirement"""
    
#     text: str = Field(..., min_length=5, max_length=1000)
#     category: str = Field(default="functional")
#     confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
#     @field_validator("category")
#     @classmethod
#     def normalize_category(cls, v: str) -> str:
#         v = str(v).lower().strip().replace("-", "_").replace(" ", "_")
#         allowed = {"functional", "non_functional", "technical", "business"}
#         if v not in allowed:
#             return "functional"
#         return v


# class RawFeature(BaseModel):
#     """A single extracted canonical feature"""
    
#     name: Optional[str] = Field(default=None, min_length=1, max_length=100)
#     canonical_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
#     description: str = Field(default="", max_length=1000)
#     priority: str = Field(default="medium")
#     complexity: Union[str, int] = Field(default="medium")
#     confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
#     @field_validator("name", "canonical_name", "description", "priority", mode="before")
#     @classmethod
#     def normalize_strings(cls, value):
#         if value is None:
#             return None
#         return str(value).strip()
    
#     @field_validator("name", "canonical_name")
#     @classmethod
#     def reject_blank_names(cls, value: Optional[str]) -> Optional[str]:
#         if value is not None and not value.strip():
#             raise ValueError("Feature name must not be blank")
#         return value
    
#     @field_validator("priority", mode="before")
#     @classmethod
#     def normalize_priority(cls, v) -> str:
#         """Accept both int and str for priority."""
#         if v is None:
#             return "medium"
        
#         # If integer, convert
#         if isinstance(v, int):
#             if v <= 1:
#                 return "low"
#             elif v <= 3:
#                 return "medium"
#             elif v <= 4:
#                 return "high"
#             else:
#                 return "critical"
        
#         v = str(v).lower().strip()
#         allowed = {"low", "medium", "high", "critical"}
#         return v if v in allowed else "medium"
    
#     @field_validator("complexity", mode="before")
#     @classmethod
#     def normalize_complexity(cls, v) -> str:
#         """Accept both int (1-10) and str (low/medium/high) for complexity."""
#         if v is None:
#             return "medium"
        
#         # If integer, convert to string level
#         if isinstance(v, int):
#             if v <= 2:
#                 return "low"
#             elif v <= 4:
#                 return "medium"
#             else:
#                 return "high"
        
#         # If string, normalize
#         v = str(v).lower().strip()
#         allowed = {"low", "medium", "high"}
#         return v if v in allowed else "medium"
    
#     @model_validator(mode="after")
#     def require_feature_name(self) -> "RawFeature":
#         """Ensure at least one of name/canonical_name is present."""
#         if not (self.name or self.canonical_name):
#             raise ValueError("Feature must include name or canonical_name")
        
#         # Fallback: if name missing, use canonical_name (and vice versa)
#         if not self.name and self.canonical_name:
#             self.name = self.canonical_name
#         if not self.canonical_name and self.name:
#             self.canonical_name = self.name
        
#         return self


# class RawAnalysisResponse(BaseModel):
#     """
#     Complete LLM analysis response schema.
#     All LLM output must validate against this before being processed.
#     """
    
#     project_type: str = Field(default="web", max_length=100)
#     users: List[str] = Field(default_factory=list)
#     requirements: List[RawRequirement] = Field(default_factory=list, max_length=100)
#     features: List[RawFeature] = Field(default_factory=list, max_length=100)
#     missing_information: List[str] = Field(default_factory=list)
#     assumptions: List[str] = Field(default_factory=list)
    
#     @field_validator("users")
#     @classmethod
#     def clean_users(cls, v: List) -> List[str]:
#         if not isinstance(v, list):
#             return []
#         return [str(u).strip()[:100] for u in v if u][:20]
    
#     @field_validator("missing_information")
#     @classmethod
#     def clean_missing(cls, v: List) -> List[str]:
#         if not isinstance(v, list):
#             return []
#         return [str(m).strip()[:500] for m in v if m][:20]
    
#     @field_validator("assumptions")
#     @classmethod
#     def clean_assumptions(cls, v: List) -> List[str]:
#         if not isinstance(v, list):
#             return []
#         return [str(a).strip()[:500] for a in v if a][:20]


# class LLMUsageMetadata(BaseModel):
#     """Token usage and timing metadata from provider"""
    
#     provider: str
#     model: str
#     model_version: Optional[str] = None
#     prompt_tokens: Optional[int] = None
#     response_tokens: Optional[int] = None
#     total_tokens: Optional[int] = None
#     latency_ms: int = 0
#     retry_count: int = 0
#     fallback_used: bool = False
"""
Phase 24: Structured Output Schemas for LLM Responses
Validates all LLM output using Pydantic v2 before processing.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Union


# ============================================
# HELPER — String validation
# ============================================

def _require_non_blank(value: Optional[str], field_name: str) -> str:
    """Reject blank or whitespace-only strings."""
    if value is None:
        raise ValueError(f"{field_name} is required")
    stripped = str(value).strip()
    if not stripped:
        raise ValueError(f"{field_name} must not be blank")
    return stripped


# ============================================
# RAW REQUIREMENT
# ============================================

class RawRequirement(BaseModel):
    """A single extracted requirement"""
    
    text: str = Field(..., min_length=5, max_length=1000)
    category: str = Field(default="functional")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
    @field_validator("text", mode="before")
    @classmethod
    def strip_text(cls, v):
        return _require_non_blank(v, "text")
    
    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v) -> str:
        # ✅ Reject blank category
        if v is None or not str(v).strip():
            raise ValueError("category must not be blank")
        
        v = str(v).lower().strip().replace("-", "_").replace(" ", "_")
        allowed = {"functional", "non_functional", "technical", "business"}
        if v not in allowed:
            return "functional"
        return v


# ============================================
# RAW FEATURE
# ============================================

class RawFeature(BaseModel):
    """A single extracted canonical feature"""
    
    name: Optional[str] = Field(default=None, max_length=100)
    canonical_name: Optional[str] = Field(default=None, max_length=100)
    description: str = Field(default="", max_length=1000)
    priority: Union[str, int] = Field(default="medium")
    complexity: Union[str, int] = Field(default="medium")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
    @field_validator("name", "canonical_name", "description", mode="before")
    @classmethod
    def strip_optional_strings(cls, v):
        if v is None:
            return None
        return str(v).strip()
    
    @field_validator("name", "canonical_name")
    @classmethod
    def reject_blank_names(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Feature name must not be blank")
        return v
    
    @field_validator("name", "canonical_name")
    @classmethod
    def reject_long_names(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 100:
            raise ValueError("Feature name too long (max 100)")
        return v
    
    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v) -> str:
        if v is None:
            return "medium"
        
        if isinstance(v, int):
            if v <= 1:
                return "low"
            elif v <= 3:
                return "medium"
            elif v <= 4:
                return "high"
            else:
                return "critical"
        
        v = str(v).lower().strip()
        allowed = {"low", "medium", "high", "critical"}
        if v not in allowed:
            raise ValueError(f"Invalid priority: {v}")  # ✅ Reject unknown
        return v
    
    @field_validator("complexity", mode="before")
    @classmethod
    def normalize_complexity(cls, v) -> str:
        """Accept int (1-5) or str (low/medium/high)."""
        if v is None:
            return "medium"
        
        if isinstance(v, int):
            # ✅ Reject int > 5
            if v < 1 or v > 5:
                raise ValueError(f"complexity integer must be 1-5, got {v}")
            
            if v <= 1:
                return "low"
            elif v <= 3:
                return "medium"
            else:  # 4-5
                return "high"
        
        v = str(v).lower().strip()
        allowed = {"low", "medium", "high"}
        if v not in allowed:
            raise ValueError(f"Invalid complexity: {v}")  # ✅ Reject unknown
        return v
    
    @model_validator(mode="after")
    def require_feature_name(self) -> "RawFeature":
        if not (self.name or self.canonical_name):
            raise ValueError("Feature must include name or canonical_name")
        
        if not self.name and self.canonical_name:
            self.name = self.canonical_name
        if not self.canonical_name and self.name:
            self.canonical_name = self.name
        
        return self


# ============================================
# RAW ANALYSIS RESPONSE
# ============================================

class RawAnalysisResponse(BaseModel):
    """Complete LLM analysis response schema."""
    
    project_type: str = Field(default="web", max_length=100)
    users: List[str] = Field(default_factory=list)
    requirements: List[RawRequirement] = Field(default_factory=list, max_length=100)
    features: List[RawFeature] = Field(default_factory=list, max_length=100)
    missing_information: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    
    @field_validator("project_type", mode="before")
    @classmethod
    def strip_project_type(cls, v) -> str:
        # ✅ Strip whitespace
        if v is None:
            return "web"
        return str(v).strip()
    
    @field_validator("users")
    @classmethod
    def clean_users(cls, v: List) -> List[str]:
        if not isinstance(v, list):
            return []
        return [str(u).strip()[:100] for u in v if u and str(u).strip()][:20]
    
    @field_validator("missing_information")
    @classmethod
    def clean_missing(cls, v: List) -> List[str]:
        if not isinstance(v, list):
            return []
        return [str(m).strip()[:500] for m in v if m and str(m).strip()][:20]
    
    @field_validator("assumptions")
    @classmethod
    def clean_assumptions(cls, v: List) -> List[str]:
        if not isinstance(v, list):
            return []
        return [str(a).strip()[:500] for a in v if a and str(a).strip()][:20]


# ============================================
# METADATA
# ============================================

class LLMUsageMetadata(BaseModel):
    """Token usage and timing metadata from provider"""
    
    provider: str
    model: str
    model_version: Optional[str] = None
    prompt_tokens: Optional[int] = None
    response_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    latency_ms: int = 0
    retry_count: int = 0
    fallback_used: bool = False