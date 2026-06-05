#!/bin/bash
# Quick OWASP-friendly pre-commit hook.
# Runs the most common security checks before any commit lands.

set -euo pipefail

echo "== secret scan =="
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --no-banner
fi

echo "== yaml lint =="
if command -v yamllint >/dev/null 2>&1; then
  yamllint .
fi

echo "== hadolint =="
if command -v hadolint >/dev/null 2>&1; then
  find docker -type f -name "Dockerfile*" -print0 | xargs -0 -I{} hadolint {}
fi

echo "== kube-linter =="
if command -v kube-linter >/dev/null 2>&1; then
  kube-linter lint infra/k8s/
fi

echo "== helm-docs =="
if command -v helm-docs >/dev/null 2>&1; then
  find helm -name Chart.yaml -exec helm-docs {} \;
fi

echo "== conventional commit =="
commit_msg_file="${1:-.git/COMMIT_EDITMSG}"
if [ -f "$commit_msg_file" ]; then
  if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|security|quantum|zk|wasm|fl|apq)(\(.+\))?: " "$commit_msg_file"; then
    echo "WARN: commit message does not follow Conventional Commits"
  fi
fi

echo "OK"
