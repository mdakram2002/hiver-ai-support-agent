import { useState } from 'react';
import { useSupportAgent } from '../hooks/useSupportAgent';
import { MessageInput } from '../components/MessageInput';
import { ChatWindow } from '../components/ChatWindow';
import { AnalysisPanel } from '../components/AnalysisPanel';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';

export function Dashboard() {
  const [message, setMessage] = useState('');
  const agent = useSupportAgent();
  return (
    <main className="grid">
      <div>
        <ChatWindow message={message} data={agent.data} />
        <MessageInput
          loading={agent.isPending}
          onSubmit={(x) => {
            setMessage(x);
            agent.mutate(x);
          }}
        />
        {agent.isPending && <LoadingState />}
        {agent.error && <ErrorState message={agent.error.message} />}
      </div>
      {agent.data ? (
        <AnalysisPanel data={agent.data} />
      ) : (
        <aside>
          <h2>AI analysis</h2>
          <p className="muted">
            Enter a customer message to inspect the agent’s evidence and decision.
          </p>
        </aside>
      )}
    </main>
  );
}
