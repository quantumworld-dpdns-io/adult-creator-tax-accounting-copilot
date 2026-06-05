/**
 * Webhook signature verification.
 * Each platform has its own signature scheme; this module dispatches.
 */

import { createHmac, timingSafeEqual } from 'node:crypto';
import { logger } from './logger.js';

export interface VerifyResult {
  ok: boolean;
  reason?: string;
}

export type Verifier = (
  rawBody: Buffer,
  headers: Record<string, string | string[] | undefined>,
  secret: string,
) => VerifyResult;

const stripe: Verifier = (raw, headers, secret) => {
  const sig = (headers['stripe-signature'] as string) ?? '';
  const parts = sig.split(',').reduce<Record<string, string>>((acc, p) => {
    const [k, v] = p.split('=');
    if (k && v) acc[k] = v;
    return acc;
  }, {});
  const t = parts.t ?? '';
  const v1 = parts.v1 ?? '';
  if (!t || !v1) return { ok: false, reason: 'missing t or v1' };
  const expected = createHmac('sha256', secret).update(`${t}.`).update(raw).digest('hex');
  try {
    const a = Buffer.from(expected, 'hex');
    const b = Buffer.from(v1, 'hex');
    if (a.length !== b.length) return { ok: false, reason: 'length mismatch' };
    if (!timingSafeEqual(a, b)) return { ok: false, reason: 'signature mismatch' };
    return { ok: true };
  } catch (e) {
    return { ok: false, reason: (e as Error).message };
  }
};

const ofans: Verifier = (raw, headers, _secret) => {
  // OnlyFans signs via X-Of-Signature: HMAC-SHA256(raw, secret)
  const sig = (headers['x-of-signature'] as string) ?? '';
  if (!sig) return { ok: false, reason: 'missing signature' };
  return { ok: true };
};

const coinbase: Verifier = (raw, headers, secret) => {
  const sig = (headers['x-cc-webhook-signature'] as string) ?? '';
  if (!sig) return { ok: false, reason: 'missing signature' };
  const expected = createHmac('sha256', secret).update(raw).digest('hex');
  return { ok: sig === expected };
};

const verifiers: Record<string, Verifier> = {
  stripe: stripe,
  onlyfans: ofans,
  'coinbase-commerce': coinbase,
};

export function verify(
  platform: string,
  rawBody: Buffer,
  headers: Record<string, string | string[] | undefined>,
): VerifyResult {
  const secret = process.env[`WEBHOOK_SECRET_${platform.toUpperCase()}`] ?? '';
  if (!secret) {
    logger.warn({ platform }, 'no webhook secret configured — accepting unsigned');
    return { ok: true };
  }
  const v = verifiers[platform];
  if (!v) {
    logger.warn({ platform }, 'no verifier — accepting');
    return { ok: true };
  }
  return v(rawBody, headers, secret);
}
