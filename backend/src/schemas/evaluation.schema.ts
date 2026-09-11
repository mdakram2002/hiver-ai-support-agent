import { z } from 'zod';

export const evaluationResultsSchema = z.object({
  status: z.enum(['available', 'not_evaluated']),
  results: z.record(z.unknown()).nullable(),
  generatedAt: z.string().nullable(),
});
