"""
application/ports/identity_provider.py
Identity lookup contract consumed by application logic.
Concrete Supabase Auth / JWT verification adapters reside in infrastructure/security.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthenticatedInvestor:
    investor_id: str
    email: Optional[str] = None
    is_active: bool = True


class IIdentityProvider(ABC):
    @abstractmethod
    def get_current_investor(self, token: str) -> Optional[AuthenticatedInvestor]:
        """Validate token and resolve current authenticated investor."""
        pass
