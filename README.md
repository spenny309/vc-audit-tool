# VC Audit Tool

A structured, auditable backend service for estimating the fair value of private VC portfolio companies using **Comparable Company Analysis (Comps)**.

## Overview

VC auditors need a consistent, traceable workflow for valuing private, illiquid portfolio companies. This tool implements a Comps-based methodology: it selects a set of publicly-traded peer companies, computes a mean EV/Revenue multiple, and applies that multiple to the target company's LTM revenue.

**Chosen methodology: Comparable Company Analysis**

The system identifies comparable public companies by sector, computes the mean EV/Revenue multiple across the peer group, and applies it to the private company's revenue to produce a fair value estimate. Every step in the process is recorded in the report's `assumptions` and `citations` fields.

## Key Design Decisions

- **Pipeline architecture**: The valuation workflow is modelled as a `Pipeline` of `Stage` objects. Each stage has a single responsibility and enriches a shared `CompsContext` as it runs.
- **OOP extensibility**: `ValuationModel`, `Pipeline`, and `Stage` are abstract base classes. Adding a new methodology (e.g. DCF) requires implementing a new `ValuationModel` + `Pipeline` pair — no changes to existing code.
- **Auditable by design**: Each stage appends to `assumptions` and `citations` as it runs. The audit trail is built naturally through the pipeline, not reconstructed after the fact.
- **Mocked data**: External market data (Yahoo Finance API) is mocked for this implementation. The data source is recorded explicitly in every report's `citations`.

## Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Navigate to `http://localhost:5173`.

## Running Tests

```bash
cd backend
pytest -v
```

## Usage Example

Submit a POST request to `http://localhost:5000/api/valuate`:
```json
{
  "company_name": "Basis AI",
  "sector": "SaaS",
  "revenue_mm": 10.0
}
```

**Response:**
```json
{
  "company_name": "Basis AI",
  "methodology": "Comparable Company Analysis",
  "fair_value_mm": 62.9,
  "mean_revenue_multiple": 6.29,
  "comps_used": [...],
  "assumptions": [
    "Target company: Basis AI, Sector: SaaS, LTM Revenue: $10.0M",
    "Selected 4 SaaS comparables",
    "Mean EV/Revenue multiple of 6.29x across 4 comparables",
    "Mean multiple of 6.29x applied to $10.0M LTM revenue"
  ],
  "citations": ["Mock dataset (Yahoo Finance API in production)"],
  "explanation": "Basis AI was valued at $62.9M using a mean EV/Revenue multiple of 6.29x applied to $10.0M LTM revenue, derived from 4 SaaS comparables."
}
```

## Potential Improvements

- Integrate a real financial data API (Yahoo Finance, Bloomberg) in `SelectCompsStage` to replace mock data
- Add additional methodologies (DCF, Last Round) as new `ValuationModel` + `Pipeline` implementations
- Add filtering logic to `SelectCompsStage` to narrow the comp set by size or growth rate
