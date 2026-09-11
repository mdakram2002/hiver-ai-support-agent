import type { FastifyReply, FastifyRequest } from 'fastify';
import { analyzeRequestSchema } from '../schemas/support.schema.js';
import { AgentService } from '../services/agent.service.js';

export const analyze =
  (agent: AgentService) => async (request: FastifyRequest, reply: FastifyReply) => {
    const parsed = analyzeRequestSchema.safeParse(request.body);
    if (!parsed.success)
      return reply.code(400).send({
        error: 'INVALID_REQUEST',
        message: parsed.error.issues[0]?.message,
      });
    return reply.send(await agent.analyze(parsed.data.message));
  };
