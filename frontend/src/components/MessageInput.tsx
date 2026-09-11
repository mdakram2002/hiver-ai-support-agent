import { useState } from 'react';

export function MessageInput({
  onSubmit,
  loading,
}: {
  onSubmit: (s: string) => void;
  loading: boolean;
}) {
  const [message, setMessage] = useState('');
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (message.trim()) onSubmit(message);
      }}
    >
      <label htmlFor="message">Customer message</label>
      <textarea
        id="message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Describe the customer issue…"
        maxLength={2000}
      />
      <button disabled={loading || !message.trim()}>
        {loading ? 'Analyzing…' : 'Analyze message'}
      </button>
    </form>
  );
}
