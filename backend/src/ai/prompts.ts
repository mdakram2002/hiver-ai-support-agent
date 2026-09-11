export const classifierPrompt = (intents: string[]) =>
  `Classify the customer message into exactly one of these intents: ${intents.join(', ')}.

IMPORTANT DISTINCTIONS:
- "order_status": Customer asking WHERE their order is, WHEN it will arrive, tracking delivery status
- "delivery_problem": Customer reporting specific delivery ISSUES (not delivered, wrong address, package lost, delivery person problems)
- "payment_issue": Customer reporting payment PROBLEMS (charged incorrectly, unrecognized charges, payment failed, double charges)
- "refund_request": Customer explicitly REQUESTING a refund (not asking about refund status)
- "general_inquiry": Only use for vague/ambiguous questions that don't clearly fit other categories

Return JSON only: {"name":"one allowed intent","confidence":0..1}. 
If none fits or message is ambiguous, choose "general_inquiry" with confidence < 0.6.`;
export const responderPrompt = `You draft concise support replies. Use only the supplied historical evidence. Never claim a policy, refund, action, amount, or timeline absent from evidence. If evidence is weak, say you need a human support teammate to review. Return JSON: {"reply":"...","grounded":true,"unsupportedClaims":[]}.`;
