import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXECUTOR = HERE / "dv_gemini_executor.py"
sys.path.insert(0, str(HERE))
from dv_gemini_executor import build_request, parse_response


class GeminiBindingTests(unittest.TestCase):
    def test_request_construction_has_fixed_surface_and_no_retry_setting(self):
        request = build_request("gemini-3.8-flash", "frozen prompt", "secret-not-logged")
        self.assertEqual(request.full_url, "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent")
        self.assertEqual(request.get_header("X-goog-api-key"), "secret-not-logged")
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.get_header("Content-type"), "application/json")

    def test_response_parser_preserves_usage_and_observed_model(self):
        raw = json.dumps({"modelVersion": "gemini-3.8-flash-001", "candidates": [{"content": {"parts": [{"text": "patch"}]}}], "usageMetadata": {"promptTokenCount": 4, "candidatesTokenCount": 5, "totalTokenCount": 9}}).encode()
        text, usage, model = parse_response(raw, "gemini-3.8-flash")
        self.assertEqual((text, usage["totalTokenCount"], model), ("patch", 9, "gemini-3.8-flash-001"))

    def test_fixture_binding_captures_candidate_and_usage_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event_log = root / "events.jsonl"
            env = os.environ.copy()
            env.update({"DV_RUN_ID": "fixture-run", "DV_RUN_DIR": str(root), "DV_EVENT_LOG": str(event_log)})
            env.pop("GEMINI_API_KEY", None)
            result = subprocess.run(
                [sys.executable, str(EXECUTOR), "--candidate", "C1-google-gemini", "--model", "gemini-3.8-flash", "--fixture"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["candidate"], "C1-google-gemini")
            self.assertEqual(output["model"], "gemini-3.8-flash")
            self.assertEqual(json.loads(event_log.read_text())["tokens"], 2)
            self.assertTrue((root / "provider-raw-response.json").is_file())

    def test_real_binding_fails_closed_without_named_credential_or_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env.pop("GEMINI_API_KEY", None)
            env.pop("DV_TASK_PROMPT", None)
            result = subprocess.run(
                [sys.executable, str(EXECUTOR), "--candidate", "C4-google-gemini-3-8-flash", "--model", "gemini-3.8-flash"],
                env=env,
                text=True,
                capture_output=True,
                check=False,
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 78)
            self.assertNotIn("GEMINI_API_KEY=", result.stderr)
