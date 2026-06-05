// Pulumi program: Zeabur (TW)
//
// Provisions: project, services for each polyglot microservice.

import * as pulumi from "@pulumi/pulumi";
import * as zeabur from "@pulumi/zeabur";

const stack = pulumi.getStack();

const project = new zeabur.Project(`copilot-${stack}`, {
  name: `copilot-${stack}`,
  region: "tw-1",
});

const services = [
  { name: "api-gateway",     image: "ghcr.io/quantumworld-dpdns-io/api-gateway",     port: 8080 },
  { name: "tax-engine",      image: "ghcr.io/quantumworld-dpdns-io/tax-engine",      port: 8000 },
  { name: "ledger",          image: "ghcr.io/quantumworld-dpdns-io/ledger",          port: 50051 },
  { name: "payout-aggregator", image: "ghcr.io/quantumworld-dpdns-io/payout-aggregator", port: 8080 },
  { name: "crypto-tax",      image: "ghcr.io/quantumworld-dpdns-io/crypto-tax",      port: 8080 },
  { name: "realtime-pricing", image: "ghcr.io/quantumworld-dpdns-io/realtime-pricing", port: 8080 },
  { name: "mcp-server",      image: "ghcr.io/quantumworld-dpdns-io/mcp-server",      port: 9000 },
];

const created = services.map((s) => new zeabur.Service(`${stack}-${s.name}`, {
  projectID: project.id,
  name: s.name,
  image: s.image,
  port: s.port,
  healthCheck: { path: "/healthz" },
  env: {
    NODE_ENV: stack,
  },
}));

export const projectId = project.id;
export const serviceNames = created.map((s) => s.name);
