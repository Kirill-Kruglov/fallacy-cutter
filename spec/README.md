# spec/ — the decision.json format, frozen as a *format*

This directory exists so that `decision.json` can be verified by software that
has never read this repository's code. Appendix A.4 names the roadmap: first a
frozen, implementation-free specification; then a second implementation written
against it by someone who has never read the first. This is step one.

- [`decision-schema-v1.json`](decision-schema-v1.json) — JSON Schema
  (draft 2020-12) for a citable decision document.
- This file — the verification algorithm in prose, implementation-free.

## Verification algorithm (v1)

A verifier accepts a `decision.json` as **harness-valid** if and only if all of
the following hold. Any doubt — unreadable file, missing field, wrong type —
resolves to **refuse**. Nothing passes by default.

1. The document parses as a JSON object and contains a `_harness_provenance`
   object. Absence of the block means the decision was not produced by the
   sanctioned runner: refuse unconditionally, regardless of the numbers.
2. `_harness_provenance.written_by` equals the exact string
   `gate_harness.runner.run_gate`.
3. `_harness_provenance.harness_version` equals the verifier's own recomputation
   of the harness hash: for each top-level `gate_harness/*.py` file (sorted by
   filename, tests excluded), compute `"{filename}:{sha256(file bytes)}"`; join
   the lines with `\n`; the harness hash is the SHA256 of the UTF-8 encoding of
   the joined string. A mismatch means the harness changed since the run; the
   safe direction is to refuse and re-run.
4. `prereg_lock_verified`, `leakage_scan_verified`, and `tautology_check_ran`
   are each literally `true` (not truthy — `true`).
5. `evaluation_oracle_ran` is a boolean and is present.

## What the verdict word means

The reference implementation (`gate_harness/verify_decision.py`) prints `VALID`.
Read it as defined in Appendix A.1: **harness-valid** — procedural compliance
under the declared specification. It is not a claim of scientific validity; the
false-pass taxonomy (Appendix A.3) lists ten ways to be harness-valid and
worthless. A future major version renames the verdict to `GATE_PASS` with a
fresh provenance line; v1 of this spec keeps `VALID` so the spec and the
already-signed artifacts stay consistent.

## Versioning

The schema is append-only within v1: new *optional* fields may be documented,
but no required field is added, removed, or changed in meaning. Any breaking
change is v2, with a new file, and never rewrites this one.
