"""Adversarial tests for the preprocessing-order scan (fit sees test data).

The attack being reproduced: ``scaler.fit_transform(X)`` on the full dataset,
split afterwards — the classic sklearn-shaped leak that no truth-name scan sees.

Run: python3 -m gate_harness.tests.test_preprocessing_order
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gate_harness import preprocessing_order as PO  # noqa: E402


def test_catches_fit_on_full_data_before_split():
    def pipeline(X, y, scaler, model):
        Xs = scaler.fit_transform(X)                     # leak: fit sees test rows
        X_tr, X_te, y_tr, y_te = train_test_split(Xs, y)  # noqa: F821
        model.fit(X_tr, y_tr)
        return model.score(X_te, y_te)

    report = PO.scan_preprocessing_order([pipeline])
    assert report["passed"] is False
    kinds = {v["kind"] for v in report["violations"]}
    assert "fit_before_split" in kinds or "fit_on_presplit_data" in kinds
    try:
        PO.assert_preprocessing_order([pipeline])
    except PO.PreprocessingOrderError as exc:
        assert "next:" in str(exc)
        print("  [ok] fit_transform on pre-split data caught, actionable refusal")
    else:
        raise AssertionError("pre-split fit_transform must raise")


def test_catches_fit_on_variable_passed_to_split():
    def pipeline(X, y, selector, model):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y)  # noqa: F821
        selector.fit(X, y)                                # leak: fit on the FULL X
        model.fit(selector.transform(X_tr), y_tr)
        return model.score(selector.transform(X_te), y_te)

    report = PO.scan_preprocessing_order([pipeline])
    assert report["passed"] is False
    assert any(
        v["kind"] == "fit_on_presplit_data" and "X" in v["data_names"]
        for v in report["violations"]
    )
    print("  [ok] fit on the same variable that entered the split caught")


def test_clean_split_then_fit_passes():
    def pipeline(X, y, scaler, model):
        X_tr, X_te, y_tr, y_te = train_test_split(X, y)  # noqa: F821
        X_tr_s = scaler.fit_transform(X_tr)
        model.fit(X_tr_s, y_tr)
        return model.score(scaler.transform(X_te), y_te)

    report = PO.assert_preprocessing_order([pipeline])
    assert report["passed"] is True
    print("  [ok] split-first, fit-on-train-only pipeline passes")


def test_no_split_anywhere_is_not_verifiable():
    def pipeline(X_tr, y_tr, scaler, model):
        model.fit(scaler.fit_transform(X_tr), y_tr)
        return model

    report = PO.scan_preprocessing_order([pipeline])
    assert report["passed"] is False and report["computed_by"] == "NOT_VERIFIABLE"
    print("  [ok] no registered split call -> NOT_VERIFIABLE, never a silent pass")


def test_empty_registry_fails_closed():
    report = PO.scan_preprocessing_order([])
    assert report["passed"] is False and report["computed_by"] == "NOT_VERIFIABLE"
    print("  [ok] empty registry fails closed")


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
