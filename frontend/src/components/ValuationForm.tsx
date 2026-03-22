import { useState, useEffect, useReducer } from 'react';
import { getSectors, getModels, getIndices } from '../api/client';
import type { ValuationRequest, ModelType } from '../api/client';

interface Props {
  onSubmit: (request: ValuationRequest) => void;
  isLoading: boolean;
}

type FormState = {
  selectedModel: ModelType;
  companyName: string;
  sector: string;
  revenueMm: string;
  year1: string;
  year2: string;
  year3: string;
  year4: string;
  year5: string;
  ebitdaMarginPct: string;
  discountRate: string;
  terminalGrowthRate: string;
  lastPostMoneyValuationMm: string;
  lastRoundDate: string;
  index: string;
};

type FormAction =
  | { type: 'SET_MODEL'; model: ModelType; defaultIndex: string }
  | { type: 'SET_FIELD'; field: Exclude<keyof FormState, 'selectedModel'>; value: string };

const initialFormState: FormState = {
  selectedModel: 'Comps',
  companyName: '',
  sector: '',
  revenueMm: '',
  year1: '', year2: '', year3: '', year4: '', year5: '',
  ebitdaMarginPct: '',
  discountRate: '',
  terminalGrowthRate: '',
  lastPostMoneyValuationMm: '',
  lastRoundDate: '',
  index: '',
};

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_MODEL':
      return {
        ...initialFormState,
        selectedModel: action.model,
        companyName: state.companyName,
        index: action.defaultIndex,
      };
    case 'SET_FIELD':
      return { ...state, [action.field]: action.value };
    default:
      return state;
  }
}

export function ValuationForm({ onSubmit, isLoading }: Props) {
  const [models, setModels] = useState<string[]>([]);
  const [sectors, setSectors] = useState<string[]>([]);
  const [indices, setIndices] = useState<string[]>([]);
  const [state, dispatch] = useReducer(formReducer, initialFormState);

  useEffect(() => {
    getSectors().then(setSectors).catch(console.error);
    getModels().then(setModels).catch(console.error);
    getIndices().then((data) => {
      setIndices(data);
      if (data.length > 0) dispatch({ type: 'SET_FIELD', field: 'index', value: data[0] });
    }).catch(console.error);
  }, []);

  function handleModelChange(model: ModelType) {
    dispatch({ type: 'SET_MODEL', model, defaultIndex: indices[0] ?? '' });
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (state.selectedModel === 'Comps') {
      onSubmit({
        company_name: state.companyName,
        model: 'Comps',
        sector: state.sector,
        revenue_mm: parseFloat(state.revenueMm),
      });
    } else if (state.selectedModel === 'DCF') {
      onSubmit({
        company_name: state.companyName,
        model: 'DCF',
        projections: [
          parseFloat(state.year1),
          parseFloat(state.year2),
          parseFloat(state.year3),
          parseFloat(state.year4),
          parseFloat(state.year5),
        ],
        ebitda_margin_pct: parseFloat(state.ebitdaMarginPct) / 100,
        discount_rate: parseFloat(state.discountRate) / 100,
        terminal_growth_rate: parseFloat(state.terminalGrowthRate) / 100,
      });
    } else {
      onSubmit({
        company_name: state.companyName,
        model: 'Last Round',
        last_post_money_valuation_mm: parseFloat(state.lastPostMoneyValuationMm),
        last_round_date: state.lastRoundDate,
        index: state.index || undefined,
      });
    }
  }

  return (
    <div className="card">
      <p className="card-title">New Valuation</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="model">Model</label>
          <select
            id="model"
            className="form-select"
            value={state.selectedModel}
            onChange={(e) => handleModelChange(e.target.value as ModelType)}
          >
            {models.map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="company-name">Company Name</label>
          <input
            id="company-name"
            className="form-input"
            type="text"
            value={state.companyName}
            onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'companyName', value: e.target.value })}
            placeholder="e.g. Modus"
            required
          />
        </div>

        {state.selectedModel === 'Comps' && (
          <>
            <div className="form-group">
              <label className="form-label" htmlFor="sector">Sector</label>
              <select
                id="sector"
                className="form-select"
                value={state.sector}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'sector', value: e.target.value })}
                required
              >
                <option value="">Select a sector</option>
                {sectors.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="revenue">LTM Revenue (USD millions)</label>
              <input
                id="revenue"
                className="form-input"
                type="number"
                value={state.revenueMm}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'revenueMm', value: e.target.value })}
                placeholder="e.g. 10"
                min="0.01"
                step="0.01"
                required
              />
            </div>
          </>
        )}

        {state.selectedModel === 'DCF' && (
          <>
            {[
              { id: 'year1', label: 'Year 1 Revenue ($M)', field: 'year1' as Exclude<keyof FormState, 'selectedModel'>, value: state.year1 },
              { id: 'year2', label: 'Year 2 Revenue ($M)', field: 'year2' as Exclude<keyof FormState, 'selectedModel'>, value: state.year2 },
              { id: 'year3', label: 'Year 3 Revenue ($M)', field: 'year3' as Exclude<keyof FormState, 'selectedModel'>, value: state.year3 },
              { id: 'year4', label: 'Year 4 Revenue ($M)', field: 'year4' as Exclude<keyof FormState, 'selectedModel'>, value: state.year4 },
              { id: 'year5', label: 'Year 5 Revenue ($M)', field: 'year5' as Exclude<keyof FormState, 'selectedModel'>, value: state.year5 },
            ].map(({ id, label, field, value }) => (
              <div className="form-group" key={id}>
                <label className="form-label" htmlFor={id}>{label}</label>
                <input
                  id={id}
                  className="form-input"
                  type="number"
                  value={value}
                  onChange={(e) => dispatch({ type: 'SET_FIELD', field, value: e.target.value })}
                  placeholder="e.g. 10"
                  min="0.01"
                  step="0.01"
                  required
                />
              </div>
            ))}

            <div className="form-group">
              <label className="form-label" htmlFor="ebitda-margin">EBITDA Margin (%)</label>
              <input
                id="ebitda-margin"
                className="form-input"
                type="number"
                value={state.ebitdaMarginPct}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'ebitdaMarginPct', value: e.target.value })}
                placeholder="e.g. 20"
                min="0.01"
                max="99.99"
                step="0.01"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="discount-rate">Discount Rate / WACC (%)</label>
              <input
                id="discount-rate"
                className="form-input"
                type="number"
                value={state.discountRate}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'discountRate', value: e.target.value })}
                placeholder="e.g. 15"
                min="0.01"
                max="99.99"
                step="0.01"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="terminal-growth">Terminal Growth Rate (%)</label>
              <input
                id="terminal-growth"
                className="form-input"
                type="number"
                value={state.terminalGrowthRate}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'terminalGrowthRate', value: e.target.value })}
                placeholder="e.g. 3"
                min="0.01"
                max="99.99"
                step="0.01"
                required
              />
            </div>
          </>
        )}

        {state.selectedModel === 'Last Round' && (
          <>
            <div className="form-group">
              <label className="form-label" htmlFor="last-post-money">Last Post-Money Valuation ($M)</label>
              <input
                id="last-post-money"
                className="form-input"
                type="number"
                value={state.lastPostMoneyValuationMm}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'lastPostMoneyValuationMm', value: e.target.value })}
                placeholder="e.g. 50"
                min="0.01"
                step="0.01"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="last-round-date">Date of Last Round</label>
              <input
                id="last-round-date"
                className="form-input"
                type="date"
                value={state.lastRoundDate}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'lastRoundDate', value: e.target.value })}
                min="2015-01-01"
                max={new Date().toISOString().split('T')[0]}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="index">Market Index</label>
              <select
                id="index"
                className="form-select"
                value={state.index}
                onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'index', value: e.target.value })}
              >
                {indices.map((i) => (
                  <option key={i} value={i}>{i}</option>
                ))}
              </select>
            </div>
          </>
        )}

        <button className="btn-primary" type="submit" disabled={isLoading}>
          {isLoading ? 'Running Valuation…' : 'Run Valuation'}
        </button>
      </form>
    </div>
  );
}
