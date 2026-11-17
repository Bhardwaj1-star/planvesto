"""
core/exceptions.py
Exception definitions and compatibility aliases.
"""

from app.core.errors import (
    AppBaseException,
    DomainValidationError,
    BusinessRuleViolationError,
    EntityNotFoundError,
    UnauthorizedAccessError,
    ConflictError,
)


class DatabaseConnectionError(AppBaseException):
    def __init__(self, message: str = "Database connection error.", details=None):
        super().__init__(message=message, code="DATABASE_CONNECTION_ERROR", details=details)


class AuthenticationError(AppBaseException):
    def __init__(self, message: str = "Authentication failed.", details=None):
        super().__init__(message=message, code="UNAUTHORIZED", details=details)


class AuthorizationError(AppBaseException):
    def __init__(self, message: str = "Permission denied.", details=None):
        super().__init__(message=message, code="FORBIDDEN", details=details)


__all__ = [
    "AppBaseException",
    "DomainValidationError",
    "BusinessRuleViolationError",
    "EntityNotFoundError",
    "UnauthorizedAccessError",
    "ConflictError",
    "DatabaseConnectionError",
    "AuthenticationError",
    "AuthorizationError",
]
