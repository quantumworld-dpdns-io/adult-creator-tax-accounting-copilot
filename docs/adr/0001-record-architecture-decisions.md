# ADR 0001: Record Architecture Decisions

## Status

Accepted.

## Context

We need a way to record significant architectural decisions so future
contributors understand *why* the system is the way it is.

## Decision

We adopt Michael Nygard's "ADR" pattern. ADRs are stored as
`docs/adr/NNNN-*.md` and indexed in `docs/adr/README.md`.

## Consequences

- One ADR per significant decision.
- ADRs are immutable once accepted.
- Superseded ADRs are marked, never deleted.
