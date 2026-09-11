import type { Analysis } from '../types/support';

export async function analyze(message: string): Promise<Analysis> {
  const r = await fetch('/api/v1/support/analyze', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!r.ok) throw new Error((await r.json().catch(() => null))?.message ?? 'Analysis failed');
  return r.json();
}

export async function evaluation() {
  const r = await fetch('/api/v1/evaluation/results');
  return r.json();
}
