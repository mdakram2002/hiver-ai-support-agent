import type { FastifyInstance } from 'fastify';
import { pool } from '../db/client.js';

export async function healthRoutes(app: FastifyInstance) {
  app.get('/health', async () => {
    try {
      await pool.query('SELECT 1');
      return { status: 'ok', database: 'ok' };
    } catch {
      return { status: 'degraded', database: 'unavailable' };
    }
  });
}
