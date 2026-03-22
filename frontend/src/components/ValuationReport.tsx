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
            <div className="fair-value-amount">${report.fair_value_mm.toFixed(2)}M</div>
          </div>
          {report.mean_revenue_multiple != null && (
            <div className="fair-value-right">
              <div className="multiple-label">Mean EV / Revenue</div>
              <div className="multiple-value">{report.mean_revenue_multiple?.toFixed(2)}x</div>
            </div>
          )}
        </div>

        <p className="card-title">Explanation</p>
        <p className="explanation-text">{report.explanation}</p>
      </div>

      {report.comps_used && (
        <div className="card">
          <p className="card-title">Comparable Companies</p>
          <table className="data-table">
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
      )}

      {report.dcf_cashflows && (
        <>
          <div className="card">
            <p className="card-title">Key Inputs</p>
            <table className="data-table">
              <tbody>
                <tr>
                  <td>EBITDA Margin</td>
                  <td>{((report.ebitda_margin_pct ?? 0) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td>Discount Rate (WACC)</td>
                  <td>{((report.discount_rate ?? 0) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td>Terminal Growth Rate</td>
                  <td>{((report.terminal_growth_rate ?? 0) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td>Discounted Terminal Value</td>
                  <td>${(report.terminal_value_mm ?? 0).toFixed(2)}M</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="card">
            <p className="card-title">Projected Cash Flows</p>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Revenue ($M)</th>
                  <th>FCF ($M)</th>
                  <th>Discounted FCF ($M)</th>
                </tr>
              </thead>
              <tbody>
                {report.dcf_cashflows.map((cf) => (
                  <tr key={cf.year}>
                    <td>Year {cf.year}</td>
                    <td>{cf.revenue_mm.toFixed(2)}</td>
                    <td>{cf.fcf_mm.toFixed(2)}</td>
                    <td>{cf.discounted_fcf_mm.toFixed(2)}</td>
                  </tr>
                ))}
                <tr>
                  <td><strong>Terminal Value</strong></td>
                  <td>—</td>
                  <td>—</td>
                  <td><strong>{(report.terminal_value_mm ?? 0).toFixed(2)}</strong></td>
                </tr>
              </tbody>
            </table>
          </div>
        </>
      )}

      {report.index_pct_change != null && (
        <div className="card">
          <p className="card-title">Market Adjustment</p>
          <table className="data-table">
            <tbody>
              <tr>
                <td>Last Post-Money Valuation</td>
                <td>${report.last_post_money_valuation_mm?.toFixed(2)}M</td>
              </tr>
              <tr>
                <td>Date of Last Round</td>
                <td>{report.last_round_date}</td>
              </tr>
              <tr>
                <td>Index Used</td>
                <td>{report.index_name}</td>
              </tr>
              <tr>
                <td>Index at Round Date</td>
                <td>{report.index_value_at_round?.toLocaleString()}</td>
              </tr>
              <tr>
                <td>Index Today</td>
                <td>{report.index_value_today?.toLocaleString()}</td>
              </tr>
              <tr>
                <td>Market Adjustment</td>
                <td style={{ color: (report.index_pct_change ?? 0) >= 0 ? 'green' : 'red' }}>
                  {((report.index_pct_change ?? 0) * 100).toFixed(1)}%
                  {(report.index_pct_change ?? 0) >= 0 ? ' ▲' : ' ▼'}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

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
