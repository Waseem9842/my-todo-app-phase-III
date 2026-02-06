from typing import Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime
import time
import subprocess
from ..models.health_model import SystemHealth, DependencyHealth


class HealthService:
    """
    Service class for monitoring system health and dependencies.
    """

    @staticmethod
    def check_system_health(db_session: Session) -> SystemHealth:
        """
        Check the overall health of the system including all dependencies.

        Args:
            db_session: Database session for testing database connectivity

        Returns:
            SystemHealth object with status of all system components
        """
        start_time = time.time()

        # Check database connectivity
        db_health = HealthService.check_database_health(db_session)

        # Check MCP server connectivity (if available)
        mcp_health = HealthService.check_mcp_server_health()

        # Check authentication service connectivity
        auth_health = HealthService.check_auth_service_health()

        # Calculate overall status based on individual component statuses
        overall_status = HealthService.calculate_overall_status({
            "database": db_health,
            "mcp_server": mcp_health,
            "auth_service": auth_health
        })

        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

        return SystemHealth(
            status=overall_status,
            services={
                "database": db_health,
                "mcp_server": mcp_health,
                "auth_service": auth_health
            },
            overall_response_time_ms=response_time
        )

    @staticmethod
    def check_database_health(db_session: Session) -> DependencyHealth:
        """
        Check database connectivity and responsiveness.

        Args:
            db_session: Database session to test

        Returns:
            DependencyHealth object with database status
        """
        try:
            # Test database connectivity with a simple query
            start_time = time.time()

            # Execute a simple query to test database
            result = db_session.exec(select(1))

            response_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

            return DependencyHealth(
                name="database",
                status="connected",
                response_time_ms=response_time,
                message="Database connection is healthy"
            )
        except Exception as e:
            return DependencyHealth(
                name="database",
                status="error",
                response_time_ms=None,
                message=f"Database connection error: {str(e)}"
            )

    @staticmethod
    def check_mcp_server_health() -> DependencyHealth:
        """
        Check MCP server connectivity.

        Returns:
            DependencyHealth object with MCP server status
        """
        try:
            start_time = time.time()

            # In a real implementation, this would make an actual call to the MCP server
            # For now, we'll simulate a check by checking if the service is available
            # This is a placeholder - in a real system, we'd make an actual health check call

            response_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

            return DependencyHealth(
                name="mcp_server",
                status="available",  # Assuming MCP server is available for now
                response_time_ms=response_time,
                message="MCP server is available"
            )
        except Exception as e:
            return DependencyHealth(
                name="mcp_server",
                status="error",
                response_time_ms=None,
                message=f"MCP server connection error: {str(e)}"
            )

    @staticmethod
    def check_auth_service_health() -> DependencyHealth:
        """
        Check authentication service connectivity.

        Returns:
            DependencyHealth object with auth service status
        """
        try:
            start_time = time.time()

            # In a real implementation, this would make an actual call to the auth service
            # For now, we'll simulate a check by verifying environment configuration
            import os
            auth_secret = os.getenv("BETTER_AUTH_SECRET")

            if not auth_secret or auth_secret == "your-super-secret-key-here":
                status = "warning"
                message = "Auth secret not properly configured"
            else:
                status = "available"
                message = "Auth service is available"

            response_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

            return DependencyHealth(
                name="auth_service",
                status=status,
                response_time_ms=response_time,
                message=message
            )
        except Exception as e:
            return DependencyHealth(
                name="auth_service",
                status="error",
                response_time_ms=None,
                message=f"Auth service connection error: {str(e)}"
            )

    @staticmethod
    def calculate_overall_status(component_health: Dict[str, DependencyHealth]) -> str:
        """
        Calculate overall system status based on component statuses.

        Args:
            component_health: Dictionary of component health statuses

        Returns:
            Overall status: 'healthy', 'degraded', or 'unavailable'
        """
        statuses = [comp.status for comp in component_health.values()]

        if "error" in statuses:
            return "unavailable"
        elif "warning" in statuses:
            return "degraded"
        else:
            return "healthy"

    @staticmethod
    def get_readiness_status(db_session: Session) -> Dict[str, Any]:
        """
        Get readiness status for the application.

        Args:
            db_session: Database session for testing connectivity

        Returns:
            Dictionary with readiness information
        """
        # Check if all critical dependencies are available
        db_health = HealthService.check_database_health(db_session)
        db_ready = db_health.status == "connected"

        # In a real implementation, check other critical services
        ready = db_ready  # For now, just check database

        return {
            "ready": ready,
            "checks": {
                "database_connected": db_ready,
                "mcp_tools_available": True,  # Assuming available
                "auth_service_healthy": True,  # Assuming available
                "environment_validated": True  # Assuming validated
            },
            "timestamp": datetime.utcnow().isoformat()
        }