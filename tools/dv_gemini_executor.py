#!/usr/bin/env python3
"""Narrow Gemini generateContent binding for the frozen P1 smoke specs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_request(model: str, prompt: str, api_key: str) -> urllib.request.Request:
    payload = json.dumps({"contents": [{"role": "user", "parts": [{"text": prompt}]}]}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    return urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")


def parse_response(raw: bytes, requested_model: str) -> tuple[str, dict, str]:
    decoded = json.loads(raw)
    text = "".join(part.get("text", "") for part in decoded.get("candidates", [{}])[0].get("content", {}).get("parts", []))
    return text, decoded.get("usageMetadata", {}), decoded.get("modelVersion", requested_model)


def emit_fixture(args: argparse.Namespace, run_dir: Path) -> int:
    response = {
        "candidates": [{"content": {"parts": [{"text": "FIXTURE_RESPONSE"}]}, "finishReason": "STOP"}],
        "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1, "totalTokenCount": 2},
        "modelVersion": args.model,
    }
    raw = json.dumps(response, separators=(",", ":"), ensure_ascii=False).encode()
    artifact = run_dir / "provider-raw-response.json"
    artifact.write_bytes(raw)
    event_log = os.environ.get("DV_EVENT_LOG")
    if event_log:
        event = {
            "run_id": os.environ.get("DV_RUN_ID"),
            "event_id": "fixture-gemini-usage",
            "token_category": "execution",
            "tokens": 2,
            "source": "provider-usage-fixture",
            "provider": "Google",
            "model_or_service": args.model,
            "cache_status": "unknown",
            "application_retry_count": 0,
            "provider_retry_metadata": "UNMEASURED",
        }
        with open(event_log, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, separators=(",", ":")) + "\n")
    print(json.dumps({"provider": "Google", "candidate": args.candidate, "model": args.model, "response": response, "raw_response_sha256": hashlib.sha256(raw).hexdigest()}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args()
    run_dir = Path(os.environ.get("DV_RUN_DIR", ".")).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    if args.fixture:
        return emit_fixture(args, run_dir)

    api_key = os.environ.get("GEMINI_API_KEY")
    prompt = os.environ.get("DV_TASK_PROMPT")
    if not api_key or not prompt:
        print("GEMINI_BINDING_BLOCKED: missing named credential or frozen task prompt", file=sys.stderr)
        return 78
    request = build_request(args.model, prompt, api_key)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=1800) as response:
            raw = response.read()
            status = response.status
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"GEMINI_PROVIDER_FAILURE: {type(exc).__name__}", file=sys.stderr)
        return 75
    artifact = run_dir / "provider-raw-response.json"
    artifact.write_bytes(raw)
    try:
        text, usage, observed_model = parse_response(raw, args.model)
    except (ValueError, IndexError, KeyError, TypeError):
        print("GEMINI_PROVIDER_FAILURE: invalid response", file=sys.stderr)
        return 75
    event_log = os.environ.get("DV_EVENT_LOG")
    if event_log:
        event = {"run_id": os.environ.get("DV_RUN_ID"), "event_id": f"gemini-{int(time.time_ns())}", "token_category": "execution", "source": "provider-usage", "provider": "Google", "model_or_service": observed_model, "cache_status": "unknown", "application_retry_count": 0, "provider_retry_metadata": "UNMEASURED"}
        mapping = (("promptTokenCount", "input_tokens"), ("candidatesTokenCount", "output_tokens"), ("totalTokenCount", "total_tokens"), ("cachedContentTokenCount", "cached_input_tokens"), ("thoughtsTokenCount", "reasoning_tokens"))
        for source, target in mapping:
            if source in usage:
                event[target] = usage[source]
        if isinstance(usage.get("totalTokenCount"), int):
            event["tokens"] = usage["totalTokenCount"]
        with open(event_log, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event, separators=(",", ":")) + "\n")
    print(json.dumps({"provider": "Google", "candidate": args.candidate, "requested_model": args.model, "observed_model": observed_model, "status": status, "latency_ms": round((time.monotonic() - started) * 1000, 3), "response": text, "usage": usage, "raw_response_sha256": hashlib.sha256(raw).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
