"""Append-only exploration ledger — makes the quiet room audible.

Addresses false-pass taxonomy item #3 (Appendix A.3): *thresholds informed by
off-the-record exploratory runs, then "preregistered" fresh*. The two-rooms
discipline (Appendix A.5) permits exploration without gates — but agentic
environments make exploratory runs cheap and invisible, so the gap between the
rooms becomes the main channel for a false pass.

This module does NOT block anything in the exploration room. It records. Each
logged run is chained to the previous one by SHA256, so the ledger can be
appended to but not silently edited, reordered, or truncated from the middle.
``prereg.lock_prereg`` then requires an explicit ``exploration_basis``: either
the literal string ``"none"`` (a declaration: no exploratory runs informed these
thresholds) or a path to a ledger whose chain verifies. Both answers are honest;
silence stops being an option.

What this structurally cannot catch: exploration performed outside the ledger
(a second clone, a notebook, a colleague's machine). Like every module here, it
makes the honest path checkable — it does not make the dishonest path impossible.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEDGER_NAME = "EXPLORATION.jsonl"
GENESIS_HASH = "0" * 64


class LedgerError(RuntimeError):
    """Raised on any fail-closed ledger violation."""


def _canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _entry_hash(entry_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(entry_without_hash)).hexdigest()


def read_entries(ledger_path: Path) -> list[dict[str, Any]]:
    """Parse every ledger line; any unparseable line is a hard failure."""
    ledger_path = Path(ledger_path)
    if not ledger_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for i, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise LedgerError(
                f"{ledger_path}:{i} is not valid JSON ({exc}); a ledger that cannot "
                f"be parsed cannot be cited as an exploration basis (fail closed)"
            ) from exc
    return entries


def append_entry(ledger_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Append one exploration record, chained to the current head. Returns the entry."""
    if not isinstance(payload, dict) or not payload:
        raise LedgerError("exploration payload must be a non-empty dict")
    ledger_path = Path(ledger_path)
    entries = read_entries(ledger_path)
    prev = entries[-1]["entry_sha256"] if entries else GENESIS_HASH
    entry = {
        "seq": len(entries) + 1,
        "logged_at_utc": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
        "prev": prev,
    }
    entry["entry_sha256"] = _entry_hash(entry)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def verify_chain(ledger_path: Path) -> tuple[bool, list[str]]:
    """Verify seq order, hash chaining, and per-entry hashes. Fail closed."""
    try:
        entries = read_entries(ledger_path)
    except LedgerError as exc:
        return False, [str(exc)]
    if not entries:
        return False, [f"{ledger_path}: ledger is empty or missing — nothing to cite"]

    reasons: list[str] = []
    prev = GENESIS_HASH
    for i, entry in enumerate(entries, 1):
        recorded = entry.get("entry_sha256")
        body = {k: v for k, v in entry.items() if k != "entry_sha256"}
        if entry.get("seq") != i:
            reasons.append(f"entry {i}: seq is {entry.get('seq')!r}, expected {i} (reordered or truncated)")
        if entry.get("prev") != prev:
            reasons.append(f"entry {i}: prev hash broken (entry deleted or inserted before it)")
        if recorded != _entry_hash(body):
            reasons.append(f"entry {i}: entry_sha256 does not match its content (edited after logging)")
        prev = recorded
    return (not reasons), reasons


def ledger_head(ledger_path: Path) -> tuple[str, int]:
    """Return (head hash, entry count) of a chain-valid ledger, else raise."""
    ok, reasons = verify_chain(ledger_path)
    if not ok:
        raise LedgerError(
            f"ledger {ledger_path} failed chain verification:\n  "
            + "\n  ".join(reasons)
        )
    entries = read_entries(ledger_path)
    return entries[-1]["entry_sha256"], len(entries)


def resolve_exploration_basis(basis: str | Path) -> str | dict[str, Any]:
    """Resolve the mandatory exploration-basis declaration for a prereg lock.

    Accepts exactly two honest answers:
      - the literal string ``"none"``: no exploratory runs informed the thresholds;
      - a path to a chain-valid exploration ledger: returns ``{ledger, head, entries}``.
    Anything else fails closed.
    """
    if isinstance(basis, str) and basis.strip().lower() == "none":
        return "none"
    path = Path(basis)
    if not path.exists():
        raise LedgerError(
            f"exploration_basis {basis!r} is neither the literal 'none' nor an "
            f"existing ledger file; declare 'none' explicitly, or log exploratory "
            f"runs first: python -m gate_harness.exploration_ledger log "
            f"<ledger.jsonl> '<json payload>'"
        )
    head, count = ledger_head(path)
    return {"ledger": str(path), "head": head, "entries": count}


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = argv if argv is not None else sys.argv[1:]
    usage = (
        "usage: python -m gate_harness.exploration_ledger log <ledger.jsonl> <json-payload>\n"
        "       python -m gate_harness.exploration_ledger head <ledger.jsonl>\n"
        "       python -m gate_harness.exploration_ledger verify <ledger.jsonl>"
    )
    if len(argv) < 2:
        print(usage, file=sys.stderr)
        return 2
    cmd, path = argv[0], Path(argv[1])
    try:
        if cmd == "log":
            if len(argv) != 3:
                print(usage, file=sys.stderr)
                return 2
            try:
                payload = json.loads(argv[2])
            except json.JSONDecodeError:
                payload = {"note": argv[2]}
            if not isinstance(payload, dict):
                payload = {"note": payload}
            entry = append_entry(path, payload)
            print(f"LOGGED  seq={entry['seq']}  head={entry['entry_sha256']}")
            return 0
        if cmd == "head":
            head, count = ledger_head(path)
            print(f"HEAD    {head}  ({count} entries)")
            return 0
        if cmd == "verify":
            ok, reasons = verify_chain(path)
            if ok:
                print(f"CHAIN-VALID  {path}")
                return 0
            print(f"CHAIN-INVALID  {path}")
            for r in reasons:
                print(f"  - {r}")
            return 1
    except LedgerError as exc:
        print(f"REFUSED — {exc}", file=sys.stderr)
        return 1
    print(usage, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
