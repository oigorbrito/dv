#!/usr/bin/env python3
"""Controlled base→candidate Fail-to-Pass replay for Block 4N F4 tasks.

The same focal command is executed in two already-materialized workspaces.
Expected contract: base must fail because the candidate test/artifact is absent or
fails; candidate must pass. Any timeout/launch ambiguity is INCONCLUSIVE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def execute(command: list[str], cwd: Path, timeout: int) -> dict:
    started = time.time()
    try:
        p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False)
        return {"status": "COMPLETED", "exit_code": p.returncode, "stdout_sha256": digest(p.stdout), "stderr_sha256": digest(p.stderr), "elapsed_seconds": time.time()-started}
    except subprocess.TimeoutExpired as e:
        return {"status": "TIMEOUT", "exit_code": None, "stdout_sha256": digest((e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")), "stderr_sha256": digest((e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")), "elapsed_seconds": time.time()-started}
    except OSError as e:
        return {"status": "LAUNCH_ERROR", "exit_code": None, "error": str(e), "elapsed_seconds": time.time()-started}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-workspace", required=True, type=Path)
    ap.add_argument("--candidate-workspace", required=True, type=Path)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not command:
        raise SystemExit("missing focal command")
    base = execute(command, args.base_workspace, args.timeout)
    candidate = execute(command, args.candidate_workspace, args.timeout)
    if base["status"] != "COMPLETED" or candidate["status"] != "COMPLETED":
        outcome = "INCONCLUSIVE"
    elif base["exit_code"] != 0 and candidate["exit_code"] == 0:
        outcome = "YES"
    elif base["exit_code"] == 0:
        outcome = "INCONCLUSIVE"  # no demonstrated Fail-to-Pass contrast
    else:
        outcome = "NO"
    record = {"schema_version": "dv-f4-replay-v1", "command": command, "base": base, "candidate": candidate, "fail_to_pass": outcome}
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if outcome == "YES" else (1 if outcome == "NO" else 2)

if __name__ == "__main__":
    raise SystemExit(main())
