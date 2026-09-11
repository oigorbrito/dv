# Block 2B-F1 — Localized-defect oracle

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note defines only the oracle contract for F1 localized defect repair. It does not define F2-F6, executor selection, routing, escalation, or the full verifier chain.

The governing Block 2A contract remains:

- executor completion is not task verification;
- focused-test pass alone is not task verification;
- verified success requires task satisfaction, preservation/non-regression, and a valid verification harness;
- valid terminal outcomes are YES, NO, and INCONCLUSIVE.

## F1 construct

An F1 task is a defect whose behavioral surface is localized from pre-solution information. The oracle should therefore prove that the reported defect is repaired without converting a narrowly scoped task into an unnecessary whole-repository proof obligation.

## Evidence dimensions

### O1 — Defect-target evidence

Required for YES.

At least one executable, independently defined observation must distinguish the pre-fix behavior from the required post-fix behavior.

Preferred order:

1. benchmark-provided fail-to-pass regression test or equivalent deterministic reproducer;
2. predeclared project regression test that reproduces the reported defect;
3. deterministic executable assertion reconstructed from the public issue when no canonical regression test exists.

A model-written test created after seeing its own implementation cannot be the sole task-satisfaction oracle.

### O2 — Local preservation evidence

Required for YES.

The change must not break the directly affected component's existing behavior. Prefer the smallest predeclared relevant existing test set that contains the affected module/component and known neighboring behavior.

For SWE-style tasks, PASS_TO_PASS may contribute to this evidence but is not automatically sufficient if the selected set is known to be incomplete, malformed, skipped for environmental reasons, or otherwise unreliable.

### O3 — Harness integrity evidence

Required for YES.

The verification run must establish that:

- the intended tests actually executed;
- pass/fail was not inferred from missing, truncated, or forged output;
- verifier inputs/test artifacts were not modified or shadowed by the candidate patch in a way that invalidates the oracle;
- skips that affect required evidence are distinguished from passes;
- infrastructure/bootstrap failure is not converted into task failure.

If any required O1/O2 observation cannot be trusted, the result is INCONCLUSIVE rather than YES/NO unless another valid oracle independently establishes the outcome.

## Terminal decision

### VERIFIED_SOLVED_TASK = YES

Only when all are true:

1. O1 = PASS — the reported localized defect is demonstrably repaired;
2. O2 = PASS — the predeclared relevant preservation checks pass;
3. O3 = VALID — required verification observations actually executed under an uncompromised harness;
4. no contradictory higher-authority evidence demonstrates a remaining mandatory defect.

### VERIFIED_SOLVED_TASK = NO

When a valid executable oracle demonstrates at least one mandatory failure, including:

- defect-target regression/reproducer still fails;
- directly relevant pre-existing behavior regresses;
- another predeclared mandatory F1 acceptance assertion fails.

A candidate patch that does not apply or cannot build for a product-caused reason may be NO if the verifier can validly attribute the failure to the candidate rather than the environment.

### VERIFIED_SOLVED_TASK = INCONCLUSIVE

Use when task correctness cannot be distinguished from verifier failure, including:

- required test/reproducer did not execute;
- required PASS_TO_PASS check was skipped because the environment lacks required resources;
- benchmark image/build/bootstrap is broken;
- test identifiers or grading metadata are malformed/ambiguous;
- test files or grading output may have been poisoned/forged;
- conflicting valid oracles cannot be reconciled under a predeclared precedence rule;
- required evidence is missing.

## Anti-gaming rule

For F1, task verification must not trust candidate-controlled textual claims or candidate-controlled test reporting as sole authority.

Where feasible, the verifier should run from an external/read-only authority boundary or otherwise establish integrity of:

- evaluation scripts;
- oracle tests;
- grading parser inputs;
- relevant test files.

Known SWE-bench issue reports in 2026 demonstrate that patches can create false positives through test-patch path collisions, direct test poisoning, or stdout/log forging. These are reasons to treat harness integrity as part of the oracle rather than as an implementation detail.

## Scope discipline

F1 does not require an unconditional full-repository test suite merely because one exists. The initial oracle should use the minimum sufficient predeclared evidence capable of detecting:

- persistence of the target defect;
- directly relevant regressions;
- invalid verification execution.

Broader tests may be added later by the verifier policy if their marginal detection value justifies their cost. That economic policy is outside this sub-block.

## Evidence semantics

Preserve:

- `TARGET_TEST_PASS != VERIFIED_SOLVED_TASK`
- `PASS_TO_PASS_PASS != COMPLETE_NON_REGRESSION_PROOF`
- `SKIPPED != PASS`
- `HARNESS_FAILURE != PRODUCT_FAILURE`
- `CANDIDATE_CONTROLLED_LOG != INDEPENDENT_EVIDENCE`
- `GOLD_PATCH != MODEL_VISIBLE_ORACLE_INPUT`

## F1 oracle status

- task-satisfaction requirement: FROZEN
- local-preservation requirement: FROZEN
- harness-integrity requirement: FROZEN
- YES/NO/INCONCLUSIVE semantics: FROZEN
- exact per-instance commands/tests: DEFERRED to later oracle materialization
- verifier implementation: NONE

Block 2B-F1 is complete. Do not open F2 in this note.
