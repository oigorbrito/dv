# BLOCK 4AH — Offline P0 oracle closure and prospective amendments

Date: 2026-09-11
Entry commit: `a03002f09977259ba674ad74f0e14c22316aad0d`
HEAD snapshot: `a03002f09977259ba674ad74f0e14c22316aad0d`
Holdout: `SEALED`

## Scope and immutability

The six historical SHAs remained available and the six 4AF base workspaces remained exact, detached and clean.
Source checkouts were observed after probing at the same HEADs and dirty states recorded in 4AG; no source checkout,
corpus, treatment, pricing, oracle criterion, candidate or holdout was changed. All earlier evidence remains under
`pilot-runs/block-4ag-oracle-recovery/`.

No model, OpenAI API or treatment was executed. `REAL_P0_RUNS` remains `0/24`.

## F1 — RJ/.NET

The exact base contains `global.json` requesting SDK `10.0.100` with feature-band roll-forward, `Directory.Packages.props`,
`Directory.Build.props`, and the project at `tests/RJ.DomainTests/RJ.DomainTests.csproj`. No usable complete local NuGet
cache was available for the required restore state; the configured/default package location pointed to the sandbox cache.
The frozen root-relative project path was also wrong. The neutral path correction was tried with `--no-restore`, but
execution remained blocked by the previously observed `NU1301` and `NU1900` conditions. No feed, package or version was
added. Classification: `F1_ORACLE = ENVIRONMENT_BLOCKED`.

The path defect is proven to be neutral, so v2 records the same project and same test filter with `tests/` restored.

## F2 — metaO Python

Exact-tree inspection formally confirms that `tests/unit/test_mission_run_input_preflight.py` and its module are absent
from SHA `5c3bcdfb0c8aec778727a756f484a4b67a23601d`. The base uses setuptools `src/` layout and exposes `metao` through
`metao.entrypoint:main`; `PYTHONPATH=src` is neutral for imports. The preservation suite was executable but had two
failures, including the installed-console-script expectation. The current Python installation has no `setuptools`, so
an offline editable install could not be performed without introducing a dependency.

No provenance-identifiable verifier-owned focal artifact or injection operation exists in the frozen protocol. Result:
`F2_ORACLE = INCONCLUSIVE_ORACLE_DEFECT`; admissibility remains `P0_ORACLE_INVALID`.

## F3 — SMAG

The exact base package tree and `package.json` were audited. `packages/smag-governance/test/operator-session.test.mjs`
and all `operator-session*` matches are absent from SHA `76ef9277062085e113c14bf1fdbb9c4bd218045b`. Other tests were not
substituted. No versioned verifier-owned focal artifact or injection procedure is documented. Result:
`F3_ORACLE = INCONCLUSIVE_ORACLE_DEFECT`; admissibility remains `P0_ORACLE_INVALID`.

## F4 — controlled Fail-to-Pass

The base has the Cargo workspace under `experiments/rust-chassis-a`, but no `marketplace_discovery_fixture_tests` target
in the F4 base. No verifier-owned test/fixture plus immutable hash and injection command can be identified from the
versioned protocol without borrowing another task's files or inventing a test. Therefore the exact contract cannot be
closed. The required procedure remains: clean base; inject only a prospectively identified verifier-owned artifact;
run base expected-fail; bind candidate; run the same verifier; require candidate expected-pass; run preservation;
clean up and prove provenance. Result: `F4_REPLAY = INCONCLUSIVE / VERIFIER_ARTIFACT_UNSPECIFIED`, admissibility
`P0_ORACLE_INVALID`.

## F5 — Python packaging

The metadata declares the setuptools backend and console entry point `metao = metao.entrypoint:main`, with no runtime
dependencies. `PYTHONPATH=src` made the focal test discoverable and 10 tests passed. The full 469-test preservation
suite failed on one console-script installation expectation. The missing local setuptools backend prevents a legitimate
offline editable-install recovery. Result: `F5_ORACLE = ENVIRONMENT_BLOCKED`; admissibility remains temporarily blocked.

## F6 — Cargo workspace

The exact base contains `experiments/rust-chassis-a/Cargo.toml` and `Cargo.lock`; the repository root does not contain a
Cargo manifest. Running from the recovered workspace directory with `CARGO_NET_OFFLINE=true`, a separate temporary
`CARGO_TARGET_DIR`, and `--locked --offline` produced:

- `discovery_persistence_tests`: exit `0`, 6 passed, 0 failed;
- `phase6_shadow`: exit `0`, 5 passed, 0 failed;
- `cargo test --locked --offline --workspace`: exit `0`, all executed test binaries passed.

This proves the v1 defect was only the working directory. Result: `F6_ORACLE = READY` with a neutral cwd amendment;
admissibility is `P0_ADMISSIBLE_WITH_V2_ORACLE`. Generated build output was kept outside the repository commit and no
source lock was removed or changed.

## Oracle contract v2

`experiments/p0/oracle-contract-v2.json` is a new prospective identity. It contains only two demonstrated,
treatment-neutral operational amendments:

1. F1: restore `tests/` in the root-relative .NET project path, preserving project and filter identity;
2. F6: execute the unchanged Cargo commands from `experiments/rust-chassis-a`, the actual workspace root.

F2, F3 and F4 are explicitly recorded as `UNRESOLVED_ORACLE_DEFECT`; no verifier artifact was fabricated. The old v1
specs and evidence are preserved. A new 4AH run-spec set was generated for all 24 identities; only F1/F6 concrete specs
reference `oracle-contract-v2`, with task, treatment, model, rollout and run order unchanged.

## Admissibility and P0 impact

The machine-readable matrix is `pilot-runs/block-4ah-offline-oracle-closure/evidence/task-admissibility.json`.

| Task | V1 status | V2 status | Baseline | Admissibility | Blocker |
|---|---|---|---|---|---|
| D-F1-01 | path defect + environment block | valid neutral path amendment | not executable | `P0_TEMPORARILY_ENVIRONMENT_BLOCKED` | NuGet cache/restore/audit |
| D-F2-01 | focal absent | unresolved defect | preservation fail | `P0_ORACLE_INVALID` | no verifier-owned focal artifact |
| D-F3-01 | focal absent | unresolved defect | not executable | `P0_ORACLE_INVALID` | no same-test path/artifact |
| D-F4-01 | replay unspecified | unresolved defect | inconclusive | `P0_ORACLE_INVALID` | verifier artifact/procedure absent |
| D-F5-01 | valid | no v2 needed | focal pass, suite fail | `P0_TEMPORARILY_ENVIRONMENT_BLOCKED` | setuptools/console setup |
| D-F6-01 | wrong cwd | valid neutral cwd amendment | pass | `P0_ADMISSIBLE_WITH_V2_ORACLE` | none |

`P0_CORPUS_STATUS = BLOCKED_BY_ORACLE_VALIDITY`. No task was removed or replaced. The three invalid tasks remain in the
corpus pending an explicit future protocol decision. `P0_ADMISSIBLE_WITH_V2_ORACLE = 1/6`.

## Revalidation and limitations

The regenerated 4AH set contains 24/24 unique concrete run IDs. Static validation passed 24/24; exact bases,
treatments, oracle bindings, cwd mappings, telemetry fields and holdout exclusion were checked. No gold patch or solution
reference was introduced. Harness v1 self-test passed 6/6, exit `0`. `git diff --check` was run; any trailing whitespace
reported belongs to preserved raw stderr from 4AG and was not normalized.

This is offline oracle/readiness evidence, not treatment evidence. F6 baseline success does not certify any treatment;
F1/F5 environmental failures do not imply treatment failures; and F2/F3/F4 cannot be made executable by selecting a
similar test.

## Final state

```text
BLOCK_4AH = COMPLETE
BLOCK_4AH_OUTCOME = P0_PROTOCOL_DEFECT_CONFIRMED
ORACLE_V2 = CREATED
F4_REPLAY = INCONCLUSIVE / VERIFIER_ARTIFACT_UNSPECIFIED
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
```

Next defensible step: obtain an explicit protocol amendment that supplies immutable verifier-owned artifacts for F2/F3/F4,
and separately restore the offline package environments for F1/F5. Only after those gates and the real executor/API gate
are satisfied should treatment execution be considered.
