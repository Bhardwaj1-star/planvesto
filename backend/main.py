"""
backend/main.py
Root entrypoint bridge for Render and deployment platform compatibility.
Exposes the single composition root from app.main.
"""

from app.main import app

__all__ = ["app"]
