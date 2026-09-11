#!/usr/bin/env python3
"""Narrow Block-4M oracle adapter.

Runs only predeclared verifier commands from a task oracle spec and emits the
terminal dv verifier JSON contract. It is not a test framework or workflow
engine.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_check(check: dict[str, Any], cwd: Path, evidence_dir: Path) -> dict[str, Any]:
    check_id = str(check["id"])
    command = check["command"]
    expected = set(check.get("expected_exit_codes", [0]))
    stdout_path = evidence_dir / f"{check_id}.stdout.log"
    stderr_path = evidence_dir / f"{check_id}.stderr.log"
    started = time.monotonic()
    try:
        with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
            proc = subprocess.run(
                command,
                cwd=str(cwd),
                env=os.environ.copy(),
                stdout=out,
                stderr=err,
                text=True,
                check=False,
                timeout=check.get("timeout_seconds"),
            )
        rc = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        rc = None
        timed_out = True
    duration = time.monotonic() - started
    result = {
        "id": check_id,
        "role": check.get("role", "mandatory"),
        "command": command,
        "exit_code": rc,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "passed": (not timed_out and rc in expected),
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
    }
    if stdout_path.exists():
        result["stdout_sha256"] = sha256_file(stdout_path)
    if stderr_path.exists():
        result["stderr_sha256"] = sha256_file(stderr_path)
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    args = p.parse_args()
    spec_path = Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    cwd = Path(spec["working_directory"]).resolve()
    run_dir = Path(os.environ.get("DV_RUN_DIR", cwd / ".dv-run")).resolve()
    evidence_dir = run_dir / "oracle"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    if spec.get("status") != "EXECUTABLE":
        print(json.dumps({
            "outcome": "INCONCLUSIVE",
            "harness_valid": False,
            "evidence_refs": [str(spec_path)],
            "failure_attribution": "ORACLE_DEFECT",
            "reason": spec.get("blocker", "oracle spec is not executable"),
        }))
        return 0

    results = [run_check(check, cwd, evidence_dir) for check in spec.get("checks", [])]
    evidence_path = evidence_dir / "oracle-results.json"
    evidence_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    timed_out = [r for r in results if r["timed_out"]]
    failed = [r for r in results if not r["passed"] and not r["timed_out"]]
    mandatory_count = sum(1 for r in results if r["role"] == "mandatory")

    if not results or mandatory_count == 0:
        outcome, valid, attribution, reason = "INCONCLUSIVE", False, "ORACLE_DEFECT", "no mandatory executable checks"
    elif timed_out:
        outcome, valid, attribution, reason = "INCONCLUSIVE", False, "HARNESS_FAILURE", "one or more oracle checks timed out"
    elif failed:
        outcome, valid, attribution, reason = "NO", True, "PRODUCT_FAILURE", "one or more mandatory oracle checks failed"
    else:
        outcome, valid, attribution, reason = "YES", True, None, None

    print(json.dumps({
        "outcome": outcome,
        "harness_valid": valid,
        "evidence_refs": [str(evidence_path)],
        "failure_attribution": attribution,
        "reason": reason,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
