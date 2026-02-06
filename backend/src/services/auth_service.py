from typing import Dict, Any, Optional
from datetime import datetime, timezone
import jwt
import os
from fastapi import HTTPException, status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.log_model import LogEntry


class AuthService:
    """
    Service class for handling JWT authentication validation and user isolation.
    """

    @staticmethod
    def validate_jwt_token(token: str) -> Dict[str, Any]:
        """
        Validate a JWT token and extract user information with comprehensive validation.

        Args:
            token: JWT token to validate

        Returns:
            Dictionary with user information if token is valid

        Raises:
            HTTPException: If token is invalid, expired, or fails validation
        """
        try:
            # Get secret key from environment
            secret_key = os.getenv("BETTER_AUTH_SECRET")
            if not secret_key or secret_key == "your-super-secret-key-change-in-production":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Authentication configuration error: Missing or invalid secret key",
                )

            algorithm = os.getenv("AUTH_ALGORITHM", "HS256")

            # Decode the token
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])

            # Check if token is expired
            exp = payload.get("exp")
            if exp:
                if isinstance(exp, str):
                    exp = int(exp)
                if datetime.fromtimestamp(exp) < datetime.utcnow():
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token has expired",
                    )

            # Check if token is not yet valid (nbf claim)
            nbf = payload.get("nbf")
            if nbf:
                if isinstance(nbf, str):
                    nbf = int(nbf)
                if datetime.fromtimestamp(nbf) > datetime.utcnow():
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token is not yet valid",
                    )

            # Check if audience matches expected value
            aud = payload.get("aud")
            expected_aud = os.getenv("AUTH_AUDIENCE", "todo-api")
            if aud and expected_aud != aud:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token audience mismatch",
                )

            # Check if issuer matches expected value
            iss = payload.get("iss")
            expected_iss = os.getenv("AUTH_ISSUER", "better-auth")
            if iss and expected_iss != iss:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token issuer mismatch",
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidAudienceError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token audience invalid",
            )
        except jwt.InvalidIssuerError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token issuer invalid",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation error: {str(e)}",
            )

    @staticmethod
    def extract_user_id_from_token(token: str) -> str:
        """
        Extract the user ID from a JWT token.

        Args:
            token: JWT token to extract user ID from

        Returns:
            User ID string if found in token

        Raises:
            HTTPException: If user ID is not found in token
        """
        payload = AuthService.validate_jwt_token(token)

        # Common JWT claims for user ID: sub, user_id, id
        user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
            )

        return str(user_id)

    @staticmethod
    def validate_user_access(requested_user_id: str, current_user_id: str) -> bool:
        """
        Validate that the current user has access to the requested user's resources.

        Args:
            requested_user_id: The user_id being requested
            current_user_id: The user_id from the current JWT token

        Returns:
            True if user has access, raises HTTPException otherwise
        """
        if requested_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Insufficient permissions to access requested resource",
            )

        return True

    @staticmethod
    def validate_user_isolation_for_task(task_user_id: str, current_user_id: str) -> bool:
        """
        Validate that a user has access to a specific task based on user isolation.

        Args:
            task_user_id: The user_id associated with the task
            current_user_id: The user_id from the current JWT token

        Returns:
            True if user has access to the task, raises HTTPException otherwise
        """
        if task_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this task",
            )

        return True

    @staticmethod
    def validate_user_isolation_for_conversation(conversation_user_id: str, current_user_id: str) -> bool:
        """
        Validate that a user has access to a specific conversation based on user isolation.

        Args:
            conversation_user_id: The user_id associated with the conversation
            current_user_id: The user_id from the current JWT token

        Returns:
            True if user has access to the conversation, raises HTTPException otherwise
        """
        if conversation_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this conversation",
            )

        return True

    @staticmethod
    def validate_token_consistency() -> Dict[str, Any]:
        """
        Validate that authentication configuration is consistent across the system.

        Returns:
            Dictionary with validation results and messages
        """
        results = {
            "auth_secret_configured": False,
            "auth_algorithm_valid": False,
            "auth_audience_set": False,
            "auth_issuer_set": False
        }

        better_auth_secret = os.getenv("BETTER_AUTH_SECRET")
        auth_algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
        auth_audience = os.getenv("AUTH_AUDIENCE", "todo-api")
        auth_issuer = os.getenv("AUTH_ISSUER", "better-auth")

        # Validate auth secret is properly set (not default placeholder)
        if better_auth_secret and better_auth_secret != "your-super-secret-key-here" and better_auth_secret != "your-super-secret-key-change-in-production" and len(better_auth_secret) >= 32:
            results["auth_secret_configured"] = True

        # Validate auth algorithm is supported
        valid_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        if auth_algorithm in valid_algorithms:
            results["auth_algorithm_valid"] = True

        # Validate audience and issuer are set
        if auth_audience and auth_audience.strip() != "":
            results["auth_audience_set"] = True

        if auth_issuer and auth_issuer.strip() != "":
            results["auth_issuer_set"] = True

        all_valid = all(results.values())

        return {
            "all_valid": all_valid,
            "results": results,
            "message": "Authentication configuration is consistent and properly set" if all_valid
                      else "Some authentication configuration issues detected"
        }

    @staticmethod
    def verify_user_isolation_for_task(task_user_id: str, current_user_id: str) -> bool:
        """
        Verify that a user has access to a specific task based on user isolation.

        Args:
            task_user_id: The user_id associated with the task
            current_user_id: The user_id from the current JWT token

        Returns:
            True if user has access to the task, raises HTTPException otherwise
        """
        if task_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this task",
            )

        return True

    @staticmethod
    def verify_user_isolation_for_conversation(conversation_user_id: str, current_user_id: str) -> bool:
        """
        Verify that a user has access to a specific conversation based on user isolation.

        Args:
            conversation_user_id: The user_id associated with the conversation
            current_user_id: The user_id from the current JWT token

        Returns:
            True if user has access to the conversation, raises HTTPException otherwise
        """
        if conversation_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this conversation",
            )

        return True

    @staticmethod
    def validate_environment_variables() -> Dict[str, Any]:
        """
        Validate that required environment variables for authentication are set.

        Returns:
            Dictionary with validation results and messages
        """
        results = {
            "BETTER_AUTH_SECRET": False,
            "AUTH_ALGORITHM": False,
            "AUTH_AUDIENCE": False,
            "AUTH_ISSUER": False
        }

        # Check each required environment variable
        for var_name in results.keys():
            var_value = os.getenv(var_name)
            if var_value and var_value != "your-super-secret-key-here" and var_value.strip() != "":
                results[var_name] = True
            else:
                results[var_name] = False

        # Overall validation status
        all_valid = all(results.values())

        return {
            "all_valid": all_valid,
            "results": results,
            "message": "All authentication environment variables are properly configured" if all_valid else "Some authentication environment variables are missing or improperly configured"
        }

    @staticmethod
    def validate_token_consistency(frontend_token: str, backend_token: str) -> bool:
        """
        Validate that tokens are consistent between frontend and backend (conceptual - in practice they'd be the same).

        Args:
            frontend_token: Token from frontend (conceptual)
            backend_token: Token from backend (would be the same in practice)

        Returns:
            True if tokens are consistent
        """
        # In a real implementation, this would validate that the same JWT signing method is used
        # across both frontend and backend for proper validation
        # For now, we'll just validate that both tokens are valid JWTs
        try:
            AuthService.validate_jwt_token(frontend_token)
            AuthService.validate_jwt_token(backend_token)
            return True
        except HTTPException:
            return False