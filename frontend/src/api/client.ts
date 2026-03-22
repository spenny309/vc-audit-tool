export type ModelType = "Comps" | "DCF" | "Last Round";

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

export interface CompsDetails {
  mean_revenue_multiple: number;
  comps_used: CompData[];
}

export interface DcfDetails {
  dcf_cashflows: DcfYearData[];
  terminal_value_mm: number;
  ebitda_margin_pct: number;
  discount_rate: number;
  terminal_growth_rate: number;
}

export interface LastRoundDetails {
  last_post_money_valuation_mm: number;
  last_round_date: string;
  index_name: string;
  index_value_at_round: number;
  index_value_today: number;
  index_pct_change: number;
}

export interface CompsRequest {
  model: 'Comps';
  company_name: string;
  sector: string;
  revenue_mm: number;
}

export interface DcfRequest {
  model: 'DCF';
  company_name: string;
  projections: number[];
  ebitda_margin_pct: number;
  discount_rate: number;
  terminal_growth_rate: number;
}

export interface LastRoundRequest {
  model: 'Last Round';
  company_name: string;
  last_post_money_valuation_mm: number;
  last_round_date: string;
  index?: string;
}

export type ValuationRequest = CompsRequest | DcfRequest | LastRoundRequest;

export interface ValuationReport {
  company_name: string;
  methodology: string;
  fair_value_mm: number;
  assumptions: string[];
  citations: string[];
  explanation: string;
  comps_details?: CompsDetails;
  dcf_details?: DcfDetails;
  last_round_details?: LastRoundDetails;
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

export async function getIndices(): Promise<string[]> {
  const response = await fetch('/api/indices');
  if (!response.ok) throw new Error('Failed to fetch indices');
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
