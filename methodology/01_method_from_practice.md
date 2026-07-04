# 01 — The method as actually practiced

Reverse-engineered from the worked examples that *succeeded as method* (i.e.
produced an honest, defensible decision), not from the playbook drafts. Each step
cites the worked example(s) that demonstrate it. Steps with no worked example are
marked `unsupported-by-practice`.

Tags: **FACT** (demonstrable), **INFERENCE** (my reading).

---

## The procedure, as practiced

### Step 1 — Frame one decisive question with a kill condition

**FACT.** Each worked experiment states a single decisive question and a verdict
vocabulary in which "fail" is a first-class outcome.
- 18.1 task spec: "Does the 2-counter shield correctly classify real justitia
  states?" with explicit verdicts `fidelity_ok | fidelity_fails_false_safe |
  fidelity_conservative`.
- JB0: "Does standard CEGAR produce a useful boundary?" verdict
  `Conservative_but_vacuous`.
- FA2.5: "Does a faithful candidate exist?" verdict `No_discriminative_candidate`.

**INFERENCE.** The question is chosen so that one measurement can *kill* the line.
The verdict set is fixed in advance and includes named failure verdicts.

### Step 2 — Pre-register the kill threshold in code, before measuring

**FACT (strongest single piece of evidence).**
`experiments/JB/18_1_shielded_training/outputs_18_1/level_A_preregistration.json`
fixes `threshold: 0.05`, the decision rule, the ground-truth definition, and the
note *"Threshold fixed here, in code, before the confusion matrix is computed; it
is not moved to fit the result."* The 18.1 task spec mandates writing this file
"BEFORE computing the confusion matrix." The summary confirms it was not moved.

**INFERENCE.** Pre-registration is the load-bearing anti-Goodhart move. It is the
difference between a kill-gate and a post-hoc rationalization.

### Step 3 — Require positive AND negative controls; an instrument that cannot detect failure cannot confirm success

**FACT.** The 18.1 task spec makes three controls mandatory: a `control learner`
(unfiltered, equal data volume), random/majority baselines, and a
*trivially-safe / no-op baseline* — with the explicit rule "if it matches the
shielded learner on safety, the shielded learner's safety is trivial." Equal data
volumes are required so "safer" does not confound with "less data."

**FACT.** 18.1's Level A reports a *policy-independent purity signal* (of states
ALREADY collapsed, 19.3% labeled SAFE) — a check that needs no lookahead and no
policy, i.e. an instrument that cannot be gamed by the analysis pipeline.

**INFERENCE.** The 15.x origin of this rule ("keep falsification cheap; identical-
except-the-filter design") is cited in the 18.1 task spec itself
("lesson from 15.x").

### Step 4 — The kill-gate halts downstream work; do not run Level B behind a failed Level A

**FACT.** 18.1: false_safe 0.299 > 0.05 → "Level B: not_run." The summary: "training
behind a lying shield manufactures false confidence." The task spec: "Do not run
Level B if false_safe_rate exceeds the pre-registered threshold."

**INFERENCE.** The gate is not advisory. A failed gate stops the pipeline; results
computed downstream of a failed precondition are treated as artifacts, not data.

### Step 5 — Separate FACT / INFERENCE / HYPOTHESIS in the output

**FACT.** `Door1_Extracted_Knowledge_v1.md` tags every durable result FACT /
INFERENCE / HYPOTHESIS and states "only FACT and directly supported INFERENCE are
intended to survive." `01_empirical_basis.md` uses [FACT]/[INFERENCE] per result
and isolates a "What Has NOT Been Demonstrated" section.

**INFERENCE.** The discipline is enforced at *write-up* time, not just analysis
time. The negative-space section ("what was NOT shown") is mandatory.

### Step 6 — "Decidability/result bought by simplification?" — check what the abstraction or metric discarded

**FACT.** BA4 layer audit asks exactly what each variable's *role* is and flags
that 18.0's projection dropped `total_mass` and `failed_zone_count` — the
coordinates whose loss produced the false-safe blindness. 15.2's structural caveat:
the exponential class count is "the combinatorially trivial exponential — maximal
diversity with zero structure," i.e. an "open" result bought by a free-monoid
simplification, not by real structure.

**INFERENCE.** Whenever a step makes something tractable (a projection, a compact
metric, an abstraction), the method demands an explicit accounting of what was
discarded, and treats a "clean" result as suspect until that accounting is done.

### Step 7 — Non-saturation is inconclusive; only exhaustion/saturation informs

**FACT.** 15.2 honesty note: "Non-saturation under a budget is never a positive
signal; we only ever claim openness from points that are *exactly* exhausted." The
scaling law was fit only on exhausted points; censored points were excluded.

**INFERENCE.** "We didn't find a bound" is not evidence of no bound. Only an
exhausted search (or a saturated metric) carries information.

### Step 8 — Compression / coverage is not discrimination; refuse constructive claims without the discriminating measurement

**FACT.** FA2.5 refused to call a 99.83%-coverage proxy a success because precision
could not be estimated (true SAFE states absent); the compact candidate failed the
precision margin (−0.084 vs required +0.05) and was ruled
`Equivalent_to_standard_history_refinement`. `01_empirical_basis.md` §6: "Witness
coverage alone is insufficient … compression alone should never be interpreted as
constructive progress."

**INFERENCE.** An elegant/compact description is not evidence of the target
property. The method withholds the positive verdict until the *discriminating*
metric (precision against real negatives) is in hand.

### Step 9 — Treat a negative result as an anchor, not a defeat; extract durable constraints

**FACT.** `Door1_Extracted_Knowledge_v1.md`: "Negative results reduce future search
space"; it converts the Justitia failure into a 6-item empirical design checklist
for future candidates and an explicit closed/open ledger. JB0 and FA2.5 close
specific directions while leaving the objective open.

**INFERENCE.** The output of a kill is a constraint on the next search, stated so
it survives even if the failed artifact is abandoned.

### Step 10 — Parallel-reality check: does this step serve the goal, or is it theory-for-theory?

**FACT.** 15.2 explicitly separates "the COUNT is unbounded by structure" from "the
meanings are non-trivial," and orders a learnability probe *before* any
architectural/substrate claim — refusing to let an interesting count stand in for
the goal. The Claude review (`Claude_kill-gate_review.md`) names the inverse failure
in the programme: "a disciplined harness pointed at a target that quietly moved …
form-rich and substance-deferred."

**INFERENCE.** The method repeatedly asks whether the current activity advances the
actual objective or only the theory about it. This is the move that catches goal
drift.

### Step 11 — Apply the same gates to the programme itself (programme-gate layer)

**FACT.** KG0 treats the research programme as a scientific object: criticism is
"evidence, not authority"; the burden of proof lies on the programme; the verdict
`continue_after_revision` froze expansion until KG1–KG3. KG_SPEC formalizes this.

**INFERENCE.** This is a genuine extension of the experimental method to the meta
level, but it is N=1 (only KG0 has fired). See `03_not_yet_method.md`.

---

## Steps in the playbook drafts with NO worked example

`unsupported-by-practice` (aspirational, not yet method):

- **The 8 headers of `playbook/00_monograph_kill_gates.md`** (Claim Traceability,
  Counterexample Section, Alternative Hypothesis Section, What Survives If False,
  Existing-Theory Reduction Check, Human/LLM Usability Check) — **FACT:** zero of
  these has a worked instance *under that name*. Several map onto real practice
  (e.g. "Alternative Hypothesis" ≈ JB0's baseline comparison; "What Survives If
  False" ≈ Door1's durable-constraint extraction; "Existing-Theory Reduction" ≈
  KG2/KG6, not yet fired), but as section headings in the playbook they are empty.
- **KG1–KG6** (`KG_PIPELINE.md`) — **FACT:** all marked Pending; specced, never
  executed. The "Goal Anchor Identity Gate" (KG1) has a spec but no run.
- **"Review packet discipline" / "decision JSON patterns"** named in
  `playbook/01` and `playbook/02` — **INFERENCE:** these *do* exist in practice
  (final_decision.json files, FA REVIEW_PACKET) but the playbook only *points at*
  them; it does not contain the extracted procedure.

---

## The recurring disciplinary moves, named

Consolidated from the steps above (each backed by ≥1 worked example):

1. **Pre-registration** of the kill threshold before measuring (18.1).
2. **Positive + negative + trivially-safe controls**; equal-volume; an instrument
   that cannot detect failure cannot confirm success (18.1, 15.x).
3. **Kill-gate halts downstream** (18.1 Level B not run).
4. **FACT / INFERENCE / HYPOTHESIS separation**, incl. a mandatory "what was NOT
   shown" section (Door1, FA empirical basis).
5. **Non-saturation-is-inconclusive**; only exhaustion informs (15.2).
6. **"Bought by simplification?"** — account for what an abstraction/metric
   discarded (BA4, 15.2 free-monoid caveat).
7. **Compression/coverage ≠ discrimination** (FA2.5).
8. **Negative result = anchor**, extract durable constraints (Door1).
9. **Parallel-reality check** against the actual goal (15.2; Claude review).
10. **Programme-level gates** — apply the method to the programme (KG0). *N=1.*
