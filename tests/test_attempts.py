import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import unittest

from _support import ROOT, temporary_directory
from vital_rehearsal import builtin
from vital_rehearsal.attempts import list_attempts, run, verify_bundle
from vital_rehearsal.contracts import ContractError, canonical_json, digest


def rehash_manifest(directory):
    records = []
    for path in sorted(directory.iterdir()):
        if path.name != "manifest.json":
            data = path.read_bytes()
            records.append({"path": path.name, "bytes": len(data), "sha256": digest(data)})
    (directory / "manifest.json").write_bytes(canonical_json({"schema_version": 1, "files": records}))


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_directory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "attempts"

    def execute(self, fault="none"):
        return run(builtin.study(), self.output, fault)

    def test_complete_bundle_roundtrip_and_unique_rerun(self):
        first, result = self.execute()
        before = {p.name: p.read_bytes() for p in first.iterdir()}
        second, next_result = self.execute()
        self.assertNotEqual(first, second)
        self.assertEqual(result["study_sha256"], next_result["study_sha256"])
        self.assertEqual(verify_bundle(first)["evaluation"]["conclusion"], "CONTROL_AGREEMENT")
        self.assertEqual(before, {p.name: p.read_bytes() for p in first.iterdir()})
        self.assertEqual(len(list_attempts(self.output)), 2)

    def test_real_worker_failures_preserve_evidence_and_distinct_states(self):
        for fault, state, conclusion in (
            ("perturbed", "COMPLETED", "CONTRADICTED"),
            ("wrong-unit", "INVALID_MODEL", "INVALID_EVIDENCE"),
            ("truncated", "INVALID_MODEL", "INVALID_EVIDENCE"),
            ("nonfinite", "INVALID_MODEL", "INVALID_EVIDENCE"),
            ("impossible", "INVALID_MODEL", "INVALID_EVIDENCE"),
            ("nonconvergence", "FAILED_NUMERICAL", "INVALID_EVIDENCE"),
            ("crash", "FAILED_SYSTEM", "INVALID_EVIDENCE"),
        ):
            with self.subTest(fault=fault):
                directory, result = self.execute(fault)
                self.assertEqual(result["execution_state"], state)
                self.assertEqual(result["evaluation"]["conclusion"], conclusion)
                self.assertEqual(verify_bundle(directory)["control_fault"], fault)
                self.assertTrue((directory / "stderr.log").exists())

    def test_timeout_is_bounded_and_retained(self):
        start = time.monotonic()
        directory, result = self.execute("pause")
        self.assertLess(time.monotonic() - start, 4)
        self.assertEqual(result["execution_state"], "TIMED_OUT")
        self.assertEqual(verify_bundle(directory)["evaluation"]["observables"], [])

    def test_modified_csv_is_detected(self):
        directory, _ = self.execute()
        (directory / "trajectory.csv").write_text("changed")
        with self.assertRaises(ContractError):
            verify_bundle(directory)

    def test_false_success_in_rehashed_failed_bundle_is_rejected(self):
        directory, result = self.execute("crash")
        result["evaluation"]["conclusion"] = "CONTROL_AGREEMENT"
        (directory / "result.json").write_bytes(canonical_json(result))
        rehash_manifest(directory)
        with self.assertRaises(ContractError):
            verify_bundle(directory)

    def test_rehashed_fault_provenance_conflict_is_rejected(self):
        directory, result = self.execute()
        result["control_fault"] = "crash"
        (directory / "result.json").write_bytes(canonical_json(result))
        invocation = json.loads((directory / "invocation.json").read_text())
        invocation["control_fault"] = "crash"
        (directory / "invocation.json").write_bytes(canonical_json(invocation))
        rehash_manifest(directory)
        with self.assertRaises(ContractError):
            verify_bundle(directory)

    def test_fifo_manifest_fails_without_blocking(self):
        directory, _ = self.execute()
        (directory / "manifest.json").unlink()
        os.mkfifo(directory / "manifest.json")
        result = subprocess.run([sys.executable, str(ROOT / "vital-rehearsal"), "inspect", str(directory)],
                                capture_output=True, timeout=2)
        self.assertEqual(result.returncode, 2)

    def test_malicious_manifest_path_and_symlink_are_rejected(self):
        directory, _ = self.execute()
        manifest = json.loads((directory / "manifest.json").read_text())
        manifest["files"][0]["path"] = "../outside"
        (directory / "manifest.json").write_bytes(canonical_json(manifest))
        with self.assertRaises(ContractError):
            verify_bundle(directory)
        second, _ = self.execute()
        (second / "trajectory.csv").unlink()
        (second / "trajectory.csv").symlink_to(ROOT / "LICENSE")
        with self.assertRaises(ContractError):
            verify_bundle(second)

    def _interrupt(self, sig):
        process = subprocess.Popen(
            [sys.executable, str(ROOT / "vital-rehearsal"), "run", str(ROOT / "scenarios/contract-control.json"),
             "--output", str(self.output), "--control-fault", "pause"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.addCleanup(lambda: process.poll() is None and process.kill())
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            if any(p.stat().st_size > 0 for p in self.output.glob("*.partial/trajectory.csv")):
                break
            if process.poll() is not None:
                self.fail("coordinator stopped before interruption")
            time.sleep(.01)
        else:
            self.fail("coordinator did not start")
        process.send_signal(sig)
        process.communicate(timeout=3)
        return process.returncode

    def test_sigterm_finalizes_cancelled_evidence(self):
        self.assertEqual(self._interrupt(signal.SIGTERM), 130)
        entries = list_attempts(self.output)
        self.assertEqual(entries[0]["state"], "CANCELLED")
        self.assertTrue(entries[0]["complete"])

    def test_hard_interruption_preserves_partial_and_previous_complete_bundle(self):
        first, _ = self.execute()
        before = (first / "manifest.json").read_bytes()
        self.assertEqual(self._interrupt(signal.SIGKILL), -signal.SIGKILL)
        entries = list_attempts(self.output)
        self.assertIn("PARTIAL_INTERRUPTED", [entry["state"] for entry in entries])
        partial = next(self.output.glob("*.partial"))
        self.assertIn("1,1", (partial / "trajectory.csv").read_text())
        with self.assertRaises(ContractError):
            verify_bundle(partial)
        second, _ = self.execute()
        self.assertNotEqual(first, second)
        self.assertEqual((first / "manifest.json").read_bytes(), before)
        # The worker has a self alarm, so even a killed parent leaves no lasting process.
        time.sleep(4.1)

    def test_invalid_input_never_starts_or_persists_private_payload(self):
        spec = builtin.study()
        spec["patient_record"] = "PRIVATE_SENTINEL"
        with self.assertRaises(ContractError):
            run(spec, self.output)
        self.assertFalse(self.output.exists())
