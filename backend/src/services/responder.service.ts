import type { Llm } from '../ai/llm.js';
import type { Evidence } from '../schemas/support.schema.js';
import { responderPrompt } from '../ai/prompts.js';

export type Draft = {
  reply: string;
  grounded: boolean;
  unsupportedClaims: string[];
};

export class ResponderService {
  constructor(private llm: Llm | null) {}
  async draft(message: string, intent: string, evidence: Evidence[]): Promise<Draft> {
    if (!this.llm || !evidence.length)
      return {
        reply: 'Thanks for reaching out. A support teammate will review this and get back to you.',
        grounded: false,
        unsupportedClaims: [],
      };
    try {
      const data = await this.llm.json<Draft>(
        responderPrompt,
        JSON.stringify({ customerMessage: message, intent, evidence }),
      );
      if (!data.reply || !Array.isArray(data.unsupportedClaims))
        throw new Error('invalid LLM response');
      return {
        reply: data.reply,
        grounded: data.grounded === true,
        unsupportedClaims: data.unsupportedClaims,
      };
    } catch {
      return {
        reply: 'Thanks for reaching out. A support teammate will review this and get back to you.',
        grounded: false,
        unsupportedClaims: [],
      };
    }
  }
}
