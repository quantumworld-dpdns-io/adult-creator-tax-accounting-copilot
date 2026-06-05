// Pulumi program: Northflank (EU)
//
// Provisions: project, services, addons (Postgres, Redis, S3, vector DB).

import * as pulumi from "@pulumi/pulumi";
import * as northflank from "@pulumi/northflank";

const stack = pulumi.getStack();

const project = new northflank.Project(`copilot-${stack}`, {
  name: `copilot-${stack}`,
  region: "eu-west-1",
});

const postgres = new northflank.Addon(`${stack}-postgres`, {
  projectId: project.id,
  type: "postgres",
  version: "16",
  plan: "nf-compute-100",
});

const redis = new northflank.Addon(`${stack}-redis`, {
  projectId: project.id,
  type: "redis",
  version: "7",
  plan: "nf-compute-100",
});

const objectstore = new northflank.Addon(`${stack}-objectstore`, {
  projectId: project.id,
  type: "object-storage",
  plan: "nf-storage-100",
});

const services = ["api-gateway", "tax-engine", "ledger", "payout-aggregator", "crypto-tax", "realtime-pricing", "mcp-server"];

const created = services.map((s) => new northflank.Service(`${stack}-${s}`, {
  projectId: project.id,
  name: s,
  deployment: {
    type: "image",
    image: `ghcr.io/quantumworld-dpdns-io/${s}:latest`,
    port: 8080,
  },
}));

export const projectId = project.id;
export const serviceCount = created.length;
