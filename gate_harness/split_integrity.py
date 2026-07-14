"""Group-aware split integrity — leakage through data structure, not code.

The AST leakage scanner catches truth *names* in the fit path. In domains with
grouped observations (patients with multiple samples, subjects with repeated
measures, batches) the dominant real-world leak is different: the same group
appears on both sides of a train/test split, so the model memorizes the group
and the held-out score is fiction. No forbidden name ever appears in the code.

This module checks the split itself, at runtime, against a *declared* grouping:

  - the grouping key MUST be declared (``declared_group_key``); an undeclared
    grouping is NOT_VERIFIABLE and fails closed — "we did not think about
    grouping" is precisely the failure being caught;
  - every sample MUST carry a group value; a missing/None group fails closed;
  - no group value may appear in more than one split.

What this structurally cannot catch: a wrong-but-declared grouping (grouping by
sample when the confound is the patient), and dependence that crosses declared
groups (site effects, time). The declaration makes the choice auditable; it does
not make it right.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Sequence


class SplitIntegrityError(RuntimeError):
    """Raised when the split violates (or cannot prove) group integrity."""


def check_group_split_integrity(
    groups: Sequence[Any],
    splits: Sequence[Any],
    *,
    declared_group_key: str,
) -> dict[str, Any]:
    """Return an audit report; ``passed`` is True only if no group crosses splits.

    ``groups[i]`` is the group value of sample *i* (e.g. its patient id);
    ``splits[i]`` is the split it was assigned to (e.g. ``"train"``/``"test"``).
    """
    if not isinstance(declared_group_key, str) or not declared_group_key.strip():
        return {
            "computed_by": "NOT_VERIFIABLE",
            "reason": (
                "no declared_group_key — an undeclared grouping cannot be checked; "
                "next: declare the unit of independence (e.g. 'patient_id') and "
                "pass its per-sample values"
            ),
            "passed": False,
        }

    groups = list(groups)
    splits = list(splits)
    if not groups or len(groups) != len(splits):
        return {
            "computed_by": "NOT_VERIFIABLE",
            "reason": (
                f"groups ({len(groups)}) and splits ({len(splits)}) must be equal-"
                f"length non-empty sequences aligned by sample"
            ),
            "declared_group_key": declared_group_key,
            "passed": False,
        }

    missing = [i for i, g in enumerate(groups) if g is None or (isinstance(g, float) and g != g)]
    if missing:
        return {
            "computed_by": "NOT_VERIFIABLE",
            "reason": (
                f"{len(missing)} sample(s) have no {declared_group_key!r} value "
                f"(first at index {missing[0]}); a sample without a group cannot be "
                f"checked; next: assign every sample a group or exclude it before "
                f"the split"
            ),
            "declared_group_key": declared_group_key,
            "passed": False,
        }

    splits_by_group: dict[Any, dict[Any, int]] = defaultdict(lambda: defaultdict(int))
    split_sizes: dict[Any, int] = defaultdict(int)
    for g, s in zip(groups, splits):
        splits_by_group[g][s] += 1
        split_sizes[s] += 1

    violations = [
        {
            "group": repr(g),
            "splits": {str(s): n for s, n in sorted(seen.items(), key=lambda kv: str(kv[0]))},
        }
        for g, seen in splits_by_group.items()
        if len(seen) > 1
    ]

    return {
        "computed_by": "group_membership_scan",
        "declared_group_key": declared_group_key,
        "n_samples": len(groups),
        "n_groups": len(splits_by_group),
        "split_sizes": {str(s): n for s, n in sorted(split_sizes.items(), key=lambda kv: str(kv[0]))},
        "groups_crossing_splits": violations,
        "passed": not violations,
    }


def assert_group_split_integrity(
    groups: Sequence[Any],
    splits: Sequence[Any],
    *,
    declared_group_key: str,
) -> dict[str, Any]:
    """Runner entrypoint: raise SplitIntegrityError unless the check passes cleanly."""
    report = check_group_split_integrity(groups, splits, declared_group_key=declared_group_key)
    if not report.get("passed"):
        if report.get("computed_by") == "NOT_VERIFIABLE":
            raise SplitIntegrityError(f"split integrity NOT_VERIFIABLE: {report['reason']}")
        crossing = report["groups_crossing_splits"]
        sample = ", ".join(
            f"{v['group']} in {sorted(v['splits'])}" for v in crossing[:5]
        )
        raise SplitIntegrityError(
            f"{len(crossing)} group(s) by {declared_group_key!r} appear in more "
            f"than one split ({sample}{', ...' if len(crossing) > 5 else ''}) — "
            f"held-out metrics are not held out; next: re-split with a group-aware "
            f"splitter (e.g. GroupKFold/GroupShuffleSplit over {declared_group_key!r})"
        )
    return report
