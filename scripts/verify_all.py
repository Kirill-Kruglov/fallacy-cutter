#!/usr/bin/env python3
"""Verify every worked-example decision, and fail if any is not VALID.

Every ``decision.json`` under ``examples/`` must carry harness provenance and pass
the independent ``gate_harness.verify_decision`` check. This is the promise the
project makes — a run through the harness is either provenance-signed VALID or it
fails closed — checked on every push, not just asserted.

    python scripts/verify_all.py    # exits non-zero on any INVALID / if none found
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gate_harness.verify_decision import verify_decision  # noqa: E402

EXAMPLES = ROOT / "examples"


def main() -> int:
    decisions = sorted(EXAMPLES.rglob("decision.json"))
    if not decisions:
        print("FAIL: no example decision.json found")
        return 1

    failures = []
    for p in decisions:
        ok, reasons = verify_decision(p)
        print(f"  {'VALID  ' if ok else 'INVALID'}  {p.relative_to(ROOT)}")
        if not ok:
            failures.append(f"{p.relative_to(ROOT)}: {reasons}")

    print(f"\n{len(decisions)} example decision(s) checked.")
    if failures:
        print(f"FAIL: {len(failures)} not VALID:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK: every example decision is provenance-signed VALID.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
