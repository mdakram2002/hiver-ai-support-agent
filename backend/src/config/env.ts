import dotenv from 'dotenv';
import { fileURLToPath } from 'node:url';
import { z } from 'zod';

dotenv.config({ path: fileURLToPath(new URL('../../../.env', import.meta.url)) });

const schema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().positive().default(3001),
  DATABASE_URL: z.string().default('postgresql://postgres:postgres@127.0.0.1:55432/hiver'),
  OPENAI_API_KEY: z.string().optional(),
  OPENAI_MODEL: z.string().default('gpt-4o-mini'),
  SELECTED_BRAND: z.string().optional(),
  RETRIEVAL_K: z.coerce.number().int().min(1).max(10).default(5),
  CONFIDENCE_THRESHOLD: z.coerce.number().min(0).max(1).default(0.7),
  SIMILARITY_THRESHOLD: z.coerce.number().min(0).max(1).default(0.72),
});
export const env = schema.parse(process.env);
