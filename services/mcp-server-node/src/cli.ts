#!/usr/bin/env node
import { startServer } from './server.js';

const transport = process.env.MCP_TRANSPORT ?? 'stdio';
const port = Number(process.env.MCP_PORT ?? 8000);

startServer({ transport, port }).catch((err) => {
  console.error('mcp-server-node failed:', err);
  process.exit(1);
});
