from fastapi import APIRouter, Depends
from typing import Dict, Any
from sqlmodel import Session
from datetime import datetime

from ..database.database import get_session
from ..services.health_service import HealthService

# Create router for health endpoints
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def get_system_health(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    Get overall system health status including all dependencies.

    Args:
        db_session: Database session (dependency)

    Returns:
        Dictionary with system health status and dependency information
    """
    health_status = HealthService.check_system_health(db_session)

    return {
        "status": health_status.status,
        "timestamp": health_status.timestamp.isoformat(),
        "services": health_status.services,
        "overall_response_time_ms": health_status.overall_response_time_ms
    }


@router.get("/ready")
async def get_readiness_status(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    Get system readiness status for container orchestration.

    Args:
        db_session: Database session (dependency)

    Returns:
        Dictionary with readiness information
    """
    readiness_status = HealthService.get_readiness_status(db_session)

    return readiness_status


@router.get("/live")
async def get_liveness_status() -> Dict[str, Any]:
    """
    Get system liveness status for container orchestration.

    Returns:
        Dictionary confirming the service is alive
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Service is running"
    }


# Additional health endpoints for specific components
@router.get("/database")
async def get_database_health(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    Get specific database health status.

    Args:
        db_session: Database session (dependency)

    Returns:
        Dictionary with database health status
    """
    db_health = HealthService.check_database_health(db_session)

    return {
        "name": db_health.name,
        "status": db_health.status,
        "response_time_ms": db_health.response_time_ms,
        "message": db_health.message,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/auth")
async def get_auth_health() -> Dict[str, Any]:
    """
    Get authentication service health status.

    Returns:
        Dictionary with auth service health status
    """
    auth_health = HealthService.check_auth_service_health()

    return {
        "name": auth_health.name,
        "status": auth_health.status,
        "response_time_ms": auth_health.response_time_ms,
        "message": auth_health.message,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/mcp")
async def get_mcp_health() -> Dict[str, Any]:
    """
    Get MCP server health status.

    Returns:
        Dictionary with MCP server health status
    """
    mcp_health = HealthService.check_mcp_server_health()

    return {
        "name": mcp_health.name,
        "status": mcp_health.status,
        "response_time_ms": mcp_health.response_time_ms,
        "message": mcp_health.message,
        "timestamp": datetime.utcnow().isoformat()
    }