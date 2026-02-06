from typing import Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
import logging
from ..models.log_model import LogEntry, LogEntryCreate


class LoggingService:
    """
    Service class for handling operation logging with proper user isolation and security.
    """

    @staticmethod
    def log_operation(
        user_id: str,
        operation_type: str,
        success: bool,
        db_session: Session,
        tool_name: Optional[str] = None,
        request_payload: Optional[Dict[str, Any]] = None,
        response_payload: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> LogEntry:
        """
        Log an operation with security-sensitive information appropriately filtered.

        Args:
            user_id: ID of the user associated with the operation
            operation_type: Type of operation being logged
            success: Whether the operation was successful
            db_session: Database session for logging
            tool_name: Name of the tool called (if applicable)
            request_payload: Original request data (filtered for security)
            response_payload: Response data (filtered for security)
            duration_ms: Time taken to complete the operation in milliseconds
            error_message: Error message if operation failed

        Returns:
            Created LogEntry object
        """
        # Create log entry data
        log_data = LogEntryCreate(
            user_id=user_id,
            operation_type=operation_type,
            success=success,
            tool_name=tool_name,
            request_payload=LoggingService.filter_sensitive_data(request_payload),
            response_payload=LoggingService.filter_sensitive_data(response_payload),
            duration_ms=duration_ms,
            error_message=error_message
        )

        # Create log entry in database
        log_entry = LogEntry(
            user_id=log_data.user_id,
            operation_type=log_data.operation_type,
            success=log_data.success,
            tool_name=log_data.tool_name,
            request_payload=log_data.request_payload,
            response_payload=log_data.response_payload,
            duration_ms=log_data.duration_ms,
            error_message=log_data.error_message,
            timestamp=datetime.utcnow()
        )

        db_session.add(log_entry)
        db_session.commit()
        db_session.refresh(log_entry)

        return log_entry

    @staticmethod
    def filter_sensitive_data(payload: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Filter sensitive data from payloads before logging for security.

        Args:
            payload: Payload to filter

        Returns:
            Filtered payload with sensitive information removed
        """
        if not payload:
            return None

        # Create a copy of the payload to avoid modifying the original
        filtered_payload = payload.copy()

        # Remove sensitive keys commonly found in requests/responses
        sensitive_keys = [
            "password", "token", "jwt", "authorization", "secret", "key",
            "api_key", "access_token", "refresh_token", "bearer"
        ]

        # Recursively filter sensitive data
        return LoggingService._filter_recursive(filtered_payload, sensitive_keys)

    @staticmethod
    def _filter_recursive(obj: Any, sensitive_keys: list) -> Any:
        """
        Recursively filter sensitive data from nested objects.

        Args:
            obj: Object to filter (dict, list, or primitive)
            sensitive_keys: List of keys to treat as sensitive

        Returns:
            Filtered object with sensitive data removed
        """
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key.lower() in sensitive_keys:
                    # Replace sensitive values with masked string
                    result[key] = "[FILTERED]"
                else:
                    result[key] = LoggingService._filter_recursive(value, sensitive_keys)
            return result
        elif isinstance(obj, list):
            return [LoggingService._filter_recursive(item, sensitive_keys) for item in obj]
        else:
            # For primitive types, return as-is
            return obj

    @staticmethod
    def log_chat_interaction(
        user_id: str,
        user_message: str,
        assistant_response: str,
        success: bool,
        db_session: Session,
        duration_ms: Optional[int] = None
    ) -> LogEntry:
        """
        Log a chat interaction between user and AI assistant.

        Args:
            user_id: ID of the user participating in the chat
            user_message: Message from the user
            assistant_response: Response from the AI assistant
            success: Whether the interaction was successful
            db_session: Database session for logging
            duration_ms: Time taken to process the interaction

        Returns:
            Created LogEntry object for the chat interaction
        """
        return LoggingService.log_operation(
            user_id=user_id,
            operation_type="chat_interaction",
            success=success,
            db_session=db_session,
            request_payload={"message": user_message},
            response_payload={"response": assistant_response},
            duration_ms=duration_ms
        )

    @staticmethod
    def log_tool_call(
        user_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
        result: Dict[str, Any],
        success: bool,
        db_session: Session,
        duration_ms: Optional[int] = None
    ) -> LogEntry:
        """
        Log an MCP tool call made by the AI assistant.

        Args:
            user_id: ID of the user whose data was affected by the tool call
            tool_name: Name of the tool called
            arguments: Arguments passed to the tool
            result: Result returned by the tool
            success: Whether the tool call was successful
            db_session: Database session for logging
            duration_ms: Time taken to execute the tool call

        Returns:
            Created LogEntry object for the tool call
        """
        return LoggingService.log_operation(
            user_id=user_id,
            operation_type="tool_call",
            success=success,
            db_session=db_session,
            tool_name=tool_name,
            request_payload={"arguments": arguments},
            response_payload={"result": result},
            duration_ms=duration_ms
        )

    @staticmethod
    def log_authentication_check(
        user_id: str,
        success: bool,
        db_session: Session,
        error_message: Optional[str] = None
    ) -> LogEntry:
        """
        Log an authentication validation check.

        Args:
            user_id: ID of the user being authenticated
            success: Whether the authentication check was successful
            db_session: Database session for logging
            error_message: Error message if authentication failed

        Returns:
            Created LogEntry object for the authentication check
        """
        return LoggingService.log_operation(
            user_id=user_id,
            operation_type="auth_check",
            success=success,
            db_session=db_session,
            error_message=error_message
        )

    @staticmethod
    def get_user_operation_logs(user_id: str, db_session: Session, limit: int = 50) -> list:
        """
        Get operation logs for a specific user.

        Args:
            user_id: ID of the user whose logs to retrieve
            db_session: Database session
            limit: Maximum number of logs to return

        Returns:
            List of LogEntry objects for the user
        """
        from sqlmodel import select
        statement = select(LogEntry).where(LogEntry.user_id == user_id).order_by(LogEntry.timestamp.desc()).limit(limit)
        logs = db_session.exec(statement).all()
        return logs

    @staticmethod
    def log_agent_action(
        user_id: str,
        action_type: str,
        action_details: Dict[str, Any],
        success: bool,
        db_session: Session,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> LogEntry:
        """
        Log an agent action with structured information for observability.

        Args:
            user_id: ID of the user associated with the action
            action_type: Type of action performed (e.g., "tool_call", "response_generation", "task_creation")
            action_details: Detailed information about the action
            success: Whether the action was successful
            db_session: Database session for logging
            duration_ms: Time taken to complete the action in milliseconds
            error_message: Error message if action failed

        Returns:
            Created LogEntry object
        """
        return LoggingService.log_operation(
            user_id=user_id,
            operation_type=action_type,
            success=success,
            db_session=db_session,
            request_payload=action_details.get("request"),
            response_payload=action_details.get("response"),
            duration_ms=duration_ms,
            error_message=error_message
        )

    @staticmethod
    def log_tool_call_execution(
        user_id: str,
        tool_name: str,
        tool_arguments: Dict[str, Any],
        tool_result: Dict[str, Any],
        success: bool,
        db_session: Session,
        duration_ms: Optional[int] = None
    ) -> LogEntry:
        """
        Log the execution of an MCP tool call by the AI agent.

        Args:
            user_id: ID of the user whose data was affected
            tool_name: Name of the tool that was called
            tool_arguments: Arguments passed to the tool
            tool_result: Result returned by the tool
            success: Whether the tool call was successful
            db_session: Database session for logging
            duration_ms: Time taken to execute the tool in milliseconds

        Returns:
            Created LogEntry object for the tool call
        """
        action_details = {
            "request": {
                "tool_name": tool_name,
                "arguments": tool_arguments
            },
            "response": {
                "result": tool_result
            }
        }

        return LoggingService.log_agent_action(
            user_id=user_id,
            action_type="tool_call",
            action_details=action_details,
            success=success,
            db_session=db_session,
            duration_ms=duration_ms,
            error_message=error_message
        )

    @staticmethod
    def add_logging_to_tool_call(
        tool_func,
        user_id: str,
        tool_name: str,
        tool_arguments: Dict[str, Any],
        db_session: Session
    ):
        """
        Decorator-like method to add logging to tool calls.

        Args:
            tool_func: The actual tool function to execute
            user_id: ID of the user making the request
            tool_name: Name of the tool being called
            tool_arguments: Arguments to pass to the tool
            db_session: Database session for logging

        Returns:
            Result of the tool function execution
        """
        import time
        start_time = time.time()

        try:
            result = tool_func(tool_arguments)
            duration_ms = int((time.time() - start_time) * 1000)

            # Log successful tool execution
            LoggingService.log_tool_call_execution(
                user_id=user_id,
                tool_name=tool_name,
                tool_arguments=tool_arguments,
                tool_result=result,
                success=True,
                db_session=db_session,
                duration_ms=duration_ms
            )

            return result
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)

            # Log failed tool execution
            LoggingService.log_tool_call_execution(
                user_id=user_id,
                tool_name=tool_name,
                tool_arguments=tool_arguments,
                tool_result={"error": str(e)},
                success=False,
                db_session=db_session,
                duration_ms=duration_ms,
                error_message=str(e)
            )

            raise e