/**
 * Webhook entry point (Express + NestJS-style).
 * Endpoints:
 *   POST /v1/webhooks/:platform
 */

import express from 'express';
import { verify } from './verify.js';
import { logger } from './logger.js';
import { dispatch } from './dispatch.js';

const app = express();
app.use(express.raw({ type: '*/*', limit: '5mb' }));

const platforms = ['onlyfans', 'fansly', 'chaturbate', 'stripe', 'coinbase-commerce', 'nowpayments', 'stripchat', 'manyvids'];

for (const p of platforms) {
  app.post(`/v1/webhooks/${p}`, async (req, res) => {
    const result = verify(p, req.body as Buffer, req.headers as Record<string, string | string[] | undefined>);
    if (!result.ok) {
      logger.warn({ platform: p, reason: result.reason }, 'webhook rejected');
      res.status(401).json({ error: 'invalid signature', reason: result.reason });
      return;
    }
    const parsed = JSON.parse((req.body as Buffer).toString('utf-8') || '{}');
    try {
      await dispatch(p, parsed);
      res.status(202).json({ ok: true });
    } catch (e) {
      logger.error({ err: (e as Error).message, platform: p }, 'webhook dispatch failed');
      res.status(500).json({ error: 'dispatch failed' });
    }
  });
}

app.get('/healthz', (_req, res) => {
  res.status(200).json({ status: 'ok' });
});

const port = Number(process.env.PORT ?? 8081);
app.listen(port, () => logger.info({ port }, 'webhook-router listening'));
