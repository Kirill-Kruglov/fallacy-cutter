# 00 — Inventory of method-material (read-only)

No files were moved, renamed, staged, or committed to produce this inventory.
Tags: **FACT** = demonstrable from the repo; **INFERENCE** = my reading;
**RECOMMENDATION** = proposed action.

A note on a distinction the rest of this pass depends on:

**INFERENCE.** There are *two* candidate "methods" tangled together in this repo,
plus one near-empty artifact that claims to be the method:

1. **The experimental kill-gate method** — demonstrated by the BA/FA/JB and 15.x
   worked examples and their task specs. This is the part with the most
   worked-example support.
2. **The programme-gate method** (KG_SPEC / KG_PIPELINE / KG0 / PR1 / KG1) — a
   newer, higher-level governance layer with exactly one worked example (KG0
   itself).
3. **The `research/playbook/` directory** — the artifact explicitly *labelled*
   the playbook, which is almost entirely empty skeleton.

The method is real and demonstrated; the *artifact named "playbook" is not where
the method currently lives.* The method lives in the experiment task specs and
the durable-lesson docs. This gap is the central finding of the whole pass.

---

## A. Procedural artifacts (the candidate method)

| artifact | what it is | classification | basis |
|---|---|---|---|
| `research/playbook/README.md` | states the playbook is a skeleton, "not yet a finished method" | aspirational | FACT: self-describes as skeleton |
| `research/playbook/00_monograph_kill_gates.md` | 8 section headers, **zero body content** | aspirational | FACT: file is headers only |
| `research/playbook/01_playbook_extraction_plan.md` | bullet list of future extraction sources | aspirational | FACT: a to-do list, not a procedure |
| `research/playbook/02_source_artifact_map.md` | table mapping source specs → what to extract | aspirational | FACT: a map to the method, not the method |
| `research/playbook/03_preservation_rule.md` | historical-banner vs historical-rewrite rule | drafted-only | FACT: substantive ~1pp; INFERENCE: reflects actual repo practice (banners added, commit `3e3d7ca`), so *partially* tested |
| `research/playbook/04_repository_philosophy.md` | Ascesis = archive; Justitia external; evidence-preservation | drafted-only | FACT: substantive; INFERENCE: describes enacted structure |
| `research/substrate_discovery_v1/KG_SPEC.md` | general Programme Gate spec (decisions, lifecycle, burden of proof, evidence rules) | drafted-only | FACT: detailed spec; only KG0 has instantiated it |
| `research/substrate_discovery_v1/KG_PIPELINE.md` | gate DAG KG0→PR1→KG1→KG2…KG6 | drafted-only | FACT: KG0/PR1 marked Complete; KG1–KG6 Pending |
| `research/substrate_discovery_v1/KG1_SPEC.md` | Goal-Anchor Identity Gate spec | aspirational | FACT: marked "next gate", not yet executed |
| `experiments/JB/18_1_shielded_training/.../level_A_preregistration.json` | pre-registered kill threshold (0.05) fixed before measuring | **tested** | FACT: this *is* the pre-registration discipline, in code |
| `experiments/*/SPEC_original.md`, `claude_code_task_*.md` | per-experiment kill-gate designs (e.g. 18.1 task spec) | **tested** | FACT: each was executed; the 18.1 task spec encodes most of the disciplinary moves |

**INFERENCE.** The only procedural artifacts that are *tested* (a worked example
demonstrably followed them) are the per-experiment task specs and the 18.1
pre-registration JSON. Everything filed under `research/playbook/` is `drafted-only`
or `aspirational`. That is the honest expected result, and it is not a problem —
it is the finding.

**INFERENCE.** KG0 is a genuine worked example *of the programme-gate spec*: it
followed KG_SPEC's required output structure and reached `continue_after_revision`.
But it is N=1, and it is self-referential (the spec and its first use were authored
together), so KG_SPEC is `drafted-only`, not yet `tested` in the strong sense of
"a different agent reproduced it."

---

## B. Worked examples (the method in action — evidence it was ever applied)

| example | file | what it demonstrates | result type |
|---|---|---|---|
| **18.1 fidelity kill-gate** | `experiments/JB/18_1_shielded_training/outputs_18_1/summary.md` + `level_A_preregistration.json` + `claude_code_task_18_1_shielded_training.md` | pre-registration before measuring; kill-gate fires (false_safe 0.299 > 0.05); downstream (Level B) NOT run; mandatory positive+negative+trivially-safe controls; equal data volumes; held-out transfer | honest negative; strongest worked example |
| **JB0 CEGAR assessment** | `experiments/JB/JB0_E1_standard_cegar_boundary_assessment/outputs/final_report.md` | a negative accepted not fought; "conservative_but_vacuous"; useful≠correct (FPR 0.54); Justitia dropped as Door-1 candidate | honest negative |
| **FA2.5 candidate validation** | `experiments/FA/FA2_5_E1_candidate_validation/outputs/final_report.md` | compression ≠ discrimination; refused to claim success without precision margin; "equivalent_to_standard_history_refinement" | honest negative |
| **BA4 layer audit** | `experiments/BA/BA4_layer_audit/justitia_layer_audit.md` | layer discipline: dynamics / policy / observation / projection / reporting separated; "decidability bought by simplification?" check on `resource_hhi` | method/diagnostic |
| **FA1 witness taxonomy** | (summarized in `research/faithful_abstraction_v1/01_empirical_basis.md` §5) | begin failure analysis from witness populations, not isolated counterexamples | structured-negative |
| **15.2 enumeration-to-exhaustion** | `experiments/15_collapse_boundary/outputs_15_2/summary.md` | non-saturation-is-inconclusive (only exhausted points used); "decidability bought by simplification?" (free-monoid / noisy-TV trap); parallel-reality check (count-open ≠ meaning-non-trivial) | open-candidate w/ caveat |
| **KG0 programme review** | `research/substrate_discovery_v1/KG0_programme_review.md` | applying kill-gate discipline to the *programme*; criticism = evidence not authority; burden on programme | continue_after_revision |

**FACT.** All BA/FA/JB worked examples reached *negative or limiting* verdicts and
were accepted as anchors rather than fought. The repo contains no worked example
of the method confirming a positive constructive claim.

---

## C. Method-relevant durable lessons

| doc | content | tag |
|---|---|---|
| `research/door1_postmortem/Door1_Extracted_Knowledge_v1.md` | FACT/INFERENCE/HYPOTHESIS-tagged durable results; "negative results reduce future search space"; empirical design checklist | core method-lesson source |
| `research/faithful_abstraction_v1/01_empirical_basis.md` | [FACT]/[INFERENCE] split; "witness coverage ≠ discrimination"; "compression alone is not constructive progress" | core method-lesson source |
| `research/Claude_kill-gate_review.md` | external hostile review that triggered KG0; "a disciplined harness pointed at a target that quietly moved" | review-layer evidence |
| snapshot §3 / §9 (`repo_reorg_inventory/current_repo_state_for_playbook_test.md`) | visibility rules and three test modes (Packages A/B/C) | harness source material |

---

## D. Historical / sandbox (NOT method — excluded from extraction)

**FACT.** The following exist and are explicitly historical; they are noted for
completeness and excluded from extraction:

- `ascesis_of_learning_grace/*` — original sandbox: status, field_check, dialogue
  parts 1–22, archive index. Banners mark it historical.
- `research/monograph_17/*` — post-17F reference packet (project index,
  methodology, ontology, programme, ledger, Memo v1.3, GPT notes).

These are useful for historical reconstruction (snapshot Package A) but are not
candidate procedure.

---

## E. Classification summary

**FACT (counts of procedural artifacts):**

- `tested`: 2 (the per-experiment task-spec pattern; the 18.1 pre-registration JSON).
- `drafted-only`: 4 (KG_SPEC, KG_PIPELINE, playbook/03, playbook/04).
- `aspirational`: 5 (playbook README, playbook/00, playbook/01, playbook/02, KG1_SPEC).

**INFERENCE.** Of the artifacts that *carry the name* "playbook"
(`research/playbook/*`), none is `tested`; the two non-empty ones (03, 04) are
preservation/navigation principles, not the kill-gate method. The actual tested
method is encoded in the experiment task specs, which are *not* under
`research/playbook/`. The playbook directory is a signboard; the building is in
`experiments/*`.
