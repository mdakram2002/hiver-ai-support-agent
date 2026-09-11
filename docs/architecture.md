# Architecture

The frontend calls Fastify's `/api/v1/support/analyze`. `AgentService` orchestrates a structured LLM classifier, pgvector retrieval, evidence-constrained response draft, and deterministic escalation policy. Offline Python scripts clean a bounded input, reconstruct threads, require human taxonomy/pair review, and create embeddings. The API never processes raw tweets.

`resolution_examples` contains only reviewed historical pairs; the golden set is excluded from both training and retrieval. If an embedding, database call, classification, or evidence check fails, the agent returns a safe escalation rather than a fabricated answer.
