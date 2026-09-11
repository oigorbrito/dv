import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
HARNESS = HERE / "dv_pilot_harness.py"

class HarnessTests(unittest.TestCase):
    def _scripts_and_spec(self, root: Path, *, telemetry=True):
        executor = root / "executor.py"
        if telemetry:
            executor.write_text(
                "import json,os,uuid\n"
                "p=os.environ['DV_EVENT_LOG']; rid=os.environ['DV_RUN_ID']\n"
                "with open(p,'a',encoding='utf-8') as f:\n"
                " f.write(json.dumps({'run_id':rid,'event_id':str(uuid.uuid4()),'token_category':'execution','tokens':10,'monetary_cost':0.02,'currency':'USD'})+'\\n')\n",
                encoding="utf-8",
            )
        else:
            executor.write_text("print('no telemetry')\n", encoding="utf-8")
        verifier = root / "verifier.py"
        verifier.write_text(
            "import json\nprint(json.dumps({'outcome':'YES','harness_valid':True,'evidence_refs':['fixture:test'],'failure_attribution':None}))\n",
            encoding="utf-8",
        )
        spec = {
            "protocol_version": "4R-v1", "corpus_version": "v0", "task_id": "D-F1-01", "task_family": "F1",
            "base_revision": "fixture", "oracle_version": "fixture-oracle", "treatment_id": "E0",
            "treatment_version": "fixture", "rollout_id": "r1", "environment_id": "fixture-env",
            "executor_command": [sys.executable, str(executor)], "verifier_command": [sys.executable, str(verifier)],
        }
        spec_path = root / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        return spec_path

    def test_run_reconciles_complete_telemetry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self._scripts_and_spec(root)
            proc = subprocess.run([sys.executable, str(HARNESS), "run", "--spec", str(spec), "--out", str(root/"runs")], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            self.assertEqual(rec["status"], "PASS")
            self.assertTrue(rec["primary_metrics_complete"])
            self.assertEqual(rec["recomputed"]["total_system_tokens"], 10)
            self.assertAlmostEqual(rec["recomputed"]["total_monetary_cost"], 0.02)

    def test_missing_telemetry_is_not_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self._scripts_and_spec(root, telemetry=False)
            proc = subprocess.run([sys.executable, str(HARNESS), "run", "--spec", str(spec), "--out", str(root/"runs")], text=True, capture_output=True)
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
            (root / "verifier.py").write_text("import json\nprint(json.dumps({'outcome':'YES','harness_valid':True,'evidence_refs':[]}))\n", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(HARNESS), "run", "--spec", str(spec), "--out", str(root/"runs")], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 2)
            run_dir = Path(proc.stdout.strip())
            rec = json.loads((run_dir / "reconciliation.json").read_text(encoding="utf-8"))
            self.assertEqual(rec["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
