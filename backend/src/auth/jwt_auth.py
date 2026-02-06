from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.config.auth_config import auth_config


# Initialize security scheme
security = HTTPBearer()


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and extract payload.

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Get secret key from auth config
        secret_key = auth_config.auth_secret
        algorithm = auth_config.auth_algorithm

        # Decode the token without audience validation initially
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
            options={"verify_aud": False}  # Don't validate audience initially
        )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate audience if specified in config
        aud = payload.get("aud")
        if auth_config.auth_audience:
            if isinstance(aud, str):
                if aud != auth_config.auth_audience:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token audience",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            elif isinstance(aud, list):
                if auth_config.auth_audience not in aud:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token audience",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get current user from JWT token.

    Args:
        credentials: HTTP authorization credentials from request header

    Returns:
        User ID from token payload

    Raises:
        HTTPException: If token is invalid or user_id not found
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)

    # Look for user ID in multiple possible fields: sub, user_id, or id
    user_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user_id found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


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