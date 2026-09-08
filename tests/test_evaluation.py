import unittest

from _support import ROOT
from vital_rehearsal import builtin
from vital_rehearsal.evaluation import evaluate


def diagnostics():
    return {"schema_version": 1, "model_id": builtin.CONTROL_ID, "solver": "integer-enumeration",
            "solver_version": "1", "state": "COMPLETED", "samples": 5, "fault": "none"}


def check(raw, diagnostic=None, reference=None, criteria=None):
    return evaluate(raw, diagnostics() if diagnostic is None else diagnostic,
                    builtin.REFERENCE_CSV.encode() if reference is None else reference,
                    builtin.criteria() if criteria is None else criteria)


class EvaluationTests(unittest.TestCase):
    def test_independent_hand_checkable_reference(self):
        result = check(b"time[s],counter[1]\n0,0\n1,1\n2,2\n3,3\n4,4\n")
        self.assertEqual(result["conclusion"], "CONTROL_AGREEMENT")
        self.assertEqual(result["observables"][0]["maximum_absolute_error"], "0")
        self.assertEqual(result["scope"], "SOFTWARE_CONTROL_NOT_PHYSIOLOGY")

    def test_perturbation_is_retained_as_contradiction(self):
        result = check(builtin.REFERENCE_CSV.replace("2,2", "2,2.25").encode())
        self.assertEqual(result["conclusion"], "CONTRADICTED")
        self.assertEqual(result["observables"][0]["maximum_absolute_error"], "0.25")

    def test_incomplete_nonfinite_unit_time_and_domain_failures_have_no_score(self):
        base = builtin.REFERENCE_CSV
        for raw in (
            base.replace("counter[1]", "counter[mL]"), base.replace("4,4\n", ""),
            base.replace("2,2", "2,nan"), base.replace("2,2", "2,-1"),
            base.replace("2,2", "1,2"), base + "5,5\n", base.replace("2,2", "2,"),
            base.replace("0,0", "0,-1e-9999"),
        ):
            with self.subTest(raw=raw):
                result = check(raw.encode())
                self.assertEqual(result["conclusion"], "INVALID_EVIDENCE")
                self.assertEqual(result["observables"], [])

    def test_decimal_perturbation_cannot_round_into_agreement(self):
        result = check(builtin.REFERENCE_CSV.replace("2,2", "2,2.000000000000000000000000001").encode())
        self.assertEqual(result["conclusion"], "CONTRADICTED")
        self.assertEqual(result["observables"][0]["maximum_absolute_error"], "1E-27")

    def test_incomplete_diagnostics_never_receive_agreement(self):
        for key, value in (("samples", True), ("samples", 4), ("state", "FAILED_NUMERICAL"),
                           ("solver_version", "unknown"), ("fault", [])):
            diagnostic = diagnostics()
            diagnostic[key] = value
            with self.subTest(key=key):
                self.assertEqual(check(builtin.REFERENCE_CSV.encode(), diagnostic)["conclusion"], "INVALID_EVIDENCE")

    def test_producer_cannot_change_tolerance_or_reference(self):
        criteria = builtin.criteria()
        criteria["observables"][0]["absolute_tolerance"] = 100
        for kwargs in ({"criteria": criteria}, {"reference": b"changed"}):
            with self.subTest(kwargs=kwargs):
                self.assertEqual(check(builtin.REFERENCE_CSV.encode(), **kwargs)["conclusion"], "INVALID_EVIDENCE")
