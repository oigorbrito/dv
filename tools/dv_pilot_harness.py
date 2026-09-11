#!/usr/bin/env python3
"""Minimal dv Block-4R pilot measurement harness.

Stdlib-only, append-only run artifacts. It intentionally does not implement
routing, planning, provider selection, or a workflow engine.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "dv-pilot-run-v1"
OUTCOMES = {"YES", "NO", "INCONCLUSIVE"}
TOKEN_CATEGORIES = {
    "routing", "planning", "context", "execution",
    "handoff", "verification", "retry"
}
REQUIRED_SPEC = (
    "protocol_version", "corpus_version", "task_id", "task_family",
    "base_revision", "oracle_version", "treatment_id",
    "treatment_version", "rollout_id", "environment_id",
    "executor_command", "verifier_command",
)

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

def append_event(path: Path, event: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(canonical_json(event) + "\n")
        fh.flush()
        os.fsync(fh.fileno())

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors = [f"missing spec field: {k}" for k in REQUIRED_SPEC if k not in spec]
    for key in ("executor_command", "verifier_command"):
        if key in spec and (not isinstance(spec[key], list) or not spec[key] or not all(isinstance(x, str) for x in spec[key])):
            errors.append(f"{key} must be a non-empty JSON array of strings")
    if "task_family" in spec and spec["task_family"] not in {f"F{i}" for i in range(1, 7)}:
        errors.append("task_family must be F1..F6")
    return errors

def safe_run_dir(root: Path, run_id: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    target = root / run_id
    target.mkdir(exist_ok=False)
    return target

def command_event(run_id: str, phase: str, kind: str, argv: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "event_id": str(uuid.uuid4()),
        "timestamp": now(),
        "phase": phase,
        "kind": kind,
        "argv": argv,
        **extra,
    }

def run_process(argv: list[str], cwd: str | None, env: dict[str, str], stdout_path: Path, stderr_path: Path) -> tuple[int, float]:
    start = time.monotonic()
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=out, stderr=err, text=True, check=False)
    return proc.returncode, time.monotonic() - start

def read_verifier_result(stdout_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    lines = [line.strip() for line in stdout_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None, "verifier produced no JSON result"
    try:
        obj = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        return None, f"verifier final non-empty line is not JSON: {exc}"
    if not isinstance(obj, dict):
        return None, "verifier result must be a JSON object"
    outcome = obj.get("outcome")
    if outcome not in OUTCOMES:
        return None, f"verifier outcome must be one of {sorted(OUTCOMES)}"
    if obj.get("harness_valid") is not True and outcome != "INCONCLUSIVE":
        return None, "YES/NO requires harness_valid=true"
    return obj, None

def parse_child_events(path: Path, run_id: str) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], []
    events, errors = [], []
    for idx, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"child event line {idx}: invalid JSON: {exc}")
            continue
        if not isinstance(ev, dict):
            errors.append(f"child event line {idx}: event must be object")
            continue
        if ev.get("run_id") != run_id:
            errors.append(f"child event line {idx}: run_id mismatch")
            continue
        category = ev.get("token_category")
        if category is not None and category not in TOKEN_CATEGORIES:
            errors.append(f"child event line {idx}: invalid token_category {category!r}")
        events.append(ev)
    return events, errors

def reconcile(run_dir: Path, summary: dict[str, Any], child_events: list[dict[str, Any]], child_errors: list[str]) -> dict[str, Any]:
    errors = list(child_errors)
    warnings: list[str] = []
    seen_ids: set[str] = set()
    token_total = 0
    money_total = 0.0
    token_telemetry_seen = False
    money_telemetry_seen = False

    for ev in child_events:
        event_id = ev.get("event_id")
        if not event_id:
            errors.append("child event missing event_id")
        elif event_id in seen_ids:
            errors.append(f"duplicate child event_id: {event_id}")
        else:
            seen_ids.add(event_id)

        if "tokens" in ev:
            token_telemetry_seen = True
            tokens = ev["tokens"]
            if not isinstance(tokens, int) or isinstance(tokens, bool) or tokens < 0:
                errors.append(f"event {event_id}: tokens must be non-negative integer")
            else:
                token_total += tokens
        if "monetary_cost" in ev:
            money_telemetry_seen = True
            cost = ev["monetary_cost"]
            if not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0:
                errors.append(f"event {event_id}: monetary_cost must be non-negative number")
            else:
                money_total += float(cost)
            if not ev.get("currency"):
                errors.append(f"event {event_id}: monetary_cost requires currency")

    if not token_telemetry_seen:
        warnings.append("MISSING/UNRESOLVED token telemetry")
    if not money_telemetry_seen:
        warnings.append("MISSING/UNRESOLVED monetary telemetry")

    verification = summary["verification"]
    if verification["outcome"] != "INCONCLUSIVE" and not verification.get("evidence_refs"):
        errors.append("conclusive verifier result requires non-empty evidence_refs")

    primary_metrics_complete = token_telemetry_seen and money_telemetry_seen
    status = "PASS" if not errors else "FAIL"
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": summary["run_id"],
        "status": status,
        "primary_metrics_complete": primary_metrics_complete,
        "errors": errors,
        "warnings": warnings,
        "recomputed": {
            "child_event_count": len(child_events),
            "total_system_tokens": token_total if token_telemetry_seen else None,
            "total_monetary_cost": money_total if money_telemetry_seen else None,
            "wall_clock_seconds": summary["timing"]["wall_clock_seconds"],
        },
    }

def cmd_run(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec).resolve()
    spec = load_json(spec_path)
    if not isinstance(spec, dict):
        raise SystemExit("spec must be a JSON object")
    errors = validate_spec(spec)
    if errors:
        raise SystemExit("\n".join(errors))

    spec_digest = sha256_text(canonical_json(spec))
    run_id = args.run_id or f"{spec['task_id']}--{spec['treatment_id']}--{spec['rollout_id']}--{uuid.uuid4().hex[:12]}"
    run_dir = safe_run_dir(Path(args.out).resolve(), run_id)
    events_path = run_dir / "events.jsonl"
    child_event_path = run_dir / "child-events.jsonl"
    write_json(run_dir / "spec.json", spec)

    start_utc, start_mono = now(), time.monotonic()
    append_event(events_path, {
        "schema_version": SCHEMA_VERSION, "run_id": run_id, "event_id": str(uuid.uuid4()),
        "timestamp": start_utc, "phase": "harness", "kind": "run_start",
        "spec_sha256": spec_digest,
    })

    env = os.environ.copy()
    env.update({
        "DV_RUN_ID": run_id,
        "DV_EVENT_LOG": str(child_event_path),
        "DV_RUN_DIR": str(run_dir),
        "DV_TASK_ID": str(spec["task_id"]),
        "DV_TREATMENT_ID": str(spec["treatment_id"]),
    })
    cwd = spec.get("working_directory")

    executor = spec["executor_command"]
    append_event(events_path, command_event(run_id, "execution", "process_start", executor))
    exec_rc, exec_seconds = run_process(executor, cwd, env, run_dir/"executor.stdout.log", run_dir/"executor.stderr.log")
    append_event(events_path, command_event(run_id, "execution", "process_end", executor, exit_code=exec_rc, duration_seconds=exec_seconds))

    verifier = spec["verifier_command"]
    append_event(events_path, command_event(run_id, "verification", "process_start", verifier))
    ver_rc, ver_seconds = run_process(verifier, cwd, env, run_dir/"verifier.stdout.log", run_dir/"verifier.stderr.log")
    verification, verification_error = read_verifier_result(run_dir/"verifier.stdout.log")
    if verification_error:
        verification = {
            "outcome": "INCONCLUSIVE",
            "harness_valid": False,
            "evidence_refs": [],
            "failure_attribution": "HARNESS_FAILURE",
            "reason": verification_error,
        }
    append_event(events_path, command_event(run_id, "verification", "process_end", verifier, exit_code=ver_rc, duration_seconds=ver_seconds))

    end_utc = now()
    wall = time.monotonic() - start_mono
    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "spec_sha256": spec_digest,
        "identity": {k: spec[k] for k in REQUIRED_SPEC if k not in {"executor_command", "verifier_command"}},
        "commands": {"executor": executor, "verifier": verifier},
        "process_results": {"executor_exit_code": exec_rc, "verifier_exit_code": ver_rc},
        "verification": verification,
        "timing": {
            "start_utc": start_utc, "end_utc": end_utc,
            "wall_clock_seconds": wall,
            "executor_seconds": exec_seconds,
            "verifier_seconds": ver_seconds,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "artifacts": {
            "event_log": "events.jsonl",
            "child_event_log": "child-events.jsonl",
            "executor_stdout": "executor.stdout.log",
            "executor_stderr": "executor.stderr.log",
            "verifier_stdout": "verifier.stdout.log",
            "verifier_stderr": "verifier.stderr.log",
        },
    }
    child_events, child_errors = parse_child_events(child_event_path, run_id)
    rec = reconcile(run_dir, summary, child_events, child_errors)
    summary["accounting"] = rec["recomputed"]
    summary["reconciliation_status"] = rec["status"]
    summary["primary_metrics_complete"] = rec["primary_metrics_complete"]

    write_json(run_dir/"run.json", summary)
    write_json(run_dir/"reconciliation.json", rec)
    append_event(events_path, {
        "schema_version": SCHEMA_VERSION, "run_id": run_id, "event_id": str(uuid.uuid4()),
        "timestamp": now(), "phase": "harness", "kind": "run_end",
        "outcome": verification["outcome"], "reconciliation_status": rec["status"],
    })
    print(run_dir)
    return 0 if rec["status"] == "PASS" else 2

def cmd_reconcile(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    summary = load_json(run_dir/"run.json")
    child_events, child_errors = parse_child_events(run_dir/"child-events.jsonl", summary["run_id"])
    rec = reconcile(run_dir, summary, child_events, child_errors)
    write_json(run_dir/"reconciliation.json", rec)
    print(json.dumps(rec, indent=2, sort_keys=True))
    return 0 if rec["status"] == "PASS" else 2

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    r = sub.add_parser("run", help="execute one treatment run and verifier")
    r.add_argument("--spec", required=True)
    r.add_argument("--out", default="pilot-runs")
    r.add_argument("--run-id")
    r.set_defaults(func=cmd_run)
    q = sub.add_parser("reconcile", help="recompute integrity checks for an existing run")
    q.add_argument("run_dir")
    q.set_defaults(func=cmd_reconcile)
    return p

def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
