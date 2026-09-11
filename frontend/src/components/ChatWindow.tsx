import type { Analysis } from '../types/support';
export const ChatWindow = ({ message, data }: { message: string; data?: Analysis }) => (
  <section className="chat">
    <h2>Conversation</h2>
    {message && <p className="customer">{message}</p>}
    {data && <p className="agent">{data.reply}</p>}
  </section>
);
