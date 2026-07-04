# fallacy-cutter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A knife for experiments that should fail closed before they fool their author.*

`fallacy-cutter` is a small extraction from the Ascesis research forge: the
`gate_harness` instrument plus the evidence-tagged methodology it began to
enforce. It is meant for trustworthy experiments run by humans and AI agents: run
work through the knife and the result should be either a provenance-signed
`VALID` `decision.json`, or an honest refusal that cannot be cited as success.

The mission in one sentence: any agent using the instrument gets either a
provenance-signed valid result or a fail-closed stop, independent of the agent's
own research skill, as long as the agent is not deliberately attacking the
instrument itself.

## Status: instrument real, portable playbook unfinished

The important honesty constraint is this: the executable instrument is real and
has adversarial tests, but the fully self-contained transferable methodology is
not finished. The current method lives partly in code, partly in task specs, and
partly in tacit research practice. This is documented, not hidden, in
[`methodology/SUMMARY.md`](methodology/SUMMARY.md) and
[`methodology/03_not_yet_method.md`](methodology/03_not_yet_method.md).

That distinction is the product. A method that cuts fallacies must be able to cut
its own overclaims.

## The axiom

**Fail closed.** Any ambiguity, missing artifact, unverifiable audit field,
insufficient seed count, moving threshold, leakage path, absent preregistration
lock, or missing provenance resolves to `FAIL`. Nothing passes by default.

## What is inside

- [`gate_harness/`](gate_harness/) — the executable instrument. It enforces
  preregistration, leakage checks, calibration checks, seed policy, tautology
  checks, evaluation-oracle checks, runner provenance, and independent decision
  verification.
- [`methodology/`](methodology/) — the prose-method extraction from Ascesis. The
  strongest current artifact is [`02_extracted_method.md`](methodology/02_extracted_method.md):
  ten disciplinary moves, evidence-tagged against worked experiments. Items 1-9
  are multiply demonstrated; item 10, programme-level gates, has one worked
  example and is kept with that caveat.
- [`methodology/harness_spec/`](methodology/harness_spec/) — visibility rules,
  output schema, failure conditions, and a usability-test report. The usability
  test is important because it exposed gaps instead of pretending the playbook was
  complete.
- [`examples/`](examples/) — one real preregistration example from Ascesis. It is
  domain-specific; the value is the structure, not the topic.
- [`MANIFEST.md`](MANIFEST.md) — exact extraction map from Ascesis.

## The eight harness modules

See [`gate_harness/README.md`](gate_harness/README.md) for the implementation
summary. At a glance:

1. `prereg.py` — two-phase preregistration: `PREREG.json` plus `PREREG.lock`, SHA
   binding, and a strict-ancestor git check.
2. `leakage_scanner.py` — AST-based scan of fit/classify paths and audit reports;
   hardcoded audit fields become `NOT_VERIFIABLE`, not silent passes.
3. `calibration_audit.py` — rejects oversized or mislabeled calibration/anchor
   setups before learner results can be trusted.
4. `seed_policy.py` — requires enough seeds for core metrics; one lucky seed is
   not a result.
5. `tautology_check.py` — checks whether the construction itself makes a contrast
   too easy, including the `information_ratio` pre-check and generic baselines.
6. `evaluation_oracle.py` — detects ground-truth hints and literal answer labels
   entering evaluation paths.
7. `runner.py` — the only valid writing path for citable decisions; folds required
   checks into `_harness_provenance`.
8. `verify_decision.py` — an independent verifier, separate from the runner. A
   decision without `_harness_provenance` is `INVALID` no matter how good its
   numbers look.

## The ten disciplinary moves

The method extraction is in
[`methodology/02_extracted_method.md`](methodology/02_extracted_method.md). The
moves are: preregistration, controls, halt-downstream, FACT/INFERENCE/HYPOTHESIS
split with mandatory negative-space reporting, non-saturation-is-inconclusive,
"bought by simplification?", compression/coverage not equal to discrimination,
negative-result-as-anchor, parallel-reality check, and programme-level gates.

The caveat matters: moves 1-9 are supported by multiple worked examples; move 10
has one worked example. The portable, fresh-agent playbook is still a work in
progress.

## Reproduction

The harness tests are pytest-style and require `pytest` and `numpy`:

```bash
PYTHONPATH=. python3 -m pytest gate_harness/tests -q
```

The adversarial tests reproduce real audit findings: they are RED without the
corresponding defense and GREEN with it.

Basic import sanity:

```bash
PYTHONPATH=. python3 -c "import gate_harness.runner, gate_harness.verify_decision, gate_harness.leakage_scanner; print('imports OK')"
```

A citable decision is checked with the independent verifier:

```bash
PYTHONPATH=. python3 -m gate_harness.verify_decision path/to/decision.json
```

## Provenance

This repository was extracted from `/home/master/llm_projects/ascesis`. The
methodology documents remain evidence-tagged against the Ascesis experiments that
produced them. They intentionally still mention Justitia, CEGAR, Door 1, FA/JB/BA,
and other source-specific material; that is provenance, not accidental residue.

## What this does not claim

- It is not yet a complete domain-neutral playbook a fresh agent can execute from
  prose alone.
- It is not proof against malicious actors modifying the instrument.
- It is not a guarantee that a good scientific question has been asked.
- It is not a replacement for judgement; it is a way to make missing evidence,
  hidden thresholds, leakage, and provenance failures mechanically harder to hide.

## License

MIT — see [`LICENSE`](LICENSE).
