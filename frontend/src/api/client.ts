export type ModelType = "Comps" | "DCF";

export interface CompData {
  name: string;
  enterprise_value_mm: number;
  revenue_mm: number;
  revenue_multiple: number;
}

export interface DcfYearData {
  year: number;
  revenue_mm: number;
  fcf_mm: number;
  discounted_fcf_mm: number;
}

export interface ValuationRequest {
  company_name: string;
  model: ModelType;
  // Comps
  sector?: string;
  revenue_mm?: number;
  // DCF
  projections?: number[];
  ebitda_margin_pct?: number;
  discount_rate?: number;
  terminal_growth_rate?: number;
}

export interface ValuationReport {
  company_name: string;
  methodology: string;
  fair_value_mm: number;
  assumptions: string[];
  citations: string[];
  explanation: string;
  // Comps-specific
  mean_revenue_multiple?: number;
  comps_used?: CompData[];
  // DCF-specific
  dcf_cashflows?: DcfYearData[];
  terminal_value_mm?: number;
  ebitda_margin_pct?: number;
  discount_rate?: number;
  terminal_growth_rate?: number;
}

export interface ApiError {
  error: string;
  message: string;
  status: number;
}

export async function getModels(): Promise<string[]> {
  const response = await fetch('/api/models');
  if (!response.ok) throw new Error('Failed to fetch models');
  return response.json();
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
