"""Validated response schemas for requirement-analysis providers."""

from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class RawRequirement(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    category: str = Field(default="functional", min_length=1, max_length=40)
    confidence: float = Field(default=0.8, ge=0, le=1)

    @field_validator("text", "category")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value must not be blank")
        return value


class RawFeature(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    canonical_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    priority: str = Field(default="medium", min_length=1, max_length=20)
    complexity: Union[int, str] = 3
    confidence: float = Field(default=0.8, ge=0, le=1)

    @field_validator("name", "canonical_name", "description", "priority")
    @classmethod
    def strip_strings(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if value is not None else None

    @field_validator("name", "canonical_name")
    @classmethod
    def reject_blank_names(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            raise ValueError("Feature name must not be blank")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        normalized = value.lower()
        if normalized not in {"low", "medium", "high", "critical"}:
            raise ValueError("Priority must be low, medium, high, or critical")
        return normalized

    @field_validator("complexity")
    @classmethod
    def validate_complexity(cls, value: Union[int, str]) -> Union[int, str]:
        if isinstance(value, int):
            if not 1 <= value <= 5:
                raise ValueError("Numeric complexity must be between 1 and 5")
            return value
        normalized = value.strip().lower()
        if normalized not in {"low", "medium", "high"}:
            raise ValueError("Complexity must be low, medium, high, or an integer from 1 to 5")
        return normalized

    @model_validator(mode="after")
    def require_feature_name(self) -> "RawFeature":
        if not (self.name or self.canonical_name):
            raise ValueError("Feature must include name or canonical_name")
        return self


class RawAnalysisResponse(BaseModel):
    project_type: str = Field(min_length=1, max_length=80)
    users: List[str] = Field(default_factory=list, max_length=50)
    requirements: List[RawRequirement] = Field(default_factory=list, max_length=100)
    features: List[RawFeature] = Field(default_factory=list, max_length=100)
    missing_information: List[str] = Field(default_factory=list, max_length=50)
    assumptions: List[str] = Field(default_factory=list, max_length=50)

    @field_validator("project_type")
    @classmethod
    def strip_project_type(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Project type must not be blank")
        return value

    @field_validator("users", "missing_information", "assumptions")
    @classmethod
    def strip_list_items(cls, values: List[str]) -> List[str]:
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("List items must not be blank")
        return normalized
