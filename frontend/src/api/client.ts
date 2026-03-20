export interface ValuationRequest {
  company_name: string;
  sector: string;
  revenue_mm: number;
}

export interface CompData {
  name: string;
  enterprise_value_mm: number;
  revenue_mm: number;
  revenue_multiple: number;
}

export interface ValuationReport {
  company_name: string;
  methodology: string;
  fair_value_mm: number;
  mean_revenue_multiple: number;
  comps_used: CompData[];
  assumptions: string[];
  citations: string[];
  explanation: string;
}

export interface ApiError {
  error: string;
  message: string;
  status: number;
}

export async function getSectors(): Promise<string[]> {
  const response = await fetch('/api/sectors');
  if (!response.ok) throw new Error('Failed to fetch sectors');
  return response.json();
}

export async function valuate(request: ValuationRequest): Promise<ValuationReport> {
  const response = await fetch('/api/valuate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.message || 'Valuation failed');
  }

  return response.json();
}
