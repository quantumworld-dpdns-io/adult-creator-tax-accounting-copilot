import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import { registerTools } from './tools.js';
import { logger } from './logger.js';

export interface ServerOptions {
  transport: 'stdio' | 'sse' | 'streamable-http';
  port?: number;
}

export async function startServer(opts: ServerOptions): Promise<void> {
  const server = new Server(
    {
      name: 'adult-creator-tax-copilot',
      version: '0.1.0',
    },
    {
      capabilities: { tools: {} },
    },
  );

  registerTools(server);

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      {
        name: 'get_payouts',
        description: 'Fetch aggregated payouts for a creator.',
        inputSchema: {
          type: 'object',
          properties: {
            creator_id: { type: 'string' },
            start: { type: 'string' },
            end: { type: 'string' },
          },
          required: ['creator_id', 'start', 'end'],
        },
      },
      {
        name: 'compute_tax_estimate',
        description: 'Compute an estimated tax liability.',
        inputSchema: {
          type: 'object',
          properties: {
            creator_id: { type: 'string' },
            jurisdiction: { type: 'string' },
            year: { type: 'number' },
          },
          required: ['creator_id', 'jurisdiction', 'year'],
        },
      },
      {
        name: 'file_1099',
        description: 'Generate a 1099 PDF.',
        inputSchema: {
          type: 'object',
          properties: {
            creator_id: { type: 'string' },
            year: { type: 'number' },
            form: { type: 'string', enum: ['1099-NEC', '1099-MISC', '1099-K'] },
          },
          required: ['creator_id', 'year', 'form'],
        },
      },
      {
        name: 'verify_age_zk',
        description: 'ZK age proof.',
        inputSchema: {
          type: 'object',
          properties: {
            creator_id: { type: 'string' },
            min_age: { type: 'number' },
          },
          required: ['creator_id', 'min_age'],
        },
      },
    ],
  }));

  const Args = z.object({
    creator_id: z.string(),
  });
  const TaxArgs = Args.extend({
    jurisdiction: z.string(),
    year: z.number().int(),
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    logger.info({ tool: name, args }, 'tool call');
    switch (name) {
      case 'get_payouts':
        return { content: [{ type: 'text', text: JSON.stringify(stubPayouts(args)) }] };
      case 'compute_tax_estimate':
        TaxArgs.parse(args);
        return { content: [{ type: 'text', text: JSON.stringify(stubTax(args)) }] };
      case 'file_1099':
        return { content: [{ type: 'text', text: JSON.stringify(stub1099(args)) }] };
      case 'verify_age_zk':
        return { content: [{ type: 'text', text: JSON.stringify(stubAge(args)) }] };
      default:
        throw new Error(`unknown tool: ${name}`);
    }
  });

  if (opts.transport === 'stdio') {
    const transport = new StdioServerTransport();
    await server.connect(transport);
  } else if (opts.transport === 'sse') {
    const transport = new SSEServerTransport(`/messages`, undefined);
    await server.connect(transport);
    // SSE: typically use an HTTP framework. Simplified for the scaffold.
  } else {
    throw new Error(`transport not implemented in scaffold: ${opts.transport}`);
  }
}

function stubPayouts(args: unknown) {
  const a = args as { creator_id: string; start: string; end: string };
  return {
    creator_id: a.creator_id,
    start: a.start,
    end: a.end,
    currency: 'USD',
    gross: 12345.67,
    fees: 234.56,
    net: 12111.11,
  };
}

function stubTax(args: unknown) {
  const a = args as { creator_id: string; jurisdiction: string; year: number };
  return { ...a, estimated_tax_usd: 2456.78, effective_rate: 0.21, bracket: '22%' };
}

function stub1099(args: unknown) {
  const a = args as { creator_id: string; year: number; form: string };
  return { ...a, pdf_url: `s3://copilot-data/1099/${a.creator_id}/${a.year}/${a.form}.pdf`, signed: true, signature_algo: 'Dilithium-5' };
}

function stubAge(args: unknown) {
  const a = args as { creator_id: string; min_age: number };
  return { ...a, proof_system: 'noir', curve: 'bn254', expires_at: '2027-01-01T00:00:00Z' };
}
