import type { Evidence } from '../schemas/support.schema.js';
import { pool } from '../db/client.js';

export class RetrieverService {
  async retrieve(
    embedding: number[],
    brand: string,
    intent: string,
    limit: number,
  ): Promise<Evidence[]> {
    const vector = `[${embedding.join(',')}]`;
    const r = await pool.query(
      `SELECT conversation_id, customer_message, agent_response, intent, 1 - (embedding <=> $1::vector) AS similarity FROM resolution_examples WHERE brand = $2 AND embedding IS NOT NULL ORDER BY CASE WHEN intent = $3 THEN 0 ELSE 1 END, embedding <=> $1::vector LIMIT $4`,
      [vector, brand, intent, limit],
    );
    return r.rows.map((x) => ({
      conversationId: x.conversation_id,
      customerMessage: x.customer_message,
      agentResponse: x.agent_response,
      intent: x.intent,
      similarity: Number(x.similarity),
    }));
  }
}
