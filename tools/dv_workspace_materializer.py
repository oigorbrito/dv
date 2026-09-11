#!/usr/bin/env python3
"""Materialize an isolated Git workspace at an explicitly frozen revision.

Narrow Block 4N utility. It does not install dependencies, select providers,
or execute treatments. It records enough Git identity to reject drift before a run.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(argv: list[str], cwd: Path | None = None) -> str:
    p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {argv!r}\n{p.stderr}")
    return p.stdout.strip()


def materialize(repository: str, revision: str, destination: Path) -> dict:
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{repository}.git"
    run(["git", "clone", "--no-checkout", url, str(destination)])
    try:
        run(["git", "checkout", "--detach", revision], destination)
        head = run(["git", "rev-parse", "HEAD"], destination)
        if head.lower() != revision.lower():
            raise RuntimeError(f"revision mismatch: expected {revision}, got {head}")
        status = run(["git", "status", "--porcelain"], destination)
        if status:
            raise RuntimeError("fresh materialized workspace is unexpectedly dirty")
        origin = run(["git", "remote", "get-url", "origin"], destination)
        return {
            "repository": repository,
            "requested_revision": revision,
            "head_revision": head,
            "origin": origin,
            "worktree_clean": True,
            "destination": str(destination.resolve()),
        }
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repository", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--destination", required=True, type=Path)
    ap.add_argument("--identity-out", type=Path)
    args = ap.parse_args()
    identity = materialize(args.repository, args.revision, args.destination)
    encoded = json.dumps(identity, indent=2, sort_keys=True) + "\n"
    if args.identity_out:
        args.identity_out.parent.mkdir(parents=True, exist_ok=True)
        args.identity_out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
