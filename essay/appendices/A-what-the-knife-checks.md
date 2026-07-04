# Appendix A — What the Knife Checks, and What Slips Past It

The essay promises exactness about what a harness-signed result means. This appendix
is that exactness: every module, what it catches (each one was taught by a real audit
finding — a mistake I actually made), and what it structurally cannot catch. The
second column is not modesty; it is the specification of where the next false pass
will come from.

## A.1 The word `VALID`, defined

`gate_harness.verify_decision` prints `VALID` when a `decision.json` carries a
`_harness_provenance` block written by the sanctioned runner, matching the current
harness code hash, with every required check flag true. That word means, precisely:

> **harness-valid** — machine-checkable evidence that the declared gates were
> satisfied, in the declared order, by the code whose hash is recorded.

It does not mean the science is right. It cannot. A run with a meaningless question,
a mismeasuring metric, or a control too weak to fire can be fully harness-valid and
still be worthless. The verdict name is kept as `VALID` in the code because the
verifier hashes the harness sources — renaming it would invalidate every decision
already signed (the safe direction: the artifact record stays immutable). A future
major version will rename the verdict to something that cannot be misread —
`GATE_PASS` — with a fresh provenance line. Until then, every document in this
repository reads `VALID` as *harness-valid, procedural compliance under the declared
specification*, never as *scientifically valid*.

## A.2 The modules: caught vs. not caught

| module | taught by (real finding) | what it catches | what it structurally cannot catch |
|---|---|---|---|
| `prereg.py` | thresholds registered after results, committed together (#1, #2, #9) | unlocked or edited preregistrations; thresholds changed between gates without a written rationale; runs whose prereg is not a strict git ancestor | thresholds tuned in exploratory runs that never touched the record, then "preregistered" fresh; a rationale that is written but bad |
| `hooks/pre-commit` | prereg + results in one atomic commit (#1) | committing a gate's `PREREG.*` together with its `outputs/`; silent edits of a locked prereg | history rewritten before publication; work done outside the hooked clone |
| `leakage_scanner.py` | classifier branching on the generator label; audits returning hardcoded `yes` (#3, #4) | forbidden truth-names anywhere in the fit path's AST — parameters, identifiers, attributes, dict string keys, closures, globals; audit fields that are constants rather than computations (`NOT_VERIFIABLE` → FAIL) | truth renamed to an innocent word; leakage through data *values* rather than code references; channels in functions never registered for scanning |
| `calibration_audit.py` | a "sparse" anchor set heavier than the complete one (#7) | anchor volume above the declared bound; sparse ≥ complete | anchor *placement* that smuggles the answer at legal volume |
| `seed_policy.py` | conclusions from a single lucky seed (#8) | core metrics with fewer than the required seeds → `INSUFFICIENT_SEEDS`, never PASS | statistically dependent seeds; selective emphasis across many passing metrics |
| `tautology_check.py` | a world built so the contrast was guaranteed (#5) | `information_ratio` below the mandatory floor → immutable `construction_may_be_tautological`; weak-baseline theater (two strong baselines are mandatory) | constructions trivial in ways variance ratios do not see |
| `evaluation_oracle.py` | `truth_axes=3` handed to the evaluator (#6) | ground-truth hints as literal keyword arguments or dict values at evaluation call sites; unscanned non-entrypoints | hints encoded non-literally, or arriving through the data itself |
| `runner.py` | all of the above at execution time | refuses to run without a verified lock, passing leakage scan, and tautology report; folds oracle hints into the decision; forbids the experiment overriding harness-only flags | a wrong question executed flawlessly |
| `verify_decision.py` | citing results that bypassed the runner (§1.7) | decisions with no provenance, a stale harness hash, or false check flags — INVALID regardless of how good the numbers look | mistakes it shares with the runner; bugs in itself |

Read the last column as one sentence: **the knife catches the fallacies it has been
taught; against unnamed ones it is as blind as its author.**

## A.3 The false-pass taxonomy

Ways to get a harness-valid result that is scientifically worthless, none of which
require attacking the instrument:

1. an unmodeled leakage channel (the scanner's forbidden-name list is name-based);
2. a truth label semantically renamed;
3. thresholds informed by off-the-record exploratory runs;
4. a control that cannot fire (so "passing the control" is vacuous);
5. a metric that measures the wrong object;
6. dependent observations dressed as independent seeds;
7. a generator that makes the task trivial in a way `tautology_check` does not model;
8. a shared wrong assumption between runner and verifier;
9. an honestly meaningless question, flawlessly executed;
10. a bug in the verifier.

Deliberate sabotage — editing the verifier, forging provenance — is merely the
eleventh entry, and the only one that leaves fingerprints on purpose.

## A.4 The status of "independent verification"

What is true: the verifier is a separate module, and the runner cannot make it lie —
bypassing the runner produces a decision the verifier rejects.

What is not yet true: independence in the institutional sense. Same repository, same
author, same trust root, same conceptual assumptions, editable in the same commit.

Roadmap, in increasing order of cost and value:

1. extract a minimal verifier into its own package with a frozen, implementation-free
   specification;
2. a second implementation written against the spec by someone who has never read the
   first;
3. an external maintainer for the spec;
4. an adversarial audit by a party with an incentive to break it;
5. independent replication of the gated experiments themselves — which outweighs all
   of the above.

## A.5 The two rooms

Fail-closed is the right default for **confirmation**: frozen spec, preregistered
thresholds, citable output. Applied to everything, it would sterilize exploration and
teach a researcher to ask only easily-formalized questions — checklist compliance as
the new Goodhart target. So the working discipline is two explicitly separate modes:

- **exploration** — ambiguity allowed, instruments optional, strong claims forbidden;
  nothing from this room is citable;
- **confirmation** — the knife, in full; only what passes here may be cited, and only
  at the strength the gates actually license.

The failure mode is not being in either room. It is pretending to be in the one you
are not — exploratory results dressed as confirmed, or exploration strangled by
confirmation's rules until only trivial questions survive.

## A.6 Where the artifacts live

- The instrument: [`gate_harness/`](../../gate_harness/) — eight modules, adversarial
  tests (`gate_harness/tests/`), each red without its defense and green with it.
- The worked example: [`examples/hello_gate/`](../../examples/hello_gate/) —
  reproducible from scratch; CI regenerates its decision byte-for-byte and verifies it.
- The honest gap: [`methodology/SUMMARY.md`](../../methodology/SUMMARY.md) and
  [`methodology/03_not_yet_method.md`](../../methodology/03_not_yet_method.md) — the
  usability test that proved the method does not yet transfer through prose alone.
- The provenance contract: [`gate_harness/verify_decision.py`](../../gate_harness/verify_decision.py)
  — the exact conditions under which `VALID` is printed, in under a hundred lines.
