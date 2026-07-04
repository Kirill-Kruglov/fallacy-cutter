# harness/visibility_rules.md — three test modes and file visibility

Formalizes the three test modes the snapshot (`repo_reorg_inventory/
current_repo_state_for_playbook_test.md`, §3 and §9) identifies. The purpose of
visibility rules is to prevent the most common way these tests cheat: an agent
reading the answer (or another agent's answer) and reproducing it as if it had
executed the method.

Tags: **FACT** (drawn from the snapshot), **INFERENCE**, **RECOMMENDATION**.

---

## Why visibility rules exist

**INFERENCE.** A "fresh agent reproduced the decision" result is only meaningful if
the agent could not have *transcribed* the decision. Three things must be hidden by
default in any reproduction test:

1. the already-computed decision (the worked-example summary / final_report);
2. any higher-level review that pre-judges the question (KG0, the Claude review);
3. any other agent's answer.

The mode determines which of these is visible, because the modes ask different
questions.

---

## Mode 1 — Blind reconstruction (snapshot Package A)

**Question:** can an agent reconstruct project history / re-derive a question
without the programme-gate scaffolding biasing it?

| visible | hidden |
|---|---|
| `README.md`, `research/README.md` | `KG0_programme_review.md` |
| in-tree historical memos (esp. `research/monograph_17/Memo_v1.3_17.md`) | `PR1_programme_revision.md` |
| monograph_17 index / methodology / chronicle / ledger | `KG_SPEC.md`, `KG_PIPELINE.md`, `KG1_SPEC.md` |
| `Door1_Extracted_Knowledge_v1.md` | `research/Claude_kill-gate_review.md` |
| `BRIDGE_MAP_18_1_TO_FA2.md` | any other agent's answer |
| Substrate Discovery chapters `00_*`–`09_*` | the post-KG verdicts |

**FACT.** This mirrors snapshot §9 Package A exactly.

## Mode 2 — Programme-gate execution (snapshot Package B)

**Question:** can an agent *apply* the programme-gate methodology (e.g. execute
KG1) rather than rediscover it?

| visible | hidden |
|---|---|
| `KG_SPEC.md`, `KG_PIPELINE.md`, `KG1_SPEC.md`, `PR1_programme_revision.md` | `KG0` *if the test wants a fresh KG1 decision rather than KG0 replication* |
| evidence corpus: Door1, BRIDGE_MAP, FA basis, BA/FA/JB reports, monograph_17 memos | `research/Claude_kill-gate_review.md` unless the task is about the KG0 chain |
|  | any other agent's answer |

**FACT.** Mirrors §9 Package B. The KG/PR layer is visible here because the goal is
to apply the method, not to rediscover it.

## Mode 3 — Playbook usability (snapshot Package C)

**Question:** is the playbook/procedure usable by a fresh agent — can the agent
execute a decision from the *procedural artifacts plus a small evidence packet*,
and honestly report what is missing?

| visible | hidden |
|---|---|
| `research/playbook/README.md`, `00`–`04` | the worked-example **decision/summary** for the target gate (this is the answer key) |
| `KG_SPEC.md`, `KG_PIPELINE.md` | `research/Claude_kill-gate_review.md` |
| one small evidence packet (e.g. 18.1 *inputs*, BA4 audit, Door1 extraction) | any other agent's answer |

**RECOMMENDATION (a tightening of Package C).** Package C as written lists "18.1
summary" as visible. For a *reproduction* test that is self-defeating: the 18.1
summary already states the decision (false_safe 0.299 > 0.05, Level B not run). To
test whether the *playbook* can drive the decision, the worked-example summary and
its `level_A_decision.json` must be **hidden**, and only the raw inputs
(`level_A_preregistration.json` may also be hidden if testing whether the agent can
*derive* the need to pre-register) plus the playbook should be visible. See
`usability_test_01_report.md`, which runs the test under this tightened rule.

---

## Cross-mode rules (apply to all three)

**RECOMMENDATION.**

- **R1 — Answer-key hidden.** The target decision document is never visible in a
  reproduction test. If it must be visible (e.g. to grade), it is revealed only
  *after* the agent commits its decision.
- **R2 — No sibling answers.** No other agent's output for the same task is visible.
- **R3 — Review layers hidden by default.** KG0 and the external Claude review
  pre-judge questions; hidden unless the task is explicitly about them.
- **R4 — Declare inputs.** Per KG_SPEC, "implicit inputs are forbidden." The agent
  must list every file it used; anything not on the visible list is a leak.
- **R5 — Provenance of the threshold.** The agent must state *where* a
  pre-registered threshold came from. If it cannot locate it in the visible set,
  that is a recorded gap, not a number to invent.
