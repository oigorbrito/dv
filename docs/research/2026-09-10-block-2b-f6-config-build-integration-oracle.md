# Block 2B-F6 — Configuration/build/integration oracle

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

Defines only verification semantics for F6 configuration/build/dependency/packaging/CI integration tasks under the Block 2A ternary contract.

## Governing distinction

`SOURCE_TEST_PASS != DEPLOYMENT_INTEGRATION_VERIFIED`

`BUILD_EXIT_ZERO != REQUESTED_PACKAGING_BEHAVIOR`

F6 must exercise the operational boundary named by the task.

## Required evidence

### O1 — Operational-boundary reproduction
Execute the requested install/package/build/configuration/CI/repository-discovery behavior in a reproducible environment. A source-level unit test is insufficient when the defect exists only after installation, packaging, discovery, or environment integration.

### O2 — Artifact/configuration correctness
Verify the externally relevant artifact or configuration outcome: installed entry points/files, dependency resolution, package discovery, build output, configuration semantics, or equivalent task-specific property.

### O3 — Preservation
Relevant pre-existing build/install/configuration/runtime behavior continues to work. The candidate must not satisfy the new condition by breaking another mandatory supported path.

### O4 — Environment/harness validity
Pin and record the environment dimensions material to the task. Distinguish candidate failure from dependency/network/toolchain/bootstrap failure. Required commands must actually execute and outputs must bind to the exact candidate state.

## Decision

YES requires O1 + O2 + O3 + O4.
NO requires valid evidence of a mandatory operational/configuration/preservation failure.
INCONCLUSIVE covers environment drift, unavailable dependencies, bootstrap/network/toolchain failure, ambiguous skips, or any condition preventing attribution to the candidate.

## Frozen F6 mapping

- Django 12009: verify the installed command-entry-point result, not merely setup.py syntax; required outcome is one intended django-admin command rather than duplicate installation paths.
- pytest 9681: reproduce package/conftest discovery under the specified setup.cfg/pythonpath/import-mode interaction and preserve relevant normal discovery behavior.
- pytest 9780: reproduce the downstream CI/configuration collection behavior under the frozen environment assumptions; if the historical dependency/toolchain environment cannot be reconstructed sufficiently, classify INCONCLUSIVE rather than candidate failure.

## Environment identity

For F6, environment identity is part of the oracle semantics, not incidental metadata. Material versions/configuration must be frozen before confirmatory evaluation. Uncontrolled drift invalidates causal attribution.

## Minimal verification

`operational reproduction + artifact/config outcome + relevant preservation + environment/harness integrity`

No universal full-suite requirement is introduced.

## Completion

`BLOCK_2B_F6 = COMPLETE`
`BLOCK_2B = COMPLETE`
`ARCHITECTURE_APPROVAL = NONE`
