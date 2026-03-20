from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Stage(ABC, Generic[T]):
    @abstractmethod
    def execute(self, context: T) -> T:
        """Execute this stage, enriching and returning the context."""
