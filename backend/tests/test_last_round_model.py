import pytest
from unittest.mock import MagicMock
from models.last_round_model import LastRoundModel
from pipeline.last_round.last_round_pipeline import LastRoundPipeline
from schemas.last_round_context import LastRoundContext
from schemas.report import ValuationReport
from schemas.request import ValuationRequest, IndexType


def _make_request(**kwargs) -> ValuationRequest:
    defaults = dict(
        company_name="Acme",
        model="Last Round",
        last_post_money_valuation_mm=100.0,
        last_round_date="2020-03-31",
        index=IndexType.NASDAQ,
    )
    defaults.update(kwargs)
    return ValuationRequest(**defaults)


def test_run_returns_valuation_report():
    model = LastRoundModel()
    request = _make_request()
    result = model.run(request)
    assert isinstance(result, ValuationReport)


def test_run_passes_company_name_to_context():
    captured_contexts = []

    class CapturingPipeline:
        def execute(self, context):
            captured_contexts.append(context)
            # Return a minimal report to satisfy the model
            return ValuationReport(
                company_name=context.company_name,
                methodology="Last Round (Market-Adjusted)",
                fair_value_mm=100.0,
                explanation="test",
                assumptions=[],
                citations=[],
            )

    model = LastRoundModel(pipeline=CapturingPipeline())
    model.run(_make_request(company_name="Test Co"))
    assert captured_contexts[0].company_name == "Test Co"


def test_run_passes_valuation_and_date_to_context():
    captured_contexts = []

    class CapturingPipeline:
        def execute(self, context):
            captured_contexts.append(context)
            return ValuationReport(
                company_name=context.company_name,
                methodology="Last Round (Market-Adjusted)",
                fair_value_mm=200.0,
                explanation="test",
                assumptions=[],
                citations=[],
            )

    model = LastRoundModel(pipeline=CapturingPipeline())
    model.run(_make_request(last_post_money_valuation_mm=200.0, last_round_date="2021-06-30"))
    ctx = captured_contexts[0]
    assert ctx.last_post_money_valuation_mm == 200.0
    assert ctx.last_round_date == "2021-06-30"


def test_default_pipeline_is_last_round_pipeline():
    model = LastRoundModel()
    assert isinstance(model._pipeline, LastRoundPipeline)


def test_pipeline_is_injectable():
    mock_pipeline = MagicMock()
    mock_pipeline.execute.return_value = ValuationReport(
        company_name="Test",
        methodology="Last Round (Market-Adjusted)",
        fair_value_mm=100.0,
        explanation="test",
        assumptions=[],
        citations=[],
    )
    model = LastRoundModel(pipeline=mock_pipeline)
    request = _make_request()
    model.run(request)
    mock_pipeline.execute.assert_called_once()
