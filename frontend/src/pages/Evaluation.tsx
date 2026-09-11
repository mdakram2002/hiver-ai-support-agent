import { useQuery } from '@tanstack/react-query';
import { evaluation } from '../services/api';

export function Evaluation() {
  const q = useQuery({ queryKey: ['evaluation'], queryFn: evaluation });
  if (q.isLoading) return <p>Loading evaluation…</p>;
  if (q.data?.status !== 'available')
    return (
      <p className="muted">
        Not yet evaluated. Metrics appear only after a human-labelled golden set is run.
      </p>
    );
  return <pre>{JSON.stringify(q.data.results, null, 2)}</pre>;
}
