import pytest
from models.exceptions import ValuationError, NoCompsFoundError, InsufficientDataError, CalculationError


def test_exception_hierarchy():
    assert issubclass(NoCompsFoundError, ValuationError)
    assert issubclass(InsufficientDataError, ValuationError)
    assert issubclass(CalculationError, ValuationError)


def test_exceptions_are_raiseable():
    with pytest.raises(NoCompsFoundError):
        raise NoCompsFoundError("No comps for sector 'X'")

    with pytest.raises(InsufficientDataError):
        raise InsufficientDataError("Only 1 comp found, need at least 2")

    with pytest.raises(CalculationError):
        raise CalculationError("Division by zero")
