# Branching & Release Strategy

This repository uses a trunk-based development model with short-lived feature
branches. Releases are cut from `main` via signed, attested tags.

## Branches

| Branch      | Purpose                                       | Protection                 |
| ----------- | --------------------------------------------- | -------------------------- |
| `main`      | trunk; always deployable                     | signed commits, 2 reviews  |
| `dev`       | integration (auto-commit bot)                 | protected                  |
| `release/*` | release-candidate stabilization               | squash-merge               |
| `feat/*`    | feature branch (≤ 7 days)                     | conventional commit        |
| `fix/*`     | hotfix (≤ 24h)                                | hotfix policy              |
| `quantum/*` | quantum-specific work                         | tagged commits             |
| `zk/*`      | zero-knowledge work                           | tagged commits             |
| `sec/*`     | security-sensitive (private until merged)    | signed                     |

## Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) enforced by
commitlint. See `commitlint.config.js` for the type enum.

## Release Cadence

- `1.0.0-rc.1` → `1.0.0` → `1.x.y` (monthly minor, weekly patch)
- Release-please bot creates release PRs
- Releases are multi-cloud (Zeabur, Northflank, Scaleway, Exoscale)

## Auto-commit Bot

`auto_commit.sh` is the project's own commit bot driving the 1,055-todo roadmap
incrementally. It is **not** for external contributors.
