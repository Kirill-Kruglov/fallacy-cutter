# Claude Science adapter

`fallacy-cutter` and an agentic workbench like Claude Science are an
*asymmetric pair*, not overlapping tools: the workbench gives reproducibility
(code, environment, history — provenance in the A.1 sense), the knife gives
precedence and fail-closed refusal (thresholds frozen *before* the result,
fit path scanned, otherwise no citable decision). A reproducibly-executed
meaningless run is taxonomy item #9; nothing about reproducibility prevents it.

**Design rule.** The core (`gate_harness/`) is self-contained and host-agnostic
— it is also the hashed trust surface (`harness_version`), so nothing
integration-shaped belongs inside it. Everything in this directory is an
adapter that talks to the core only through its public API/CLI, and can be
deleted without touching a single guarantee.

## What's here

- [`skill/fallacy-cutter/SKILL.md`](skill/fallacy-cutter/SKILL.md) — the
  instrument packaged as an agent skill: when to trigger (result will be
  cited/published/decided on), the two-rooms protocol, exact commands, and the
  refusal→next-action table. Install by copying/symlinking the
  `skill/fallacy-cutter/` directory into the host's skills location (for
  Claude Code: `.claude/skills/fallacy-cutter/` in the project, or
  `~/.claude/skills/` globally).
- [`mcp_server.py`](mcp_server.py) — a dependency-free stdio MCP server with
  exactly three tools: `gate_lock`, `verify_decision` (the confirmation room)
  and `log_exploration` (the exploration room). Deliberately absent: any tool
  that writes a `decision.json` — the only sanctioned writer is
  `gate_harness.runner.run_gate` in the experiment's own process.

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

## What the agent environment changes, honestly

An agent that autonomously runs experiments makes exploratory runs cheap and
invisible — which is exactly taxonomy item #3 (thresholds informed by
off-the-record runs). The exploration ledger exists for this: it blocks
nothing, but `gate_lock` demands an explicit `exploration_basis` ("none" or a
chain-valid ledger), so silence about tuning stops being an option.

Two limits stay open and should be stated, not hidden. First, the same-hand
problem mutates rather than disappears: if the agent writes the experiment,
the prereg, and calls the verifier, the hand is still one — two-phase commit
protects order, not origin; keep exploration and confirmation in separate
sessions/branches. Second, a host's background reviewer sharing weights with
the runner is taxonomy item #8 (shared wrong assumption), not independent
verification — that is what [`spec/`](../../spec/) is for: a frozen format a
second implementation can be written against.
