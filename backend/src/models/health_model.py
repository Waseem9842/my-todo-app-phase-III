from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class DependencyHealth(SQLModel):
    """
    Model representing the health of a specific dependency.
    """
    name: str
    status: str  # connected, disconnected, error
    response_time_ms: Optional[int] = None
    message: Optional[str] = None


class SystemHealth(SQLModel):
    """
    Model representing the overall system health.
    """
    status: str  # healthy, degraded, unavailable
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    services: Dict[str, 'DependencyHealth']  # Using string forward reference
    overall_response_time_ms: Optional[int] = None


class HealthStatusBase(SQLModel):
    """
    Base model for health status with common fields.
    """
    service_name: str = Field(description="Name of the service being checked")
    status: str = Field(description="Overall health status: healthy, degraded, unavailable")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthStatus(HealthStatusBase, table=True):
    """
    Model representing the health status of system components.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    details: Optional[str] = Field(default=None, description="Detailed status information for each component (JSON string)")
    response_time_ms: Optional[int] = Field(default=None, description="Response time in milliseconds")


class HealthStatusRead(HealthStatusBase):
    """
    Response model for reading health status.
    """
    id: int
    details: Optional[str]  # JSON string representation of details
    response_time_ms: Optional[int]