from __future__ import annotations

from typing import Generic, TypeVar

from models.exceptions import CalculationError, ValuationError
from schemas.report import ValuationReport

T = TypeVar("T")


class Pipeline(Generic[T]):
    def __init__(self, stages: list | None = None) -> None:
        self._stages = stages or []

    def execute(self, context: T) -> ValuationReport:
        """Run all stages and return the final ValuationReport."""
        try:
            for stage in self._stages:
                context = stage.execute(context)
            return context.report
        except ValuationError:
            raise
        except Exception as e:
            raise CalculationError(f"Unexpected pipeline error: {e}") from e
