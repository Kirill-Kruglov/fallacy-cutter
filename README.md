# fallacy-cutter

[![CI](https://github.com/Kirill-Kruglov/fallacy-cutter/actions/workflows/ci.yml/badge.svg)](https://github.com/Kirill-Kruglov/fallacy-cutter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A knife for experiments that should fail closed before they fool their author.*

**[📖 Read the essay](https://kirill-kruglov.github.io/fallacy-cutter/)**
([md](essay/instruments-not-intentions.md) ·
[PDF](essay/instruments-not-intentions.pdf)) ·
**[▶ Worked example](examples/hello_gate/)** ·
**[Appendix A](https://kirill-kruglov.github.io/fallacy-cutter/appendix-a.html)** ·
**[How it was made](https://kirill-kruglov.github.io/fallacy-cutter/about.html)**

`fallacy-cutter` is a small extraction from the Ascesis research forge: the
`gate_harness` instrument plus the evidence-tagged methodology it began to
enforce. It is meant for trustworthy experiments run by humans and AI agents: run
work through the knife and the result is either a `decision.json` carrying
machine-checkable evidence that every declared gate was satisfied, or a
fail-closed refusal that cannot be cited as success.

The mission in one sentence: the instrument removes the researcher's *virtue*
from the trust chain — not the researcher's *skill*. What was declared, when it
was frozen, and what touched the data become facts a stranger can check without
trusting anyone; whether the right thing was declared remains research skill,
made legible instead of taken on faith.

## What `VALID` means (and does not)

The verifier's verdict word is `VALID`. Read it as defined: **harness-valid** —
procedural compliance under the declared specification (provenance present,
prereg locked before the run, declared scans passed). It is *not* a claim of
scientific validity: a run with a meaningless question, a mismeasuring metric, or
a control too weak to fire can be fully harness-valid and still be worthless.
There are many ways to get a false pass without attacking the instrument — the
complete taxonomy is in
[Appendix A](essay/appendices/A-what-the-knife-checks.md). The verdict keeps its
name in code because the verifier hashes the harness sources (renaming would
invalidate every already-signed decision); a future major version renames it to
`GATE_PASS`.

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
- [`examples/`](examples/) — a runnable end-to-end example,
  [`hello_gate/`](examples/hello_gate/), that goes through the whole harness and
  comes out as a provenance-signed `VALID` decision (its control fails where it
  should); plus one real preregistration from Ascesis as a format reference.
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

Python 3.11+; the only runtime dependency is numpy.

```bash
pip install -e ".[dev]"                              # numpy + pytest

pytest -q                                            # harness adversarial self-tests
python examples/hello_gate/run.py                    # reproduce the worked example
python scripts/verify_all.py                         # every example decision is VALID
python -m gate_harness.verify_decision path/to/decision.json   # verify any decision
```

The adversarial tests each reproduce a real audit finding: RED without the
corresponding defense, GREEN with it. CI runs exactly this on every push — including
regenerating `hello_gate`'s decision from scratch and asserting it is byte-identical,
which is only possible because the preregistration is a strict ancestor of `HEAD`.

## Provenance

This repository was extracted from `/home/master/llm_projects/ascesis`. The
methodology documents remain evidence-tagged against the Ascesis experiments that
produced them. They intentionally still mention Justitia, CEGAR, Door 1, FA/JB/BA,
and other source-specific material; that is provenance, not accidental residue.

## What this does not claim

- It is not yet a complete domain-neutral playbook a fresh agent can execute from
  prose alone — the repository's own usability test proved exactly that.
- It is not proof of scientific validity: harness-valid means the declared gates
  were satisfied, nothing more (see Appendix A's false-pass taxonomy).
- It is not proof against malicious actors modifying the instrument — nor against
  honest gaps the gates were never taught to see.
- The verifier is separated from the runner, but not independent in the
  institutional sense: same repository, same author, same trust root.
- It is not a guarantee that a good scientific question has been asked.
- It is not a replacement for judgement; it is a way to make missing evidence,
  hidden thresholds, leakage, and provenance failures mechanically harder to hide.

## Roadmap

In increasing order of cost and value:

1. **Two modes, explicitly.** Exploration (ambiguity allowed, strong claims
   forbidden, nothing citable) vs. confirmation (the knife in full). Fail-closed
   applied to everything would sterilize early research.
2. **Independent verifier.** A minimal verifier as its own frozen-spec package; a
   second implementation written against the spec by someone who never read the
   first; an external maintainer; `GATE_PASS` as the verdict name.
3. **Adversarial audit** by a party with an incentive to break the gates.
4. **Independent replication** of the gated experiments — which outweighs
   everything above.

## The triptych

This repository is one panel of three, sharing a single thesis — *do not try to
certify intentions; build contact, consequences, and constraints that can be
checked* — and a single honest caveat: all three come from one forge, one author,
the same AI partners. The knife is real, and it cuts; but it is still in the same
hand. Independent replication is invited and would outweigh any further internal
check.

- [**justitia**](https://github.com/Kirill-Kruglov/justitia) — what keeps a world
  of powerful, evolving agents livable when no one can read anyone's soul.
- [**proxylimen**](https://github.com/Kirill-Kruglov/proxylimen) — where a mind's
  world comes from, and where blind derivation measurably breaks.
- **fallacy-cutter** (this repo) — the fail-closed instrument both were cut with.

## License

MIT — see [`LICENSE`](LICENSE).
