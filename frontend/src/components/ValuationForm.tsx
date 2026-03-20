import { useState, useEffect } from 'react';
import { getSectors } from '../api/client';
import type { ValuationRequest } from '../api/client';

interface Props {
  onSubmit: (request: ValuationRequest) => void;
  isLoading: boolean;
}

export function ValuationForm({ onSubmit, isLoading }: Props) {
  const [sectors, setSectors] = useState<string[]>([]);
  const [companyName, setCompanyName] = useState('');
  const [sector, setSector] = useState('');
  const [revenueMm, setRevenueMm] = useState('');

  useEffect(() => {
    getSectors().then(setSectors).catch(console.error);
  }, []);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit({
      company_name: companyName,
      sector,
      revenue_mm: parseFloat(revenueMm),
    });
  }

  return (
    <div className="card">
      <p className="card-title">New Valuation</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="company-name">Company Name</label>
          <input
            id="company-name"
            className="form-input"
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g. Basis AI"
            required
          />
        </div>

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

        <button className="btn-primary" type="submit" disabled={isLoading}>
          {isLoading ? 'Running Valuation…' : 'Run Valuation'}
        </button>
      </form>
    </div>
  );
}
