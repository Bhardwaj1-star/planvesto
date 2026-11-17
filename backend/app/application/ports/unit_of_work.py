"""
application/ports/unit_of_work.py
Transaction boundary contract used to coordinate atomic persistence across repositories.
Domain code and application use cases rely on this port without coupling to concrete DB drivers.
"""

from abc import ABC, abstractmethod
from typing import Any


class IUnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        """Enter transaction context."""
        pass

    @abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit transaction context, committing if no exception, rolling back otherwise."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Commit the ongoing transaction."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Roll back the ongoing transaction."""
        pass
