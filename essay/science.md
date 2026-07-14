# Using fallacy-cutter with Claude Science

Claude Science is Anthropic's AI workbench for researchers: an agent that runs
computational experiments on your own machines, keeps every artifact tied to
the exact code and environment that produced it, and lets you replay any
result. fallacy-cutter is a small fail-closed instrument that does something a
workbench cannot: it refuses. This page explains, in plain language, why the
two belong together and how to connect them in a few minutes.

## Why bother: reproducibility is not validity

A workbench answers *"can this result be reproduced?"* — here is the code, the
environment, the history; run it again. That is provenance, and it is
valuable. But a meaningless experiment reproduces perfectly. So does one whose
thresholds were quietly tuned until the data passed, one whose test set
contains the training patients, and one whose "unsupervised" classifier was
handed the answer through a side door. Reproducibility guarantees the *record*
is honest; it says nothing about whether the *procedure* was.

fallacy-cutter guards the procedure, and only the procedure:

- **Precedence.** Thresholds are frozen and committed *before* the run; the
  runner checks git ancestry and refuses if the preregistration came after.
- **Leakage.** The fit path is statically scanned for ground-truth names; the
  train/test split is checked against declared groups (no patient on both
  sides); fit-transformations must not see pre-split data.
- **Refusal as output.** If any check fails, there is no citable result — not
  a result with a caveat. A decision either carries machine-checkable
  provenance that every declared gate passed, or it cannot be cited at all.

The two tools are an asymmetric pair. Claude Science makes your work
replayable; fallacy-cutter makes your shortcuts non-citable. Neither replaces
the other.

## Why especially with an agent

An agent that runs experiments for you makes exploratory runs cheap, fast, and
invisible. That is exactly the channel through which post-hoc thresholds
masquerade as preregistered ones: try fourteen values off the record, then
"preregister" the one that worked. A human does this slowly and guiltily; an
agent does it in a loop, with good intentions all the way down. The essay's
premise applies with full force here — an experimenter's good intentions are
not a guarantee, and an LLM's are even weaker.

fallacy-cutter's answer is not to forbid exploration but to make it audible.
The **exploration ledger** is an append-only, hash-chained log: the agent can
add entries but cannot silently edit, reorder, or truncate them. And when
thresholds are frozen, the preregistration *must* declare its
`exploration_basis` — either `none` ("no exploratory runs informed these
thresholds", a checkable claim) or the ledger that did. Silence stops being an
option.

## Connecting it

Claude Science runs on your infrastructure, so the instrument sits directly in
the agent's path. You need a git repository and Python 3.11+.

**1. Get the code.**

```
git clone https://github.com/Kirill-Kruglov/fallacy-cutter
pip install ./fallacy-cutter
```

**2. Install the skill** — this is what makes the agent reach for the knife on
its own. Copy the skill folder into your project (or your global skills
directory):

```
cp -r fallacy-cutter/integrations/claude_science/skill/fallacy-cutter \
      your-project/.claude/skills/
```

The skill tells the agent when to trigger (a result will be cited, published,
or used for a decision), when *not* to (pure exploration — log to the ledger
instead), and what to do with every refusal.

**3. Optionally, add the MCP server** — three tools and nothing more:

```json
{
  "mcpServers": {
    "fallacy-cutter": {
      "command": "python",
      "args": ["/path/to/fallacy-cutter/integrations/claude_science/mcp_server.py"]
    }
  }
}
```

`gate_lock` freezes thresholds, `verify_decision` says whether a decision is
citable, `log_exploration` records an exploratory run. There is deliberately
no tool that can *write* a decision: the only sanctioned writer is the runner
inside your experiment's own process, so the adapter cannot become a bypass.

Everything also works without the skill or MCP — plain CLI:

```
python -m gate_harness.exploration_ledger log EXPLORATION.jsonl '{"tried": 0.6, "result": "FAIL"}'
python -m gate_harness.prereg lock experiments/my_gate \
    --thresholds-json '{"auroc_min": 0.75}' --exploration-basis EXPLORATION.jsonl
python -m gate_harness.verify_decision experiments/my_gate/decision.json
```

## Using it: two rooms

The working discipline is two explicitly separate modes, and the agent is
instructed to know which one it is in.

**Exploration.** Try things. Nothing is blocked, nothing is citable. Every run
worth remembering goes to the ledger — one line each: what was tried, what
came out.

**Confirmation.** Four steps, in order:

1. **Lock** the thresholds, declaring the exploration basis
   (`gate_lock` / `prereg lock`).
2. **Commit** `PREREG.json` + `PREREG.lock` in their own commit, with no
   outputs. The runner will verify this commit is a strict git ancestor of the
   run — that is what "before" means, mechanically.
3. **Run** the experiment through `gate_harness.runner.run_gate`, which takes
   the leakage scan, the tautology pre-check, and the evaluation-oracle log,
   and writes a provenance-signed `decision.json`. For grouped data (patients,
   subjects, batches), also assert split integrity and preprocessing order —
   in biology the leak is usually in the data, not the code.
4. **Verify** before citing: `verify_decision` prints `VALID` or the reasons
   it refuses, each with a concrete next action.

A [worked end-to-end example](https://github.com/Kirill-Kruglov/fallacy-cutter/tree/main/examples/hello_gate)
is about 140 lines, and CI reproduces its decision byte-for-byte.

When the knife refuses, the refusal names its own fix: *commit the prereg
first*, *re-split group-aware*, *fit on the train fold only*. The agent is
instructed to do the fix, never to argue with the gate — and a refusal that
survives the fix is not an obstacle, it is the finding.

## What a green gate does and does not mean

`VALID` means **harness-valid**: the declared gates were satisfied, in the
declared order, by code whose hash is recorded. It does not mean the science
is right — a meaningless question, flawlessly executed, passes every gate.
The [complete taxonomy of what slips past](appendix-a.html) is published, and
citing it beats overclaiming.

Two limits are worth naming out loud in this setting. If the same agent writes
the experiment, the preregistration, and the analysis in one session, the
two-phase commit protects the *order* of events, not the *origin* of the
thresholds — the ledger makes the origin visible; keeping exploration and
confirmation in separate sessions or branches keeps the rooms honest. And a
host's built-in reviewer that shares weights with the agent it reviews is not
independent verification — which is why the
[decision format is frozen as a public spec](https://github.com/Kirill-Kruglov/fallacy-cutter/tree/main/spec),
so a verifier can be written by someone who has never read this code.

## In one sentence

Claude Science makes your experiments reproducible; fallacy-cutter makes them
refusable — and a result that survives both is one a stranger can trust
without trusting you.
