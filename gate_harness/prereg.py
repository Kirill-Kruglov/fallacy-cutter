"""Two-phase-commit pre-registration lock.

Fixes audit findings:
  #1  prereg + code + results committed in ONE atomic commit -> prereg undecidable
  #2  B2.1 classifier thresholds introduced in the same commit as the result they fit
  #9  thresholds silently loosened between gates without justification

Mechanism
---------
1. ``lock_prereg`` serialises the thresholds to ``PREREG.json`` and writes a
   sibling ``PREREG.lock`` recording a SHA256 of that file, a timestamp, and the
   git rev of HEAD *at lock time*. If any threshold shared with the previous
   gate changed value, a non-empty rationale for that metric is MANDATORY, or
   the function raises and writes nothing.

2. A git ``pre-commit`` hook (see ``hooks/pre-commit``) forbids committing a
   gate's ``PREREG.*`` together with that gate's ``outputs/`` in one commit, and
   forbids silently editing a locked ``PREREG.json``.

3. ``verify_prereg_lock`` (used by the runner before an experiment runs) refuses
   to proceed unless the lock exists, its SHA matches the current ``PREREG.json``,
   and the lock's git rev is a *strict ancestor* of the current HEAD — i.e. the
   prereg was committed in an *earlier* commit than the run.

All three layers must agree; any single failure is a hard FAIL.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PREREG_NAME = "PREREG.json"
LOCK_NAME = "PREREG.lock"


class PreregError(RuntimeError):
    """Raised on any fail-closed pre-registration violation."""


# --------------------------------------------------------------------------- #
# git helpers
# --------------------------------------------------------------------------- #
def _git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise PreregError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _repo_root(start: Path) -> Path:
    return Path(_git("rev-parse", "--show-toplevel", cwd=start))


def _head_rev(cwd: Path) -> str:
    return _git("rev-parse", "HEAD", cwd=cwd)


def _is_strict_ancestor(rev: str, descendant: str, cwd: Path) -> bool:
    if rev == descendant:
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", rev, descendant],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


# --------------------------------------------------------------------------- #
# serialisation helpers
# --------------------------------------------------------------------------- #
def _canonical_bytes(data: Any) -> bytes:
    """Deterministic JSON encoding so hashes are stable across processes."""
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _natkey(name: str) -> list[Any]:
    """Natural sort key so B1 < B1_1 < B2 < B2_1."""
    return [int(tok) if tok.isdigit() else tok for tok in re.split(r"(\d+)", name)]


def _flatten(prefix: str, obj: Any, out: dict[str, Any]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            _flatten(f"{prefix}.{key}" if prefix else str(key), value, out)
    else:
        out[prefix] = obj


def flatten_thresholds(thresholds: dict[str, Any]) -> dict[str, Any]:
    """Flatten nested threshold dicts to dotted leaf keys for cross-gate compare."""
    out: dict[str, Any] = {}
    _flatten("", thresholds, out)
    return out


# --------------------------------------------------------------------------- #
# gate directory resolution
# --------------------------------------------------------------------------- #
def resolve_gate_dir(gate_name: str, experiments_root: Path) -> Path:
    """Resolve a gate name to exactly one directory, or fail closed.

    Accepts an existing path, or a bare gate name searched (recursively) under
    ``experiments_root``. Zero or multiple matches -> PreregError.
    """
    candidate = Path(gate_name)
    if candidate.is_dir():
        return candidate.resolve()
    matches = sorted(
        p for p in experiments_root.rglob(gate_name) if p.is_dir()
    )
    if not matches:
        raise PreregError(f"no gate directory named {gate_name!r} under {experiments_root}")
    if len(matches) > 1:
        raise PreregError(
            f"ambiguous gate name {gate_name!r}: {len(matches)} matches "
            f"({', '.join(str(m) for m in matches)}); pass an explicit path"
        )
    return matches[0].resolve()


def _previous_gate_prereg(gate_dir: Path) -> Path | None:
    """Immediately-preceding sibling gate that has a PREREG.json, by natural order.

    The current gate is included in the ordering even if it does not yet have a
    PREREG.json (it is being locked right now); we then walk backwards to the
    nearest *earlier* sibling that already carries one.
    """
    parent = gate_dir.parent
    siblings = sorted(
        (
            p
            for p in parent.iterdir()
            if p.is_dir() and ((p / PREREG_NAME).exists() or p == gate_dir)
        ),
        key=lambda p: _natkey(p.name),
    )
    idx = next((i for i, p in enumerate(siblings) if p == gate_dir), None)
    if idx is None:
        return None
    for prev in reversed(siblings[:idx]):
        if (prev / PREREG_NAME).exists():
            return prev / PREREG_NAME
    return None


# --------------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------------- #
def lock_prereg(
    gate_name: str,
    thresholds: dict[str, Any],
    rationale_for_any_threshold_changes: dict[str, str] | None = None,
    *,
    exploration_basis: str | Path | None = None,
    experiments_root: Path | None = None,
    extra_metadata: dict[str, Any] | None = None,
) -> dict[str, Path]:
    """Write PREREG.json + PREREG.lock for a gate. Fail closed.

    Raises PreregError if a threshold shared with the previous gate changed
    value and no non-empty rationale is supplied for that metric.

    ``exploration_basis`` is mandatory (taxonomy item #3: thresholds informed by
    off-the-record exploratory runs). Exactly two honest answers exist: the
    literal string ``"none"`` — an explicit declaration that no exploratory runs
    informed these thresholds — or a path to a chain-valid exploration ledger
    (see ``gate_harness.exploration_ledger``). Silence is not an option.
    """
    from . import exploration_ledger as _ledger

    if exploration_basis is None:
        raise PreregError(
            "exploration_basis is mandatory: pass 'none' to declare that no "
            "exploratory runs informed these thresholds, or a path to an "
            "exploration ledger (gate_harness.exploration_ledger) that did. "
            "Silence is not an option (taxonomy item #3)."
        )
    try:
        basis_record = _ledger.resolve_exploration_basis(exploration_basis)
    except _ledger.LedgerError as exc:
        raise PreregError(str(exc)) from exc

    rationale = rationale_for_any_threshold_changes or {}
    start = Path.cwd()
    root = experiments_root or (_repo_root(start) / "experiments")
    gate_dir = resolve_gate_dir(gate_name, root)

    # --- cross-gate threshold-change guard (finding #9) --------------------- #
    prev_path = _previous_gate_prereg(gate_dir)
    if prev_path is not None:
        prev = json.loads(prev_path.read_text(encoding="utf-8"))
        prev_flat = flatten_thresholds(prev.get("thresholds", {}))
        this_flat = flatten_thresholds(thresholds)
        for key in sorted(set(prev_flat) & set(this_flat)):
            if prev_flat[key] != this_flat[key]:
                # match rationale by leaf key or dotted key
                leaf = key.split(".")[-1]
                justification = rationale.get(key) or rationale.get(leaf)
                if not justification or not str(justification).strip():
                    raise PreregError(
                        f"threshold {key!r} changed from {prev_flat[key]} "
                        f"(prev gate {prev_path.parent.name}) to {this_flat[key]} "
                        f"without a rationale; supply "
                        f"rationale_for_any_threshold_changes[{leaf!r}]. "
                        f"(This is audit finding #9.)"
                    )

    payload = {
        "gate": gate_dir.name,
        "thresholds": thresholds,
        "threshold_change_rationale": rationale,
        "exploration_basis": basis_record,
    }
    if extra_metadata:
        payload["metadata"] = extra_metadata

    prereg_bytes = _canonical_bytes(payload)
    prereg_path = gate_dir / PREREG_NAME
    lock_path = gate_dir / LOCK_NAME

    lock_payload = {
        "prereg_sha256": _sha256(prereg_bytes),
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "locked_at_git_rev": _head_rev(gate_dir),
        "note": (
            "Two-phase commit required: commit this PREREG.json + PREREG.lock "
            "in a commit that contains NO outputs/. Run the experiment and commit "
            "results separately. The runner verifies this rev is a strict ancestor "
            "of the run's HEAD."
        ),
    }

    prereg_path.write_bytes(prereg_bytes)
    lock_path.write_bytes(_canonical_bytes(lock_payload))
    return {"prereg": prereg_path, "lock": lock_path}


def verify_prereg_lock(gate_dir: Path) -> tuple[bool, str]:
    """Fail-closed gate: return (ok, reason). The runner refuses to run if not ok.

    Checks:
      (a) PREREG.lock exists,
      (b) SHA256(PREREG.json) == lock.prereg_sha256 (no post-hoc edit),
      (c) lock.locked_at_git_rev is a STRICT ancestor of current HEAD
          (prereg committed in an earlier commit than this run).
    """
    gate_dir = Path(gate_dir).resolve()
    prereg_path = gate_dir / PREREG_NAME
    lock_path = gate_dir / LOCK_NAME

    next_lock = (
        f"next: freeze thresholds first — python -m gate_harness.prereg lock "
        f"{gate_dir} --thresholds-file <thresholds.json> --exploration-basis none|<ledger.jsonl>, "
        f"then commit PREREG.json + PREREG.lock (no outputs/) before running"
    )
    if not prereg_path.exists():
        return False, f"missing {PREREG_NAME}; {next_lock}"
    if not lock_path.exists():
        return False, f"missing {LOCK_NAME} (prereg was never locked); {next_lock}"

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    actual_sha = _sha256(prereg_path.read_bytes())
    if actual_sha != lock.get("prereg_sha256"):
        return False, (
            "PREREG.json SHA does not match PREREG.lock — thresholds were edited "
            "after locking (audit finding #2); next: re-lock deliberately via "
            "gate_harness.prereg.lock_prereg (the change and its rationale become "
            "part of the record), commit, then re-run"
        )

    locked_rev = lock.get("locked_at_git_rev")
    if not locked_rev:
        return False, "PREREG.lock has no git rev"
    try:
        head = _head_rev(gate_dir)
    except PreregError as exc:
        return False, str(exc)
    if not _is_strict_ancestor(locked_rev, head, gate_dir):
        return False, (
            f"PREREG.lock rev {locked_rev[:10]} is not a strict ancestor of HEAD "
            f"{head[:10]} — prereg was not committed before this run "
            f"(audit finding #1); next: commit PREREG.json + PREREG.lock in their "
            f"own commit (no outputs/), then re-run"
        )
    return True, "prereg lock verified: committed before run, unedited since lock"


def main(argv: list[str] | None = None) -> int:
    """CLI so agents and adapters can lock/verify without writing Python.

    lock   <gate_dir> (--thresholds-json '<json>' | --thresholds-file <path>)
           --exploration-basis none|<ledger.jsonl>
           [--rationale-json '<json>'] [--metadata-json '<json>']
    verify <gate_dir>
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog="python -m gate_harness.prereg")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_lock = sub.add_parser("lock", help="freeze thresholds for a gate (two-phase commit, phase 1)")
    p_lock.add_argument("gate_dir")
    group = p_lock.add_mutually_exclusive_group(required=True)
    group.add_argument("--thresholds-json")
    group.add_argument("--thresholds-file")
    p_lock.add_argument("--exploration-basis", required=True,
                        help="'none' or a path to a chain-valid exploration ledger")
    p_lock.add_argument("--rationale-json", default="{}")
    p_lock.add_argument("--metadata-json", default=None)

    p_verify = sub.add_parser("verify", help="check the lock as the runner would")
    p_verify.add_argument("gate_dir")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "lock":
            if args.thresholds_file:
                thresholds = json.loads(Path(args.thresholds_file).read_text(encoding="utf-8"))
                if "thresholds" in thresholds and isinstance(thresholds["thresholds"], dict):
                    thresholds = thresholds["thresholds"]
            else:
                thresholds = json.loads(args.thresholds_json)
            paths = lock_prereg(
                args.gate_dir,
                thresholds,
                json.loads(args.rationale_json),
                exploration_basis=args.exploration_basis,
                extra_metadata=json.loads(args.metadata_json) if args.metadata_json else None,
            )
            print(f"LOCKED  {paths['prereg']}")
            print(f"        {paths['lock']}")
            print("next: commit PREREG.json + PREREG.lock in their own commit "
                  "(no outputs/), then run the gate")
            return 0
        ok, reason = verify_prereg_lock(Path(args.gate_dir))
        print(("LOCK-VALID  " if ok else "REFUSED — ") + reason)
        return 0 if ok else 1
    except (PreregError, json.JSONDecodeError, OSError) as exc:
        print(f"REFUSED — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
