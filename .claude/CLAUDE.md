# Claude Code configuration for the Adult Creator Tax & Accounting Copilot.

# This file is read by Claude Code (Anthropic) to enable project-specific
# permissions, subagents, and commands.

# Subagents
subagents:
  tax-reviewer:
    description: "Reviews changes to tax-rule code (svc/tax-engine, .skills/tax-*, openapi/)"
    tools: [Read, Grep, Glob, Bash]
    prompt: |
      You are a tax-compliance reviewer. Your job is to catch mistakes in
      US 1099, W-8BEN, EU VAT MOSS, UK MTD, and Canadian/AU/JP tax code.
      Always cite the relevant IRS publication or treaty in your review.

  security-reviewer:
    description: "Reviews changes against OWASP Top-10 2021 + API Security Top-10"
    tools: [Read, Grep, Glob, Bash]
    prompt: |
      You are a security reviewer. Run the Robot Framework OWASP suites
      locally and verify the change does not regress any of the A01-A10
      or API1-API10 controls. Flag any secret leak, PII exposure, or
      missing audit-log emit.

  quantum-auditor:
    description: "Reviews quantum circuit changes (quantum/, qiskit/, cudaq/, qrng/)"
    tools: [Read, Grep, Glob, Bash]
    prompt: |
      You are a quantum-audit reviewer. Verify that all PQC signatures
      use Dilithium-5, all KEM use Kyber-1024, and all RNG is sourced
      from a quantum entropy provider or a CSPRNG with documented seeding.

# Permissions
permissions:
  allow:
    - "Bash(pytest tests/)"
    - "Bash(robot --variable ENV:dev tests/robot/)"
    - "Bash(ruff check .)"
    - "Bash(mypy .)"
    - "Bash(golangci-lint run)"
    - "Bash(cargo clippy)"
    - "Bash(docker build .)"
    - "Bash(helm template)"
    - "Bash(pulumi preview)"
    - "Bash(terraform plan)"
  deny:
    - "Bash(git push --force)"
    - "Bash(rm -rf /)"

# Hooks
hooks:
  pre-commit:
    command: "pre-commit run --files"
  post-edit:
    command: "scripts/owasp_quick_check.sh"
