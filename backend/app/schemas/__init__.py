from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    detail: str
    error_code: str | None = None


class DetectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    class_id: int | None = None
    class_name: str
    confidence: float
    bbox: list[float] | None = None


class PrimaryFindingOut(BaseModel):
    class_id: int | None = None
    class_name: str
    confidence: float
    bbox: list[float] | None = None


class RecommendationOut(BaseModel):
    text: str
    priority: str = "normal"


class CowCreate(BaseModel):
    cow_id: str = Field(..., min_length=1, max_length=64, examples=["COW-001"])
    name: str | None = Field(default=None, max_length=128)
    breed: str | None = Field(default=None, max_length=128)
    age: float | None = Field(default=None, ge=0, le=40)
    farm_location: str | None = Field(default=None, max_length=256)
    notes: str | None = None


class CowUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=128)
    breed: str | None = Field(default=None, max_length=128)
    age: float | None = Field(default=None, ge=0, le=40)
    farm_location: str | None = Field(default=None, max_length=256)
    notes: str | None = None


class CowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cow_id: str
    name: str | None = None
    breed: str | None = None
    age: float | None = None
    farm_location: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    current_status: str | None = None
    last_analysis_at: datetime | None = None
    analysis_count: int = 0


class AnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool = True
    analysis_id: int
    cow_id: str
    prediction: str
    confidence: float
    risk_level: str
    detections: list[DetectionOut] = Field(default_factory=list)
    primary_finding: PrimaryFindingOut | None = None
    recommendations: list[str] = Field(default_factory=list)
    timestamp: datetime
    model_version: str
    demo_mode: bool
    image_url: str | None = None
    annotated_image_url: str | None = None
    risk_explanation: str | None = None
    screening_type: str = "AI-assisted screening result"
    care_guidance: dict | None = None
    disclaimer: str = (
        "BOVIMED provides AI-assisted screening and care guidance. It is not a "
        "veterinary diagnosis and does not replace a qualified veterinarian."
    )


class AnalysisSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis_id: int
    cow_id: str
    prediction: str
    confidence: float
    risk_level: str
    timestamp: datetime
    model_version: str
    demo_mode: bool


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analysis_id: int
    cow_id: str
    severity: str
    title: str
    message: str
    risk_level: str
    confidence: float
    is_read: bool
    created_at: datetime


class DashboardStats(BaseModel):
    total_cows: int
    healthy: int
    at_risk: int
    analyses_this_month: int
    total_analyses: int
    unread_alerts: int
    risk_distribution: dict[str, int]
    monthly_analyses: list[dict[str, Any]]
    recent_analyses: list[AnalysisSummary]
    demo_mode: bool


class HealthResponse(BaseModel):
    status: str
    service: str
    demo_mode: bool
    demo_forced_by_env: bool
    model_path: str
    model_exists: bool
    model_loaded: bool
    model_classes: dict[str, str] | None = None
    load_error: str | None = None
    database: str
    message: str
