# harness/output_schema.md — what a kill-gate execution output must contain

A kill-gate execution is "complete" only if its output contains every field below.
The schema is reverse-engineered from what the *successful* worked examples
actually produced (18.1, JB0, FA2.5), cross-checked against KG_SPEC's required
output sections for the programme-gate variant.

Tags: **FACT** (field is present in a worked example), **INFERENCE**,
**RECOMMENDATION**.

---

## Required fields (experimental kill-gate)

| # | field | what it must contain | demonstrated by |
|---|---|---|---|
| 1 | **Question** | one decisive question with a fixed verdict vocabulary that includes named failure verdicts | **FACT:** 18.1 (`fidelity_ok\|fails_false_safe\|conservative`); JB0; FA2.5 |
| 2 | **Pre-registered threshold** | the kill threshold + decision rule + ground-truth definition, fixed *before* the metric, with provenance (the file it was committed to) and a "not moved" attestation | **FACT:** `level_A_preregistration.json` |
| 3 | **Metric** | the actual measured value(s) against the threshold | **FACT:** 18.1 false_safe 0.299; JB0 FPR 0.541; FA2.5 precision margin −0.084 |
| 4 | **Controls** | positive + negative controls, equal-volume guarantee, and a trivially-safe/no-op baseline (or an explicit statement of why none applies) | **FACT:** 18.1 task spec controls; FA2.5 B0/B1/B2 baselines; JB0 baseline table |
| 5 | **Decision** | exactly one verdict from the field-1 vocabulary | **FACT:** all three worked examples |
| 6 | **Downstream consequence** | what is now gated/stopped/allowed as a result (esp. "downstream NOT run" if the gate fired) | **FACT:** 18.1 "Level B: not_run"; JB0 "T-C: NO"; FA2.5 "T-C: NO" |
| 7 | **FACT / INFERENCE / HYPOTHESIS split** | claims tagged; a mandatory "what was NOT shown" section | **FACT:** Door1; FA `01_empirical_basis.md` §8 |
| 8 | **What-was-discarded accounting** | for any abstraction/metric/simplification used, what it dropped ("bought by simplification?") | **FACT:** 18.1 blind coordinates; BA4; 15.2 free-monoid caveat |
| 9 | **Durable constraint** | if the verdict is negative, the constraint it imposes on the next search | **FACT:** Door1 checklist; JB0/FA2.5 closed-direction ledger |

---

## Required sections (programme-gate variant)

**FACT.** KG_SPEC mandates exactly: Scope, Question, Evidence, Competing
hypotheses, Analysis, Decision, Consequences — and one of the four decisions
`Continue | Continue After Revision | Pause | Reject`. KG0 produced all of these.

**INFERENCE.** Fields 1, 5, 6, 7 above map onto the programme-gate sections;
fields 2, 3, 4 (pre-registration, metric, controls) are weaker at the programme
level because programme gates evaluate arguments, not measurements. This is a real
asymmetry, not a defect — but it is why programme gates are easier to ritualize
(see `failure_conditions.md`).

---

## Minimum pass bar

**RECOMMENDATION.** An output that is missing field 2 (pre-registration with
provenance) or field 4 (controls) is **not a kill-gate execution** — it is a
post-hoc narrative, regardless of how disciplined it reads. These two fields are
the anti-Goodhart core; everything else can be reconstructed, these cannot be
added after the fact without losing their meaning.

**RECOMMENDATION.** Field 7's "what was NOT shown" subsection is mandatory even for
a *passing* gate. Its absence is the signature of an overclaim
(`Claude_kill-gate_review.md` flags exactly this pattern in the substrate
chapters: form-rich, negative-space-absent).
