#!/usr/bin/env python3
"""hello_gate — a minimal, honest end-to-end example of the fallacy-cutter harness.

It runs a toy calibration experiment *through the gate*: a real AST leakage scan of
the fit path, a real tautology pre-check, and a real evaluation-oracle scan, all
behind a two-phase-committed preregistration. The output is a provenance-signed
``decision.json`` that ``gate_harness.verify_decision`` accepts as VALID.

The experiment is deliberately simple and PASSES; its purpose is to show a green
end-to-end run and a citable decision, not to establish a scientific finding. The
shuffled-anchor control is included to show the same instrument reports a failure
when the calibration signal is destroyed.

Reproduce (only works once PREREG.json + PREREG.lock are committed in an *earlier*
commit than HEAD — that is what the runner checks):

    PYTHONPATH=. python examples/hello_gate/run.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # repo root, so `import gate_harness` works

from gate_harness import evaluation_oracle as EO  # noqa: E402
from gate_harness import leakage_scanner as LS  # noqa: E402
from gate_harness import tautology_check as TC  # noqa: E402
from gate_harness.runner import run_gate  # noqa: E402

SEED = 20260704
N = 400
N_ANCHORS = 12


def make_world(seed: int):
    """A latent scalar (audit-only truth) and an observer-scaled, shifted reading."""
    rng = np.random.default_rng(seed)
    latent = rng.normal(0.0, 1.0, N)
    observation = 2.0 * latent + 3.0 + rng.normal(0.0, 0.1, N)
    return latent, observation


def recover(observations, anchors):
    """Fit a calibration (observation -> value) from anchor pairs, apply it.

    Uses ONLY the observations and the provided anchor pairs. It never touches the
    latent truth, and the AST leakage scan proves it: no forbidden truth name
    appears anywhere in this function or its referenced globals.
    """
    xs = np.array([obs for obs, _ in anchors])
    ys = np.array([val for _, val in anchors])
    slope, intercept = np.polyfit(xs, ys, 1)
    return slope * np.asarray(observations, dtype=float) + intercept


def _rmse(a, b) -> float:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def score(estimate, held_out_value):
    """Evaluation entrypoint — scored against held-out truth, with NO truth hint."""
    return _rmse(estimate, held_out_value)


def _evaluation_suite():
    # A clean evaluation call site: the entrypoint receives no ground-truth hint.
    return score([0.0], [0.0])


def main() -> int:
    latent, observation = make_world(SEED)
    anchors = list(zip(observation[:N_ANCHORS], latent[:N_ANCHORS]))
    test_obs, test_latent = observation[N_ANCHORS:], latent[N_ANCHORS:]

    thresholds = json.loads((HERE / "PREREG.json").read_text(encoding="utf-8"))["thresholds"]

    # Real instrument checks, computed BEFORE the verdict.
    leak = LS.scan_fit_path([recover])
    taut = TC.tautology_precheck(
        list(observation), list(latent),
        thresholds={"information_ratio_min": thresholds["information_ratio_min"]},
    )
    eo_log = EO.scan_evaluation_call_sites(
        _evaluation_suite, entrypoint_names=["score"]
    )["evaluation_oracle_log"]

    def experiment():
        recovery_rmse = _rmse(recover(test_obs, anchors), test_latent)
        # Control: destroy the calibration by shuffling the value side of the anchors.
        rng = np.random.default_rng(SEED + 1)
        shuffled = list(zip(observation[:N_ANCHORS], rng.permutation(latent[:N_ANCHORS])))
        control_rmse = _rmse(recover(test_obs, shuffled), test_latent)
        rmse_max = thresholds["recovery_rmse_max"]
        passed = recovery_rmse <= rmse_max and control_rmse > rmse_max
        return {
            "question": (
                "Does anchor calibration recover a latent scalar from a "
                "scaled-and-shifted noisy reading, where a shuffled-anchor control "
                "cannot?"
            ),
            "metric": "RMSE(recovered, latent) on held-out samples (lower is better)",
            "preregistered_thresholds": thresholds,
            "recovery_rmse": recovery_rmse,
            "shuffled_anchor_control_rmse": control_rmse,
            "decision": "PASS" if passed else "FAIL",
            "downstream_consequence": (
                "PASS licenses only the toy claim below; a fired control would halt it."
            ),
            "fact": (
                "With 12 anchors the linear calibration recovers the latent scalar "
                "to the reported RMSE; the shuffled-anchor control does not."
            ),
            "inference": (
                "The recovery is carried by the calibration signal, not by the raw "
                "reading alone."
            ),
            "what_was_not_shown": (
                "This is a toy demonstration of the harness, not a real-world "
                "disentanglement result."
            ),
        }

    decision = run_gate(
        HERE, experiment,
        leakage_report=leak, tautology_report=taut, evaluation_oracle_log=eo_log,
    )
    print(
        f"decision: {decision['decision']}  "
        f"recovery_rmse={decision['recovery_rmse']:.4f}  "
        f"control_rmse={decision['shuffled_anchor_control_rmse']:.4f}"
    )
    print(f"written to {HERE / 'decision.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
