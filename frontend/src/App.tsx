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
    <>
      <header className="app-header">
        <h1>VC Audit Tool</h1>
        <span className="header-divider" />
        <span className="header-tagline">Comparable Company Analysis</span>
      </header>

      <main className="app-main">
        <ValuationForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
          </div>
        )}

        {report && <ValuationReport report={report} />}
      </main>
    </>
  );
}
