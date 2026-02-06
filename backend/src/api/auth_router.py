from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, Any
import os
from datetime import datetime
from src.auth.jwt_handler import JWTHandler
from src.models.user_model import User, UserCreate, UserPublic
from src.database.database import get_session
from sqlmodel import Session
from src.services.user_service import UserService
from src.auth.auth_dependencies import get_current_user
from pydantic import BaseModel, Field

# Create the API router
auth_router = APIRouter()
security = HTTPBearer()

class LoginData(BaseModel):
    email: str
    password: str


class UserWithToken(BaseModel):
    """Response model that includes both user data and authentication token"""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    token: str


class LoginResponse(BaseModel):
    """Response model for login endpoint"""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    token: str

@auth_router.post("/auth/register", response_model=UserWithToken)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user and return a JWT token.
    """
    try:
        # Check if user already exists
        existing_user = UserService.get_user_by_email(session, user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create the user
        user = UserService.create_user(session, user_create)

        # Create JWT token
        from datetime import timezone

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": "todo-api",
            "iss": "better-auth",
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "nbf": int(datetime.now(timezone.utc).timestamp())
        }
        access_token = JWTHandler.create_access_token(data=token_data)

        # Return user data with token using the proper response model
        return UserWithToken(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token=access_token
        )
    except HTTPException:
        raise
    except ValueError as ve:
        # Specifically catch bcrypt-related value errors
        if "cannot be longer than 72 bytes" in str(ve):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be longer than 72 characters. Please use a shorter password."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(ve)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@auth_router.post("/auth/login", response_model=LoginResponse)
def login_user(login_data: LoginData, session: Session = Depends(get_session)):
    """
    Authenticate user and return a JWT token.
    """
    try:
        email = login_data.email
        password = login_data.password

        # Verify user credentials
        user = UserService.authenticate_user(session, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create JWT token
        from datetime import timezone

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": "todo-api",
            "iss": "better-auth",
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "nbf": int(datetime.now(timezone.utc).timestamp())
        }
        access_token = JWTHandler.create_access_token(data=token_data)

        # Return user data with token using the proper response model
        return LoginResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            token=access_token
        )
    except HTTPException:
        raise
    except ValueError as ve:
        # Specifically catch bcrypt-related value errors
        if "cannot be longer than 72 bytes" in str(ve):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be longer than 72 characters. Please use a shorter password."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(ve)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@auth_router.get("/auth/me")
def get_current_user_data(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user's data using the JWT token.
    """
    # Return user data based on the token
    return {
        "user_id": current_user["user_id"],
        "email": current_user.get("claims", {}).get("email", ""),
        "authenticated": True
    }


@auth_router.get("/auth/session")
def get_session_data(credentials=Depends(security)):
    """
    Get session data (for compatibility with frontend auth expectations).
    """
    token = credentials.credentials
    try:
        payload = JWTHandler.validate_token_claims(token)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "token": token,
            "authenticated": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )