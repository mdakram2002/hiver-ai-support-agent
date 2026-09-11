export const loggerOptions = {
  level: process.env.LOG_LEVEL ?? 'info',
  redact: ['req.headers.authorization', 'OPENAI_API_KEY'],
};
