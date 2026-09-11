export const classifierPrompt = (intents: string[]) =>
  `Classify the customer message into exactly one of: ${intents.join(', ')}.
    Return JSON only: {"name":"one allowed intent","confidence":0..1}. If none fits choose unknown with low confidence.`;
export const responderPrompt = `You draft concise support replies. Use only the supplied historical evidence. Never claim a policy, refund, action, amount, or timeline absent from evidence. If evidence is weak, say you need a human support teammate to review. Return JSON: {"reply":"...","grounded":true,"unsupportedClaims":[]}.`;
