export function EscalationCard({
  escalation,
}: {
  escalation: { shouldEscalate: boolean; reason: string | null };
}) {
  return (
    <section className={escalation.shouldEscalate ? 'decision escalate' : 'decision'}>
      <b>{escalation.shouldEscalate ? 'Escalate to human' : 'Auto-handle'}</b>
      <p>{escalation.reason ?? 'High confidence and sufficiently grounded historical evidence.'}</p>
    </section>
  );
}
