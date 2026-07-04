# SUMMARY — extract-and-test pass on the falsification-playbook

Working label only; the framework is **not named** here (a name is a commitment
that should follow, not precede, a passing reproduction test).

This pass applied falsification to the falsification method itself. It did not
write the method up as if it exists; it tested whether the method *transfers* and
extracted the part that does. Honest one-page state below.

---

## 1. How much of the playbook is supported by worked examples vs aspirational?

**Bimodal — and the two modes must not be averaged into a misleading "half done."**

- **The experimental kill-gate method is strongly supported.** Nine disciplinary
  moves (pre-registration, controls, halt-downstream, FACT/INFERENCE split,
  non-saturation-inconclusive, "bought by simplification?", compression≠discrimination,
  negative-as-anchor, parallel-reality check) each have ≥1 worked example across
  18.1 / JB0 / FA2.5 / BA4 / FA1 / 15.2 / Door1. This is real, extracted method
  (`02_extracted_method.md`).
- **The artifact named "playbook" (`research/playbook/*`) is almost empty.**
  `00_monograph_kill_gates.md` is 8 headers with zero content; `01`/`02` are maps
  *to* the method; only `03`/`04` carry content, and those are
  preservation/navigation principles, **not the kill-gate method**. The kill-gate
  method is 0% present in the playbook directory.
- **The programme-gate layer (KG_SPEC/PIPELINE/KG0/PR1/KG1) is drafted with one
  worked example (KG0).** KG1–KG6 are specced but unfired; KG1 is currently
  *unrunnable* (its required v1.1–v1.4 memos are missing from the tree).

So: **method strong, playbook artifact nearly empty.** The method lives in the
experiment task specs and durable-lesson docs, *outside* the playbook directory.

## 2. Did the usability test reproduce a decision, or expose missing instructions?

**It exposed missing instructions — the more honest and more useful result.**

Run A (playbook + KG_SPEC + evidence packet, answer key hidden): a fresh agent
**cannot** execute the 18.1 kill-gate. It cannot find the metric, the 0.05
threshold, the pre-registration rule, the mandatory controls, or the
halt-downstream rule — none is in `research/playbook/*`. All eight failure
conditions F1–F8 fire.

Run B (task spec also visible): the agent **can** set up the gate — but only
because it is reading the method out of the *experiment task spec*, which is not
part of the playbook. This proves the **task-spec genre, not the playbook, is the
real procedural artifact.**

The clean-looking success only appears when the agent is handed the method
elsewhere. That is the inverted success criterion working as intended: the test
succeeded by surfacing that the playbook is a signboard, not the building.

## 3. The single most important missing piece before this is a transferable method

**Externalizing the pre-registration-and-controls discipline out of the per-
experiment task specs into the playbook itself** — concretely, populating
`playbook/00`'s empty headers with the decision rules, threshold-selection
reasoning, mandatory-controls list, and halt rule, each citing the worked example
it came from. Today this knowledge is tacit: it is re-written from scratch in every
experiment prompt and otherwise lives in Kirill+analyst conversation history.

The close-second missing piece: **an independent reproduction** — re-running the
usability test with the answer key hidden and confirming that Run A (playbook-only)
then succeeds. Until that passes, "transferable" is unproven.

## 4. Is "falsification-driven inquiry for agents+humans" a real extractable artifact yet?

**Partly. The *method* is real and demonstrated; the *transferable playbook* is
not yet built — it is a goal the repo is close to but has not reached.**

What is real now: a battle-tested experimental kill-gate discipline that produced
multiple honest negatives on a hard research question. That discipline is concrete
enough (thresholds, controls, halt rules, evidence-tagging) to be reused, and it is
genuinely valuable for agents and humans doing falsification-first work.

What is not real yet: a self-contained artifact a fresh agent can execute from
*alone*. The method currently transfers through the task-spec genre and expert
tacit knowledge, not through the playbook. And a sharper caveat: every worked
example is a *negative* — the method is demonstrated as a falsifier, not yet as a
constructor of durable positive knowledge.

**Bottom line.** This pass did not produce a finished method, and it should not
have. It produced: an honest inventory, a harness that ran, a usability test that
exposed the real gap, and an extraction that keeps the strong part separate from
the empty part. The most valuable output is the finding that the method is real but
mis-located — which is a precise, actionable next step (externalize + reproduce),
not a polished document pretending the playbook is done.

---

## Next step (recommended)

1. Populate `playbook/00` from the task-spec genre (each step evidence-cited) —
   a dedicated extraction, not a quiet patch inside this pass.
2. Re-run `harness/usability_test_01` with the answer key hidden; the playbook
   passes only when Run A succeeds.
3. Only after a passing reproduction: consider naming the framework.
4. Commit the small KG/PR layer + 15_collapse_boundary + this directory per
   `04_commit_recommendation.md`; defer the rest of the post-17 trees.
