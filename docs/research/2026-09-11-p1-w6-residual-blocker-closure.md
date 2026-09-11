# P1-W6 residual blocker closure

## Decision

W6 closes the local analytical ambiguity without executing a treatment, model,
P1 task, or holdout. The final state is:

```text
D-F1-01 = FAIL_FROZEN_BASE_RUNNER_INCOMPATIBLE / NOT_ADMITTED
P1-W5-D-F1-01 = CLOSED
P1-W1-BLK-004 = CLOSED
S1_CORPUS_READY = PASS
COMPARATIVE_CORPUS_READY = NO
HARNESS_P1_REMOTE_READINESS = PASS
P1_S1_RELEASE = NO
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
```

The master plan remains the normative source. This document records only the
W6 diagnosis and the resulting blocker separation.

## Baseline and evidence integrity

The initial local and `origin/main` heads were both
`4caf12f239cc06ac59c533fe1ab2f4aa0d53b85b`. The worktree was clean. The
initial fetch could not open `.git/FETCH_HEAD` because of the execution
identity's permission boundary; no remote divergence was observed in the
existing refs. The Harness self-test ran 6 tests and exited 0.

The D-F1 reproduction used a new local clone at
`C:\Projetos\dv\.tmp-w6-d-f1`, detached at
`c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`. The source checkout was not
modified. Complete command logs and exit codes are under
`pilot-runs/p1-w6-residual-blocker-closure/`.

## D-F1 causal classification

The frozen `global.json` requests SDK `10.0.100` with
`rollForward=latestFeature`, and selects `Microsoft.Testing.Platform`. The
machine resolves `10.0.401`, which is a valid later feature band under that
rule. The base contains five xUnit v3 test projects with the VSTest-targeted
project shape. It contains no `Directory.Build.targets` or `NuGet.config`.

Both frozen commands exit 1 before test execution:

```text
dotnet test tests/RJ.DomainTests/RJ.DomainTests.csproj --filter FullyQualifiedName~ProcessTextNormalizerTests --no-restore
dotnet test RJ.slnx --configuration Release --no-build --no-restore
```

Microsoft.Testing.Platform reports that the projects use VSTest and are not
supported by the selected runner. The focal command names `RJ.DomainTests`; the
solution command names all five test projects. This failure is independent of
the valid SDK feature-band resolution. No package, SDK, runner, project, or
source file was changed. Exact SDK installation was therefore
`NOT_PERFORMED_NOT_JUSTIFIED`.

This is not a perpetual environment blocker and not a treatment result. The
frozen D-F1 task is not admissible under its own base configuration. Fixing it
would require a prospective protocol/task amendment, such as changing the
runner or project configuration, which W6 does not apply.

## BLK-004 and telemetry

The frozen promotion contract requires retry visibility at the run boundary,
but it does not require provider-internal retry metadata. The run-result schema
has no provider-internal retry field and explicitly supports missing usage
fields with a reason. The application policy records zero application retries
because the frozen probe policy uses no retry; provider-internal retry remains
`UNMEASURED_NONBLOCKING`, never zero.

The preserved W3 Gemini response exposes input tokens 12, thoughts tokens 12,
and total tokens 24. Therefore `ACCOUNTING_PRIMARY=PASS` without fabricated
values. Output and cached partitions are `UNMEASURED`, so
`ACCOUNTING_PARTITION_DETAIL=PARTIAL`. The complete matrix is in
`telemetry-requirement-matrix.json`.

## Gate recalculation

The two admitted tasks, D-F5-01 and D-F6-01, span two families and satisfy the
frozen preference for a pipeline/smoke stage. They do not make the corpus
comparative-ready. Accordingly, the former corpus blocker is retained only for
S2, while the S1 blocker set contains only the missing strong executor
qualification.

Gemini remains the carried-forward economic path with
`S0_READY_TELEMETRY_LIMITED`; no new remote probe was made. Harness remote
readiness passes for the currently planned remote S1 needs because identity,
raw evidence, candidate/evidence references, timeout, accounting fields, and
explicit missingness are representable. Local executor readiness remains
`NOT_TESTED` and is not an S1 blocker while no local path is selected.

## Blocker separation

```text
S1_BLOCKERS:
  - P1-W4-BLK-STRONG-CREDENTIAL

S2_BLOCKERS:
  - corpus expansion
  - variance/sample work after S2 observations

NONBLOCKING_LIMITATIONS:
  - provider-internal retry metadata UNMEASURED
  - cached-token partition UNMEASURED
  - local GPU/energy schema NOT_TESTED
```

The detailed before/after register and promotion checks are preserved as JSON
evidence. P0 artifacts are unchanged. No treatment, candidate, model API,
holdout, or solution artifact was accessed.

## Validation and next objective

The Harness self-test passed 6/6 with exit 0. JSON parsing, secret-scan,
holdout-seal, P0-immutability, evidence-path, and `git diff --check` results
are recorded in the commit validation output. The next objective is to obtain
an authorized strong executor qualification, then materialize—but not yet
execute—the P1-S1 smoke specs. Corpus expansion remains required before any
comparative S2 claim.
