import pytest
from unittest.mock import MagicMock
from models.dcf_model import DcfModel
from schemas.request import ValuationRequest, ModelType
from schemas.report import ValuationReport, DcfYearData


def _make_dcf_request():
    return ValuationRequest(
        company_name="Alpha",
        model=ModelType.DCF,
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )


def _make_mock_report():
    return ValuationReport(
        company_name="Alpha",
        methodology="Discounted Cash Flow",
        fair_value_mm=19.81,
        assumptions=["some assumption"],
        citations=["some citation"],
        explanation="Alpha was valued at $19.8M.",
        dcf_cashflows=[DcfYearData(year=1, revenue_mm=10.0, fcf_mm=2.0, discounted_fcf_mm=1.74)],
        terminal_value_mm=11.95,
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )


def test_dcf_model_delegates_to_pipeline():
    mock_pipeline = MagicMock()
    mock_pipeline.execute.return_value = _make_mock_report()
    model = DcfModel(pipeline=mock_pipeline)
    request = _make_dcf_request()
    report = model.run(request)
    assert mock_pipeline.execute.called
    assert report.methodology == "Discounted Cash Flow"


def test_dcf_model_passes_correct_context_to_pipeline():
    mock_pipeline = MagicMock()
    mock_pipeline.execute.return_value = _make_mock_report()
    model = DcfModel(pipeline=mock_pipeline)
    request = _make_dcf_request()
    model.run(request)
    context = mock_pipeline.execute.call_args[0][0]
    assert context.company_name == "Alpha"
    assert context.projections == [10.0, 11.0, 12.0, 13.0, 14.0]
    assert context.ebitda_margin_pct == 0.20
    assert context.discount_rate == 0.15
    assert context.terminal_growth_rate == 0.03


def test_dcf_model_uses_dcf_pipeline_by_default():
    from pipeline.dcf.dcf_pipeline import DcfPipeline
    model = DcfModel()
    assert isinstance(model._pipeline, DcfPipeline)
