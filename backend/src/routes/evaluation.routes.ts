import type { FastifyInstance } from 'fastify';
import { evaluationResults } from '../controllers/evaluation.controller.js';
export async function evaluationRoutes(app: FastifyInstance) {
  app.get('/results', evaluationResults);
}
