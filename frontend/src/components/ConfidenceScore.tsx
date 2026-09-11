export const ConfidenceScore = ({ value }: { value: number }) => (
  <div className="confidence">
    <span>Confidence</span>
    <strong>{Math.round(value * 100)}%</strong>
    <i>
      <b style={{ width: `${value * 100}%` }} />
    </i>
  </div>
);
