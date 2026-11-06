"""Safe structured logging and diagnostic conventions without leaking secrets."""

import logging
import re
from typing import Any

# Patterns to mask sensitive tokens and credentials
SENSITIVE_PATTERNS = [
    (re.compile(r"Bearer\s+([A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE), "Bearer [REDACTED]"),
    (re.compile(r"(password|secret|service_role_key|apikey)=([^\s&]+)", re.IGNORECASE), r"\1=[REDACTED]"),
]


class SafeFormatter(logging.Formatter):
    """Logging formatter that redacts bearer tokens, passwords, and secrets."""

    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        sanitized = original
        for pattern, replacement in SENSITIVE_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)
        return sanitized


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with safe redaction formatter."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            SafeFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
