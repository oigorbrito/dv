import json
import io
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXECUTOR = HERE / "dv_gemini_executor.py"
sys.path.insert(0, str(HERE))
from dv_gemini_executor import build_request, extract_unified_diff, parse_response, response_request_id, safe_response_headers, write_candidate


class GeminiBindingTests(unittest.TestCase):
    def test_request_construction_has_fixed_surface_and_no_retry_setting(self):
        request = build_request("gemini-3.8-flash", "frozen prompt", "secret-not-logged")
        self.assertEqual(request.full_url, "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent")
        self.assertEqual(request.get_header("X-goog-api-key"), "secret-not-logged")

    def test_candidate_contract_accepts_only_unified_diff(self):
        self.assertIsNone(extract_unified_diff("plain answer"))
        self.assertEqual(extract_unified_diff("```diff\n--- a/a.txt\n+++ b/a.txt\n@@\n-x\n+y\n```"), "--- a/a.txt\n+++ b/a.txt\n@@\n-x\n+y\n")

    def test_response_headers_redact_credentials_and_preserve_request_id(self):
        headers = {"x-request-id": "req-1", "x-goog-api-key": "secret", "content-type": "application/json"}
        self.assertEqual(response_request_id(headers), "req-1")
        self.assertNotIn("x-goog-api-key", {k.lower() for k in safe_response_headers(headers)})

    def test_http_error_fixtures_preserve_status_body_and_retry_zero(self):
        for status in (429, 500):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                error = urllib.error.HTTPError("https://example.invalid", status, "fixture", {"x-request-id": "req-fixture", "x-goog-api-key": "secret"}, io.BytesIO(b'{"error":"fixture"}'))
                env = os.environ.copy()
                env.update({"DV_RUN_DIR": str(root), "DV_EVENT_LOG": str(root / "events.jsonl"), "DV_RUN_ID": "fixture-http" , "GEMINI_API_KEY": "secret-not-logged", "DV_TASK_PROMPT": "prompt"})
                with mock.patch("urllib.request.urlopen", side_effect=error), mock.patch.dict(os.environ, env, clear=True), mock.patch.object(sys, "argv", [str(EXECUTOR), "--candidate", "C1-google-gemini", "--model", "gemini-3.8-flash"]):
                    from dv_gemini_executor import main
                    self.assertEqual(main(), 75)
                payload = json.loads((root / "provider-error.json").read_text(encoding="utf-8"))
                self.assertEqual(payload["status"], status)
                self.assertEqual(payload["request_id"], "req-fixture")
                self.assertNotIn("x-goog-api-key", {key.lower() for key in payload["headers"]})
                event = json.loads((root / "events.jsonl").read_text(encoding="utf-8"))
                self.assertEqual(event["application_retry_count"], 0)

    def test_malformed_response_fixture_is_rejected(self):
        with self.assertRaises(json.JSONDecodeError):
            parse_response(b"not-json", "gemini-3.8-flash")

    def test_candidate_file_is_captured_with_canonical_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            self.assertTrue(write_candidate("```diff\n--- a/a.txt\n+++ b/a.txt\n@@\n-x\n+y\n```", path))
            self.assertEqual((path / "candidate.diff").read_text(encoding="utf-8"), "--- a/a.txt\n+++ b/a.txt\n@@\n-x\n+y\n")

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
