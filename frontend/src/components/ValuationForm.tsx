import { useState, useEffect } from 'react';
import { getSectors, getModels } from '../api/client';
import type { ValuationRequest, ModelType } from '../api/client';

interface Props {
  onSubmit: (request: ValuationRequest) => void;
  isLoading: boolean;
}

export function ValuationForm({ onSubmit, isLoading }: Props) {
  const [models, setModels] = useState<string[]>([]);
  const [sectors, setSectors] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState<ModelType>('Comps');
  const [companyName, setCompanyName] = useState('');

  // Comps fields
  const [sector, setSector] = useState('');
  const [revenueMm, setRevenueMm] = useState('');

  // DCF fields
  const [year1, setYear1] = useState('');
  const [year2, setYear2] = useState('');
  const [year3, setYear3] = useState('');
  const [year4, setYear4] = useState('');
  const [year5, setYear5] = useState('');
  const [ebitdaMarginPct, setEbitdaMarginPct] = useState('');
  const [discountRate, setDiscountRate] = useState('');
  const [terminalGrowthRate, setTerminalGrowthRate] = useState('');

  useEffect(() => {
    getSectors().then(setSectors).catch(console.error);
    getModels().then(setModels).catch(console.error);
  }, []);

  function handleModelChange(model: ModelType) {
    setSelectedModel(model);
    // Reset model-specific fields
    setSector('');
    setRevenueMm('');
    setYear1(''); setYear2(''); setYear3(''); setYear4(''); setYear5('');
    setEbitdaMarginPct(''); setDiscountRate(''); setTerminalGrowthRate('');
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (selectedModel === 'Comps') {
      onSubmit({
        company_name: companyName,
        model: 'Comps',
        sector,
        revenue_mm: parseFloat(revenueMm),
      });
    } else {
      onSubmit({
        company_name: companyName,
        model: 'DCF',
        projections: [
          parseFloat(year1),
          parseFloat(year2),
          parseFloat(year3),
          parseFloat(year4),
          parseFloat(year5),
        ],
        ebitda_margin_pct: parseFloat(ebitdaMarginPct) / 100,
        discount_rate: parseFloat(discountRate) / 100,
        terminal_growth_rate: parseFloat(terminalGrowthRate) / 100,
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
            value={selectedModel}
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
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g. Modus"
            required
          />
        </div>

        {selectedModel === 'Comps' && (
          <>
            <div className="form-group">
              <label className="form-label" htmlFor="sector">Sector</label>
              <select
                id="sector"
                className="form-select"
                value={sector}
                onChange={(e) => setSector(e.target.value)}
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
                value={revenueMm}
                onChange={(e) => setRevenueMm(e.target.value)}
                placeholder="e.g. 10"
                min="0.01"
                step="0.01"
                required
              />
            </div>
          </>
        )}

        {selectedModel === 'DCF' && (
          <>
            {[
              { id: 'year1', label: 'Year 1 Revenue ($M)', value: year1, set: setYear1 },
              { id: 'year2', label: 'Year 2 Revenue ($M)', value: year2, set: setYear2 },
              { id: 'year3', label: 'Year 3 Revenue ($M)', value: year3, set: setYear3 },
              { id: 'year4', label: 'Year 4 Revenue ($M)', value: year4, set: setYear4 },
              { id: 'year5', label: 'Year 5 Revenue ($M)', value: year5, set: setYear5 },
            ].map(({ id, label, value, set }) => (
              <div className="form-group" key={id}>
                <label className="form-label" htmlFor={id}>{label}</label>
                <input
                  id={id}
                  className="form-input"
                  type="number"
                  value={value}
                  onChange={(e) => set(e.target.value)}
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
                value={ebitdaMarginPct}
                onChange={(e) => setEbitdaMarginPct(e.target.value)}
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
                value={discountRate}
                onChange={(e) => setDiscountRate(e.target.value)}
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
                value={terminalGrowthRate}
                onChange={(e) => setTerminalGrowthRate(e.target.value)}
                placeholder="e.g. 3"
                min="0.01"
                max="99.99"
                step="0.01"
                required
              />
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
