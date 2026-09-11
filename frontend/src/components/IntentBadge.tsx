export const IntentBadge = ({ name }: { name: string }) => (
  <span className="badge">{name.split('_').join(' ')}</span>
);
