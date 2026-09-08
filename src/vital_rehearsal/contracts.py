"""Closed, bounded JSON input contracts. No document grants execution authority."""

import hashlib
import json
import math
import os
import stat
from decimal import Decimal, InvalidOperation
from pathlib import Path

from . import builtin

MAX_JSON_BYTES = 1024 * 1024


class ContractError(ValueError):
    """Input cannot be accepted under the reviewed fixed contract."""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("duplicate JSON field")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ContractError("non-finite JSON number")


def _parse_float(token):
    # Reject decimal literals that float parsing would silently round or underflow
    # into a supported fixed input. Ordinary JSON emitted by this build round-trips.
    try:
        exact = Decimal(token)
        value = float(token)
        if not math.isfinite(value) or Decimal(str(value)) != exact:
            raise ContractError("JSON numeric literal loses precision or is non-finite")
    except (InvalidOperation, OverflowError) as exc:
        raise ContractError("unsupported JSON numeric literal") from exc
    return value


def _check_finite(value, depth=0):
    if depth > 32:
        raise ContractError("JSON nesting exceeds 32 levels")
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            _check_finite(child, depth + 1)
    elif isinstance(value, list):
        for child in value:
            _check_finite(child, depth + 1)


def decode_json(data: bytes):
    if len(data) > MAX_JSON_BYTES:
        raise ContractError("JSON exceeds 1 MiB limit")
    try:
        result = json.loads(
            data.decode("utf-8"), object_pairs_hook=_unique_object,
            parse_constant=_reject_constant, parse_float=_parse_float,
        )
        _check_finite(result)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError("invalid UTF-8 JSON document") from exc
    return result


def read_regular(path: Path, limit=MAX_JSON_BYTES):
    """Do not block on FIFOs/devices or follow a swapped symlink."""
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ContractError("input artifact cannot be opened as a regular file") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ContractError("input artifact must be a regular file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise ContractError("input artifact exceeds its byte limit")
        return data
    finally:
        os.close(fd)


def read_json(path: Path):
    return decode_json(read_regular(path))


def canonical_json(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def study_identity(spec: dict) -> str:
    """Bind the study to model scope, source-defined reference and full criteria."""
    return digest(canonical_json({
        "study": spec, "model_card": builtin.model_card(), "criteria": builtin.criteria(),
        "reference_sha256": digest(builtin.REFERENCE_CSV.encode()),
    }))


def _match(value, expected, location="study"):
    if isinstance(expected, dict):
        if not isinstance(value, dict):
            raise ContractError(f"{location}: expected an object")
        if set(value) != set(expected):
            # Do not echo arbitrary input keys: rejected documents may contain private text.
            raise ContractError(f"{location}: unknown or missing fields")
        for key in expected:
            _match(value[key], expected[key], f"{location}.{key}")
    elif isinstance(expected, list):
        if not isinstance(value, list) or len(value) != len(expected):
            raise ContractError(f"{location}: unsupported item count")
        for index, item in enumerate(expected):
            _match(value[index], item, f"{location}[{index}]")
    elif type(expected) is int:
        if type(value) not in (int, float) or value != expected:
            raise ContractError(f"{location}: unsupported numeric value")
    elif type(value) is not type(expected) or value != expected:
        if location.endswith(".unit"):
            raise ContractError(f"{location}: incompatible or unsupported unit")
        raise ContractError(f"{location}: unsupported value")


def validate_study(value):
    _check_finite(value)
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int:
        raise ContractError("study.schema_version: expected integer version")
    _match(value, builtin.study())
    # Normalize numerically identical literals so study identity is semantic here.
    return builtin.study()
