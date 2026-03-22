from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from schemas.report import ValuationReport

R = TypeVar("R")


class ValuationModel(ABC, Generic[R]):
    @abstractmethod
    def run(self, request: R) -> ValuationReport:
        """Run the valuation workflow and return the report."""
