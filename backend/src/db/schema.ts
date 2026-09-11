export const schemaSql = `CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS resolution_examples (id bigserial PRIMARY KEY, conversation_id text NOT NULL, brand text NOT NULL, customer_message text NOT NULL, agent_response text NOT NULL, intent text NOT NULL, metadata jsonb NOT NULL DEFAULT '{}', embedding vector(1536), created_at timestamptz NOT NULL DEFAULT now());
CREATE INDEX IF NOT EXISTS resolution_examples_brand_intent_idx ON resolution_examples (brand, intent);
CREATE INDEX IF NOT EXISTS resolution_examples_embedding_idx ON resolution_examples USING hnsw (embedding vector_cosine_ops);`;
