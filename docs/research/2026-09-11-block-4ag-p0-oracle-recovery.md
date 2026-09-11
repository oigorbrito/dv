# BLOCK 4AG — P0 oracle recovery and baseline validation

Date: 2026-09-11
Repository: `oigorbrito/dv`
Entry commit: `94f7620598c0a6f23048f6100a4b8a221aefebd3`
Holdout: `SEALED / NOT OPENED`

## Scope

This block inspected and validated the six frozen base workspaces without executing a treatment, calling a model,
opening the holdout, producing a candidate, changing source code, changing dependencies, or changing the oracle
criteria. The 4AF workspaces were reused. All six remained at their exact frozen detached HEADs and clean worktrees.

The distinction in this report is intentional: a base failure is not a treatment failure, and an oracle path defect is
not evidence about task correctness.

## A. Preserved bases and source integrity

| Task | Source checkout | Base SHA | Workspace HEAD | Detached | Clean | Source after probe |
|---|---|---|---|---:|---:|---|
| D-F1-01 | `C:\Projetos\RJ` | `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d` | exact | YES | YES | unchanged |
| D-F2-01 | `C:\Projetos\metao-gate` | `5c3bcdfb0c8aec778727a756f484a4b67a23601d` | exact | YES | YES | unchanged |
| D-F3-01 | `C:\Projetos\smag` | `76ef9277062085e113c14bf1fdbb9c4bd218045b` | exact | YES | YES | unchanged |
| D-F4-01 | `C:\Projetos\metao-gate` | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | exact | YES | YES | unchanged |
| D-F5-01 | `C:\Projetos\metao-gate` | `9cc5d6d722d509175a669624c9235156dffb4f85` | exact | YES | YES | unchanged |
| D-F6-01 | `C:\Projetos\metao-gate` | `5d00cd284ce8fe810b0f5192c56d98608be516d4` | exact | YES | YES | unchanged |

Detailed structural and identity evidence is under `pilot-runs/block-4ag-oracle-recovery/evidence/`.

## B. Structural inventory

The inventory was taken from the exact base commits only. No PR head, gold patch, or later solution was supplied to an
executor. The compact machine-readable record is `evidence/structural-inventory.json`.

| Task | Observed base layout | Relevant fact |
|---|---|---|
| D-F1-01 | `RJ.slnx`, `global.json`, projects under `tests/` | `tests/RJ.DomainTests/RJ.DomainTests.csproj` exists; frozen root-relative path omits `tests/` |
| D-F2-01 | `pyproject.toml`, package under `src/metao`, tests under `tests/unit` | `test_mission_run_input_preflight.py` is absent; setuptools src layout requires `PYTHONPATH=src` or editable install |
| D-F3-01 | root `package.json`, `bun.lock`, `packages/smag-governance/test` | many `*.test.mjs` exist, but `operator-session.test.mjs` is absent |
| D-F4-01 | Python root plus Cargo workspace under `experiments/rust-chassis-a` | base lacks the candidate-side marketplace fixture test and its fixture |
| D-F5-01 | `pyproject.toml`, `src/metao`, `tests/unit` | `test_operator_ux_doctor.py` exists and is discoverable with `PYTHONPATH=src` |
| D-F6-01 | Python root plus Cargo workspace under `experiments/rust-chassis-a` | required Cargo manifests and targets exist below the root, not at root |

## C. Task diagnostics and recovered execution

### D-F1-01 / RJ

`global.json` requests SDK `10.0.100` with latest-feature roll-forward. The frozen command from the workspace root
does not name the actual project path, so the diagnostic recovered command used the same project and test with the
neutral path correction:

```text
dotnet test tests/RJ.DomainTests/RJ.DomainTests.csproj --filter FullyQualifiedName~ProcessTextNormalizerTests --no-restore
dotnet test tests/RJ.DomainTests/RJ.DomainTests.csproj --no-restore
```

Both remained unavailable because the local restore state required NuGet access. The exact errors are `NU1301` for
`https://api.nuget.org/v3/index.json` with a prohibited socket and `NU1900` vulnerability-audit warning promoted to
error by `TreatWarningsAsErrors=true`. Classification: `MISSING_DEPENDENCY_SETUP` / `ENVIRONMENT_SETUP_REQUIRED`.
This is not evidence that the base code is intrinsically uncompilable, and no dependency update or internet fetch was
performed.

### D-F2-01 / metaO

The base has a valid `pyproject.toml` with setuptools package discovery from `src`. Adding `PYTHONPATH=src` is a
neutral environment recovery. It makes `metao` importable, but the frozen focal module
`tests.unit.test_mission_run_input_preflight` does not exist in this SHA. The preservation suite then ran 480 tests and
had two failures, including the installed-console-script expectation. Classification: `ORACLE_SPEC_DEFECT` for the
missing frozen focal test, plus `BASELINE_EXECUTABLE_FAIL` for the recovered preservation suite.

No similarly named test was substituted.

### D-F3-01 / smag

Exact search of the base found the package and many `*.test.mjs` files, but no `operator-session.test.mjs` anywhere.
The frozen command therefore has no discoverable target in this SHA. A different test would change the measured
construct and was not run. Classification: `ORACLE_SPEC_DEFECT`.

### D-F4-01 / metaO controlled replay

The Cargo workspace and `metao-contracts` manifest exist under `experiments/rust-chassis-a`, but the base does not
contain `marketplace_discovery_fixture_tests` or its fixture. The manifest/target is present in another already-frozen
task identity, but the current protocol does not specify a verifier-owned injection artifact, exact injection operation,
or independent base expected-fail command. Copying it would be an ad hoc reconstruction and could leak solution-side
material.

The controlled replay is therefore:

```text
1. clean base
2. inject only a prospectively identified verifier-owned test/fixture
3. run base expected-fail
4. bind candidate workspace
5. run the same verifier evidence
6. require candidate expected-pass
7. run preservation evidence
```

Current result: `F4_BASE_FAIL_TO_PASS_READINESS = INCONCLUSIVE` and `ORACLE_SPEC_DEFECT`. Verifier-owned versus
solution-owned files are not determinable from the materialized protocol. No candidate treatment was produced.

### D-F5-01 / metaO

The focal test exists in the exact base. With neutral `PYTHONPATH=src`, the focal command passed 10 tests with exit
code 0: `BASELINE_EXECUTABLE_PASS` for the focal dimension. The full preservation suite ran 469 tests and failed one
installed-console-script expectation, exit code 1. Classification: `MISSING_DEPENDENCY_SETUP` for the missing editable
console installation and `BASELINE_EXECUTABLE_FAIL` for the full suite. The oracle itself is not defective.

### D-F6-01 / metaO

The frozen root working directory is wrong for this repository shape. The real Cargo workspace is
`experiments/rust-chassis-a`; `cargo metadata --no-deps --manifest-path <workspace>/Cargo.toml` passed with exit code 0.
The required targets include `discovery_persistence_tests`, `phase6_shadow`, and the marketplace fixture target in the
relevant bases. Recovered Cargo test execution began local compilation but could not complete because of environment
build-lock/setup contention; it was stopped without modifying the source or base. Classification:
`WRONG_WORKING_DIRECTORY` plus `ENVIRONMENT_SETUP_REQUIRED`, not an oracle defect.

## D. Oracle recovery decision

| Task | Frozen command valid | Neutral recovery | Oracle defect | Base executable | Base outcome | P0 blocking |
|---|---:|---:|---:|---|---|---:|
| D-F1-01 | NO | NO | NO | NO | not executed, dependency setup blocked | YES |
| D-F2-01 | NO | NO | YES | PARTIAL | executable preservation, focal absent; recovered suite FAIL | YES |
| D-F3-01 | NO | NO | YES | NO | missing frozen test | YES |
| D-F4-01 | NO | NO | YES | NO | controlled replay INCONCLUSIVE | YES |
| D-F5-01 | YES | YES | NO | PARTIAL | focal PASS, preservation FAIL | YES |
| D-F6-01 | NO | YES | NO | INCONCLUSIVE | metadata PASS, tests blocked by setup/build lock | YES |

Machine-readable decision: `evidence/oracle-recovery-decision.json`.

The requested dimensions were kept separate in `evidence/oracle-dimensions.json`:

| Task | Harness validity | Focal discoverable | Preservation discoverable | Base result |
|---|---|---|---|---|
| D-F1-01 | PASS | YES after neutral path correction | YES after neutral path correction | not executed, dependency setup blocked |
| D-F2-01 | PASS | NO, frozen module absent | YES with `PYTHONPATH=src` | FAIL |
| D-F3-01 | PASS | NO, frozen file absent | N/A | not executed, target absent |
| D-F4-01 | INCONCLUSIVE | NO in base | N/A | INCONCLUSIVE, replay underspecified |
| D-F5-01 | PASS | YES with `PYTHONPATH=src` | YES with `PYTHONPATH=src` | focal PASS, preservation FAIL |
| D-F6-01 | PASS | YES from recovered Cargo workspace | YES from recovered Cargo workspace | INCONCLUSIVE, setup/build incomplete |

## E. Amendment decision

No amendment was applied. F2, F3 and F4 show prospective oracle-spec defects, but this block does not have enough
authority to identify a minimal unbiased replacement or verifier-owned replay injection. F6 requires only a neutral cwd
recovery, but its full execution remains environmentally incomplete. The 24 run specs were therefore not regenerated;
their treatment bindings and oracle bindings remain unchanged. Holdout remains sealed.

## F. Revalidation and tests

The existing 4AF 24 specs were revalidated without model execution:

```text
24/24 concrete specs parsed
24 unique run IDs
cwd mappings present
oracle bindings present
telemetry requirements present
holdout references: 0
solution/gold-patch references: 0
missing telemetry converted to zero: false
```

Harness v1 self-test was not changed and was reexecuted in this block with `python -B tools/test_dv_pilot_harness.py`:
`6 tests`, exit code `0`. The 24 concrete specs were independently revalidated now with `validate_spec`: `24/24`
valid, exit code `0`. This block added no new harness or runtime. `git diff --check HEAD^ HEAD` reported only the
trailing blank after the assertion marker in two preserved raw stderr logs; those bytes were intentionally retained.

## G. Final classification

```text
BLOCK_4AG = COMPLETE
BLOCK_4AG_OUTCOME = ORACLE_READINESS_PARTIAL
F4_BASE_FAIL_TO_PASS_READINESS = INCONCLUSIVE
ORACLE_AMENDMENT = NONE_APPLIED
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
```

Remaining blockers are the NuGet/package setup for F1, Python editable-console setup and the missing F2 focal artifact,
the absent F3 frozen test, the underspecified verifier-owned F4 replay, and Cargo setup/build completion for F6. A
defensible next step is a prospective oracle amendment for the proven missing artifacts and a controlled environment
setup pass, followed by revalidation of only affected specs; no treatment should run before that gate and the real
executor/API gate are both satisfied.
