"""Pydantic schemas for request/response validation."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class DocumentTypeEnum(str, Enum):
    """Supported document types."""
    INVOICE = "invoice"
    SUPPORT_TICKET = "support_ticket"
    HR_REQUEST = "hr_request"
    CONTRACT = "contract"
    EMAIL = "email"
    SLACK_MESSAGE = "slack_message"
    OTHER = "other"


class ConfidenceLevel(str, Enum):
    """Confidence levels for predictions."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    """Task processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class IngestionRequest(BaseModel):
    """Schema for document ingestion request."""
    content: str = Field(..., description="Document content or text")
    source_type: str = Field(..., description="Source type: pdf, email, slack, csv")
    source_id: Optional[str] = Field(None, description="Unique identifier for the source")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ExtractionResult(BaseModel):
    """Schema for data extraction result."""
    document_type: DocumentTypeEnum
    confidence_score: float = Field(..., ge=0, le=1)
    extracted_data: Dict[str, Any]
    errors: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Validate confidence score is between 0 and 1."""
        if not (0 <= v <= 1):
            raise ValueError("Confidence score must be between 0 and 1")
        return v


class ClassificationResult(BaseModel):
    """Schema for document classification result."""
    document_type: DocumentTypeEnum
    confidence_score: float = Field(..., ge=0, le=1)
    confidence_level: ConfidenceLevel


class TaskResponse(BaseModel):
    """Schema for task creation response."""
    task_id: str
    status: TaskStatus
    created_at: datetime
    message: str


class TaskStatusResponse(BaseModel):
    """Schema for task status query response."""
    task_id: str
    status: TaskStatus
    progress: Optional[float] = Field(None, ge=0, le=100)
    result: Optional[ExtractionResult] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    escalation_reason: Optional[str] = None


class Rule(BaseModel):
    """Schema for automation rule."""
    id: Optional[str] = None
    name: str = Field(..., description="Rule name")
    description: Optional[str] = None
    condition: str = Field(..., description="Condition expression (e.g., 'document_type == invoice AND amount > 10000')")
    action: str = Field(..., description="Action to execute")
    action_params: Optional[Dict[str, Any]] = None
    enabled: bool = True
    priority: int = Field(default=0, description="Rule priority (higher = execute first)")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RuleResponse(BaseModel):
    """Schema for rule creation/update response."""
    id: str
    message: str
    rule: Rule


class MetricsResponse(BaseModel):
    """Schema for metrics response."""
    documents_processed_total: int
    processing_time_avg: float
    error_rate: float
    automation_actions_total: int
    successful_actions: int
    failed_actions: int
    escalated_actions: int
    timestamp: datetime


class EscalationNotification(BaseModel):
    """Schema for escalation notification."""
    task_id: str
    document_type: DocumentTypeEnum
    confidence_score: float
    reason: str
    extracted_data: Dict[str, Any]
    escalation_channel: str = Field(default="slack", description="slack or email")
    recipient: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: str
    timestamp: datetime
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(default="healthy")
    version: str
    database: str = "connected"
    cache: str = "connected"
    vector_db: str = "connected"
    timestamp: datetime
