import type { FastifyInstance } from 'fastify';
import { analyze } from '../controllers/support.controller.js';
import type { AgentService } from '../services/agent.service.js';

export async function supportRoutes(app: FastifyInstance, agent: AgentService) {
  app.post('/analyze', { config: { rawBody: false } }, analyze(agent));
}
