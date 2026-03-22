# Last Round (Market-Adjusted) Valuation — Design Spec

**Date:** 2026-03-22
**Status:** Approved

---

## Overview

Add a third valuation model — Last Round (Market-Adjusted) — to the VC Audit Tool. This model takes a company's post-money valuation from its most recent funding round and adjusts it by the percentage change in the Nasdaq Composite index from the round date to today, producing an auditable, mark-to-market fair value estimate.

The implementation follows the existing pipeline architecture exactly: a typed `LastRoundContext` dataclass flows through four ordered `Stage` implementations inside a `LastRoundPipeline`, wired together by `LastRoundModel`. All index data is mocked via a static quarterly lookup table.

---

## Algorithm

```
index_pct_change = (index_today - index_at_round) / index_at_round
fair_value_mm    = last_post_money_valuation_mm * (1 + index_pct_change)
```

---

## New Files

```
backend/data/mock_index.py
backend/schemas/last_round_context.py
backend/pipeline/last_round/__init__.py
backend/pipeline/last_round/last_round_pipeline.py
backend/pipeline/last_round/stages/__init__.py
backend/pipeline/last_round/stages/ingest.py
backend/pipeline/last_round/stages/fetch_index.py
backend/pipeline/last_round/stages/apply_adjustment.py
backend/pipeline/last_round/stages/build_report.py
backend/models/last_round_model.py
backend/tests/stages/last_round/__init__.py
backend/tests/stages/last_round/test_ingest.py
backend/tests/stages/last_round/test_fetch_index.py
backend/tests/stages/last_round/test_apply_adjustment.py
backend/tests/stages/last_round/test_build_report.py
backend/tests/test_last_round_model.py
backend/tests/test_last_round_integration.py
```

## Modified Files

```
backend/schemas/request.py          # ModelType.LAST_ROUND, new fields, extended model_validator
backend/schemas/report.py           # 5 new optional fields on ValuationReport
backend/app.py                      # Register LastRoundModel in MODEL_REGISTRY
frontend/src/api/client.ts          # Extend ModelType, ValuationRequest, ValuationReport
frontend/src/components/ValuationForm.tsx    # Add Last Round field section
frontend/src/components/ValuationReport.tsx  # Add Last Round display section
```

---

## Data Model

### Request (`schemas/request.py`)

New enum value:
```python
class ModelType(str, Enum):
    COMPS = "Comps"
    DCF = "DCF"
    LAST_ROUND = "Last Round"
```

New optional fields on `ValuationRequest`:
```python
last_post_money_valuation_mm: Optional[float] = None  # post-money valuation in $M
last_round_date: Optional[str] = None                  # ISO date: "YYYY-MM-DD"
```

New validation branch in `model_validator` for `ModelType.LAST_ROUND`:
- `last_post_money_valuation_mm` must be present and > 0
- `last_round_date` must be present, parseable as a valid ISO date (`YYYY-MM-DD`), not in the future, and not before `2015-01-01` (earliest mock data)

### Context (`schemas/last_round_context.py`)

`last_round_date` is kept as a `str` on the context (matching the request type). `IngestStage` parses it and populates `last_round_date_parsed` (`datetime.date`). All downstream stages read from `last_round_date_parsed`.

```python
@dataclass
class LastRoundContext:
    # Set at construction (from ValuationRequest)
    company_name: str
    last_post_money_valuation_mm: float
    last_round_date: str                          # ISO string: "YYYY-MM-DD"

    # Set by IngestStage
    last_round_date_parsed: Optional[date] = None # parsed datetime.date

    # Set by FetchIndexStage
    index_value_at_round: Optional[float] = None
    index_value_today: Optional[float] = None

    # Set by ApplyAdjustmentStage
    index_pct_change: Optional[float] = None      # e.g. 0.142 = +14.2%
    fair_value_mm: Optional[float] = None

    # Set by BuildReportStage
    report: Optional[ValuationReport] = None

    # Accumulated throughout
    assumptions: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
```

### Report (`schemas/report.py`)

New optional fields added to `ValuationReport`:
```python
last_post_money_valuation_mm: Optional[float] = None
last_round_date: Optional[str] = None
index_value_at_round: Optional[float] = None
index_value_today: Optional[float] = None
index_pct_change: Optional[float] = None
```

---

## Mock Index Data (`data/mock_index.py`)

`NASDAQ_QUARTERLY_CLOSES: dict[date, float]` — approximately 45 entries covering 2015-Q1 through 2026-Q1, using real historical quarterly closing values for the Nasdaq Composite.

`get_nasdaq_at_date(d: date) -> float` — returns the value from the entry with the smallest absolute date difference:
```python
def get_nasdaq_at_date(d: date) -> float:
    nearest = min(NASDAQ_QUARTERLY_CLOSES, key=lambda k: abs(k - d))
    return NASDAQ_QUARTERLY_CLOSES[nearest]
```

The "today" value is a module-level constant derived from the most recent table entry, not from `date.today()`. This ensures deterministic behaviour and makes tests assertable against known values:
```python
INDEX_DATE_TODAY: date = max(NASDAQ_QUARTERLY_CLOSES)
INDEX_VALUE_TODAY: float = NASDAQ_QUARTERLY_CLOSES[INDEX_DATE_TODAY]
```

---

## Pipeline

### `LastRoundPipeline`

```
LastRoundIngestStage
  → LastRoundFetchIndexStage
  → LastRoundApplyAdjustmentStage
  → LastRoundBuildReportStage
```

Follows the same pattern as `DcfPipeline`: iterates stages, re-raises `ValuationError` as-is, wraps unexpected exceptions in `CalculationError`.

### Stage Responsibilities

**`LastRoundIngestStage`**
- Strip/normalize `company_name`
- Parse `context.last_round_date` (str) → `datetime.date`, store as `context.last_round_date_parsed`
- Append assumption: `"Target company: {name}, Last Round (Market-Adjusted) valuation as of {round_date}"` where `{round_date}` is `last_round_date_parsed`

**`LastRoundFetchIndexStage`**
- Call `get_nasdaq_at_date(context.last_round_date_parsed)` → set `context.index_value_at_round`
- Set `context.index_value_today = INDEX_VALUE_TODAY` (the module-level constant — not `date.today()`)
- Append citation: `"Nasdaq Composite index data: mock historical quarterly close prices (source: mocked for audit demo)"`
- Append assumption: `"Index at round date ({date}): {value:.2f} (nearest quarterly close)"`

**`LastRoundApplyAdjustmentStage`**
- Guard first: if `context.index_value_at_round == 0`, raise `CalculationError("Index value at round date is zero; cannot compute adjustment")`
- Calculate `index_pct_change = (index_today - index_at_round) / index_at_round`
- Calculate `fair_value_mm = round(last_post_money_valuation_mm * (1 + index_pct_change), 2)`
- Append assumption: `"Nasdaq moved {pct:+.1f}% from round date to today; applied to last post-money valuation of ${val:.1f}M"`

**`LastRoundBuildReportStage`**
- Construct `ValuationReport` with all common fields + all Last Round optional fields
- `report.last_round_date` is set from `context.last_round_date` (the original request string)
- Explanation: `"{name} was valued at ${fair:.1f}M, starting from a last post-money valuation of ${orig:.1f}M (round date: {date}) and adjusting by {pct:+.1f}% to reflect Nasdaq Composite performance over that period."`

### `LastRoundModel`

```python
class LastRoundModel(ValuationModel):
    def __init__(self, pipeline: Pipeline[LastRoundContext] | None = None) -> None:
        self._pipeline = pipeline or LastRoundPipeline()

    def run(self, request: ValuationRequest) -> ValuationReport:
        context = LastRoundContext(
            company_name=request.company_name,
            last_post_money_valuation_mm=request.last_post_money_valuation_mm,
            last_round_date=request.last_round_date,
        )
        return self._pipeline.execute(context)
```

---

## App Registration (`app.py`)

```python
from models.last_round_model import LastRoundModel

MODEL_REGISTRY: dict[ModelType, ValuationModel] = {
    ModelType.COMPS: CompsModel(),
    ModelType.DCF: DcfModel(),
    ModelType.LAST_ROUND: LastRoundModel(),
}
```

---

## Error Handling

| Scenario | Where caught | HTTP status |
|---|---|---|
| Missing/invalid `last_round_date` format | `model_validator` → `ValueError` → Pydantic `ValidationError` | 400 |
| Date in the future | `model_validator` → `ValueError` | 400 |
| Date before 2015-01-01 | `model_validator` → `ValueError` | 400 |
| `last_post_money_valuation_mm` ≤ 0 | `model_validator` → `ValueError` | 400 |
| `index_at_round == 0` (division by zero) | `ApplyAdjustmentStage` → `CalculationError` (guard runs before division) | 500 |
| Unexpected pipeline failure | `LastRoundPipeline.execute()` → `CalculationError` | 500 |

---

## Frontend

### `client.ts`

```typescript
export type ModelType = "Comps" | "DCF" | "Last Round";

// Added to ValuationRequest
last_post_money_valuation_mm?: number;
last_round_date?: string;   // "YYYY-MM-DD"

// Added to ValuationReport
last_post_money_valuation_mm?: number;
last_round_date?: string;
index_value_at_round?: number;
index_value_today?: number;
index_pct_change?: number;
```

### `ValuationForm.tsx`

New field section rendered when `selectedModel === 'Last Round'`:
- **Last Post-Money Valuation ($M)** — number input, min 0.01
- **Date of Last Round** — date input (`type="date"`, max set to today, min `2015-01-01`)

`handleModelChange` extended to reset the two new state fields.
`handleSubmit` extended with a `'Last Round'` branch.

### `ValuationReport.tsx`

New conditional block rendered when `report.index_pct_change !== undefined` (numeric guard; avoids empty-string falsiness of a string field):

**"Market Adjustment" card** — table with:
| Row | Value |
|---|---|
| Last Post-Money Valuation | `${last_post_money_valuation_mm}M` |
| Date of Last Round | `last_round_date` |
| Nasdaq at Round Date | formatted number |
| Nasdaq Today | formatted number |
| Market Adjustment | `{pct:+.1%}` — green if ≥ 0, red if < 0 |

---

## Test Plan

### Stage unit tests

**`test_ingest.py`**
- Company name is stripped of whitespace
- `last_round_date_parsed` is set to the correct `datetime.date` on context
- Assumption text is appended

**`test_fetch_index.py`**
- Exact date match returns correct value for `index_value_at_round`
- Date between two entries returns nearest for `index_value_at_round`
- `index_value_today` equals `INDEX_VALUE_TODAY` constant (deterministic, no `date.today()` call)
- Citation is appended

**`test_apply_adjustment.py`**
- Positive market move: `fair_value_mm > last_post_money_valuation_mm`
- Negative market move: `fair_value_mm < last_post_money_valuation_mm`
- Zero market move (`index_at_round == index_today`): `fair_value_mm == last_post_money_valuation_mm`
- `index_at_round == 0` raises `CalculationError` before any division occurs
- Assumption text appended with correct sign

**`test_build_report.py`**
- All Last Round optional fields populated on report
- `explanation` contains company name, fair value, original valuation, and adjustment pct

### Model-level tests (`test_last_round_model.py`)
- `run()` returns a `ValuationReport`
- `run()` passes correct field values to pipeline (asserts `company_name`, `last_post_money_valuation_mm`, `last_round_date` arrive on context as expected)
- Default pipeline is an instance of `LastRoundPipeline`
- Pipeline is injectable (test with mock pipeline)

### Integration tests (`test_last_round_integration.py`)
- `POST /api/valuate` with valid Last Round payload → 200, exact `fair_value_mm` asserted (pick a round date whose nearest quarterly close is known, compute expected value by hand)
- Missing `last_post_money_valuation_mm` → 400
- Missing `last_round_date` → 400
- Future `last_round_date` → 400
- `last_round_date` before 2015-01-01 → 400
