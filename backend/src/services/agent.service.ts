import { embed } from '../ai/embeddings.js';
import { env } from '../config/env.js';
import type { Analysis, Evidence } from '../schemas/support.schema.js';
import { ClassifierService } from './classifier.service.js';
import { RetrieverService } from './retriever.service.js';
import { ResponderService } from './responder.service.js';
import { EscalationService } from './escalation.service.js';

export class AgentService {
  constructor(
    private classifier: ClassifierService,
    private retriever: RetrieverService,
    private responder: ResponderService,
    private escalation: EscalationService,
    private brand = env.SELECTED_BRAND,
  ) {}

  async analyze(message: string): Promise<Analysis> {
    const started = Date.now();
    if (!this.brand)
      return {
        intent: { name: 'unknown', confidence: 0, uncertain: true },
        reply: 'A brand must be selected after running the data pipeline.',
        escalation: {
          shouldEscalate: true,
          reason: 'SELECTED_BRAND is not configured.',
        },
        evidence: [],
        metadata: { retrievalCount: 0, latencyMs: Date.now() - started },
      };

    const intent = await this.classifier.classify(message);
    let evidence: Evidence[] = [];
    try {
      evidence = await this.retriever.retrieve(
        await embed(message),
        this.brand,
        intent.name,
        env.RETRIEVAL_K,
      );
    } catch {
      evidence = [];
    }

    const draft = await this.responder.draft(message, intent.name, evidence);
    const escalation = this.escalation.decide({
      confidence: intent.confidence,
      topSimilarity: evidence[0]?.similarity ?? 0,
      evidenceCount: evidence.length,
      grounded: draft.grounded,
      unsupportedClaims: draft.unsupportedClaims,
      intent: intent.name,
      message,
      evidenceIntents: evidence.map(e => e.intent).filter((intent): intent is string => Boolean(intent)),
    });

    return {
      intent,
      reply: draft.reply,
      escalation,
      evidence,
      metadata: {
        retrievalCount: evidence.length,
        latencyMs: Date.now() - started,
      },
    };
  }
}
