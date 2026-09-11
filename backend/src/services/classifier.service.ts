import type { Llm } from '../ai/llm.js';
import { classifierPrompt } from '../ai/prompts.js';

export type Classification = {
  name: string;
  confidence: number;
  uncertain: boolean;
};

export class ClassifierService {
  constructor(
    private intents: string[],
    private llm: Llm | null,
  ) {}
  async classify(message: string): Promise<Classification> {
    if (!this.intents.length) return { name: 'unknown', confidence: 0, uncertain: true };
    if (!this.llm) return { name: 'unknown', confidence: 0, uncertain: true };
    try {
      const r = await this.llm.json<{ name: string; confidence: number }>(
        classifierPrompt([...this.intents, 'unknown']),
        message,
      );
      const name = this.intents.includes(r.name) ? r.name : 'unknown';
      const confidence = Number.isFinite(r.confidence) ? Math.min(1, Math.max(0, r.confidence)) : 0;
      return {
        name,
        confidence,
        uncertain: name === 'unknown' || confidence < 0.7,
      };
    } catch {
      return { name: 'unknown', confidence: 0, uncertain: true };
    }
  }
}
