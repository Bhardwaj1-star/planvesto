"""
core/errors.py
Domain and application exception hierarchy.
Maps structured domain failures cleanly without leaking system internals.
"""

from typing import Any, Dict, Optional


class AppBaseException(Exception):
    """Base exception for all application and domain errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class DomainValidationError(AppBaseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="DOMAIN_VALIDATION_ERROR", details=details)


class BusinessRuleViolationError(AppBaseException):
    def __init__(self, message: str, rule_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        d = details or {}
        if rule_id:
            d["rule_id"] = rule_id
        super().__init__(message=message, code="BUSINESS_RULE_VIOLATION", details=d)


class EntityNotFoundError(AppBaseException):
    def __init__(self, entity_name: str, identifier: str):
        super().__init__(
            message=f"{entity_name} with identifier '{identifier}' was not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity": entity_name, "identifier": identifier},
        )


class UnauthorizedAccessError(AppBaseException):
    def __init__(self, message: str = "Unauthorized access."):
        super().__init__(message=message, code="UNAUTHORIZED")


class ConflictError(AppBaseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="CONFLICT", details=details)
