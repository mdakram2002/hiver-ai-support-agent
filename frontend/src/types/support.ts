export type Analysis = {
  intent: { name: string; confidence: number; uncertain: boolean };
  reply: string;
  escalation: { shouldEscalate: boolean; reason: string | null };
  evidence: {
    conversationId: string;
    similarity: number;
    customerMessage: string;
    agentResponse: string;
    intent?: string;
  }[];
  metadata: { retrievalCount: number; latencyMs: number };
};
