from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Dict, Any
from sqlmodel import Session

from backend.src.database.database import get_session
from backend.src.services.auth_service import AuthService

# Create router for auth endpoints
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/validate-jwt")
async def validate_jwt_endpoint(token: str) -> Dict[str, Any]:
    """
    Validate a JWT token and return user information.

    Args:
        token: JWT token to validate (in request body)

    Returns:
        Dictionary with validation results and user information
    """
    try:
        payload = AuthService.validate_jwt_token(token)

        # Extract user information from token
        user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
            )

        return {
            "valid": True,
            "user_id": user_id,
            "expires_at": payload.get("exp"),
            "message": "Token is valid"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        return {
            "valid": False,
            "error": "invalid_token",
            "message": f"Token validation failed: {str(e)}"
        }


@router.get("/current-user")
async def get_current_user_info(token: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get information about the currently authenticated user.

    Args:
        token: JWT token from Authorization header (extracted via dependency)

    Returns:
        Dictionary with current user information
    """
    try:
        payload = AuthService.validate_jwt_token(token)

        user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
            )

        return {
            "user_id": user_id,
            "authenticated": True,
            "token_expires_at": payload.get("exp")
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Error getting user info: {str(e)}"
        )


# Helper function to get current user from token
def get_current_user(authorization: str = Depends(get_authorization_header)):
    """
    Extract and validate the current user from the Authorization header.

    Args:
        authorization: Authorization header value

    Returns:
        Validated token string
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    AuthService.validate_jwt_token(token)  # This will raise an exception if invalid
    return token


def get_authorization_header(authorization: str = Header(default=None)):
    """
    Extract the Authorization header value.

    Args:
        authorization: Authorization header value

    Returns:
        Authorization header value
    """
    from fastapi import Header
    return authorization