#!/usr/bin/env python3
"""Materialize an isolated Git workspace at an explicitly frozen revision.

Narrow Block 4N utility. It does not install dependencies, select providers,
or execute treatments. It records enough Git identity to reject drift before a run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path


def run(argv: list[str], cwd: Path | None = None) -> str:
    p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {argv!r}\n{p.stderr}")
    return p.stdout.strip()


def run_bytes(argv: list[str], cwd: Path | None = None) -> bytes:
    p = subprocess.run(argv, cwd=cwd, capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {argv!r}\n{p.stderr.decode(errors='replace')}")
    return p.stdout


def local_git(source: Path, args: list[str]) -> list[str]:
    return ["git", "-c", f"safe.directory={source.resolve()}", "-C", str(source), *args]


@contextmanager
def blob_stream(source: Path):
    process = subprocess.Popen(
        local_git(source, ["cat-file", "--batch"]),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        yield process
    finally:
        process.stdin.close()
        process.wait(timeout=30)
        if process.returncode:
            stderr = process.stderr.read().decode(errors="replace") if process.stderr else ""
            raise RuntimeError(f"git cat-file --batch failed ({process.returncode}): {stderr}")
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()


def materialize_local(source: Path, revision: str, destination: Path) -> dict:
    """Materialize Git blobs without checkout filters or archive normalization."""
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    source = source.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    try:
        entries = run_bytes(local_git(source, ["ls-tree", "-r", "-z", revision]))
        parsed = []
        for record in entries.split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, oid = header.split(b" ", 2)
            if object_type != b"blob":
                raise RuntimeError(f"unexpected tree entry type: {object_type!r}")
            parsed.append((mode.decode(), oid.decode(), raw_path.decode("utf-8", "surrogateescape")))

        symlink_fallbacks = []
        file_hashes = {}
        with blob_stream(source) as stream:
            assert stream.stdin is not None and stream.stdout is not None
            for mode, oid, relative in parsed:
                stream.stdin.write((oid + "\n").encode())
                stream.stdin.flush()
                header = stream.stdout.readline()
                parts = header.split()
                if len(parts) != 3 or parts[1] != b"blob":
                    raise RuntimeError(f"unexpected blob response for {relative}: {header!r}")
                size = int(parts[2])
                data = stream.stdout.read(size)
                if stream.stdout.read(1) != b"\n" or len(data) != size:
                    raise RuntimeError(f"truncated blob response for {relative}")
                target = destination / Path(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                if mode == "120000":
                    link_target = data.decode("utf-8", "surrogateescape")
                    try:
                        os.symlink(link_target, target)
                    except OSError as exc:
                        target.write_bytes(data)
                        symlink_fallbacks.append({"path": relative, "error": str(exc)})
                else:
                    target.write_bytes(data)
                file_hashes[relative] = hashlib.sha256(data).hexdigest()

        head = run(local_git(source, ["rev-parse", revision]))
        run(["git", "init", "--quiet"], destination)
        git_dir = destination / ".git"
        alternate_file = git_dir / "objects" / "info" / "alternates"
        alternate_file.parent.mkdir(parents=True, exist_ok=True)
        alternate_file.write_bytes(((source / ".git" / "objects").resolve().as_posix() + "\n").encode("utf-8"))
        run(["git", "config", "core.autocrlf", "false"], destination)
        run(["git", "config", "core.eol", "lf"], destination)
        run(["git", "update-ref", "HEAD", head], destination)
        run(["git", "read-tree", head], destination)
        status = run(["git", "status", "--porcelain"], destination)
        return {
            "repository": str(source),
            "requested_revision": revision,
            "head_revision": head,
            "source_git_object_database": str((source / ".git").resolve()),
            "materialization_method": "direct_git_blob_plumbing_with_isolated_git_identity",
            "isolated_git_dir": str(git_dir.resolve()),
            "tracked_entry_count": len(parsed),
            "symlink_fallbacks": symlink_fallbacks,
            "byte_preserving_regular_files": True,
            "file_sha256": file_hashes,
            "worktree_clean": not status,
            "destination": str(destination.resolve()),
        }
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        raise


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
    ap.add_argument("--source", type=Path, help="local source checkout; avoids network and checkout filters")
    ap.add_argument("--identity-out", type=Path)
    args = ap.parse_args()
    identity = materialize_local(args.source, args.revision, args.destination) if args.source else materialize(args.repository, args.revision, args.destination)
    encoded = json.dumps(identity, indent=2, sort_keys=True) + "\n"
    if args.identity_out:
        args.identity_out.parent.mkdir(parents=True, exist_ok=True)
        args.identity_out.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
