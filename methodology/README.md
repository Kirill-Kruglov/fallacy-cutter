# playbook_extraction

Working label: **falsification-playbook** (not a name — a placeholder until the
method is shown to transfer). Do not treat any document here as a finished or
named framework.

## What this directory is

An extract-and-test pass over the method-material accumulated in this repo. The
goal is NOT to write up "the falsification method" as if it exists. The goal is
to apply falsification to the falsification method itself: extract only the parts
that a worked example demonstrably used, build a harness that checks whether a
fresh agent could reproduce a decision from the artifacts alone, and report
honestly what is missing.

A document here that *looks* like a complete method without having been tested is
a failure of this pass, not a success — it would be the exact self-deception the
method is supposed to prevent.

## Discipline used in every file

Every claim is tagged:

- **FACT** — what the repo demonstrably shows (file + line/section cited).
- **INFERENCE** — my reading of those facts.
- **RECOMMENDATION** — what to do; for Kirill to decide.

This mirrors the project's own FACT / INFERENCE / HYPOTHESIS discipline
(`research/door1_postmortem/Door1_Extracted_Knowledge_v1.md`,
`research/faithful_abstraction_v1/01_empirical_basis.md`).

## Files

| file | role |
|---|---|
| `00_inventory.md` | what method-material exists, classified tested / drafted-only / aspirational |
| `01_method_from_practice.md` | the method as actually practiced, reverse-engineered from worked examples |
| `harness/visibility_rules.md` | the three test modes and file visibility per mode |
| `harness/output_schema.md` | what a kill-gate execution output must contain |
| `harness/failure_conditions.md` | what counts as the playbook being exposed as incomplete |
| `harness/usability_test_01_report.md` | fresh-agent simulation; what the playbook failed to specify |
| `02_extracted_method.md` | ONLY what passed, evidence-tagged |
| `03_not_yet_method.md` | gaps, aspirational steps, tacit knowledge to externalize |
| `04_commit_recommendation.md` | untracked-tree triage (recommend, don't execute) |
| `SUMMARY.md` | honest one-page state of the method |

## How this connects to the larger goal

Kirill's main question: a substrate where an LLM's world-model is *derived, not
generalized*. The falsification playbook is the *method* that produced the honest
negative results on that question (Justitia not a usable safety substrate; CEGAR
boundary conservative-but-vacuous; compression ≠ discrimination; the free-monoid
trap). A transferable version of that method is independently valuable — for
agents and humans doing falsification-first research — but only if it actually
transfers. This pass tests whether it transfers and extracts the part that does.
If little transfers yet, that honest finding is worth more than a polished
document that pretends otherwise.
