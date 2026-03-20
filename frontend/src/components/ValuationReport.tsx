import type { ValuationReport as ReportData } from '../api/client';

interface Props {
  report: ReportData;
}

export function ValuationReport({ report }: Props) {
  return (
    <div>
      <div className="card">
        <div className="report-header">
          <h2 className="report-company">{report.company_name}</h2>
          <p className="report-methodology">{report.methodology}</p>
        </div>

        <div className="fair-value-hero">
          <div className="fair-value-left">
            <div className="fair-value-label">Fair Value Estimate</div>
            <div className="fair-value-amount">${report.fair_value_mm.toFixed(1)}M</div>
          </div>
          <div className="fair-value-right">
            <div className="multiple-label">Mean EV / Revenue</div>
            <div className="multiple-value">{report.mean_revenue_multiple}x</div>
          </div>
        </div>

        <p className="card-title">Explanation</p>
        <p className="explanation-text">{report.explanation}</p>
      </div>

      <div className="card">
        <p className="card-title">Comparable Companies</p>
        <table className="comps-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Enterprise Value ($M)</th>
              <th>Revenue ($M)</th>
              <th>EV / Revenue</th>
            </tr>
          </thead>
          <tbody>
            {report.comps_used.map((comp) => (
              <tr key={comp.name}>
                <td>{comp.name}</td>
                <td>{comp.enterprise_value_mm.toLocaleString()}</td>
                <td>{comp.revenue_mm.toLocaleString()}</td>
                <td>{comp.revenue_multiple}x</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <p className="card-title">Assumptions</p>
        <ul className="audit-list">
          {report.assumptions.map((a, i) => <li key={i}>{a}</li>)}
        </ul>
      </div>

      <div className="card">
        <p className="card-title">Data Sources</p>
        <ul className="audit-list">
          {report.citations.map((c, i) => <li key={i}>{c}</li>)}
        </ul>
      </div>
    </div>
  );
}
