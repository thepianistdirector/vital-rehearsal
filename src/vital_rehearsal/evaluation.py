"""Evaluator-owned contract and independent reference; no producer thresholds."""

import csv
import io
from decimal import Decimal, InvalidOperation, localcontext

from . import builtin
from .contracts import ContractError, canonical_json

MAX_TRAJECTORY_BYTES = 64 * 1024


def _trajectory(data: bytes, label: str):
    if len(data) > MAX_TRAJECTORY_BYTES:
        raise ContractError(f"{label}: trajectory exceeds 64 KiB")
    try:
        rows = list(csv.reader(io.StringIO(data.decode("utf-8")), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise ContractError(f"{label}: malformed CSV") from exc
    if not rows or rows[0] != builtin.criteria()["reference_header"]:
        raise ContractError(f"{label}: missing or incompatible observable units/header")
    if len(rows) != 6:
        raise ContractError(f"{label}: incomplete or excessive trajectory")
    values = []
    for row in rows[1:]:
        if len(row) != 2 or any(not cell.strip() for cell in row):
            raise ContractError(f"{label}: invalid trajectory row")
        try:
            if any(len(cell) > 100 for cell in row):
                raise ContractError(f"{label}: excessive numeric token")
            point = tuple(Decimal(cell) for cell in row)
        except (ValueError, InvalidOperation) as exc:
            raise ContractError(f"{label}: non-numeric cell") from exc
        if not all(x.is_finite() for x in point):
            raise ContractError(f"{label}: non-finite trajectory")
        if any(abs(x.as_tuple().exponent) > 1000 for x in point):
            raise ContractError(f"{label}: numeric exponent exceeds control limits")
        values.append(point)
    if [point[0] for point in values] != builtin.criteria()["time_grid"]:
        raise ContractError(f"{label}: incomplete, duplicate or reordered sampling times")
    return values


def invalid(reason: str):
    return {
        "conclusion": "INVALID_EVIDENCE",
        "scope": "SOFTWARE_CONTROL_NOT_PHYSIOLOGY",
        "observables": [],
        "failures": [reason],
        "uncertainty": builtin.model_card()["uncertainty"],
        "conservation": "NOT_APPLICABLE",
    }


def evaluate(data: bytes, diagnostics: dict, reference: bytes, criteria: dict):
    # Frozen config and reference must still match the reviewed built-in contract.
    try:
        if canonical_json(criteria) != canonical_json(builtin.criteria()) or reference != builtin.REFERENCE_CSV.encode():
            return invalid("evaluation contract or independent reference changed")
    except (TypeError, ValueError):
        return invalid("malformed evaluation contract")
    required = {"schema_version", "model_id", "solver", "solver_version", "state", "samples", "fault"}
    if not isinstance(diagnostics, dict) or set(diagnostics) != required:
        return invalid("missing or malformed adapter diagnostics")
    if (
        type(diagnostics["schema_version"]) is not int or diagnostics["schema_version"] != 1
        or diagnostics["model_id"] != builtin.CONTROL_ID
        or diagnostics["solver"] != "integer-enumeration"
        or diagnostics["solver_version"] != "1"
        or diagnostics["state"] != "COMPLETED"
        or type(diagnostics["samples"]) is not int or diagnostics["samples"] != 5
        or not isinstance(diagnostics["fault"], str)
        or diagnostics["fault"] not in {
            "none", "perturbed", "wrong-unit", "truncated", "nonfinite", "impossible",
        }
    ):
        return invalid("adapter did not supply a complete supported execution")
    try:
        actual = _trajectory(data, "adapter")
        expected = _trajectory(reference, "reference")
    except ContractError as exc:
        return invalid(str(exc))
    if any(value < 0 or value > 4 for _, value in actual):
        return invalid("counter outside the declared control domain [0, 4]")
    with localcontext() as context:
        # Exact for the bounded 100-character tokens and exponent range above.
        context.prec = 2048
        differences = [abs(a[1] - b[1]) for a, b in zip(actual, expected)]
    matches = all(error == 0 for error in differences)
    return {
        "conclusion": "CONTROL_AGREEMENT" if matches else "CONTRADICTED",
        "scope": "SOFTWARE_CONTROL_NOT_PHYSIOLOGY",
        "observables": [{
            "name": "counter", "unit": "1", "samples": len(actual),
            "maximum_absolute_error": str(max(differences)), "absolute_tolerance": 0,
            "state": "MATCH" if matches else "MISMATCH",
        }],
        "failures": [] if matches else ["counter differs from the exact independent control"],
        "uncertainty": builtin.model_card()["uncertainty"],
        "conservation": "NOT_APPLICABLE",
    }
