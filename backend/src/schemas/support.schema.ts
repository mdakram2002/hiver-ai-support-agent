import { z } from 'zod';

export const analyzeRequestSchema = z.object({
  message: z.string().trim().min(2).max(2000),
});

export const intentSchema = z.object({
  name: z.string(),
  confidence: z.number().min(0).max(1),
  uncertain: z.boolean(),
});

export const evidenceSchema = z.object({
  conversationId: z.string(),
  similarity: z.number(),
  customerMessage: z.string(),
  agentResponse: z.string(),
  intent: z.string().optional(),
});

export const analysisSchema = z.object({
  intent: intentSchema,
  reply: z.string(),
  escalation: z.object({
    shouldEscalate: z.boolean(),
    reason: z.string().nullable(),
  }),
  evidence: z.array(evidenceSchema),
  metadata: z.object({ retrievalCount: z.number(), latencyMs: z.number() }),
});

export type AnalyzeRequest = z.infer<typeof analyzeRequestSchema>;
export type Analysis = z.infer<typeof analysisSchema>;
export type Evidence = z.infer<typeof evidenceSchema>;
