# Block 2B-F2 — Cross-component / integration-defect oracle

Date: 2026-09-10
Status: COMPLETE / RESEARCH ONLY
Architecture approval: NONE

## Scope

This block defines only the verification oracle for F2 cross-component/integration defects. It does not define F3-F6, verifier ordering, routing, executor choice, escalation policy, or measurement accounting.

## Governing rule

For F2, removal of one visible symptom is not sufficient. A verified solution must restore the relevant component interaction and preserve the contract surfaces on both sides of that interaction.

`SYMPTOM_GONE != INTEGRATION_RESTORED`

`ONE_COMPONENT_PASS != CROSS_COMPONENT_VERIFIED`

## Oracle dimensions

An F2 task may be classified `VERIFIED_SOLVED_TASK = YES` only when all four dimensions below are satisfied by valid executed evidence.

### O1 — Interaction reproduction

There must be a predeclared reproducer or integration-focused test that exercises the actual failing interaction described by the task statement.

It must demonstrate the expected before/after distinction on the frozen base versus candidate state where technically feasible.

A unit test that exercises only one internal helper is insufficient when the task is classified F2 because the public problem statement itself establishes a cross-component failure.

### O2 — Boundary/contract preservation

Evidence must demonstrate that the participating boundary still satisfies its required input/output, state, ordering, serialization, compatibility, or lifecycle contract after the repair.

The exact contract depends on the task. Examples include:

- producer output remains consumable by downstream component;
- media/dependency ordering remains valid;
- dataframe/array shape or type boundaries remain compatible;
- storage/backend integration does not duplicate or omit externally observable work.

This does not require a universal contract-testing framework. The oracle only requires that the relevant interaction contract be represented by executable evidence appropriate to the instance.

### O3 — Adjacent regression preservation

At least the directly participating components or the narrow subsystem containing their interaction must retain previously valid behavior under a predeclared regression set.

The minimum regression set may be narrower than the full repository suite, but it must cover both sides of the interaction when both sides expose executable tests.

A solution that fixes the integration reproducer by breaking a participant's existing obligations is `NO`, not `YES`.

### O4 — Harness validity and integrity

The verification run must be valid and attributable to the candidate state.

Required conditions include:

- intended tests/commands actually executed;
- no unresolved infrastructure/bootstrap failure prevented the oracle from running;
- candidate did not alter protected evaluator inputs, hidden tests, grading scripts, or result reporting in a way that can mint a false pass;
- repository/base/candidate identity is bound to the evidence;
- unexpected skips, flaky disagreement, or incompatible environment behavior are classified rather than silently treated as pass/fail.

## Ternary decision

### YES

`VERIFIED_SOLVED_TASK = YES` iff:

1. O1 passes;
2. O2 passes;
3. O3 passes;
4. O4 is valid;
5. no mandatory oracle obligation has conflicting conclusive evidence.

### NO

`VERIFIED_SOLVED_TASK = NO` when valid executed evidence demonstrates at least one mandatory failure, including:

- the original interaction still fails;
- required component-boundary contract remains violated;
- the repair introduces a directly relevant regression;
- the candidate depends on modifying the evaluator rather than fixing product behavior.

### INCONCLUSIVE

Use `INCONCLUSIVE` when the available evidence cannot support YES or NO without conflating product failure with evaluation uncertainty. Examples:

- integration environment could not be constructed;
- required dependency/service is unavailable and no accepted reproducible substitute exists;
- relevant tests are skipped for environmental reasons;
- independent executions disagree beyond the predeclared flake policy;
- the integration reproducer is broken or ambiguous;
- evidence identity is not bound to the evaluated candidate;
- conflicting verifiers cannot be resolved under the later precedence policy.

## Why F2 differs from F1

F1 may often be established using a narrow defect reproducer plus local preservation evidence. F2 must additionally prove the interaction itself.

The distinction is behavioral, not file-count based. Two components can fail while the eventual repair touches one file; conversely a multi-file patch can still be a localized defect. The oracle therefore follows the pre-solution task construct, not patch topology.

## Minimum-sufficient verification principle

F2 does not automatically require the complete repository test suite.

The minimum sufficient oracle is:

```text
interaction reproducer
+ relevant boundary/contract checks
+ adjacent regression checks for participating components
+ harness integrity
```

Expand beyond this set only when the task's risk/uncertainty or observed evidence requires it. The economic policy for expansion remains out of scope for this block.

## Evidence basis

Current SWE-bench evaluation reconstructs repository environments, applies a candidate patch, and executes repository tests. This is useful evidence, but benchmark resolution alone is not treated as universal truth.

Software-component integration literature also emphasizes that integration defects concern interactions and mismatches between components rather than merely isolated component correctness. Contract-based integration testing specifically targets pre/postconditions and interaction coverage between components. These principles support making the cross-component boundary an explicit oracle obligation rather than relying on isolated unit success.

## What this block does NOT approve

This block does not approve:

- full-suite-always verification;
- contract-testing infrastructure;
- an LLM judge;
- a static or learned router;
- cheap-first execution;
- strong-first execution;
- a particular workflow engine;
- any `dv` implementation.

## Completion status

`BLOCK_2B_F2 = COMPLETE`

Next block, if continued, is only F3 (feature/change oracle).
