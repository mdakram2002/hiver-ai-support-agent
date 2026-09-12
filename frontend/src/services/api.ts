import type { Analysis } from '../types/support';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function analyze(message: string): Promise<Analysis> {
  const r = await fetch(`${API_BASE_URL}/api/v1/support/analyze`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!r.ok) throw new Error((await r.json().catch(() => null))?.message ?? 'Analysis failed');
  return r.json();
}

export async function evaluation() {
  const r = await fetch(`${API_BASE_URL}/api/v1/evaluation/results`);
  return r.json();
}
