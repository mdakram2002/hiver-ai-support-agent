import OpenAI from 'openai';
import { env } from '../config/env.js';

export async function embed(text: string): Promise<number[]> {
  if (!env.OPENAI_API_KEY) throw new Error('OPENAI_API_KEY is required for embeddings');
  const client = new OpenAI({ apiKey: env.OPENAI_API_KEY, timeout: 12_000 });
  const r = await client.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  return r.data[0].embedding;
}
