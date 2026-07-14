"""Adversarial tests for group-aware split integrity (data-structure leakage).

The attack being reproduced: samples from the same patient land in both train
and test, so the held-out metric measures memorization, not generalization —
with no truth name anywhere in the code.

Run: python3 -m gate_harness.tests.test_split_integrity
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gate_harness import split_integrity as SI  # noqa: E402


def test_catches_group_crossing_splits():
    groups = ["p1", "p1", "p2", "p2", "p3", "p3"]
    splits = ["train", "test", "train", "train", "test", "test"]  # p1 leaks
    report = SI.check_group_split_integrity(groups, splits, declared_group_key="patient_id")
    assert report["passed"] is False
    assert any(v["group"] == "'p1'" for v in report["groups_crossing_splits"])
    try:
        SI.assert_group_split_integrity(groups, splits, declared_group_key="patient_id")
    except SI.SplitIntegrityError as exc:
        assert "patient_id" in str(exc) and "next:" in str(exc)
        print("  [ok] patient crossing train/test caught, with actionable refusal")
    else:
        raise AssertionError("group-crossing split must raise")


def test_clean_group_split_passes():
    groups = ["p1", "p1", "p2", "p2", "p3", "p3"]
    splits = ["train", "train", "train", "train", "test", "test"]
    report = SI.assert_group_split_integrity(groups, splits, declared_group_key="patient_id")
    assert report["passed"] is True and report["n_groups"] == 3
    print("  [ok] group-respecting split passes with evidence counts")


def test_undeclared_grouping_fails_closed():
    report = SI.check_group_split_integrity(["p1"], ["train"], declared_group_key="")
    assert report["passed"] is False and report["computed_by"] == "NOT_VERIFIABLE"
    print("  [ok] undeclared grouping is NOT_VERIFIABLE, never a silent pass")


def test_missing_group_value_fails_closed():
    report = SI.check_group_split_integrity(
        ["p1", None, "p2"], ["train", "train", "test"], declared_group_key="patient_id"
    )
    assert report["passed"] is False and report["computed_by"] == "NOT_VERIFIABLE"
    print("  [ok] a sample without a group value fails closed")


def test_length_mismatch_fails_closed():
    report = SI.check_group_split_integrity(
        ["p1", "p2"], ["train"], declared_group_key="patient_id"
    )
    assert report["passed"] is False and report["computed_by"] == "NOT_VERIFIABLE"
    print("  [ok] misaligned groups/splits fail closed")


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
