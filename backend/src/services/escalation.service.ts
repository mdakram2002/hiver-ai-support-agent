import { env } from '../config/env.js';

export type EscalationInput = {
  confidence: number;
  topSimilarity: number;
  evidenceCount: number;
  grounded: boolean;
  unsupportedClaims: string[];
  intent: string;
  message: string;
  evidenceIntents: string[]; // Intents of retrieved evidence
};

export class EscalationService {
  constructor(
    private readonly riskyIntents = new Set<string>(['account_security', 'fraud', 'legal', 'payment_issue']),
  ) {}
  
  private isAmbiguousMessage(message: string): boolean {
    const ambiguousPatterns = [
      'can you check',
      'what happened',
      'please check',
      'what is going on',
      'help me',
      'i need help',
      'can you help',
      'what is this',
      'why',
      'how'
    ];
    
    const lowerMessage = message.toLowerCase().trim();
    // Very short messages are often ambiguous
    if (lowerMessage.length < 15) return true;
    
    // Check for ambiguous patterns
    return ambiguousPatterns.some(pattern => lowerMessage.includes(pattern));
  }
  
  private checkIntentEvidenceAlignment(intent: string, evidenceIntents: string[]): boolean {
    if (evidenceIntents.length === 0) return false;
    
    // For specific intents, we want evidence to match
    if (intent !== 'unknown' && intent !== 'general_inquiry') {
      const matchingEvidence = evidenceIntents.filter(e => e === intent);
      // At least 50% of evidence should match the predicted intent
      return matchingEvidence.length / evidenceIntents.length >= 0.5;
    }
    
    return true; // For general intents, alignment is less critical
  }
  
  decide(input: EscalationInput) {
    // Check for ambiguous messages first
    if (this.isAmbiguousMessage(input.message)) {
      return {
        shouldEscalate: true,
        reason: 'Message is ambiguous and requires clarification.',
      };
    }
    
    // Check intent confidence
    if (input.confidence < env.CONFIDENCE_THRESHOLD)
      return {
        shouldEscalate: true,
        reason: 'Intent classification is uncertain.',
      };
    
    // Check evidence quality with higher threshold
    const EVIDENCE_THRESHOLD = 0.78; // More conservative than default
    if (!input.evidenceCount || input.topSimilarity < EVIDENCE_THRESHOLD)
      return {
        shouldEscalate: true,
        reason: 'Insufficient high-quality historical evidence for a confident response.',
      };
    
    // Check intent-evidence alignment
    if (!this.checkIntentEvidenceAlignment(input.intent, input.evidenceIntents)) {
      return {
        shouldEscalate: true,
        reason: 'Retrieved evidence does not align with the predicted intent.',
      };
    }
    
    // Check grounding
    if (!input.grounded || input.unsupportedClaims.length)
      return {
        shouldEscalate: true,
        reason: 'The draft cannot be verified against historical evidence.',
      };
    
    // Check for risky intents that require human review
    if (this.riskyIntents.has(input.intent))
      return {
        shouldEscalate: true,
        reason: 'This intent requires human review due to security/payment sensitivity.',
      };
    
    return { shouldEscalate: false, reason: null };
  }
}
