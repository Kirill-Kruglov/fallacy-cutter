"""Adversarial tests for the exploration ledger (taxonomy item #3).

Each test reproduces the attack the module exists to catch: silent editing,
truncation, and — the central one — preregistering thresholds while staying
silent about the exploratory runs that produced them.

Run: python3 -m gate_harness.tests.test_exploration_ledger
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gate_harness import exploration_ledger as EL  # noqa: E402
from gate_harness import prereg as PR  # noqa: E402


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def _init_repo(repo: Path):
    _run(["git", "init", "-q"], repo)
    _run(["git", "config", "user.email", "t@t"], repo)
    _run(["git", "config", "user.name", "t"], repo)
    (repo / "seed.txt").write_text("x")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-q", "-m", "init"], repo)


def test_append_and_verify_chain():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / EL.LEDGER_NAME
        e1 = EL.append_entry(ledger, {"run": 1, "threshold_tried": 0.6, "result": "FAIL"})
        e2 = EL.append_entry(ledger, {"run": 2, "threshold_tried": 0.7, "result": "PASS"})
        assert e2["prev"] == e1["entry_sha256"]
        ok, reasons = EL.verify_chain(ledger)
        assert ok, reasons
        head, count = EL.ledger_head(ledger)
        assert head == e2["entry_sha256"] and count == 2
        print("  [ok] append chains entries; chain verifies; head is last entry")


def test_edited_entry_breaks_chain():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / EL.LEDGER_NAME
        EL.append_entry(ledger, {"run": 1, "threshold_tried": 0.6, "result": "FAIL"})
        EL.append_entry(ledger, {"run": 2, "threshold_tried": 0.7, "result": "PASS"})
        # attack: rewrite history — the failed 0.6 run becomes a pass
        lines = ledger.read_text().splitlines()
        entry = json.loads(lines[0])
        entry["payload"]["result"] = "PASS"
        lines[0] = json.dumps(entry, sort_keys=True)
        ledger.write_text("\n".join(lines) + "\n")
        ok, reasons = EL.verify_chain(ledger)
        assert ok is False
        assert any("edited after logging" in r for r in reasons)
        print("  [ok] silently edited entry breaks the chain")


def test_truncated_ledger_breaks_chain():
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / EL.LEDGER_NAME
        for i in range(3):
            EL.append_entry(ledger, {"run": i + 1})
        # attack: delete the middle run
        lines = ledger.read_text().splitlines()
        ledger.write_text("\n".join([lines[0], lines[2]]) + "\n")
        ok, reasons = EL.verify_chain(ledger)
        assert ok is False
        print("  [ok] deleting a middle entry breaks the chain")


def test_lock_prereg_requires_exploration_basis():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        (repo / "experiments" / "G1").mkdir(parents=True)
        cwd0 = os.getcwd(); os.chdir(repo)
        try:
            try:
                PR.lock_prereg("G1", {"corr_min": 0.9}, experiments_root=repo / "experiments")
            except PR.PreregError as exc:
                assert "exploration_basis" in str(exc)
                print("  [ok] silent prereg (no exploration_basis) rejected")
            else:
                raise AssertionError("lock_prereg without exploration_basis must fail closed")
        finally:
            os.chdir(cwd0)


def test_lock_prereg_records_ledger_head():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        gate = repo / "experiments" / "G1"
        gate.mkdir(parents=True)
        ledger = repo / EL.LEDGER_NAME
        EL.append_entry(ledger, {"tried": 0.6, "result": "FAIL"})
        EL.append_entry(ledger, {"tried": 0.7, "result": "PASS"})
        head, count = EL.ledger_head(ledger)
        cwd0 = os.getcwd(); os.chdir(repo)
        try:
            PR.lock_prereg(
                "G1", {"corr_min": 0.7},
                exploration_basis=ledger,
                experiments_root=repo / "experiments",
            )
        finally:
            os.chdir(cwd0)
        payload = json.loads((gate / "PREREG.json").read_text())
        basis = payload["exploration_basis"]
        assert basis["head"] == head and basis["entries"] == count == 2
        print("  [ok] prereg records the ledger head it was based on")


def test_lock_prereg_rejects_tampered_ledger():
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _init_repo(repo)
        (repo / "experiments" / "G1").mkdir(parents=True)
        ledger = repo / EL.LEDGER_NAME
        EL.append_entry(ledger, {"tried": 0.6, "result": "FAIL"})
        entry = json.loads(ledger.read_text())
        entry["payload"]["result"] = "PASS"
        ledger.write_text(json.dumps(entry, sort_keys=True) + "\n")
        cwd0 = os.getcwd(); os.chdir(repo)
        try:
            try:
                PR.lock_prereg(
                    "G1", {"corr_min": 0.7},
                    exploration_basis=ledger,
                    experiments_root=repo / "experiments",
                )
            except PR.PreregError as exc:
                assert "chain" in str(exc)
                print("  [ok] prereg citing a tampered ledger rejected")
            else:
                raise AssertionError("tampered ledger must not be citable as a basis")
        finally:
            os.chdir(cwd0)


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        print(f"- {t.__name__}")
        try:
            t()
        except AssertionError as exc:
            failed += 1
            print(f"  [FAIL] {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
