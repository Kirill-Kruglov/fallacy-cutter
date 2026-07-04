# 03 — Not yet method (gaps, aspirational steps, tacit knowledge)

The honest remainder. If this file is longer or heavier than `02_extracted_method.md`,
that is the true current state and is reported as such — not padded down.

Tags: **FACT**, **INFERENCE**, **RECOMMENDATION**.

---

## A. Playbook steps with no worked example (aspirational)

| item | status | note |
|---|---|---|
| `playbook/00_monograph_kill_gates.md` — 8 section headers | **FACT: aspirational.** Zero body content. | Several headers map onto real practice but none is populated *under that name*. |
| "Claim Traceability" | aspirational | no worked instance under this name |
| "Counterexample Section" | aspirational | closest practice: FA1 witness taxonomy (populations, not single counterexamples) — not yet written as a playbook step |
| "Alternative Hypothesis Section" | aspirational | closest practice: JB0/FA2.5 baseline comparison — not extracted into the playbook |
| "What Survives If False" | aspirational | closest practice: Door1 durable-constraint extraction — not extracted into the playbook |
| "Existing-Theory Reduction Check" | aspirational | maps to KG2/KG6 — **both unfired** |
| "Human/LLM Usability Check" | aspirational | this very harness is the first instance; not yet a playbook step |
| KG1–KG6 (`KG_PIPELINE.md`) | **FACT: aspirational.** All Pending. | Specced, never executed. The Goal-Anchor Identity Gate (KG1) has a spec and required inputs, but its required input "original memos v1.1–v1.4" is partly **missing from the tree** (snapshot §8) — KG1 cannot currently be run as specified. |
| KG_SPEC as a *tested* method | **FACT: drafted-only.** | Only KG0 has instantiated it; spec + first use were co-authored (N=1, self-referential). |

## B. Gaps the usability test exposed (from `usability_test_01_report.md`)

**FACT.** All eight failure conditions F1–F8 are triggered by the current playbook.
The playbook fails to specify:

1. the pre-registration requirement and its mechanics;
2. how to choose/justify a threshold (the *reasoning*, not just a number);
3. the mandatory-controls list (negative, trivially-safe, equal-volume, purity);
4. the halt-downstream rule;
5. the output schema (the empty `00` headers → fields with examples);
6. the evidence-vs-argument taxonomy;
7. the experimental-gate vs programme-gate level distinction.

## C. Tacit knowledge that must be made explicit before the method transfers

**INFERENCE.** The method currently depends on knowledge that exists only in the
task-spec genre and in Kirill+analyst conversation history, not in any reusable
procedural file:

| tacit knowledge | where it currently lives | why it must be externalized |
|---|---|---|
| "pre-register in code before measuring; never move the bar" | 18.1 task spec prose; the JSON's `note` field | the single most important move; nowhere in the playbook |
| how a *new* gate picks its threshold and metric | implicit in each task spec, re-derived each time | a transferable method needs a threshold-selection procedure, not 1 example |
| the controls suite (esp. the trivially-safe baseline that makes "safe AND useful" meaningful) | 18.1 task spec | without it, "safe" is uninterpretable; not stated as a general rule |
| when a result is "bought by simplification" | BA4 + 15.2, applied ad hoc | needs a general check, currently pattern-matched by an expert |
| the experimental-gate ↔ programme-gate relationship | KG_SPEC §"Relationship to Experimental Kill-Gates" gestures at it; the playbook does not | two methods are tangled; the playbook bridges neither |
| which negatives transfer scope and which don't | `Claude_kill-gate_review.md` Evidence Assessment table | the scope-bridge rule (PR1-R2) exists as a programme rule but has no worked procedure |

**RECOMMENDATION.** Externalize C by *populating `playbook/00` from the task-spec
genre* — lift the disciplinary moves out of the per-experiment prompts into a
general procedure, each step citing the worked example it came from. Then re-run
`usability_test_01` with the answer key hidden; the playbook passes only when Run A
(playbook-only) succeeds.

## D. Method-claims the repo does NOT yet support ("what was NOT shown")

**FACT.** Stated plainly, mirroring the project's own negative-space discipline:

- No worked example shows the method *confirming a positive constructive claim* —
  every BA/FA/JB/15.x verdict is negative or limiting. The method is demonstrated as
  a **falsifier**, not yet as a **constructor**. (This is consistent with its
  purpose, but it means "the method produces durable positive knowledge" is
  untested.)
- No fresh, independent agent has reproduced any decision from the procedural
  artifacts alone (Run A fails; Run B reads the method from the task spec).
- The programme-gate method has not yet *rejected* a programme — KG0 was
  `continue_after_revision`. KG_SPEC's own claim ("if rejection is correct,
  rejection is success") is untested; the gates that could fail (KG1–KG3) are
  frozen-pending.
- KG1 as specified is currently **unrunnable** (missing v1.1/v1.2/v1.4 memos).

## E. The honest ratio

**INFERENCE.** Counting the *named* playbook artifact (`research/playbook/*`):
~2 of 6 files carry transferable content (03 preservation, 04 philosophy), and
those two are navigation/preservation principles, **not the kill-gate method**.
The kill-gate method itself is 0% present in the playbook directory.

Counting the *method as it actually exists in the repo* (task specs + lessons):
the experimental kill-gate discipline is substantially extracted and demonstrated
(see `02`, items 1–9). So the true state is bimodal: **the method is strong and the
playbook artifact is nearly empty.** The work remaining is externalization and an
independent reproduction, not invention.
