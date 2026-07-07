# 04 — First field transfer test (justitia, July 2026)

The extraction pass in this directory ended with an honest verdict
([`SUMMARY.md`](SUMMARY.md), [`03_not_yet_method.md`](03_not_yet_method.md)):
the instrument is real; the transferable playbook is not yet built; the method
travels through task specs and expert habit, not through documents alone. That
verdict was based on a *simulated* fresh-agent test. This file records the first
**field** test: applying fallacy-cutter to a foreign project end to end.

Tags as in the rest of this directory: **FACT** (demonstrated, cited),
**INFERENCE** (my reading).

## Protocol

A fresh agent (Codex, GPT-5.5) was asked to harness
[justitia](https://github.com/Kirill-Kruglov/justitia) — a governance-simulation
study with published results — using **only** this repository's documents
(README, `methodology/`, `examples/hello_gate/`, `gate_harness/README.md`) plus
a gate specification written by the author's reviewer. The agent kept a live
[`TRANSFER_LOG.md`](https://github.com/Kirill-Kruglov/justitia/blob/main/TRANSFER_LOG.md)
recording every point where these documents were insufficient. Three gates were
defined: one confirmatory replay of published thresholds and two genuinely
prospective experiments with kill-conditions locked before the runs.

## What transferred (FACT)

- `gate_harness/` vendored **byte-identical** into the foreign repo; every module
  ran unmodified on a stdlib-only project it had never seen.
- Two-phase preregistration held end to end: three `PREREG.lock` commits strictly
  preceding their runs; the cross-gate threshold-change guard (finding #9) fired
  correctly on overlapping keys between prospective gates and was satisfied with
  a written rationale, not bypassed.
- Three provenance-signed decisions, all `VALID` by the independent verifier:
  - **J-G1** replay: PASS — 22/22 frozen expectations, headline permanence
    reproduced exactly.
  - **J-N1** adversary battery: **FAIL published as a finding** — observables
    carry sufficient statistics (0.994 held-out balanced accuracy).
  - **J-N2** speed-limit partial isolation: **FAIL published as a kill** —
    monotone in the preregistered ratio, equal-ratio equivalence broken.
- Outcome-independence survived contact with disappointing results: both FAILs
  were committed as-is, and the host project's essay was *corrected* against
  them rather than the results being softened.

## What did not transfer (FACT)

Six gaps logged in `TRANSFER_LOG.md`, verbatim in the log, summarized:

1. `install_hooks.sh` cannot install into a linked git worktree.
2. No schema or recipe for **domain-specific tautology reports** when
   `gate_harness.tautology_check`'s variance ratio does not apply.
3. `runner.run_gate` does **not** enforce `seed_policy`; gate code must call it
   — nothing in the docs says so.
4. No guidance for prospective gates whose required dials do not exist in the
   host model (the agent correctly stopped and escalated).
5. No documented exclusion rule for the vendor-verification diff
   (`__pycache__`).
6. **The serious one:** `run_gate` requires the tautology report *before*
   `experiment_fn` runs; for an experiment that produces its own baseline data,
   the first wrapper defaulted to a hardcoded
   `construction_may_be_tautological: false` — the exact fail-open anti-pattern
   of finding #3, reproduced in the harness's own glue code. **It was caught by
   external review, not by the harness.** The repair (a two-step run/gate
   protocol with a fail-closed run stamp) is now part of the host project.

## What this changes (INFERENCE)

- The diagnosis of `03_not_yet_method.md` is **confirmed in the field**, not
  softened: the *instrument* is portable; the *method* still traveled through an
  expert-written spec — the task-spec genre again, exactly as the usability test
  predicted. "Tested once, partially" replaces "untested".
- Gap 6 is the important lesson: the knife does not protect its own wiring. Gate
  glue code is exactly as dangerous as experiment code, and a fail-open default
  can reintroduce finding #3 one layer above the modules that guard against it.
  A future runner needs either a documented pattern for post-run audit reports
  or a mechanical check that no report handed to `run_gate` is a constant.
- Roadmap additions, in order of cost: worktree support in the hook installer;
  a documented vendor-diff rule; a `seed_policy` hook in the runner; a
  domain-tautology recipe; a constant-report detector.

## Second wave on the same host (FACT, July 2026)

Three more gates ran days later on the same host project: a prospective
held-out world (FAIL as a boundary finding), an **engineering equivalence
gate** for a substrate extension (PASS: with three new dials at neutral
defaults, 18/18 committed headline cells reproduced exactly, under an explicit
no-extra-RNG contract), and a prospective five-dial isolation (FAIL on all
three preregistered hypotheses, published as-is). Two observations for the
methodology:

- The equivalence-gate pattern — *extend the model only behind a preregistered
  gate whose expectation is byte-identical behavior at neutral defaults* — is a
  reusable discipline this repository did not document; it should join the
  playbook.
- The transfer log gained **one** new entry in wave 2, against six in wave 1,
  with the same agent and the same documents. **INFERENCE:** the method
  transfers through accumulated practice faster than through prose — which is
  the task-spec diagnosis of `03_not_yet_method.md` restated as a learning
  curve, not a refutation of it.

## What this does not show (FACT)

One test (in two waves), one host project, same forge: the reviewer who wrote
the gate specs and the agent that executed them share context with this
repository's author. It does not show that a stranger, with no expert in the
loop, could do the same — that remains the unmet bar from `SUMMARY.md`.
