import type { Evidence } from '../schemas/support.schema.js';
import { pool } from '../db/client.js';
import { env } from '../config/env.js';

const MIN_SIMILARITY_THRESHOLD = 0.75; // Higher threshold for evidence quality
const INTENT_ALIGNMENT_BONUS = 0.1; // Bonus for matching intent

export class RetrieverService {
  async retrieve(
    embedding: number[],
    brand: string,
    intent: string,
    limit: number,
  ): Promise<Evidence[]> {
    const vector = `[${embedding.join(',')}]`;
    const r = await pool.query(
      `SELECT conversation_id, customer_message, agent_response, intent, 1 - (embedding <=> $1::vector) AS similarity FROM resolution_examples WHERE brand = $2 AND embedding IS NOT NULL ORDER BY CASE WHEN intent = $3 THEN 0 ELSE 1 END, embedding <=> $1::vector LIMIT $4 * 3`, // Fetch more candidates for filtering
      [vector, brand, intent, limit],
    );
    
    // Filter evidence by quality and alignment
    const filteredEvidence = r.rows
      .map((x) => ({
        conversationId: x.conversation_id,
        customerMessage: x.customer_message,
        agentResponse: x.agent_response,
        intent: x.intent,
        similarity: Number(x.similarity),
      }))
      .filter((evidence) => {
        // Must meet minimum similarity threshold
        if (evidence.similarity < MIN_SIMILARITY_THRESHOLD) {
          return false;
        }
        
        // If intent is not 'unknown' and not 'general_inquiry', prefer matching intent
        if (intent !== 'unknown' && intent !== 'general_inquiry') {
          // For specific intents, evidence should either match or be very high similarity
          if (evidence.intent !== intent && evidence.similarity < 0.85) {
            return false;
          }
        }
        
        return true;
      })
      .slice(0, limit); // Return only up to requested limit
    
    // If no evidence meets quality threshold, return empty array
    if (filteredEvidence.length === 0) {
      return [];
    }
    
    return filteredEvidence;
  }
}
