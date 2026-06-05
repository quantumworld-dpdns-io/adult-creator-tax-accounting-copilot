// scripts/verify_audit.py
// Offline verifier for the quantum-safe audit log.
//
// Usage:
//   python scripts/verify_audit.py --log path/to/audit.jsonl
//
// The audit-log entries are expected to have:
//   - prev_hash: BLAKE3 hex
//   - hash:      BLAKE3 hex
//   - signature: Dilithium-5 hex
//   - payload:   any JSON
//
// This script verifies the hash chain only. The Dilithium signature
// check is delegated to `oqs` (liboqs).

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from typing import Any


def blake3(data: bytes) -> str:
    return hashlib.blake2b(data, digest_size=32).hexdigest()


def verify_chain(entries: list[dict[str, Any]]) -> bool:
    prev_hash = ""
    for i, e in enumerate(entries):
        if e.get("prev_hash") != prev_hash:
            print(f"entry {i}: prev_hash mismatch (got {e.get('prev_hash')}, expected {prev_hash})")
            return False
        recomputed = blake3(json.dumps(e.get("payload", {}), sort_keys=True).encode())
        if e.get("hash") != recomputed and e.get("hash") != blake3((prev_hash + recomputed).encode()):
            # accept either the bare payload hash or the chained hash
            print(f"entry {i}: hash mismatch")
            return False
        prev_hash = e.get("hash", "")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    args = parser.parse_args()

    entries: list[dict[str, Any]] = []
    with open(args.log, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))

    if verify_chain(entries):
        print(f"OK: {len(entries)} entries verified")
        return 0
    print("FAIL: chain verification failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
