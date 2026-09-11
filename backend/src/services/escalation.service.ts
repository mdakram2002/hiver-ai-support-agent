import { env } from '../config/env.js';

export type EscalationInput = {
  confidence: number;
  topSimilarity: number;
  evidenceCount: number;
  grounded: boolean;
  unsupportedClaims: string[];
  intent: string;
  message: string;
};

export class EscalationService {
  constructor(
    private readonly riskyIntents = new Set<string>(['account_security', 'fraud', 'legal']),
  ) {}
  decide(input: EscalationInput) {
    if (input.confidence < env.CONFIDENCE_THRESHOLD)
      return {
        shouldEscalate: true,
        reason: 'Intent classification is uncertain.',
      };
    if (!input.evidenceCount || input.topSimilarity < env.SIMILARITY_THRESHOLD)
      return {
        shouldEscalate: true,
        reason: 'Insufficient historical evidence for a confident response.',
      };
    if (!input.grounded || input.unsupportedClaims.length)
      return {
        shouldEscalate: true,
        reason: 'The draft cannot be verified against historical evidence.',
      };
    if (this.riskyIntents.has(input.intent))
      return {
        shouldEscalate: true,
        reason: 'This intent requires human review.',
      };
    return { shouldEscalate: false, reason: null };
  }
}
