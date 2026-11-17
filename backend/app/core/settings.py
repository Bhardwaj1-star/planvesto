"""
core/settings.py
Settings accessor compatibility bridge.
"""

from app.core.config import settings, Settings


def get_settings() -> Settings:
    return settings


__all__ = ["settings", "get_settings", "Settings"]
