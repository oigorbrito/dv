# P1-W25 — BPT2 environment qualification before candidate search

## Decision

`BPT2_ENVIRONMENT_QUALIFIED = NO` and `bpt2-abp = REJECT_SOURCE`.
The environment gate was evaluated before any new candidate search. The local
.NET SDK is available, but exact dependency restoration and a controlled
PostgreSQL environment are not currently reproducible. No candidate was
selected, no parent was materialized, and no solution content was inspected.

This wave produced no treatment evidence. No model, treatment, paid API, or
holdout was executed or accessed.

## Baseline and remote state

The baseline was branch `main`, clean worktree, `HEAD=
2bbe7cc8e46ff22e956870f2716f555ff42e8070`, and
`origin/main=13d2742c7b3ea2de0f5accb02089dd4edf2a2b35`. The remote was an
ancestor with `LOCAL_ONLY=3` and `REMOTE_ONLY=0`. The supported Harness
self-test passed `9/9`, and `git diff --check` passed. Remote publication was
not retried because authorization remained unavailable.

## Source checkout protection

`C:\Projetos\bpt2-abp` was used only as read-only metadata input. It was
already dirty on branch `research/deploy-rollback-topology-rehearsal`, at
`2a6d3b4a0578a722ef5f0d7cef8dfa748d8401a6`. Its four-line status snapshot has
SHA-256
`90ce91323af9b1886e47f6f819f08c1b1bd93dec605e99e575056e55115a9d29`.
No reset, clean, stash, build, restore, or source/service mutation was
performed there.

## Environment contract

The known parent used for the carried BPT2 verifier evidence is
`f3d2cd2d4c0840077451222868ca0d1c0323cdd2`. Its parent-controlled artifacts
define:

- SDK `10.0.100`, with `latestFeature` roll-forward and prerelease disabled;
- observed SDK `10.0.401`;
- `modules/Directory.Packages.props` with ABP `10.6.0` and EF tooling `10.0.9`;
- `.config/dotnet-tools.json` with `volo.abp.cli 10.6.0` and `dotnet-ef 10.0.9`;
- solution `main/BomPraTi.slnx`;
- database variables `BPT_DB_CONNECTION`,
  `ConnectionStrings__Default`, and `BPT_FIXTURE_VEHICLE_ID`;
- documented PostgreSQL 17 and disposable database bootstrap through
  `scripts/fresh-migration-gate.sh`.

The parent has no `NuGet.config` and no `packages.lock.json`. Central package
versions are present, but that does not establish a complete reproducible graph
without restore evidence.

## Package supply

`PACKAGE_SUPPLY = NOT_QUALIFIED`. The global package cache exists and contains 17
top-level directories, but the required ABP/Npgsql graph was not established
as present. No complete parent lockfile exists, and no offline restore was
attempted because the required dependency graph was not demonstrably available.
The repository-defined restore commands remain `dotnet tool restore`,
`dotnet restore main/BomPraTi.slnx`, and the documented migration gate.

The parent also declares `Volo.Abp.AspNetCore.Mvc.UI.Theme.LeptonXLite` as
`5.4.0-preview*`. This floating version, combined with the absent lockfile,
means the historical inputs do not define one exact reproducible dependency
graph. Pinning it would change the historical source semantics. The minimum
protocol-consistent recovery is a replacement historical source with exact
dependency inputs or an explicit future protocol amendment; W25 did not apply
either.

## PostgreSQL qualification

`POSTGRES_ENV = BLOCKED`. The source documentation expects PostgreSQL 17. The
machine exposes a registered `postgresql-x64-18` service, but it is stopped;
the PostgreSQL CLI tools were not found. `localhost:5432` responded, but its
owner could not be identified because process inspection returned access
denied, so it cannot be treated as a controlled disposable database.

Docker is installed, but the Docker daemon is inaccessible through
`docker_engine`. No service was started, no database was created or reset, and
no unrelated local database state was touched.

The exact unblock condition is a controlled PostgreSQL 17 instance or pinned
local image with an accessible daemon, disposable database, versioned bootstrap,
and deterministic cleanup.

## Environment smoke and candidate sequencing

The environment smoke was `NOT_TESTED` because package supply is
`NOT_QUALIFIED` and controlled PostgreSQL is `BLOCKED`. No isolated parent
workspace was created. This correctly prevents environment recovery from being
inferred from a partial cache or an uncontrolled port.

Because `BPT2_ENVIRONMENT_QUALIFIED` is `NO`, the source is now
`REJECT_SOURCE`: the historical dependency inputs are not reconstructable
without changing semantics, and no alternate reproducible historical path was
identified. The metadata-only candidate discovery stage was not entered. The
previously excluded candidate
`004cbd44dbd864af28c94c173ed1d106e1d2bf8c` was not reopened. There are no new
leads, pre-solution freezes, parent focal results, candidate executions, or
preservation results.

## State and validation

The admitted corpus remains `D-F2-05`, `D-F5-01`, and `D-F6-01`, across
families `F2`, `F5`, and `F6`, in two repositories. Counts remain `3` tasks and
`2` repositories. `TASK_CORPUS = PARTIAL`,
`COMPARATIVE_CORPUS_READY = NO`, `P1_S1_RELEASE = NO`, and
`REAL_P0_RUNS = 0/24` remain unchanged.

JSON parsing, source preservation, known-parent SHA resolution, dependency and
PostgreSQL evidence checks, parent-failure gate consistency, solution-leakage
scan, holdout scan, P0 immutability, secret scan, Harness self-test, and
`git diff --check` passed. Full evidence is under
`pilot-runs/p1-w25-bpt2-environment-qualification/`.

## Final blockers

- exact dependency graph is not reproducible from parent-controlled inputs;
- controlled PostgreSQL 17 is unavailable;
- Docker daemon access is blocked;
- external TCP/network remains unavailable;
- strong executor credential remains absent;
- W22-W25 local commits remain unpublished due authorization.

The next defensible action is a separately authorized protocol decision about a
replacement source or amendment for the floating dependency. PostgreSQL remains
an independent environment blocker, but it cannot rehabilitate this historical
source under the current reproducibility contract. Candidate search must not
begin for bpt2 in W25.
