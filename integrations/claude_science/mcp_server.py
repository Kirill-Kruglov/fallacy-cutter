#!/usr/bin/env python3
"""fallacy-cutter MCP adapter — a thin, dependency-free stdio server.

Design rule: the core (``gate_harness``) stays self-contained and knows nothing
about Claude Science, MCP, or any host. This adapter only calls the core's
public API and exposes the minimal surface an agent needs:

  - ``gate_lock``        : freeze thresholds (two-phase commit, phase 1) —
                           requires an explicit exploration_basis;
  - ``verify_decision``  : is this decision.json citable? GATE-VALID or REFUSED;
  - ``log_exploration``  : append a run to the exploration ledger (the one tool
                           for the exploration room — it blocks nothing, it
                           records).

Deliberately absent: any tool that writes a decision.json. The only sanctioned
writer is ``gate_harness.runner.run_gate`` inside the experiment's own process;
an adapter that could mint decisions would be a bypass, not an interface.

Speaks MCP over stdio (newline-delimited JSON-RPC 2.0). No third-party
dependencies. Run:  python integrations/claude_science/mcp_server.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gate_harness import exploration_ledger as EL  # noqa: E402
from gate_harness import prereg as PR  # noqa: E402
from gate_harness.verify_decision import verify_decision  # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "fallacy-cutter", "version": "0.2.0"}

TOOLS = [
    {
        "name": "gate_lock",
        "description": (
            "Freeze thresholds for a gate BEFORE running the experiment (two-phase "
            "commit, phase 1). Writes PREREG.json + PREREG.lock; they must then be "
            "committed in their own commit (no outputs/) before the run. "
            "exploration_basis is mandatory: 'none' declares that no exploratory "
            "runs informed these thresholds; a ledger path cites the runs that did."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["gate_dir", "thresholds", "exploration_basis"],
            "properties": {
                "gate_dir": {"type": "string", "description": "Path to the gate directory"},
                "thresholds": {"type": "object", "description": "The thresholds to freeze"},
                "exploration_basis": {
                    "type": "string",
                    "description": "'none', or a path to a chain-valid exploration ledger",
                },
                "rationale_for_threshold_changes": {
                    "type": "object",
                    "description": "Required for any threshold that changed vs the previous gate",
                },
                "metadata": {"type": "object"},
            },
        },
    },
    {
        "name": "verify_decision",
        "description": (
            "Check whether a decision.json is citable: provenance written by the "
            "sanctioned runner, current harness hash, all gate flags true. Returns "
            "GATE-VALID or REFUSED with reasons and a next action. A result that "
            "was never run through the harness is REFUSED regardless of its numbers."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["path"],
            "properties": {
                "path": {"type": "string", "description": "Path to decision.json"}
            },
        },
    },
    {
        "name": "log_exploration",
        "description": (
            "Exploration room: append one exploratory run (what was tried, what "
            "came out) to the append-only hash-chained ledger. Blocks nothing. "
            "When thresholds are later frozen, gate_lock can cite this ledger as "
            "its exploration_basis — making off-the-record tuning visible."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["ledger_path", "payload"],
            "properties": {
                "ledger_path": {"type": "string", "description": "Path to EXPLORATION.jsonl"},
                "payload": {"type": "object", "description": "What was run and what resulted"},
            },
        },
    },
]


def _tool_gate_lock(args: dict) -> str:
    paths = PR.lock_prereg(
        args["gate_dir"],
        args["thresholds"],
        args.get("rationale_for_threshold_changes") or {},
        exploration_basis=args["exploration_basis"],
        extra_metadata=args.get("metadata"),
    )
    return (
        f"LOCKED  {paths['prereg']}\n        {paths['lock']}\n"
        "next: commit PREREG.json + PREREG.lock in their own commit (no outputs/), "
        "then run the gate through gate_harness.runner.run_gate"
    )


def _tool_verify_decision(args: dict) -> str:
    ok, reasons = verify_decision(args["path"])
    if ok:
        return f"GATE-VALID  {args['path']}  (harness-valid: procedural compliance, not scientific truth)"
    lines = "\n".join(f"  - {r}" for r in reasons)
    return (
        f"REFUSED  {args['path']}\n{lines}\n"
        "next: a decision is citable only if written by gate_harness.runner.run_gate "
        "against the current harness — re-run the gate through the runner"
    )


def _tool_log_exploration(args: dict) -> str:
    entry = EL.append_entry(Path(args["ledger_path"]), args["payload"])
    return (
        f"LOGGED  seq={entry['seq']}  head={entry['entry_sha256']}\n"
        f"cite this ledger later via gate_lock exploration_basis={args['ledger_path']}"
    )


HANDLERS = {
    "gate_lock": _tool_gate_lock,
    "verify_decision": _tool_verify_decision,
    "log_exploration": _tool_log_exploration,
}


def _respond(msg_id, result=None, error=None) -> None:
    resp: dict = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        resp["error"] = error
    else:
        resp["result"] = result
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()


def handle(msg: dict) -> None:
    method = msg.get("method")
    msg_id = msg.get("id")
    if method == "initialize":
        _respond(msg_id, {
            "protocolVersion": msg.get("params", {}).get("protocolVersion", PROTOCOL_VERSION),
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })
    elif method == "ping":
        _respond(msg_id, {})
    elif method == "tools/list":
        _respond(msg_id, {"tools": TOOLS})
    elif method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            _respond(msg_id, error={"code": -32602, "message": f"unknown tool {name!r}"})
            return
        try:
            text = handler(params.get("arguments") or {})
            is_error = text.startswith("REFUSED")
        except Exception as exc:  # every refusal is a result, not a crash
            text = f"REFUSED — {exc}"
            is_error = True
        _respond(msg_id, {"content": [{"type": "text", "text": text}], "isError": is_error})
    elif msg_id is not None:
        _respond(msg_id, error={"code": -32601, "message": f"method {method!r} not found"})
    # notifications (no id) are acknowledged by silence


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        handle(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
