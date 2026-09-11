import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dv_pilot_harness import validate_suggestion

HERE = Path(__file__).resolve().parent
HARNESS = HERE / "dv_pilot_harness.py"


class HarnessTests(unittest.TestCase):
    def test_evidence_gated_suggestion_is_accepted(self):
        result = validate_suggestion({
            "proposed_change": "Record verifier SHA-256",
            "evidence_class": ["REPRODUCIBILITY", "ORACLE_VALIDITY"],
            "experimental_problem_addressed": "Parent and candidate verifier bytes must be reproducible",
            "necessity": True,
            "existing_artifact_sufficient": False,
            "smallest_sufficient_change": "Add one SHA-256 field to the admission evidence",
            "consequence_if_not_done": "Independent replay cannot prove identical verifier input",
        })
        self.assertEqual(result["recommendation"], "ACCEPTED")
        self.assertEqual(result["supported"], "YES")

    def test_unsupported_documentary_preference_is_rejected(self):
        result = validate_suggestion({
            "proposed_change": "Add an architecture overview",
            "evidence_class": [],
            "experimental_problem_addressed": "",
            "necessity": False,
            "existing_artifact_sufficient": True,
            "smallest_sufficient_change": "",
            "consequence_if_not_done": "None for reproduction",
        })
        self.assertEqual(result["recommendation"], "REJECTED_UNSUPPORTED")
        self.assertEqual(result["supported"], "NO")
        self.assertTrue(result["errors"])

    def test_unknown_evidence_class_is_rejected(self):
        result = validate_suggestion({
            "proposed_change": "Create a richer dashboard",
            "evidence_class": ["BEST_PRACTICE"],
            "experimental_problem_addressed": "No declared measurement problem",
            "necessity": True,
            "existing_artifact_sufficient": False,
            "smallest_sufficient_change": "Create the dashboard",
            "consequence_if_not_done": "Status is less polished",
        })
        self.assertEqual(result["recommendation"], "REJECTED_UNSUPPORTED")
    def _scripts_and_spec(self, root: Path, *, telemetry=True):
        executor = root / "executor.py"
        if telemetry:
            executor.write_text(
                "import json,os,uuid\n"
                "p=os.environ['DV_EVENT_LOG']; rid=os.environ['DV_RUN_ID']\n"
                "with open(p,'a',encoding='utf-8') as f:\n"
                " f.write(json.dumps({'run_id':rid,'event_id':str(uuid.uuid4()),'token_category':'execution','tokens':10,'monetary_cost':0.02,'currency':'USD','source':'provider-usage','provider':'fixture-provider','model_or_service':'fixture-model','cache_status':'miss','price_schedule_ref':'fixture-price-v1'})+'\\n')\n",
                encoding="utf-8",
            )
        else:
            executor.write_text("print('no telemetry')\n", encoding="utf-8")

        verifier = root / "verifier.py"
        verifier.write_text(
            "import json\n"
            "print(json.dumps({'outcome':'YES','harness_valid':True,'evidence_refs':['fixture:test'],'failure_attribution':None}))\n",
            encoding="utf-8",
        )

        spec = {
            "protocol_version": "4R-v1",
            "corpus_version": "v0",
            "task_id": "D-F1-01",
            "task_family": "F1",
            "base_revision": "fixture",
            "oracle_version": "fixture-oracle",
            "treatment_id": "E0",
            "treatment_version": "fixture",
            "rollout_id": "r1",
            "environment_id": "fixture-env",
            "working_directory": str(root),
            "executor_command": [sys.executable, str(executor)],
            "verifier_command": [sys.executable, str(verifier)],
            "executor_timeout_seconds": 5,
            "verifier_timeout_seconds": 5,
            "toolchain_versions": {"fixture": "1"},
        }
        spec_path = root / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        return spec_path

    def _run(self, root: Path, spec: Path):
        return subprocess.run(
            [sys.executable, str(HARNESS), "run", "--spec", str(spec), "--out", str(root / "runs")],
            text=True,
            capture_output=True,
        )

    def test_run_reconciles_complete_telemetry_and_hashes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = self._run(root, self._scripts_and_spec(root))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            summary = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(rec["status"], "PASS")
            self.assertTrue(rec["primary_metrics_complete"])
            self.assertEqual(rec["recomputed"]["total_system_tokens"], 10)
            self.assertAlmostEqual(rec["recomputed"]["total_monetary_cost"], 0.02)
            self.assertEqual(rec["recomputed"]["currency"], "USD")
            self.assertEqual(summary["environment"]["declared_environment_id"], "fixture-env")
            self.assertIn("git", summary["environment"])
            for name in ("spec.json", "events.jsonl", "executor.stdout.log", "executor.stderr.log", "verifier.stdout.log", "verifier.stderr.log"):
                self.assertIsNotNone(summary["artifact_manifest"][name]["sha256"])

    def test_missing_telemetry_is_not_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = self._run(root, self._scripts_and_spec(root, telemetry=False))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            self.assertFalse(rec["primary_metrics_complete"])
            self.assertIsNone(rec["recomputed"]["total_system_tokens"])
            self.assertIsNone(rec["recomputed"]["total_monetary_cost"])

    def test_conclusive_result_without_evidence_fails_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self._scripts_and_spec(root)
            (root / "verifier.py").write_text(
                "import json\nprint(json.dumps({'outcome':'YES','harness_valid':True,'evidence_refs':[]}))\n",
                encoding="utf-8",
            )
            proc = self._run(root, spec)
            self.assertEqual(proc.returncode, 2)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            self.assertEqual(rec["status"], "FAIL")

    def test_resource_telemetry_without_provenance_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self._scripts_and_spec(root)
            (root / "executor.py").write_text(
                "import json,os,uuid\n"
                "p=os.environ['DV_EVENT_LOG']; rid=os.environ['DV_RUN_ID']\n"
                "with open(p,'a',encoding='utf-8') as f:\n"
                " f.write(json.dumps({'run_id':rid,'event_id':str(uuid.uuid4()),'token_category':'execution','tokens':10,'monetary_cost':0.02,'currency':'USD'})+'\\n')\n",
                encoding="utf-8",
            )
            proc = self._run(root, spec)
            self.assertEqual(proc.returncode, 2)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            self.assertEqual(rec["status"], "FAIL")
            self.assertTrue(any("requires source" in error for error in rec["errors"]))

    def test_verifier_timeout_becomes_inconclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_path = self._scripts_and_spec(root)
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["verifier_timeout_seconds"] = 0.05
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            (root / "verifier.py").write_text("import time\ntime.sleep(1)\n", encoding="utf-8")
            proc = self._run(root, spec_path)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            run_dir = Path(proc.stdout.strip())
            summary = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["verification"]["outcome"], "INCONCLUSIVE")
            self.assertEqual(summary["verification"]["failure_attribution"], "HARNESS_FAILURE")
            self.assertTrue(summary["process_results"]["verifier"]["timed_out"])

    def test_executor_timeout_is_recorded_without_forcing_product_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_path = self._scripts_and_spec(root)
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["executor_timeout_seconds"] = 0.05
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            (root / "executor.py").write_text("import time\ntime.sleep(1)\n", encoding="utf-8")
            proc = self._run(root, spec_path)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            run_dir = Path(proc.stdout.strip())
            summary = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertTrue(summary["process_results"]["executor"]["timed_out"])
            self.assertNotEqual(summary["verification"].get("failure_attribution"), "PRODUCT_FAILURE")


if __name__ == "__main__":
    unittest.main()
