# hello_gate — a worked end-to-end example

The smallest honest run through the knife: a toy calibration experiment that comes
out the other side as a **provenance-signed `decision.json` that
`gate_harness.verify_decision` accepts as VALID**.

It is deliberately simple and it PASSES. The point is not the finding (there is
none worth citing); the point is to show the *whole flow* working, and to show the
same instrument reporting a **failure** on a shuffled-anchor control.

## What the experiment does

A latent scalar is read through a scaled, shifted, noisy observer. A learner sees
only the observations and twelve calibration *anchors* — never the latent truth —
and fits a linear calibration to recover the scalar. The decision keys on **RMSE**
(recovery error) rather than correlation, because correlation is affine-invariant
and a broken calibration would still "pass" it — exactly the kind of hidden
easiness the harness exists to catch.

- **recovery RMSE ≈ 0.05** (≤ the preregistered `recovery_rmse_max = 0.5`) → PASS
- **shuffled-anchor control RMSE ≈ 1.38** (> 0.5) → the control fires, as it must

## What makes the decision VALID (not just green numbers)

`run.py` computes, before the verdict, three *real* instrument checks and hands
them to `run_gate`:

- **AST leakage scan** of the `recover` fit path — proves it references no
  forbidden truth name (`gate_harness.leakage_scanner`).
- **Tautology pre-check** — `information_ratio = var(obs)/var(latent) ≈ 4.0`, above
  the mandatory `information_ratio_min`, so the contrast is not guaranteed by
  construction (`gate_harness.tautology_check`).
- **Evaluation-oracle scan** — the evaluation entrypoint receives no ground-truth
  hint (`gate_harness.evaluation_oracle`).

`run_gate` then refuses to proceed unless `PREREG.json` + `PREREG.lock` were
committed in an **earlier** commit than the run (two-phase commit), and only then
writes `decision.json` with a `_harness_provenance` block that the independent
`verify_decision` re-checks.

## Reproduce it

```bash
# verify the shipped decision is VALID
PYTHONPATH=. python -m gate_harness.verify_decision examples/hello_gate/decision.json

# regenerate it from scratch (deterministic; identical bytes)
PYTHONPATH=. python examples/hello_gate/run.py
```

The regeneration only works because `PREREG.*` is already in history: the runner
checks that the preregistration is a strict ancestor of `HEAD`. That is the
two-phase discipline (audit finding #1) enforced mechanically, not promised.
