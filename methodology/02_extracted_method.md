# 02 — Extracted method (ONLY what passed)

Contains only: (a) steps with worked-example support, (b) harness components that
ran. Each item is evidence-tagged with the gate/experiment that demonstrates it.
Nothing here is padded to look more complete than it is; the aspirational
remainder is in `03_not_yet_method.md`.

Tags: **FACT** (demonstrated), **INFERENCE**.

---

## Part 1 — Disciplinary steps with worked-example support

These ten moves each have at least one worked example and are therefore extracted
as method (full derivation in `01_method_from_practice.md`):

| # | move | one-line rule | demonstrated by |
|---|---|---|---|
| 1 | Pre-registration | fix the kill threshold in a file, in code, before measuring; attest it was not moved | **FACT:** `level_A_preregistration.json` (18.1) |
| 2 | Controls | require negative + trivially-safe + equal-volume controls; report a policy-independent purity signal; an instrument that can't detect failure can't confirm success | **FACT:** 18.1 task spec; FA2.5 baselines; JB0 baseline table |
| 3 | Halt-downstream | a fired gate stops the pipeline; downstream results are artifacts | **FACT:** 18.1 "Level B: not_run" |
| 4 | FACT/INFERENCE/HYPOTHESIS split + mandatory "what was NOT shown" | tag every claim; isolate the negative space | **FACT:** Door1; FA `01_empirical_basis.md` §8 |
| 5 | Non-saturation-is-inconclusive | claim openness only from exhausted/saturated points; exclude censored ones | **FACT:** 15.2 |
| 6 | "Bought by simplification?" | account for what each abstraction/metric discarded before trusting a clean result | **FACT:** BA4; 15.2 free-monoid caveat |
| 7 | Compression/coverage ≠ discrimination | withhold the positive verdict until the discriminating metric (precision vs real negatives) is in hand | **FACT:** FA2.5 (precision margin −0.084) |
| 8 | Negative-result-as-anchor | convert each kill into a durable constraint on the next search | **FACT:** Door1 design checklist; JB0/FA2.5 closed-direction ledger |
| 9 | Parallel-reality check | ask whether the step serves the goal or only the theory; separate "count-open" from "meaning-non-trivial" | **FACT:** 15.2; **INFERENCE** corroborated by `Claude_kill-gate_review.md` |
| 10 | Programme-level gates | apply the same falsification to the programme itself; criticism = evidence not authority; burden on the programme | **FACT:** KG0 (`continue_after_revision`) — **N=1** |

**INFERENCE.** Items 1–9 are robustly multiply-demonstrated across BA/FA/JB/15.x.
Item 10 has a single worked example (KG0) and is included with that caveat.

## Part 2 — Output schema fields that a worked example actually produced

Extracted in `harness/output_schema.md`. The fields that are **demonstrably
present** in ≥1 worked example: Question, Pre-registered threshold (18.1 only),
Metric, Controls, Decision, Downstream consequence, FACT/INFERENCE split,
What-was-discarded, Durable constraint. The programme-gate section set
(Scope/Question/Evidence/Competing hypotheses/Analysis/Decision/Consequences) is
demonstrated by KG0.

## Part 3 — Harness components that ran in this pass

| component | status | file |
|---|---|---|
| Visibility rules (3 modes, cross-mode R1–R5) | drafted + applied to the usability test | `harness/visibility_rules.md` |
| Output schema | drafted from worked examples | `harness/output_schema.md` |
| Failure conditions F1–F8, transcription tests T1–T4 | drafted + evaluated against current playbook (all F triggered) | `harness/failure_conditions.md` |
| Usability test 01 (Mode 3, two runs) | **ran**; produced an honest gap list | `harness/usability_test_01_report.md` |

**FACT.** The usability test executed and produced a result: the playbook cannot
drive the 18.1 decision (Run A); the task-spec genre can (Run B). This is a real
harness output, not a plan for one.

---

## What this means

**INFERENCE.** The *experimental kill-gate method* (Part 1, items 1–9) is the
genuinely extracted, transferable artifact in this repo. It is demonstrated by
multiple independent honest negatives and is encoded concretely enough
(thresholds, controls, halt rules) to be re-used. Its current problem is **location,
not existence**: it lives in experiment task specs, not in the playbook directory.

**INFERENCE.** The *programme-gate method* (item 10) is a promising extension with
one worked example; it is extracted as a documented pattern but not yet as a
*tested* method (KG1–KG6 unfired).
