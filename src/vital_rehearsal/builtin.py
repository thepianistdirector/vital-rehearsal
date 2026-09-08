"""Reviewed, fixed software-control contract; never a physiology benchmark.

The producer does not import this evaluator-owned reference definition.
"""

import copy

CONTROL_ID = "integer-counter-control-v1"
LIMITATION = (
    "Software contract control only. No physiology model is admitted. "
    "These values verify bookkeeping and evaluation, not physiology, "
    "clinical validity, treatment, or benefit."
)

_STUDY = {
    "schema_version": 1,
    "model_id": CONTROL_ID,
    "model_version": "1",
    "source_id": "vital-rehearsal:analytic-integer-identity-v1",
    "input_kind": "wholly-synthetic-software-control",
    "purpose": "software-verification",
    "conditions": {
        "start": {"value": 0, "unit": "s", "quantity_kind": "elapsed_time"},
        "stop": {"value": 4, "unit": "s", "quantity_kind": "elapsed_time"},
        "interval": {"value": 1, "unit": "s", "quantity_kind": "elapsed_time"},
    },
    "solver": {"method": "integer-enumeration", "version": "1"},
    "observables": [
        {"name": "counter", "unit": "1", "quantity_kind": "dimensionless_count"}
    ],
    "comparison_id": "exact-integer-identity-v1",
    "applicability": "fixed-software-control-only",
}

_CARD = {
    "schema_version": 1,
    "model_id": CONTROL_ID,
    "model_version": "1",
    "classification": "SOFTWARE_CONTROL_NOT_PHYSIOLOGY",
    "question": "Does the runner retain and evaluate the exact integer identity?",
    "source": {
        "id": "vital-rehearsal:analytic-integer-identity-v1",
        "kind": "hand-checkable-analytic-identity",
        "definition": "counter(t) = t at t = 0, 1, 2, 3, 4 seconds; counter is dimensionless",
        "reference_origin": "Evaluator-owned literal values, independent of producer output",
        "original_code_license": "AGPL-3.0-only",
        "third_party_model_or_data": False,
    },
    "applicability": "Fixed wholly synthetic software control; no organism or population",
    "supported_variations": [],
    "solver": "Integer enumeration, not a numerical integrator",
    "uncertainty": {
        "control_arithmetic": "Exact integer values within binary64 exact range",
        "physiology": "NOT ASSESSED; no physiological model",
        "clinical": "NOT ASSESSED; no clinical claim",
    },
    "conservation": "NOT APPLICABLE; no physical conserved quantity is modeled",
    "human_review": "No qualified physiology review supplied; control is software evidence only",
    "limits": [LIMITATION, "No patient, cohort, treatment, or user-defined parameter inputs"],
    "execution_boundary": "Trusted built-in code with resource limits; not a sandbox",
}

_CRITERIA = {
    "schema_version": 1,
    "comparison_id": "exact-integer-identity-v1",
    "reference_header": ["time[s]", "counter[1]"],
    "sample_count": 5,
    "time_grid": [0, 1, 2, 3, 4],
    "observables": [{
        "name": "counter", "unit": "1", "quantity_kind": "dimensionless_count",
        "absolute_tolerance": 0,
        "basis": "The analytic control has exact integer values; no interpolation or solver error",
        "minimum": 0, "maximum": 4,
    }],
    "interpolation": "forbidden",
    "missing_output": "invalid",
    "conservation": "not-applicable",
    "physiological_reuse": "forbidden; each admitted model requires its own source-justified criteria",
}

REFERENCE_CSV = "time[s],counter[1]\n0,0\n1,1\n2,2\n3,3\n4,4\n"


def study():
    return copy.deepcopy(_STUDY)


def model_card():
    return copy.deepcopy(_CARD)


def criteria():
    return copy.deepcopy(_CRITERIA)
