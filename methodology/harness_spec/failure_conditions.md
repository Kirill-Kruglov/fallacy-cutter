# harness/failure_conditions.md — what counts as the playbook being exposed as incomplete

These are the conditions under which a usability test has *succeeded at its real
job*: surfacing that the playbook does not yet contain a transferable method. The
success criterion of the usability test is inverted — it succeeds by exposing
gaps, not by producing a clean decision.

Tags: **INFERENCE**, **RECOMMENDATION** unless marked FACT.

---

## A failure condition is triggered when a fresh agent, using only the visible procedural set, cannot…

| # | failure condition | why it exposes a gap | met by current playbook? |
|---|---|---|---|
| F1 | **determine the kill threshold** (e.g. 0.05 for 18.1) from the playbook alone | the threshold lives in `level_A_preregistration.json` and the task spec, not in `research/playbook/*` | **FACT: yes, triggered** (see usability_test_01) |
| F2 | **know it must pre-register** before measuring | no playbook file states the pre-registration rule | **FACT: yes, triggered** |
| F3 | **tell which files are evidence vs argument** | playbook gives no evidence/argument taxonomy; the snapshot does, but the snapshot is not in the playbook | **FACT: yes, triggered** |
| F4 | **know which controls are mandatory** (negative + trivially-safe + equal-volume) | the controls rule lives in the 18.1 task spec, not the playbook | **FACT: yes, triggered** |
| F5 | **know that a fired gate halts downstream** | the "do not run Level B" rule is in the task spec, not the playbook | **FACT: yes, triggered** |
| F6 | **reproduce the decision** without reading the answer key (the worked-example summary) | if reproduction requires the summary, the method is not in the playbook | **FACT: yes, triggered** |
| F7 | **produce the required output fields** (`output_schema.md`) from the playbook's own instructions | `playbook/00` is 8 empty headers; it specifies no field content | **FACT: yes, triggered** |
| F8 | **distinguish a programme-gate from an experimental kill-gate** | KG_SPEC is programme-level; the 18.1 task is experimental; the playbook does not bridge the two levels | **FACT: yes, triggered** |

**INFERENCE.** All eight conditions are currently triggered. The honest reading:
the playbook directory does not yet encode the method; the method is encoded in
the experiment task specs and durable-lesson docs, which are *outside* the
playbook's visible set.

---

## Distinguishing a real reproduction from a transcription

**RECOMMENDATION.** A claimed "reproduction" must be rejected as a *transcription*
if any of:

- **T1** — the agent's decision matches the worked example but the agent had the
  worked-example summary/decision file in its visible set (it read the answer).
- **T2** — the agent states the threshold but cannot cite where in the *playbook*
  it came from (it imported tacit knowledge or invented the number).
- **T3** — the agent's output omits the pre-registration provenance (field 2 of
  `output_schema.md`): it cannot have pre-registered if it never said where.
- **T4** — the agent supplies a control/threshold the playbook never specified and
  does not flag it as a gap (it silently patched the method's holes).

**INFERENCE.** T1–T4 are why "a clean decision" is the *suspicious* outcome, not
the reassuring one. The trustworthy outcome of a current-state usability test is a
list of triggered F-conditions plus an honest "I could not execute this from the
playbook alone."

---

## When the playbook would PASS (future bar)

**RECOMMENDATION.** The playbook becomes a transferable method when a fresh agent,
in Mode 3 with the answer key hidden, can:

1. derive the need to pre-register and locate/justify the threshold from the
   playbook (clears F1, F2);
2. enumerate the mandatory controls and the halt-downstream rule from the playbook
   (clears F4, F5);
3. emit every `output_schema.md` field (clears F7);
4. reach the *same* decision the worked example reached, with the answer key hidden
   (clears F6 without triggering T1–T4).

Until then, the honest status is: **method demonstrated in practice, not yet
externalized into the playbook artifact.**
