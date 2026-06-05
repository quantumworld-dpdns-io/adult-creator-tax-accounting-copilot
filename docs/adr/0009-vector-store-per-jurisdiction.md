# ADR 0009: Vector Store per Jurisdiction

## Status

Accepted.

## Context

Tax rules, treaties, and platform ToS vary by jurisdiction. We need
jurisdiction-aware retrieval.

## Decision

- One **Qdrant** collection per jurisdiction (US, EU, UK, CA, AU, JP, …).
- One **Milvus** cluster for shared embeddings (corpus, IRS pubs).
- A `vector-router` service chooses the collection based on creator profile.
- Reranking is **cross-encoder** (BAAI) + ColBERT for legal accuracy.

## Consequences

- Schema migration per jurisdiction is a first-class operation.
- Per-jurisdiction RLS in Qdrant.
