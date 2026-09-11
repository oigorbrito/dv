# BLOCK 4AI — P0 protocol repair, task admissibility and executable corpus freeze

Date: 2026-09-11
Entry commit: `4d4b22dddbd4f1482736b8ea112ac3eac496a9f8`
Snapshot HEAD: `4d4b22dddbd4f1482736b8ea112ac3eac496a9f8`
Holdout: `SEALED`

## Scope

This block froze an executable-corpus decision without treatment, model or API execution. No holdout material, gold
solution, candidate output, treatment result or post-hoc performance signal was used. Prior evidence under
`pilot-runs/block-4ag-oracle-recovery/` was preserved.

## Frozen admissibility criteria

Before replacement search, `evidence/admissibility-criteria.json` froze ten requirements: exact historical base;
independent versioned verifier; explicit verifier semantics; executable focal verification; executable or explicitly
scoped preservation evidence; reproducible environment; no gold-solution leakage; treatment independence; deterministic
Harness binding; and separable failure attribution. Exclusion reasons were frozen as `INVALID_ORACLE`,
`VERIFIER_ARTIFACT_UNAVAILABLE`, `ENVIRONMENT_NOT_REPRODUCIBLE`, `BASE_UNUSABLE`, `SOLUTION_LEAKAGE_REQUIRED` and
`OTHER_EXPLICIT_REASON`.

Replacement order was frozen before search: original selected task, then the second development task in canonical
manifest order, then the third, always within the same family. The development manifest remains v0 and the holdout was
not consulted.

## Snapshot and original task decisions

The snapshot is `evidence/pre-repair-snapshot.json`. Canonical manifest SHA-256 is
`8b8d97239acc08c0b30471778705991ff05c2b3397435baa0a0104f1ef689f47`; operational manifest SHA-256 is
`a25f5fd453c95db6ae0a57db62a9d0f0557594e8ac51db2dee12acebd2758e09`; oracle-contract-v2 SHA-256 is
`4741d6a24e2a51e6c50d75595b4ca70d481eb00b2e1f2b726921fbac15edef93`. The v1 identity is
`block-2b-v1+4m-command-manifest-v1`; no standalone v1 artifact file exists to hash.

| Task | Original admissibility | Evidence-based disposition |
|---|---|---|
| D-F1-01 | temporary environment block | correct v2 path, but NuGet restore/cache remains unavailable offline |
| D-F2-01 | invalid oracle | focal module absent; no independent verifier artifact |
| D-F3-01 | invalid oracle | focal test absent; no independent verifier artifact |
| D-F4-01 | invalid oracle | controlled replay verifier artifact/procedure absent |
| D-F5-01 | temporary environment block | focal passes, full preservation fails on console setup; setuptools unavailable |
| D-F6-01 | admissible with v2 | locked offline Cargo workspace commands pass |

## Verifier recovery

F2 exact-tree and history inspection confirmed `test_mission_run_input_preflight` is absent from the selected base.
The next same-family candidate, D-F2-02, has `mission-operator-supervision.test.mjs` and its focal/preservation commands
passed locally in a materialized base. However, its supervision implementation lineage is already an ancestor of the
stated candidate base, so it is not clean pre-solution provenance for the associated task. It was rejected under
`BASE_UNUSABLE`/provenance contamination, not based on treatment convenience. D-F2-03's staging test is unrelated.

F3 D-F3-02 has no exact ProjectCompletionGate focal test and D-F3-03 has no exact discovery-coordinator focal test in
their exact bases. F4 D-F4-02 lacks the property harness; D-F4-03's boundary test is coupled to a source-fix commit,
not an independent verifier-owned artifact. No verifier artifact was copied or invented. Consequently F2, F3 and F4
remain `P0_ORACLE_INVALID`.

## Environment findings

F1 retains the neutral v2 path amendment from 4AH, but the exact packages/assets cannot be restored from the available
offline cache and no package or feed was added. It remains `P0_TEMPORARILY_ENVIRONMENT_BLOCKED`, distinguished from an
oracle defect.

F5 metadata declares `setuptools>=70` as the build backend, no runtime dependencies, and the console entry point
`metao = metao.entrypoint:main`. The focal test passed with `PYTHONPATH=src`; the 469-test preservation suite failed at
the console-script installation expectation. The current Python environment has no setuptools and no local wheel/cache
was available for a legitimate editable install. It remains temporarily environment-blocked; the preservation suite was
not weakened.

F6 reconfirmed the v2 cwd and exact locked commands. Offline execution passed discovery persistence (6/6), phase6 shadow
(5/5) and the complete Cargo workspace suite. This is baseline/control evidence only.

## Replacement screening

The complete deterministic screening record is `evidence/replacement-screening.json`. No replacement was selected:

- F1-02 had an existing preflight test, not the numeric-coercion construct; F1-03's lifecycle test was not the selected freshness-flag verifier.
- F2-02 was rejected for non-clean pre-solution provenance; F2-03 was unrelated.
- F3-02 and F3-03 lacked exact focal artifacts.
- F4-02 lacked its property harness; F4-03's test was coupled to the source fix.
- F5-02's UX tests did not verify runtime command-store wiring; F5-03 had no exact independent retirement verifier.

No family borrowed a task from another family. Canonical tasks remain in the corpus history and no original spec/evidence
was deleted.

## Oracle versions and executable corpus

No `oracle-contract-v3` was justified: the unresolved tasks lack independent verifier artifacts, while F1/F6 are fully
covered by the neutral v2 amendments already versioned in 4AH. The v2 artifact was not mutated.

`experiments/p0/p0-executable-corpus-v1.json` freezes the distinct executable corpus. Five original families remain
unavailable; F6 remains the same selected task. Therefore:

```text
final executable families = 1/6
final planned real runs = 4
P0_CORPUS_STATUS = BLOCKED_BY_ORACLE_VALIDITY
```

The new matrix is under `pilot-runs/block-4ai-protocol-repair/run-specs/`: D-F6-01 E0/E1/E2/E3 × r1, using namespace
`4AI--D-F6-01--E*-r1`. The old 24 v1/v2 identities remain untouched. The four new specs use `oracle-contract-v2`,
preserve the exact base and treatment mapping, and do not contain holdout or solution material.

## Validation

The 24 4AH specs were revalidated: 24/24 valid. The new executable matrix was validated: 4/4 valid, 4 unique run IDs.
Exact base mapping, family integrity, oracle provenance, treatment mapping, executor bindings, pricing identity,
holdout absence and no gold/solution references were checked. Harness v1 self-tests passed 6/6 with exit code 0.
`git diff --check` passed for this commit; prior raw evidence whitespace was preserved rather than normalized.

## Threats, limitations and final state

Development tasks carry the previously recorded familiarity/contamination risk and are not external-generalization
evidence. F6 baseline success does not imply treatment success. F1/F5 setup blocks do not imply product failure. The
three invalid families cannot be repaired by selecting similar tests, and the one selected F6 task does not support the
original six-family P0 coverage claim.

```text
BLOCK_4AI = COMPLETE
BLOCK_4AI_OUTCOME = P0_PROTOCOL_PARTIALLY_REPAIRED
ORACLE_CONTRACT_V3 = NOT_CREATED
REAL_P0_RUNS = 0/24 (planned executable matrix: 4)
P0_RELEASE = NO
HOLDOUT = SEALED
TREATMENT_EXECUTION = false
```

The next defensible step is to obtain an explicit, independently versioned verifier protocol for F2/F3/F4 and a
reproducible package environment for F1/F5. No post-hoc treatment optimization occurred.
