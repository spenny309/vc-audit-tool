from models.dcf_model import DcfModel
from schemas.request import DcfRequest


def _make_request():
    return DcfRequest(
        model="DCF",
        company_name="  Alpha  ",
        projections=[10.0, 11.0, 12.0, 13.0, 14.0],
        ebitda_margin_pct=0.20,
        discount_rate=0.15,
        terminal_growth_rate=0.03,
    )


def test_dcf_integration_returns_report():
    model = DcfModel()
    report = model.run(_make_request())
    assert report is not None
    assert report.methodology == "Discounted Cash Flow"


def test_dcf_integration_strips_company_name():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.company_name == "Alpha"


def test_dcf_integration_five_cashflows():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.dcf_details is not None
    assert len(report.dcf_details.dcf_cashflows) == 5
    assert [cf.year for cf in report.dcf_details.dcf_cashflows] == [1, 2, 3, 4, 5]


def test_dcf_integration_cashflow_year1():
    model = DcfModel()
    report = model.run(_make_request())
    cf1 = report.dcf_details.dcf_cashflows[0]
    assert cf1.revenue_mm == 10.0
    assert cf1.fcf_mm == 2.0
    assert cf1.discounted_fcf_mm == 1.74


def test_dcf_integration_cashflow_year5():
    model = DcfModel()
    report = model.run(_make_request())
    cf5 = report.dcf_details.dcf_cashflows[4]
    assert cf5.revenue_mm == 14.0
    assert cf5.fcf_mm == 2.8
    assert cf5.discounted_fcf_mm == 1.39


def test_dcf_integration_terminal_value():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.dcf_details.terminal_value_mm == 11.95


def test_dcf_integration_fair_value():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.fair_value_mm == 19.81


def test_dcf_integration_rate_fields():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.dcf_details.ebitda_margin_pct == 0.20
    assert report.dcf_details.discount_rate == 0.15
    assert report.dcf_details.terminal_growth_rate == 0.03


def test_dcf_integration_assumptions_and_citations():
    model = DcfModel()
    report = model.run(_make_request())
    assert len(report.assumptions) == 4  # ingest + project + discount + terminal
    assert len(report.citations) == 1    # "Projections provided by user"
    assert "Projections provided by user" in report.citations


def test_dcf_integration_fair_value_equals_cashflows_plus_tv():
    model = DcfModel()
    report = model.run(_make_request())
    sum_discounted = sum(cf.discounted_fcf_mm for cf in report.dcf_details.dcf_cashflows)
    assert round(sum_discounted + report.dcf_details.terminal_value_mm, 2) == report.fair_value_mm


def test_dcf_integration_comps_fields_are_none():
    model = DcfModel()
    report = model.run(_make_request())
    assert report.comps_details is None
