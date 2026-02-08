from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import os


class AppConfig(BaseSettings):
    """Application configuration settings"""

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Authentication settings
    better_auth_secret: str = os.getenv("AUTH_SECRET", "")  # Using same variable as auth_config
    auth_algorithm: str = os.getenv("AUTH_ALGORITHM", "HS256")
    auth_audience: str = os.getenv("AUTH_AUDIENCE", "todo-api")
    auth_issuer: str = os.getenv("AUTH_ISSUER", "better-auth")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Debug settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "info")

    # AI/Agent settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    model_config = {"env_file": ".env", "extra": "ignore"}


def validate_environment_variables() -> Dict[str, Any]:
    """
    Validate that all required environment variables are set and properly configured.

    Returns:
        Dictionary with validation results and messages
    """
    required_vars = [
        "DATABASE_URL",
        "BETTER_AUTH_SECRET",
        "OPENAI_API_KEY"
    ]

    results = {}
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value and value.strip() != "" and value != "your-super-secret-key-change-in-production":
            results[var] = True
        else:
            results[var] = False
            missing_vars.append(var)

    all_valid = len(missing_vars) == 0

    return {
        "all_valid": all_valid,
        "results": results,
        "missing_variables": missing_vars,
        "message": "All required environment variables are properly configured" if all_valid
                  else f"Missing required environment variables: {', '.join(missing_vars)}"
    }


def validate_auth_configuration() -> Dict[str, Any]:
    """
    Validate authentication-specific configuration settings.

    Returns:
        Dictionary with auth validation results
    """
    auth_validation = {
        "secret_strength": False,
        "algorithm_valid": False,
        "audience_set": False,
        "issuer_set": False
    }

    better_auth_secret = os.getenv("BETTER_AUTH_SECRET")
    auth_algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
    auth_audience = os.getenv("AUTH_AUDIENCE", "todo-api")
    auth_issuer = os.getenv("AUTH_ISSUER", "better-auth")

    # Check if auth secret is properly set (not default placeholder)
    if better_auth_secret and better_auth_secret != "your-super-secret-key-change-in-production" and len(better_auth_secret) >= 32:
        auth_validation["secret_strength"] = True

    # Check if algorithm is valid
    valid_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
    if auth_algorithm in valid_algorithms:
        auth_validation["algorithm_valid"] = True

    # Check if audience and issuer are set
    if auth_audience and auth_audience != "":
        auth_validation["audience_set"] = True

    if auth_issuer and auth_issuer != "":
        auth_validation["issuer_set"] = True

    all_valid = all(auth_validation.values())

    return {
        "all_valid": all_valid,
        "results": auth_validation,
        "message": "Authentication configuration is properly set" if all_valid
                  else "Some authentication configuration issues detected"
    }


def get_config_summary() -> Dict[str, Any]:
    """
    Get a summary of the current configuration.

    Returns:
        Dictionary with configuration summary
    """
    return {
        "database_configured": bool(os.getenv("DATABASE_URL")),
        "auth_configured": validate_auth_configuration()["all_valid"],
        "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "env_file_exists": os.path.exists(".env")
    }


# Create global instance
app_config = AppConfig()