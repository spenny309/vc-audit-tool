import { useState } from 'react';
import { ValuationForm } from './components/ValuationForm';
import { ValuationReport } from './components/ValuationReport';
import { valuate } from './api/client';
import type { ValuationRequest, ValuationReport as ReportData } from './api/client';

export default function App() {
  const [report, setReport] = useState<ReportData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(request: ValuationRequest) {
    setIsLoading(true);
    setError(null);
    setReport(null);

    try {
      const result = await valuate(request);
      setReport(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      <h1>VC Audit Tool</h1>
      <p>Estimate the fair value of private portfolio companies using Comparable Company Analysis.</p>

      <ValuationForm onSubmit={handleSubmit} isLoading={isLoading} />

      {error && (
        <div style={{ color: 'red', marginTop: '1rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {report && <ValuationReport report={report} />}
    </main>
  );
}
