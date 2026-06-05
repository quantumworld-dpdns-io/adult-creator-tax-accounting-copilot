# Contributing

> Thank you for investing in the adult-creator tax & accounting copilot. This guide explains the development workflow, coding standards, and review process.

## Code of Conduct

This project follows the [Contributor Covenant](../CODE_OF_CONDUCT.md). By participating, you agree to uphold it. Report violations to `conduct@quantumworld-dpdns-io`.

## How to report a bug

Open an issue using the [bug template](../.github/ISSUE_TEMPLATE/bug.md). Include:

- Reproduction steps
- Expected vs actual behaviour
- Environment (OS, Python/Go/Node/Rust version, commit SHA)
- Logs / stack trace

## How to suggest a feature

Open an issue using the [feature template](../.github/ISSUE_TEMPLATE/feature.md). Describe the use-case, the user value, and any design ideas.

## How to report a security vulnerability

**Do not open a public issue.** Follow the process in [`SECURITY.md`](../SECURITY.md). We aim to acknowledge within 24 h and ship a fix within 90 days.

## Development setup

### 1. Fork & clone

```bash
git clone https://github.com/<your-handle>/adult-creator-tax-accounting-copilot.git
cd adult-creator-tax-accounting-copilot
git remote add upstream https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot.git
```

### 2. Bootstrap

```bash
./scripts/bootstrap.sh   # installs pre-commit, generates dev TLS, sets up hooks
```

### 3. Branching

Follow [`docs/BRANCHING.md`](BRANCHING.md):

- `main` — production-ready
- `feature/<short-slug>` — new feature
- `fix/<short-slug>` — bug fix
- `chore/<short-slug>` — refactor, deps, etc.
- `docs/<short-slug>` — docs only
- `release/vX.Y.Z` — release branch
- `hotfix/vX.Y.Z` — emergency patch

### 4. Coding style

See [`docs/CODE_STYLE.md`](CODE_STYLE.md). Highlights:

- **Python** — ruff + black + mypy strict; type hints mandatory
- **Go** — `gofmt`, `go vet`, `staticcheck`, `golangci-lint`
- **TypeScript** — eslint + prettier
- **Rust** — `rustfmt`, `clippy --deny warnings`
- **TOML / YAML** — `taplo` / `yamllint`
- **Markdown** — `markdownlint`

### 5. Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/) enforced by `commitlint.config.js`:

```
feat(tax-engine): add UK SA108 estimate endpoint
fix(qrng): clamp count to 4096
docs(arch): add C4 container diagram
chore(deps): bump fastapi to 0.116.1
```

Sign off your commits (`git commit -s`) to certify the [DCO](../.github/DCO.md).

### 6. Tests

Every PR must include or update tests. Coverage target: **85 %** (enforced by `ci.yml`).

| Layer | Framework | File convention |
|---|---|---|
| Unit (Py) | pytest | `tests/test_*.py` next to source |
| Unit (Go) | go test | `<pkg>_test.go` |
| Unit (TS) | vitest | `*.test.ts` next to source |
| Unit (Rust) | cargo test | `#[cfg(test)] mod tests` |
| E2E | Robot Framework | `tests/robot/<area>/<feature>.robot` |
| Property-based | hypothesis (Py), rapid (Go) | `tests/property/` |
| Fuzz | go-fuzz, cargo-fuzz | `fuzz/<target>/` |
| Contract | Pact | `tests/contract/` |
| Load | k6 | `tests/load/<scenario>.js` |
| Browser | Playwright | `apps/web/e2e/` |
| Security | OWASP ZAP, Nuclei | `.github/workflows/security.yml` |

### 7. Pull request

- Target branch: `main`
- Title follows Conventional Commits
- Description uses the [PR template](../.github/PULL_REQUEST_TEMPLATE.md)
- CI must be green
- One approval from a codeowner (`CODEOWNERS`)
- Squash-merge with the PR title as the commit message

## Architecture

Read [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) and the ADRs in [`docs/adr/`](adr/) before submitting large changes. New services go through an ADR.

## Security

Read [`docs/SECURITY.md`](SECURITY.md) and [`docs/THREAT_MODEL.md`](THREAT_MODEL.md). Never commit secrets. Use Vault or `.env` (git-ignored). Pre-commit runs `gitleaks` and `trufflehog`.

## Community

- Discussions: GitHub Discussions
- Chat: (TBD — Discord / Matrix)
- Office hours: every other Thursday 16:00 UTC (calendar in `SUPPORT.md`)
- Maintainers: see `CODEOWNERS`

## Recognition

Contributors are listed in the release notes (`CHANGELOG.md`) and the GitHub contributors graph. Significant contributions earn co-maintainer status per [`docs/GOVERNANCE.md`](GOVERNANCE.md).

## License

By contributing, you agree that your contributions are licensed under the project's [MIT license](../LICENSE).
