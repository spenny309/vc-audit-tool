from abc import ABC, abstractmethod

from schemas.request import ValuationRequest
from schemas.report import ValuationReport


class ValuationModel(ABC):
    @abstractmethod
    def run(self, request: ValuationRequest) -> ValuationReport:
        """Run the valuation workflow and return the report."""
