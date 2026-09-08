import json
from pathlib import Path
import subprocess
import sys
import unittest

from _support import ROOT, temporary_directory


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_directory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def invoke(self, *args, executable=None):
        return subprocess.run([sys.executable, "-I", str(executable or ROOT / "vital-rehearsal"), *map(str, args)],
                              cwd=self.root, text=True, capture_output=True, timeout=6)

    def test_validate_has_no_physiology_claim(self):
        result = self.invoke("validate", ROOT / "scenarios/contract-control.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no physiology", result.stdout.lower())

    def test_invalid_cli_input_fails_without_traceback_or_payload(self):
        bad = self.root / "invalid.json"
        bad.write_text('{"patient_name":"PRIVATE_SENTINEL"}')
        result = self.invoke("validate", bad)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("PRIVATE_SENTINEL", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_example_does_not_overwrite_existing_file(self):
        example = self.root / "study.json"
        example.write_text("preserve me")
        self.assertNotEqual(self.invoke("example", "--output", example).returncode, 0)
        self.assertEqual(example.read_text(), "preserve me")

    def test_zipapp_is_reproducible_and_runs_without_checkout_imports(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from package_cli import build
        first = build(self.root / "first.pyz")
        second = build(self.root / "second.pyz")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        example = self.root / "study.json"
        self.assertEqual(self.invoke("example", "--output", example, executable=first).returncode, 0)
        result = self.invoke("run", example, "--output", self.root / "runs", executable=first)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        bundle = Path(json.loads(result.stdout)["bundle"])
        inspected = self.invoke("inspect", bundle, executable=first)
        self.assertEqual(inspected.returncode, 0, inspected.stdout + inspected.stderr)
        self.assertEqual(json.loads(inspected.stdout)["integrity"], "VERIFIED")
        replay = self.invoke("run", bundle / "study.json", "--output", self.root / "replay", executable=bundle / "runner.pyz")
        self.assertEqual(replay.returncode, 0, replay.stdout + replay.stderr)
        self.assertEqual((bundle / "runner.pyz").read_bytes(), first.read_bytes())
