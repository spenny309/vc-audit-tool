class ValuationError(Exception):
    """Base class for all valuation pipeline errors."""


class NoCompsFoundError(ValuationError):
    """Raised when no comparable companies are found for the given sector."""


class InsufficientDataError(ValuationError):
    """Raised when fewer than MIN_COMPS comparables are available."""


class CalculationError(ValuationError):
    """Raised when an unexpected arithmetic or pipeline error occurs."""
