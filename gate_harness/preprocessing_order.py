"""AST preprocessing-order scan — fit-transformations must not see test data.

The second dominant real-world leak in ML-on-tabular/omics pipelines needs no
truth name in the code: a scaler, PCA, or feature selector is *fit* on the full
dataset and the split happens afterwards, so test-set statistics contaminate the
features every model trains on. Every downstream metric is then optimistic, and
nothing in the fit path mentions ground truth.

Like ``leakage_scanner``, this is a static scan of *registered* functions, not a
self-report. For every registered function it locates:

  (a) split call sites — calls whose name is a known splitter
      (``train_test_split`` and friends) or a ``.split(...)`` method call that
      receives at least one variable; the variables passed to a split call are
      recorded as *pre-split data names*;
  (b) fit call sites — ``.fit(...)`` / ``.fit_transform(...)`` method calls.

Violations:
  - ``fit_on_presplit_data``: a fit call receives a variable that is also passed
    to a split call (the full dataset);
  - ``fit_before_split``: within a function that contains a split call, a fit
    call occurs on an earlier line than the first split.

Fail closed: an empty registry, an uninspectable function, or a registry in
which *no* function contains a split call (so the fit/split order cannot be
established) is NOT_VERIFIABLE -> FAIL, never a silent pass.

What this structurally cannot catch: aliasing (``X2 = X``; the alias is not a
recorded pre-split name), splits and fits split across functions the scan cannot
order, fitting hidden inside library pipelines, and normalization done with raw
array math instead of a ``fit`` method. The scan makes the common sklearn-shaped
mistake visible; it does not prove the pipeline leak-free.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Any, Callable, Iterable

DEFAULT_SPLIT_CALL_NAMES: frozenset[str] = frozenset(
    {
        "train_test_split",
        "KFold",
        "StratifiedKFold",
        "GroupKFold",
        "StratifiedGroupKFold",
        "GroupShuffleSplit",
        "ShuffleSplit",
        "StratifiedShuffleSplit",
        "LeaveOneGroupOut",
        "LeavePGroupsOut",
        "TimeSeriesSplit",
        "train_val_test_split",
    }
)
DEFAULT_FIT_METHOD_NAMES: frozenset[str] = frozenset({"fit", "fit_transform"})


class PreprocessingOrderError(RuntimeError):
    pass


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _name_args(node: ast.Call) -> list[str]:
    names = [a.id for a in node.args if isinstance(a, ast.Name)]
    names += [k.value.id for k in node.keywords if isinstance(k.value, ast.Name)]
    return names


def _scan_function(
    fn: Callable,
    split_call_names: frozenset[str],
    fit_method_names: frozenset[str],
) -> dict[str, Any]:
    try:
        raw = inspect.getsource(fn)
        base_line = inspect.getsourcelines(fn)[1]
        source_file = inspect.getsourcefile(fn) or "<unknown>"
    except (OSError, TypeError) as exc:
        raise PreprocessingOrderError(
            f"cannot read source of {getattr(fn, '__name__', fn)!r}: {exc}; "
            f"a function whose source cannot be inspected is NOT_VERIFIABLE -> FAIL"
        ) from exc

    tree = ast.parse(textwrap.dedent(raw))
    split_calls: list[dict[str, Any]] = []
    fit_calls: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name is None:
            continue
        line = base_line + getattr(node, "lineno", 1) - 1
        if name in split_call_names or (
            name == "split" and isinstance(node.func, ast.Attribute) and _name_args(node)
        ):
            split_calls.append({"call": name, "line": line, "data_names": _name_args(node)})
        elif name in fit_method_names:
            fit_calls.append({"call": name, "line": line, "data_names": _name_args(node)})
    return {
        "file": source_file,
        "split_calls": split_calls,
        "fit_calls": fit_calls,
    }


def scan_preprocessing_order(
    pipeline_functions: Iterable[Callable],
    *,
    split_call_names: Iterable[str] = (),
    fit_method_names: Iterable[str] = (),
) -> dict[str, Any]:
    """Scan registered pipeline functions for fit-transformations that see test data.

    ``split_call_names`` / ``fit_method_names`` extend (never replace) the
    defaults. Returns an audit dict; ``passed`` is True only if at least one
    split call was found and no violation fired.
    """
    splits = DEFAULT_SPLIT_CALL_NAMES | frozenset(split_call_names)
    fits = DEFAULT_FIT_METHOD_NAMES | frozenset(fit_method_names)
    functions = list(pipeline_functions)
    if not functions:
        return {
            "computed_by": "NOT_VERIFIABLE",
            "reason": "no pipeline functions registered to scan",
            "passed": False,
        }

    per_function: dict[str, Any] = {}
    violations: list[dict[str, Any]] = []
    any_split = False
    presplit_names: set[str] = set()
    scanned: list[tuple[str, dict[str, Any]]] = []

    for fn in functions:
        fname = getattr(fn, "__qualname__", getattr(fn, "__name__", repr(fn)))
        try:
            info = _scan_function(fn, splits, fits)
        except PreprocessingOrderError as exc:
            return {
                "computed_by": "NOT_VERIFIABLE",
                "reason": str(exc),
                "passed": False,
            }
        scanned.append((fname, info))
        if info["split_calls"]:
            any_split = True
            for sc in info["split_calls"]:
                presplit_names.update(sc["data_names"])

    if not any_split:
        return {
            "computed_by": "NOT_VERIFIABLE",
            "reason": (
                "no split call found in any registered function — the fit/split "
                "order cannot be established; next: register the function where "
                "the train/test split happens (or extend split_call_names)"
            ),
            "functions_scanned": [name for name, _ in scanned],
            "passed": False,
        }

    for fname, info in scanned:
        fn_violations: list[dict[str, Any]] = []
        first_split_line = min((sc["line"] for sc in info["split_calls"]), default=None)
        for fc in info["fit_calls"]:
            leaked = sorted(set(fc["data_names"]) & presplit_names)
            if leaked:
                fn_violations.append(
                    {
                        "kind": "fit_on_presplit_data",
                        "call": fc["call"],
                        "data_names": leaked,
                        "file": info["file"],
                        "line": fc["line"],
                    }
                )
            elif first_split_line is not None and fc["line"] < first_split_line:
                fn_violations.append(
                    {
                        "kind": "fit_before_split",
                        "call": fc["call"],
                        "file": info["file"],
                        "line": fc["line"],
                    }
                )
        per_function[fname] = {
            "computed_by": "ast_scan",
            "split_calls": info["split_calls"],
            "fit_calls": info["fit_calls"],
            "violations": fn_violations,
        }
        violations.extend(fn_violations)

    return {
        "computed_by": "ast_scan",
        "presplit_data_names": sorted(presplit_names),
        "functions_scanned": [name for name, _ in scanned],
        "per_function": per_function,
        "violations": violations,
        "passed": not violations,
    }


def assert_preprocessing_order(
    pipeline_functions: Iterable[Callable],
    *,
    split_call_names: Iterable[str] = (),
    fit_method_names: Iterable[str] = (),
) -> dict[str, Any]:
    """Runner entrypoint: raise PreprocessingOrderError unless the scan passes cleanly."""
    report = scan_preprocessing_order(
        pipeline_functions,
        split_call_names=split_call_names,
        fit_method_names=fit_method_names,
    )
    if not report.get("passed"):
        if report.get("computed_by") == "NOT_VERIFIABLE":
            raise PreprocessingOrderError(
                f"preprocessing order NOT_VERIFIABLE: {report['reason']}"
            )
        lines = "\n".join(
            f"  {v['kind']}: .{v['call']}({', '.join(v.get('data_names', []))}) "
            f"@ {v['file']}:{v['line']}"
            for v in report["violations"]
        )
        raise PreprocessingOrderError(
            "fit-transformations touch pre-split data — test statistics leak into "
            f"training features:\n{lines}\n"
            "next: split first, then fit transformers on the train fold only "
            "(fit on train, transform on test)"
        )
    return report
