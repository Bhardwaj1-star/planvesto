"""Application-wide technical exception types and stable error categorization."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for all Planvesto backend technical errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ConfigurationError(AppException):
    """Raised when environment or runtime settings are invalid or missing."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="CONFIGURATION_ERROR", details=details)


class AuthenticationError(AppException):
    """Raised when request credentials are missing, invalid, or expired."""

    def __init__(self, message: str = "Authentication required", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="AUTHENTICATION_REQUIRED", details=details)


class AuthorizationError(AppException):
    """Raised when user lacks permission to access or modify a resource."""

    def __init__(self, message: str = "Permission denied", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="PERMISSION_DENIED", details=details)


class DatabaseConnectionError(AppException):
    """Raised when persistence provider or database cannot be reached."""

    def __init__(self, message: str = "Database connection error", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="DATABASE_CONNECTION_ERROR", details=details)


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code="NOT_FOUND", details=details)
