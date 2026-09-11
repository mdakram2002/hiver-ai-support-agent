import { pool } from './client.js';
import { schemaSql } from './schema.js';
await pool.query(schemaSql);
console.log('Database schema ready.');
await pool.end();
