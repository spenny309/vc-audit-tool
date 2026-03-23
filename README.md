# VC Audit Tool

Auditable fair value estimates for private VC portfolio companies — React frontend + Flask backend.

## Approach

All three assignment methodologies are implemented, selectable per valuation:

| Model | Logic |
|---|---|
| **Comparable Company Analysis** | Fetches sector peer group, computes mean EV/Revenue multiple, applies to LTM revenue |
| **Discounted Cash Flow** | Projects 5-year FCF from user revenue forecasts and EBITDA margin, discounts at WACC, adds Gordon Growth terminal value |
| **Last Round (Market-Adjusted)** | Adjusts last post-money valuation by the % change in a public index (Nasdaq or S&P 500) since the round date |

Every report includes a **fair value estimate**, **assumptions**, **citations** (data sources), and a **narrative explanation** — the full audit trail is built as the pipeline runs, not reconstructed after the fact.

## Key Design Decisions

- **Pipeline/Stage architecture**: Each model runs a typed `Pipeline[TContext]` of single-responsibility `Stage` objects. Adding a new methodology means adding a new pipeline — minimal changes to existing code.
- **Auditable by design**: Stages append to `assumptions` and `citations` as they execute. The audit trail is a natural output of computation, not a post-hoc summary.
- **Typed request/response schemas**: Requests use a Pydantic v2 discriminated union (`CompsRequest | DcfRequest | LastRoundRequest`) — invalid inputs are rejected at the boundary with structured errors. Nested response objects (`CompsDetails`, `DcfDetails`, `LastRoundDetails`) keep the report self-contained.
- **Mocked market data**: Comp datasets and index history are hardcoded mocks. Each report's `citations` field records this explicitly so the source is always traceable.

## Setup

**Backend** (Python 3.11+):
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                  # runs on http://localhost:5000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev                    # runs on http://localhost:5173
```

**Tests**:
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

## Usage

Open `http://localhost:5173`, select a model, fill in the form, and click **Run Valuation**. The report renders inline with the fair value, methodology details, assumptions, and data sources.

## Tech Stack

- **Frontend**: React + TypeScript, bundled with Vite
- **Backend**: Python / Flask REST API
- **Validation**: Pydantic v2 schemas at the API boundary
- **Tests**: pytest

## Potential Improvements

- **Real market data**: Replace mocked comp datasets and index history with live API calls (Yahoo Finance, Bloomberg)
- **Richer DCF inputs**: Accept revenue, expenses, and capex separately rather than a single EBITDA margin approximation
- **Comp filtering**: Narrow the peer group by size and growth profile, not just sector
- **Valuation ranges**: Return a confidence interval (e.g. 25th–75th percentile of comp multiples) alongside the point estimate
