from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Callable
from src.auth.jwt_handler import JWTHandler


class AuthMiddleware:
    """
    Authentication middleware to handle JWT token validation globally.
    This is an alternative approach to using FastAPI dependencies on individual routes.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        # Skip authentication for certain paths like health checks, docs, etc.
        path = request.url.path

        # Skip auth for public endpoints (like docs, health check, etc.)
        public_paths = ["/docs", "/redoc", "/openapi.json", "/health", "/"]
        if path in public_paths or path.startswith("/docs") or path.startswith("/redoc"):
            await self.app(scope, receive, send)
            return

        # Extract the authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "type": "https://todoapi.example.com/errors/unauthorized",
                    "title": "Unauthorized",
                    "status": 401,
                    "detail": "Authorization header missing or invalid"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
            await response(scope, receive, send)
            return

        token = auth_header.split(" ", 1)[1]  # Extract token after "Bearer "

        try:
            # Validate the token using the JWTHandler from auth module
            from src.auth.jwt_handler import JWTHandler
            payload = JWTHandler.validate_token_claims(token)

            # Add user info to request state for use in route handlers
            request.state.user = {
                "user_id": payload.get("sub"),
                "claims": payload,
                "authenticated": True
            }

            # Proceed with the request
            await self.app(scope, receive, send)
        except HTTPException as e:
            # Handle HTTP exceptions from JWT validation
            response = JSONResponse(
                status_code=e.status_code,
                content=getattr(e, 'detail', "Authentication failed"),
                headers=e.headers or {}
            )
            await response(scope, receive, send)
        except Exception as e:
            # Handle any other exceptions
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "type": "https://todoapi.example.com/errors/unauthorized",
                    "title": "Unauthorized",
                    "status": 401,
                    "detail": f"Could not validate credentials: {str(e)}"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
            await response(scope, receive, send)