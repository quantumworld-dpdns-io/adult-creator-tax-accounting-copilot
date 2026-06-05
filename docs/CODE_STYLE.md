# Code Style

## Per-Language

| Lang   | Tool                     | Config                       |
| ------ | ------------------------ | ---------------------------- |
| Python | ruff + black + mypy      | `pyproject.toml`             |
| Go     | gofmt + goimports + golangci-lint | `.golangci.yml`     |
| Rust   | rustfmt + clippy         | `rust-toolchain.toml`        |
| TypeScript | prettier + eslint       | `.eslintrc.cjs`, `.prettierrc` |
| Shell  | shellcheck + shfmt       | `.shellcheckrc`              |
| YAML   | yamllint                 | `.yamllint.yml`              |
| HCL    | tflint + tfsec + checkov | `tflint.hcl`                 |

## General

- Conventional Commits (enforced by commitlint).
- SPDX license headers (`SPDX-License-Identifier: MIT`).
- No comments unless they explain "why," not "what."
- No PII or secrets in code or commits.
- Public APIs must have OpenAPI / AsyncAPI / SDL specs.
- All quantum circuits must include a noise-robustness test.
- All ZK circuits must include a soundness test.
- All public REST endpoints must have Robot Framework tests.
