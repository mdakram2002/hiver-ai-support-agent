import type { Analysis } from '../types/support';
import { IntentBadge } from './IntentBadge';
import { ConfidenceScore } from './ConfidenceScore';
import { EscalationCard } from './EscalationCard';
import { EvidencePanel } from './EvidencePanel';

export function AnalysisPanel({ data }: { data: Analysis }) {
  return (
    <aside>
      <h2>AI analysis</h2>
      <IntentBadge name={data.intent.name} />
      <ConfidenceScore value={data.intent.confidence} />
      <EscalationCard escalation={data.escalation} />
      <section>
        <h3>Draft reply</h3>
        <p>{data.reply}</p>
      </section>
      <EvidencePanel evidence={data.evidence} />
    </aside>
  );
}
