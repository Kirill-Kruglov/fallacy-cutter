---
name: fallacy-cutter
description: >
  Fail-closed gate discipline for computational experiments. Use BEFORE any
  result will be cited, published, or used for a decision: freeze thresholds
  first (gate_lock), run through the harness, and cite only what verifies.
  Do NOT gate pure exploration — there, log runs to the exploration ledger
  instead. Catches: post-hoc thresholds, ground-truth leakage into the fit
  path, group-crossing train/test splits (patient_id etc.), fit-transformers
  seeing test data, tautological constructions, single-seed conclusions.
---

# fallacy-cutter — the knife for your own results

You are the experimenter this instrument was built for. Its premise: an
experimenter's good intentions are not a guarantee — an LLM's even less so.
The instrument removes *virtue* from the trust chain, not skill: what was
declared, when it was frozen, and what touched the data become facts a
stranger can check without trusting you.

Requirements: a git repository, Python ≥ 3.11, and `gate_harness` importable
(`pip install fallacy-cutter`, or the repo on `PYTHONPATH`).

## Rule zero: know which room you are in

- **Exploration** — trying things, tuning, poking at data. Nothing here is
  citable, and nothing is blocked. But every run you would be embarrassed to
  hide MUST go to the ledger (below). Exploration that leaves no trace is the
  channel through which post-hoc thresholds masquerade as preregistered ones.
- **Confirmation** — a result someone will rely on. Full discipline: lock,
  commit, run, verify. If any step refuses, the result is not citable. Do not
  soften the refusal in prose; report it as the finding.

You are at risk of being in both rooms in one session. Separate them
explicitly: exploration on its own branch or directory, confirmation only
after the lock is committed.

## Exploration room: log, don't gate

```bash
python -m gate_harness.exploration_ledger log EXPLORATION.jsonl \
  '{"tried": {"threshold": 0.6}, "result": "FAIL", "note": "0.6 too strict on pilot"}'
```

The ledger is append-only and hash-chained: entries can be added, never
silently edited, reordered, or deleted. It blocks nothing — it makes the quiet
room audible.

## Confirmation room: the four steps, in order

**1. Freeze thresholds (before the experiment exists in results form):**

```bash
python -m gate_harness.prereg lock <gate_dir> \
  --thresholds-json '{"recovery_rmse_max": 0.5, "information_ratio_min": 0.5}' \
  --exploration-basis EXPLORATION.jsonl   # or: none
```

`--exploration-basis` is mandatory and has exactly two honest values: `none`
("no exploratory runs informed these thresholds" — a checkable declaration) or
a ledger path (the runs that did inform them, with their hash-chain head
frozen into the prereg). Silence is not an option.

**2. Commit the prereg alone** — `PREREG.json` + `PREREG.lock` in their own
commit, containing no outputs. The runner verifies the lock's commit is a
strict git ancestor of the run.

**3. Run through the harness** — the experiment calls
`gate_harness.runner.run_gate(gate_dir, experiment_fn, leakage_report=...,
tautology_report=..., evaluation_oracle_log=...)`; see
`examples/hello_gate/run.py` for the complete 140-line pattern. For grouped
data (patients, subjects, batches) also run, before the verdict:

```python
from gate_harness.split_integrity import assert_group_split_integrity
from gate_harness.preprocessing_order import assert_preprocessing_order

assert_group_split_integrity(groups, splits, declared_group_key="patient_id")
assert_preprocessing_order([your_pipeline_fn])
```

**4. Verify before citing:**

```bash
python -m gate_harness.verify_decision <gate_dir>/decision.json
```

Only a decision that prints `VALID` may be cited — and `VALID` means
*harness-valid* (procedural compliance under the declared spec), never
"scientifically true". State this distinction when you report.

## When the knife refuses

Every refusal carries a `next:` action. Do the action; never work around the
refusal. The common ones:

| refusal | it means | next |
|---|---|---|
| lock rev not a strict ancestor of HEAD | prereg wasn't committed before the run | commit `PREREG.*` alone, re-run |
| PREREG SHA mismatch | thresholds edited after locking | re-lock deliberately (the change becomes part of the record), commit, re-run |
| no exploration_basis | silent about exploratory runs | pass `none` explicitly, or cite the ledger |
| ledger CHAIN-INVALID | ledger edited/truncated after the fact | the edited ledger is not citable; keep it as evidence, start a new one |
| leakage scan hit | a truth name in the fit path | remove the dependence, not the name |
| groups_crossing_splits | same patient/group in train and test | re-split group-aware (e.g. GroupKFold) |
| fit_on_presplit_data / fit_before_split | transformer fit saw test rows | split first; fit on the train fold only |
| INVALID decision.json | bypassed runner or stale harness | re-run through `run_gate` against the current harness |

## What this instrument cannot do (say so in your reports)

It cannot judge whether the question is meaningful, the metric measures the
right object, or a control can actually fire — a worthless question can be
executed harness-validly. It cannot see exploration done outside the ledger.
And it does not solve the same-hand problem: if you wrote the experiment, the
prereg, and the analysis in one session, the two-phase commit protects the
*order*, not the origin, of the thresholds — the ledger makes the origin
visible, a second implementer makes it checked. The complete taxonomy of what
slips past is Appendix A of the fallacy-cutter essay; cite it rather than
overclaiming what a green gate proves.
