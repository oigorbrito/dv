# P1-W11 dependency-supply qualification

## Outcome

W11 completed without treatment, smoke, model, API, candidate, or holdout
execution. The outcome is `ENVIRONMENT_RECOVERY_PARTIAL`: D-F2-05 now has a
reproducible local NuGet restore and build from the frozen base, but its
bounded PostgreSQL runtime remains unavailable. D-F2-04 remains blocked because
the historical contract installs an unpinned `pytest` and no dated resolution
or package-index snapshot is available. The admitted corpus is unchanged.

## D-F2-04 — searchleads

At base `2c886f863cf6d5f9473d15e60f2f55f938162876`, `pyproject.toml` provides
pytest configuration and the CI workflow runs `python -m pip install --upgrade
pip pytest`. No exact pytest version, lock file, constraints file, or dated
resolution was found in the frozen evidence. A local `.venv-baseline` contains
pytest 9.1.1, but its provenance is not a historical resolution and it is not
accepted as a reconstruction. No focal or preservation command was run under
that unbound environment.

Classification: `BLOCKED_DEPENDENCY_VERSION_NOT_REPRODUCIBLE`.

## D-F2-05 — bpt2-abp

At base `f3d2cd2d4c0840077451222868ca0d1c0323cdd2`, the exact fixture restore
resolved 91 entries for `net10.0` using the existing user NuGet cache. Central
pins remained Volo.Abp 10.6.0 and EF Core Design 10.0.9; no package version was
substituted and no package was downloaded in W11. The restore generated
`project.assets.json`, and the Release build passed with zero warnings and zero
errors. NuGet DNS passed but TCP 443 remained blocked; the build did not require
live network after cache resolution.

The historical workflow still requires PostgreSQL 17-alpine. Docker CLI 29.7.2
is installed, but the Docker daemon/API pipe is unavailable. Focal and
preservation execution therefore were not reached.

Classification: `BLOCKED_POSTGRES_RUNTIME`.

## Corpus and limitations

The admitted corpus remains `D-F5-01` and `D-F6-01`; neither F2 candidate was
admitted. Comparative readiness remains `NO`. No solution commit was applied,
no treatment was executed, and the holdout stayed sealed. Raw evidence is in
`pilot-runs/p1-w11-dependency-supply/`. The package graph is preserved as the
result of the exact-base `project.assets.json` resolution, with cached artifact
hashes in the supply evidence.

The next defensible step is to obtain either a dated, reproducible pytest
resolution for D-F2-04 or an explicitly bounded external runner, and to provide
a bounded PostgreSQL 17 runtime for D-F2-05. Do not promote either candidate
without rerunning the frozen focal and preservation commands.
