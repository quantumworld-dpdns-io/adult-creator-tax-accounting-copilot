/**
 * Dispatch a verified webhook to the ledger + payout-aggregator.
 * In production this is a Kafka producer.
 */

import { logger } from './logger.js';

export async function dispatch(platform: string, payload: unknown): Promise<void> {
  logger.info({ platform, has_payload: !!payload }, 'dispatched');
}
