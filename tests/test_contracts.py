import unittest
from unittest.mock import patch

from _support import ROOT
from vital_rehearsal import builtin
from vital_rehearsal.contracts import ContractError, canonical_json, decode_json, study_identity, validate_study


class StudyContractTests(unittest.TestCase):
    def test_fixed_study_and_semantic_numeric_identity(self):
        study = builtin.study()
        study["conditions"]["start"]["value"] = 0.0
        self.assertEqual(validate_study(study), builtin.study())

    def test_unknown_patient_or_execution_fields_are_rejected_without_echo(self):
        for field in ("patient_record", "adapter_path", "threshold", "arbitrary"):
            with self.subTest(field=field):
                study = builtin.study()
                study[field] = "PRIVATE_SENTINEL"
                with self.assertRaises(ContractError) as failure:
                    validate_study(study)
                self.assertNotIn("PRIVATE_SENTINEL", str(failure.exception))
                self.assertNotIn(field, str(failure.exception))

    def test_units_and_semantics_must_match(self):
        for field, value in (("unit", "ms"), ("unit", "S"), ("quantity_kind", "absolute_time")):
            study = builtin.study()
            study["conditions"]["stop"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ContractError):
                validate_study(study)

    def test_unsupported_numeric_inputs_do_not_coerce_to_valid(self):
        for value in (True, -1, 1, float("nan"), float("inf"), 10 ** 1000, "0"):
            study = builtin.study()
            study["conditions"]["start"]["value"] = value
            with self.subTest(value=type(value).__name__), self.assertRaises(ContractError):
                validate_study(study)

    def test_schema_version_requires_integer(self):
        for version in (True, 1.0, "1", 2):
            study = builtin.study()
            study["schema_version"] = version
            with self.subTest(version=version), self.assertRaises(ContractError):
                validate_study(study)

    def test_duplicate_keys_nonfinite_and_excessive_json_are_rejected(self):
        for raw in (
            b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e9999}',
            b'{"x":-1e-9999}', b'{"x":1.000000000000000000000000001}',
            b'\xff', b'[' * 40 + b'0' + b']' * 40, b' ' * (1024 * 1024 + 1),
        ):
            with self.subTest(prefix=raw[:20]), self.assertRaises(ContractError):
                decode_json(raw)

    def test_example_file_is_the_reviewed_contract(self):
        self.assertEqual(validate_study(decode_json((ROOT / "scenarios/contract-control.json").read_bytes())), builtin.study())

    def test_input_cannot_select_an_external_or_physiology_adapter(self):
        for model in ("pulse", "../../plugin.py", "https://example.org/model.py"):
            study = builtin.study()
            study["model_id"] = model
            with self.subTest(model=model), self.assertRaises(ContractError):
                validate_study(study)

    def test_changed_criteria_and_reference_require_new_study_identity(self):
        before = study_identity(builtin.study())
        modified = builtin.criteria()
        modified["observables"][0]["absolute_tolerance"] = 1
        with patch.object(builtin, "criteria", return_value=modified):
            self.assertNotEqual(before, study_identity(builtin.study()))
        with patch.object(builtin, "REFERENCE_CSV", "changed reference"):
            self.assertNotEqual(before, study_identity(builtin.study()))
