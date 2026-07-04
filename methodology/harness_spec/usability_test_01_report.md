# harness/usability_test_01_report.md — fresh-agent usability test (Mode 3)

**Success criterion is inverted.** This test succeeds if it honestly surfaces what
the playbook fails to specify. A clean decision would more likely mean the agent
used tacit knowledge the playbook does not contain. I ran the simulation under the
tightened Mode-3 rule (answer key hidden) and report what the playbook failed to
provide — I did **not** patch the gaps myself.

Tags: **FACT** (what the visible files do/do not contain), **INFERENCE**,
**RECOMMENDATION**.

---

## Setup

**Visible to the simulated fresh agent (procedural):**
- `research/playbook/README.md`, `00_monograph_kill_gates.md`,
  `01_playbook_extraction_plan.md`, `02_source_artifact_map.md`,
  `03_preservation_rule.md`, `04_repository_philosophy.md`
- `research/substrate_discovery_v1/KG_SPEC.md`, `KG_PIPELINE.md`

**Visible (evidence packet — inputs only):**
- `experiments/JB/18_1_shielded_training/claude_code_task_18_1_shielded_training.md`
  *(the task design)* — see note below on whether this should count as "playbook"
- `experiments/BA/BA4_layer_audit/justitia_layer_audit.md`
- `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`

**Hidden (answer key — per visibility R1):**
- `outputs_18_1/summary.md`, `level_A_decision.json`,
  `abstraction_fidelity_report.json`, `level_A_preregistration.json`

**Task given to the agent:** "Execute the 18.1 Level-A fidelity kill-gate decision
from these artifacts alone. Pre-register the threshold, state the decision, and
list every input you used."

---

## Two runs, because the packet is ambiguous

The task brief lists "18.1 summary" in the evidence packet, but the summary *is*
the answer. I therefore ran the test twice to separate "can the playbook drive the
decision" from "can the agent transcribe an answer."

### Run A — strict (answer key AND task spec hidden; only `research/playbook/*` + KG_SPEC + BA4 + Door1)

**FACT — what the agent can find:**
- `playbook/00` lists section headers including "Failure Conditions" and
  "Counterexample Section" — but **no content, no threshold, no procedure.**
- `playbook/02` *tells the agent where the method would come from* ("extract
  preregistration discipline from `experiments/*/SPEC*`") but does not contain it.
- `KG_SPEC` describes a *programme* gate (Continue/Reject decisions about the
  research programme); it never mentions false_safe rate, 0.05, confusion
  matrices, or how to pre-register an experimental threshold.
- BA4 tells the agent *which coordinates 18.0 was blind to* (`total_mass`,
  `failed_zone_count`) — useful context, but not a decision rule.
- Door1 says "projection blindness is a real failure mode (FACT, 18.1)" — i.e. it
  *states the conclusion* but gives neither the metric nor the threshold.

**Outcome (Run A): the agent CANNOT execute the gate.** It cannot determine:
- the metric (false_safe_rate) — not named in any visible procedural file;
- the threshold (0.05) — absent everywhere visible;
- the pre-registration requirement — stated in no playbook file;
- that a fired gate halts Level B — stated in no playbook file;
- the mandatory controls — stated in no playbook file.

**Honest agent output (Run A):** "I cannot execute this decision from the
playbook. The playbook directory names the disciplines (pre-registration,
kill-gates, evidence ledger) but contains none of their content. `00_monograph_
kill_gates.md` is empty headers. KG_SPEC is a *programme*-governance spec at the
wrong level for an experimental fidelity gate. From BA4 and Door1 I can infer the
*existence* of a false-safe failure but not the rule that decides it. Triggered
failure conditions: F1, F2, F4, F5, F7, F8 (see `failure_conditions.md`)."

### Run B — as-briefed (task spec visible, answer key hidden)

When the **18.1 task spec** is visible, the picture changes sharply — because the
task spec, *not the playbook*, contains the method:

**FACT — the task spec supplies what the playbook lacks:**
- the metric and decision rule (`fidelity_ok ≤ 0.05`, `fails_false_safe > 0.05`);
- the explicit instruction to write `level_A_preregistration.json` *before*
  computing the matrix;
- the mandatory controls (control learner, trivially-safe baseline, equal volume);
- the halt rule ("Do not run Level B if false_safe exceeds the threshold").

**Outcome (Run B): the agent CAN pre-register and would execute correctly** — but
only because it is reading the method out of the *experiment task spec*, which is
not part of `research/playbook/*`. With the answer key hidden the agent would
still need to actually run justitia to get the 0.299; given only the *inputs* it
can set up the gate and state the decision rule, but cannot produce the metric
without computation. It would *not* be a transcription (T1–T4 not triggered),
because the summary was hidden.

---

## The finding

**FACT.** The method required to execute the 18.1 kill-gate is fully present in the
repo — in `claude_code_task_18_1_shielded_training.md` and
`level_A_preregistration.json`. It is **absent from `research/playbook/*`**, the
directory that claims to be the playbook.

**INFERENCE.** The playbook does not yet encode the method; it encodes *pointers
to* the method. The transferable knowledge currently lives in:
1. the per-experiment task specs (the "Claude analyst, via Kirill" prompts), and
2. the pre-registration JSON files and durable-lesson docs (Door1, FA basis).

A fresh agent handed only the playbook fails (Run A). A fresh agent handed a task
spec succeeds (Run B) — which proves the *task-spec genre*, not the playbook, is
the real procedural artifact.

**INFERENCE — the deeper risk.** This is exactly the failure mode the playbook is
meant to prevent, occurring in the playbook itself: form (named sections, a
philosophy, a preservation rule) is present; substance (the decision rules,
thresholds, control requirements) is deferred. `Claude_kill-gate_review.md`
diagnosed the same pattern in the substrate chapters ("form-rich and
substance-deferred"); it applies to the playbook too.

---

## Playbook gaps surfaced (the deliverable of this test)

The playbook failed to specify, and must externalize before it transfers:

1. **the pre-registration requirement and its mechanics** (write the threshold to a
   file, in code, before measuring; attest it was not moved);
2. **how to choose/justify a threshold** (0.05 for a safety classifier's dangerous
   error — the *reasoning*, so a new gate can set its own);
3. **the mandatory-controls list** (negative control, trivially-safe baseline,
   equal-volume, policy-independent purity check);
4. **the halt-downstream rule** (a fired gate stops the pipeline; downstream
   results are artifacts);
5. **the output schema** (the empty headers of `00` must become the fields in
   `output_schema.md`, each with an example);
6. **the evidence-vs-argument taxonomy** (which files decide, which only frame);
7. **the level distinction** (experimental kill-gate vs programme gate — the
   playbook currently bridges neither).

**RECOMMENDATION.** Do not fix these by hand inside this pass and then declare the
playbook complete — that would re-commit the original sin. The fix is a separate,
explicit extraction step (populate `playbook/00` from the task-spec genre, with
worked examples cited), followed by a *re-run of this usability test with the
answer key hidden* to confirm Run A then succeeds. Until that re-run passes, the
status is unchanged: method demonstrated, not yet externalized.
