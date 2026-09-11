import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

export async function evaluationResults() {
  try {
    const raw = await readFile(
      resolve(process.cwd(), '../reports/evaluation_results.json'),
      'utf8',
    );
    return {
      status: 'available',
      results: JSON.parse(raw),
      generatedAt: new Date().toISOString(),
    };
  } catch {
    return { status: 'not_evaluated', results: null, generatedAt: null };
  }
}
