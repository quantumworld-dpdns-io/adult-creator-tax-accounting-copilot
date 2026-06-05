import type { Server } from '@modelcontextprotocol/sdk/server/index.js';

export function registerTools(_server: Server): void {
  // Tool handlers live in server.ts. This module exists for future
  // discovery/registration extensions (e.g. dynamic tool loading from
  // .skills/, hot-reload, etc.).
}
