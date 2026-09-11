import Fastify from 'fastify';
import cors from '@fastify/cors';
import { env } from './config/env.js';
import { pool } from './db/client.js';
import { loggerOptions } from './utils/logger.js';
import { createLlm } from './ai/llm.js';
import { ClassifierService } from './services/classifier.service.js';
import { RetrieverService } from './services/retriever.service.js';
import { ResponderService } from './services/responder.service.js';
import { EscalationService } from './services/escalation.service.js';
import { AgentService } from './services/agent.service.js';
import { supportRoutes } from './routes/support.routes.js';
import { healthRoutes } from './routes/health.routes.js';
import { evaluationRoutes } from './routes/evaluation.routes.js';

const app = Fastify({ logger: loggerOptions, bodyLimit: 16_384 });
await app.register(cors, { origin: true });
const llm = createLlm();
const intents = await loadIntents();

const agent = new AgentService(
  new ClassifierService(intents, llm),
  new RetrieverService(),
  new ResponderService(llm),
  new EscalationService(),
);

await app.register(healthRoutes);
await app.register(
  async (api) => {
    await api.register((i) => supportRoutes(i, agent), { prefix: '/support' });
    await api.register(evaluationRoutes, { prefix: '/evaluation' });
  },
  { prefix: '/api/v1' },
);
await app.listen({ port: env.PORT, host: '0.0.0.0' });

async function loadIntents(): Promise<string[]> {
  if (!env.SELECTED_BRAND) return [];

  try {
    const { rows } = await pool.query<{ intent: string }>(
      `SELECT DISTINCT intent
       FROM resolution_examples
       WHERE brand = $1 AND intent <> 'UNLABELLED'
       ORDER BY intent`,
      [env.SELECTED_BRAND],
    );
    return rows.map(({ intent }) => intent);
  } catch (error) {
    app.log.warn({ error }, 'Unable to load reviewed intents; requests will safely escalate');
    return [];
  }
}
