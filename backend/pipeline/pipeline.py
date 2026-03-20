from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from schemas.report import ValuationReport

T = TypeVar("T")


class Pipeline(ABC, Generic[T]):
    @abstractmethod
    def execute(self, context: T) -> ValuationReport:
        """Run all stages and return the final ValuationReport."""
