# P1-S1 — Windows newline remediation

## Outcome

The final P1-S1 parent-control blocker is resolved by a neutral, run-scoped
Git environment. The harness creates an ephemeral Git configuration with
`core.autocrlf=false` and passes it to child processes through isolated
`HOME` and `USERPROFILE` values. This preserves the frozen verifier and its
expected value; it does not normalize captured evidence after execution.

The exact parent verifier passes in a fresh workspace at
`6ddf8c7461bdb13d407e7f78239dbecd53375573`. This is environment qualification,
not a treatment result.

## Baseline

- Initial HEAD: `1616e8f7d3f448fca1e7ff32d0d0b905e0e09579`.
- Branch: `main`.
- Initial worktree: clean.
- Harness baseline: `11/11 PASS`.
- Targeted tests after remediation: `22/22 PASS`.
- Task: `D-F2-06`.
- Verifier: `packages/smag-governance/test/git-staging.test.mjs`.
- Historical base: `6ddf8c7461bdb13d407e7f78239dbecd53375573`.
- Holdout: sealed.

The previous four smoke attempts remain immutable in
`pilot-runs/p1-s1-smoke/`. No smoke attempt was repeated in this wave.

## Diagnosis

The verifier test writes `DIRTY\n`, then `backupDirectory` creates a clone
and applies a Git patch. Direct byte capture showed that the patch stdout uses
LF, but the file produced by `git apply` under the system Git configuration
was `44 49 52 54 59 0D 0A` (`DIRTY\r\n`). The same operation with an
isolated Git configuration produced `44 49 52 54 59 0A` (`DIRTY\n`).

The repository and verifier bytes are therefore not corrupt. The observed
problem is process/materialization representation drift caused by Git's
checkout conversion setting. WSL and Docker commands are present, but WSL
distribution enumeration and Docker server access are denied, so neither is
an available compatible POSIX remediation.

Raw byte evidence is in
`pilot-runs/p1-s1-remediation/raw-newline-control.json`.

## Remediation

The harness now prepares a per-run `.gitconfig` with
`core.autocrlf=false`, records its SHA-256 in the environment snapshot, and
passes only that ephemeral location to executor and verifier child processes.
The change is operationally scoped and does not modify the verifier source,
oracle, task, candidate, treatment, shaping, or success criteria.

The implementation is in `tools/dv_pilot_harness.py`, with a focused test in
`tools/test_dv_pilot_harness.py`.

## Control results

The fresh parent workspace was detached, clean, and at the exact historical
SHA. The frozen command completed with exit code `0`, one passing test, and no
candidate or model call. The captured control output is in
`pilot-runs/p1-s1-remediation/parent-control-v2.stdout.log`.

- `RAW_NEWLINE_CONTROL = PASS`.
- `PARENT_VERIFIER_REPRODUCTION = PASS`.
- Attribution: none; the former `ENVIRONMENT_DRIFT` is remediated.
- `NEWLINE_REPRODUCTION_READY = YES`.
- Candidate capture readiness: yes.
- Candidate application readiness: yes.
- HTTP error telemetry readiness: yes.
- Local fixture-only pipeline: pass.

## Scope and remaining gates

No external API call, treatment execution, P0 run, P1-S2 run, or holdout
access occurred. The four previous smoke runs remain blocked evidence and
are not converted retroactively.

`SMOKE_RERUN_READY` remains `NO` because the strong executor gate and the
frozen smoke-spec release conditions are still not satisfied. The next
defensible action is to qualify an authorized strong executor and then issue
new run identifiers only if the complete promotion gate passes.
