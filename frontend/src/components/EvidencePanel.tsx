import type { Analysis } from '../types/support';
export function EvidencePanel({ evidence }: { evidence: Analysis['evidence'] }) {
  return (
    <section>
      <h3>Historical evidence</h3>
      {evidence.length ? (
        evidence.map((e) => (
          <article className="evidence" key={e.conversationId}>
            <small>{Math.round(e.similarity * 100)}% similar</small>
            <p>
              <b>Customer:</b> {e.customerMessage}
            </p>
            <p>
              <b>Historical reply:</b> {e.agentResponse}
            </p>
          </article>
        ))
      ) : (
        <p className="muted">No usable historical evidence was found.</p>
      )}
    </section>
  );
}
