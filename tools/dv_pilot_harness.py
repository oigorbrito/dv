#!/usr/bin/env python3
"""dv Block-4R measurement harness: one treatment run, one verifier, auditable evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "dv-pilot-run-v1"
OUTCOMES = {"YES", "NO", "INCONCLUSIVE"}
TOKEN_CATEGORIES = {"routing", "planning", "context", "execution", "handoff", "verification", "retry"}
FAILURE_ATTRIBUTIONS = {None, "PRODUCT_FAILURE", "HARNESS_FAILURE", "ORACLE_DEFECT", "ENVIRONMENT_DRIFT", "INCONCLUSIVE_OTHER"}
SUGGESTION_EVIDENCE_CLASSES = {
    "EMPIRICAL_RESEARCH_GUIDANCE", "EXPERIMENTAL_DESIGN", "REPRODUCIBILITY",
    "MEASUREMENT", "ORACLE_VALIDITY", "FAILURE_ATTRIBUTION", "TRACEABILITY",
}
REQUIRED_SPEC = (
    "protocol_version", "corpus_version", "task_id", "task_family", "base_revision",
    "oracle_version", "treatment_id", "treatment_version", "rollout_id", "environment_id",
    "working_directory", "executor_command", "verifier_command",
)
MATERIAL_ARTIFACTS = (
    "spec.json", "events.jsonl", "child-events.jsonl", "executor.stdout.log",
    "executor.stderr.log", "verifier.stdout.log", "verifier.stderr.log",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(canonical_json(value) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_suggestion(suggestion: dict[str, Any]) -> dict[str, Any]:
    """Apply the evidence gate to one methodological/documentary suggestion."""
    required = (
        "proposed_change", "evidence_class", "experimental_problem_addressed",
        "necessity", "existing_artifact_sufficient", "smallest_sufficient_change",
        "consequence_if_not_done",
    )
    errors = [f"missing suggestion field: {key}" for key in required if key not in suggestion]
    classes = suggestion.get("evidence_class")
    if isinstance(classes, str):
        classes = [classes]
    if not isinstance(classes, list) or not classes or not all(isinstance(value, str) for value in classes):
        errors.append("evidence_class must be a non-empty string or array of strings")
        classes = []
    elif any(value not in SUGGESTION_EVIDENCE_CLASSES for value in classes):
        errors.append("evidence_class contains an unsupported class")
    for key in ("proposed_change", "experimental_problem_addressed", "smallest_sufficient_change", "consequence_if_not_done"):
        if key in suggestion and (not isinstance(suggestion[key], str) or not suggestion[key].strip()):
            errors.append(f"{key} must be a non-empty string")
    if "necessity" in suggestion and suggestion["necessity"] is not True:
        errors.append("necessity must be true for a supported recommendation")
    if suggestion.get("existing_artifact_sufficient") is True:
        errors.append("existing artifact is sufficient; no change is necessary")
    supported = not errors
    return {
        "supported": "YES" if supported else "NO",
        "recommendation": "ACCEPTED" if supported else "REJECTED_UNSUPPORTED",
        "evidence_class": classes,
        "experimental_problem_addressed": suggestion.get("experimental_problem_addressed"),
        "smallest_sufficient_change": suggestion.get("smallest_sufficient_change"),
        "errors": errors,
    }


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors = [f"missing spec field: {k}" for k in REQUIRED_SPEC if k not in spec]
    if spec.get("task_family") not in {f"F{i}" for i in range(1, 7)}:
        errors.append("task_family must be F1..F6")
    for key in ("executor_command", "verifier_command"):
        value = spec.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(x, str) for x in value):
            errors.append(f"{key} must be a non-empty JSON array of strings")
    wd = spec.get("working_directory")
    if wd is not None and (not Path(wd).exists() or not Path(wd).is_dir()):
        errors.append("working_directory must exist and be a directory")
    for key in ("executor_timeout_seconds", "verifier_timeout_seconds"):
        if key in spec:
            value = spec[key]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                errors.append(f"{key} must be a positive number")
    return errors


def event(run_id: str, phase: str, kind: str, **extra: Any) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "event_id": str(uuid.uuid4()),
        "timestamp": utc_now(),
        "phase": phase,
        "kind": kind,
        **extra,
    }


def run_process(argv: list[str], cwd: str, env: dict[str, str], stdout: Path, stderr: Path, timeout: float | None) -> dict[str, Any]:
    started = time.monotonic()
    timed_out = False
    with stdout.open("w", encoding="utf-8") as out, stderr.open("w", encoding="utf-8") as err:
        try:
            proc = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=err, text=True, check=False, timeout=timeout)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            exit_code = 124
            err.write(f"timeout after {timeout} seconds\n")
            err.flush()
    return {
        "exit_code": exit_code,
        "duration_seconds": time.monotonic() - started,
        "timed_out": timed_out,
        "timeout_seconds": timeout,
        "termination_reason": "TIMEOUT" if timed_out else "PROCESS_EXIT",
    }


def git_probe(cwd: str, args: list[str]) -> str | None:
    try:
        proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False, timeout=2)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def environment_snapshot(cwd: str, spec: dict[str, Any]) -> dict[str, Any]:
    head = git_probe(cwd, ["rev-parse", "HEAD"])
    status = git_probe(cwd, ["status", "--porcelain=v1"])
    root = git_probe(cwd, ["rev-parse", "--show-toplevel"])
    return {
        "declared_environment_id": spec["environment_id"],
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "git": {
            "available": head is not None,
            "worktree_root": root,
            "head": head,
            "dirty": None if status is None else bool(status),
            "status_sha256": None if status is None else sha256_bytes(status.encode()),
        },
        "toolchain": spec.get("toolchain_versions", {}),
        "container_image_digest": spec.get("container_image_digest"),
    }


def read_verifier_result(path: Path, verifier_timed_out: bool) -> dict[str, Any]:
    if verifier_timed_out:
        return {"outcome": "INCONCLUSIVE", "harness_valid": False, "evidence_refs": [], "failure_attribution": "HARNESS_FAILURE", "reason": "verifier timeout"}
    lines = [x.strip() for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    try:
        obj = json.loads(lines[-1]) if lines else None
    except json.JSONDecodeError as exc:
        obj = None
        reason = f"verifier final non-empty line is not JSON: {exc}"
    else:
        reason = "verifier produced no JSON result" if obj is None else None
    if not isinstance(obj, dict):
        return {"outcome": "INCONCLUSIVE", "harness_valid": False, "evidence_refs": [], "failure_attribution": "HARNESS_FAILURE", "reason": reason or "verifier result must be a JSON object"}
    if obj.get("outcome") not in OUTCOMES or obj.get("failure_attribution") not in FAILURE_ATTRIBUTIONS:
        return {"outcome": "INCONCLUSIVE", "harness_valid": False, "evidence_refs": [], "failure_attribution": "HARNESS_FAILURE", "reason": "invalid verifier contract"}
    if obj["outcome"] != "INCONCLUSIVE" and obj.get("harness_valid") is not True:
        return {"outcome": "INCONCLUSIVE", "harness_valid": False, "evidence_refs": [], "failure_attribution": "HARNESS_FAILURE", "reason": "YES/NO requires harness_valid=true"}
    return obj


def parse_child_events(path: Path, run_id: str) -> tuple[list[dict[str, Any]], list[str]]:
    events, errors = [], []
    if not path.exists():
        return events, errors
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"child event line {line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(ev, dict) or ev.get("run_id") != run_id:
            errors.append(f"child event line {line_no}: invalid or misbound event")
            continue
        if ev.get("token_category") is not None and ev["token_category"] not in TOKEN_CATEGORIES:
            errors.append(f"child event line {line_no}: invalid token_category")
        if ("tokens" in ev or "monetary_cost" in ev) and not ev.get("source"):
            errors.append(f"child event line {line_no}: resource telemetry requires source")
        if "tokens" in ev and (not ev.get("provider") or not ev.get("model_or_service")):
            errors.append(f"child event line {line_no}: token telemetry requires provider and model_or_service")
        if "monetary_cost" in ev and not (ev.get("billing_ref") or ev.get("price_schedule_ref")):
            errors.append(f"child event line {line_no}: monetary telemetry requires billing_ref or price_schedule_ref")
        if ev.get("cache_status") not in {None, "hit", "miss", "partial", "not_applicable", "unknown"}:
            errors.append(f"child event line {line_no}: invalid cache_status")
        events.append(ev)
    return events, errors


def artifact_manifest(run_dir: Path) -> dict[str, Any]:
    return {name: {"sha256": sha256_file(run_dir / name), "bytes": (run_dir / name).stat().st_size if (run_dir / name).is_file() else None} for name in MATERIAL_ARTIFACTS}


def reconcile(run_dir: Path, summary: dict[str, Any], events: list[dict[str, Any]], parse_errors: list[str]) -> dict[str, Any]:
    errors, warnings, seen = list(parse_errors), [], set()
    token_seen = money_seen = False
    tokens, money, currencies = 0, 0.0, set()
    for ev in events:
        eid = ev.get("event_id")
        if not eid:
            errors.append("child event missing event_id")
        elif eid in seen:
            errors.append(f"duplicate child event_id: {eid}")
        else:
            seen.add(eid)
        if "tokens" in ev:
            token_seen = True
            value = ev["tokens"]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"event {eid}: tokens must be non-negative integer")
            else:
                tokens += value
        if "monetary_cost" in ev:
            money_seen = True
            value = ev["monetary_cost"]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"event {eid}: monetary_cost must be non-negative number")
            else:
                money += float(value)
            currency = ev.get("currency")
            if not currency:
                errors.append(f"event {eid}: monetary_cost requires currency")
            else:
                currencies.add(currency)
    if not token_seen:
        warnings.append("MISSING/UNRESOLVED token telemetry")
    if not money_seen:
        warnings.append("MISSING/UNRESOLVED monetary telemetry")
    if len(currencies) > 1:
        errors.append("multiple currencies observed without predeclared normalization")
    verification = summary["verification"]
    if verification["outcome"] != "INCONCLUSIVE" and not verification.get("evidence_refs"):
        errors.append("conclusive verifier result requires non-empty evidence_refs")
    if summary["process_results"]["verifier"]["timed_out"] and verification["outcome"] != "INCONCLUSIVE":
        errors.append("verifier timeout requires INCONCLUSIVE outcome")
    base = summary["identity"]["base_revision"]
    observed_head = summary["environment"]["git"]["head"]
    if len(base) == 40 and all(c in "0123456789abcdefABCDEF" for c in base) and observed_head and base.lower() != observed_head.lower():
        errors.append(f"base revision mismatch: declared {base}, observed {observed_head}")
    metrics_complete = token_seen and money_seen and len(currencies) <= 1
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": summary["run_id"],
        "status": "PASS" if not errors else "FAIL",
        "primary_metrics_complete": metrics_complete,
        "errors": errors,
        "warnings": warnings,
        "recomputed": {
            "child_event_count": len(events),
            "total_system_tokens": tokens if token_seen else None,
            "total_monetary_cost": money if money_seen and len(currencies) <= 1 else None,
            "currency": next(iter(currencies)) if len(currencies) == 1 else None,
            "wall_clock_seconds": summary["timing"]["wall_clock_seconds"],
        },
        "artifact_manifest": artifact_manifest(run_dir),
    }


def cmd_run(args: argparse.Namespace) -> int:
    loaded = load_json(Path(args.spec).resolve())
    spec = loaded
    if isinstance(loaded, dict) and isinstance(loaded.get("specs"), list):
        if not args.run_id:
            raise SystemExit("aggregate spec requires --run-id")
        matches = [candidate for candidate in loaded["specs"] if isinstance(candidate, dict) and candidate.get("run_id") == args.run_id]
        if len(matches) != 1:
            raise SystemExit(f"aggregate spec does not contain exactly one spec for run id: {args.run_id}")
        spec = matches[0]
    if not isinstance(spec, dict):
        raise SystemExit("spec must be a JSON object")
    errors = validate_spec(spec)
    if errors:
        raise SystemExit("\n".join(errors))
    run_id = args.run_id or f"{spec['task_id']}--{spec['treatment_id']}--{spec['rollout_id']}--{uuid.uuid4().hex[:12]}"
    run_dir = Path(args.out).resolve() / run_id
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(exist_ok=False)
    spec_digest = sha256_bytes(canonical_json(spec).encode())
    write_json(run_dir / "spec.json", spec)
    (run_dir / "child-events.jsonl").touch(exist_ok=False)
    events_path = run_dir / "events.jsonl"
    started_utc, started_mono = utc_now(), time.monotonic()
    append_jsonl(events_path, event(run_id, "harness", "run_start", spec_sha256=spec_digest))
    cwd = str(Path(spec["working_directory"]).resolve())
    env_snapshot = environment_snapshot(cwd, spec)
    env = os.environ.copy()
    env.update({"DV_RUN_ID": run_id, "DV_EVENT_LOG": str(run_dir / "child-events.jsonl"), "DV_RUN_DIR": str(run_dir), "DV_TASK_ID": str(spec["task_id"]), "DV_TREATMENT_ID": str(spec["treatment_id"])})

    executor = spec["executor_command"]
    append_jsonl(events_path, event(run_id, "execution", "process_start", argv=executor, timeout_seconds=spec.get("executor_timeout_seconds")))
    exec_result = run_process(executor, cwd, env, run_dir / "executor.stdout.log", run_dir / "executor.stderr.log", spec.get("executor_timeout_seconds"))
    append_jsonl(events_path, event(run_id, "execution", "process_end", argv=executor, **exec_result))

    verifier = spec["verifier_command"]
    append_jsonl(events_path, event(run_id, "verification", "process_start", argv=verifier, timeout_seconds=spec.get("verifier_timeout_seconds")))
    ver_result = run_process(verifier, cwd, env, run_dir / "verifier.stdout.log", run_dir / "verifier.stderr.log", spec.get("verifier_timeout_seconds"))
    verification = read_verifier_result(run_dir / "verifier.stdout.log", ver_result["timed_out"])
    append_jsonl(events_path, event(run_id, "verification", "process_end", argv=verifier, **ver_result))

    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "spec_sha256": spec_digest,
        "identity": {k: spec[k] for k in REQUIRED_SPEC if k not in {"executor_command", "verifier_command", "working_directory"}},
        "working_directory": cwd,
        "commands": {"executor": executor, "verifier": verifier},
        "process_results": {"executor": exec_result, "verifier": ver_result},
        "verification": verification,
        "timing": {"start_utc": started_utc, "end_utc": utc_now(), "wall_clock_seconds": time.monotonic() - started_mono, "executor_seconds": exec_result["duration_seconds"], "verifier_seconds": ver_result["duration_seconds"]},
        "environment": env_snapshot,
    }
    child_events, child_errors = parse_child_events(run_dir / "child-events.jsonl", run_id)
    append_jsonl(events_path, event(run_id, "harness", "run_end", outcome=verification["outcome"]))
    rec = reconcile(run_dir, summary, child_events, child_errors)
    summary.update({"accounting": rec["recomputed"], "reconciliation_status": rec["status"], "primary_metrics_complete": rec["primary_metrics_complete"], "artifact_manifest": rec["artifact_manifest"]})
    write_json(run_dir / "run.json", summary)
    write_json(run_dir / "reconciliation.json", rec)
    print(run_dir)
    return 0 if rec["status"] == "PASS" else 2


def cmd_reconcile(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    summary = load_json(run_dir / "run.json")
    child_events, child_errors = parse_child_events(run_dir / "child-events.jsonl", summary["run_id"])
    rec = reconcile(run_dir, summary, child_events, child_errors)
    write_json(run_dir / "reconciliation.json", rec)
    print(json.dumps(rec, indent=2, sort_keys=True))
    return 0 if rec["status"] == "PASS" else 2


def cmd_policy_check(args: argparse.Namespace) -> int:
    suggestion = load_json(Path(args.suggestion).resolve())
    if not isinstance(suggestion, dict):
        raise SystemExit("suggestion must be a JSON object")
    result = validate_suggestion(suggestion)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["supported"] == "YES" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--spec", required=True)
    run.add_argument("--out", default="pilot-runs")
    run.add_argument("--run-id")
    run.set_defaults(func=cmd_run)
    rec = sub.add_parser("reconcile")
    rec.add_argument("run_dir")
    rec.set_defaults(func=cmd_reconcile)
    policy = sub.add_parser("policy-check", help="validate an evidence-gated methodological/documentary suggestion")
    policy.add_argument("--suggestion", required=True)
    policy.set_defaults(func=cmd_policy_check)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
