import type { ValuationReport as ReportData } from '../api/client';

interface Props {
  report: ReportData;
}

export function ValuationReport({ report }: Props) {
  return (
    <div>
      <h2>{report.company_name} — Valuation Report</h2>
      <p><strong>Methodology:</strong> {report.methodology}</p>

      <section>
        <h3>Fair Value Estimate</h3>
        <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
          ${report.fair_value_mm.toFixed(1)}M
        </p>
        <p>Mean EV/Revenue Multiple: {report.mean_revenue_multiple}x</p>
      </section>

      <section>
        <h3>Comparable Companies</h3>
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Enterprise Value ($M)</th>
              <th>Revenue ($M)</th>
              <th>EV/Revenue Multiple</th>
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
      </section>

      <section>
        <h3>Explanation</h3>
        <p>{report.explanation}</p>
      </section>

      <section>
        <h3>Assumptions</h3>
        <ul>
          {report.assumptions.map((a, i) => <li key={i}>{a}</li>)}
        </ul>
      </section>

      <section>
        <h3>Data Sources</h3>
        <ul>
          {report.citations.map((c, i) => <li key={i}>{c}</li>)}
        </ul>
      </section>
    </div>
  );
}
