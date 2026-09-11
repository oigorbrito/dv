# P1-W10 environment recovery

## Outcome

W10 completed with no treatment, smoke, model, API, or holdout execution.
The outcome is `ENVIRONMENT_RECOVERY_PARTIAL`: neither promising candidate
could be admitted because the required historical environment remains
unreproducible locally. `TASK_CORPUS` remains `PARTIAL`,
`COMPARATIVE_CORPUS_READY=NO`, `P1_S1_RELEASE=NO`, and `HOLDOUT=SEALED`.

The baseline was `89f232f2fee5713090bba2722c5c0d1a8dd06529`; `main` was clean
and equal to `origin/main`. The Harness qualification command passed 6/6.
Raw command evidence is preserved in
`pilot-runs/p1-w10-environment-recovery/`.

## D-F2-04 — searchleads

The exact detached base was
`2c886f863cf6d5f9473d15e60f2f55f938162876`. The base declares Python `>=3.11`
and contains pytest configuration in `pyproject.toml`; its README and CI
explicitly install `pytest`, while no test extra is declared. The historical
contract therefore requires an isolated environment with pytest, not a
different test runner.

The available interpreter is Python 3.13.14. The inspected pip cache contained
no pytest wheel. A residual pytest launcher pointed to a missing Python 3.12
installation and was not used as evidence of a valid environment. The exact
focal and preservation commands both terminated with exit code 1 and
`No module named pytest`. The focal verifier hash is
`8206726B9546DECE1D2751DF1FC9CB1DBD5D95225229405C4C2B60C87F79AAC0`.

Classification: `BLOCKED_DEPENDENCY_UNAVAILABLE`, not a baseline product
result. No install, upgrade, source edit, or solution application was made.

## D-F2-05 — bpt2-abp

The exact detached base was
`f3d2cd2d4c0840077451222868ca0d1c0323cdd2`. The repository pins SDK
`10.0.100` with `latestFeature` roll-forward and targets `net10.0`. Package
versions are centrally pinned in `modules/Directory.Packages.props`, including
Volo.Abp 10.6.0 and EF Core design 10.0.9. The historical workflow defines a
PostgreSQL 17-alpine service and runs the claim fixture only after build and
fresh migration.

The local global-packages cache did not contain the required Volo.Abp, EF, or
related assets. The bounded `--ignore-failed-sources` restore exited 1 with
`NU1801` for `api.nuget.org` and `NU1101` for
`Volo.Abp.Ddd.Application.Contracts`. A `--no-restore` build exited 1 with
`NETSDK1004` because `project.assets.json` was absent. DNS resolved, but TCP
443 connectivity to `api.nuget.org` failed. Docker CLI 29.7.2 exists, but the
Docker daemon pipe is unavailable. Focal and preservation execution were not
reached.

Classification: `BLOCKED_NUGET_NETWORK`, with the independent external
boundary `BLOCKED_EXTERNAL_ENVIRONMENT_NOT_BOUNDED`. No package substitution,
cache mutation, source edit, or solution application was made.

## Corpus and blockers

The admitted corpus is unchanged: `D-F5-01` and `D-F6-01`. Neither D-F2-04 nor
D-F2-05 was admitted. The W9 candidate evidence and corpus v4 remain
unchanged; W10 adds only new evidence and a narrow blocker snapshot.

`P1-W1-BLK-002`, the strong credential blockers, and closed historical blockers
were carried forward without reopening them. The two candidate blockers now
have concrete causes and next conditions in
`pilot-runs/p1-w10-environment-recovery/blocker-register.json`.

No corpus v5 was created because admission state did not change materially.
No P0 artifact was modified. No holdout path was accessed. No API credential
was persisted; boolean credential diagnostics were not included in artifacts.

## Next defensible step

Provide an approved, reproducible Python/pytest environment for D-F2-04 and an
approved package/network plus bounded PostgreSQL runtime for D-F2-05. Re-run
only the exact frozen commands in fresh detached workspaces. Until then,
expand neither the corpus nor P1-S1, and do not execute treatments.
