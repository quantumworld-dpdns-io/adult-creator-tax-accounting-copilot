# ADR 0004: Multi-Cloud Release Matrix

## Status

Accepted.

## Context

We must avoid vendor lock-in while leveraging the strengths of each regional
PaaS (data residency, latency, cost).

## Decision

We deploy the same Helm chart + container images to four providers:

| Provider | Region(s) | Primary Use |
| -------- | --------- | ----------- |
| Zeabur   | TW, SG, HK | APAC customers |
| Northflank | EU-W, US-E | preview envs, internal |
| Scaleway | EU-W      | cost-effective EU |
| Exoscale | CH        | GDPR, FINMA |

Pulumi + Terraform manage the four providers. ArgoCD rolls out per-cluster.

## Consequences

- Each provider needs its own IaC module.
- Cross-provider traffic uses anycast DNS (NS1).
- Cost comparison dashboard in Grafana.
