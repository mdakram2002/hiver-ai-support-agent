import OpenAI from 'openai';
import { env } from '../config/env.js';
export type Llm = { json<T>(system: string, user: string): Promise<T> };

export function createLlm(): Llm | null {
  if (!env.OPENAI_API_KEY) return null;
  const client = new OpenAI({ apiKey: env.OPENAI_API_KEY, timeout: 12_000 });
  return {
    async json<T>(system: string, user: string) {
      const result = await client.chat.completions.create({
        model: env.OPENAI_MODEL,
        temperature: 0,
        response_format: { type: 'json_object' },
        messages: [
          { role: 'system', content: system },
          { role: 'user', content: user },
        ],
      });
      return JSON.parse(result.choices[0]?.message.content ?? '{}') as T;
    },
  };
}
