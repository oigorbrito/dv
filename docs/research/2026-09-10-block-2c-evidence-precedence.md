# Block 2C — Oracle evidence precedence and conflict semantics

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

Closes the cross-family evidence semantics for Block 2. It does not select an executor, router, verification escalation policy, learned judge, or architecture.

## Principle

Evidence authority is based on directness, determinism, task relevance, independence, and harness validity — not on which agent produced the claim.

`SELF_REPORT < EXECUTED_EVIDENCE`

No positive low-authority claim may override a valid mandatory higher-authority failure.

## Evidence classes

E0 — metadata/self-report only: executor says done, prose rationale, unexecuted claim. Never sufficient for YES or NO.

E1 — static/deterministic structural evidence: schema, syntax, type/static checks, hashes, artifact existence/config inspection. Authoritative only for the property directly checked.

E2 — focused executable task evidence: task-specific reproducer, acceptance test, constraint test, command/package/install probe. Primary evidence for task satisfaction.

E3 — preservation/regression evidence: predeclared adjacent tests, compatibility checks, broader relevant suite. Primary evidence for preservation.

E4 — environment/harness integrity evidence: state/revision binding, environment identity, discovery/execution proof, raw logs, anti-tampering evidence. Preconditions interpretation of E1-E3.

E5 — learned/LLM judgment: may assist only where no cheaper deterministic/executable oracle captures the semantic requirement. It is not introduced as mandatory by Block 2 and cannot override contradictory valid deterministic/executable evidence without a separately predeclared protocol.

## Precedence rules

1. Invalid/unknown E4 makes affected executable evidence non-conclusive: INCONCLUSIVE.
2. A valid mandatory E2 failure implies NO regardless of executor self-report or other positive non-equivalent evidence.
3. A valid mandatory E3 failure implies NO unless the task specification explicitly authorizes that behavior change.
4. E1 cannot prove runtime behavior beyond the property it checks.
5. Passing a broader suite cannot substitute for a missing mandatory task-specific E2 check.
6. Conflicting valid mandatory checks with no predeclared semantic resolution produce INCONCLUSIVE and an oracle-defect investigation; do not choose the favorable result post hoc.
7. E5 cannot silently break ties in confirmatory evaluation unless its role and decision rule were frozen before treatment results.

## Evidence independence

Executor-generated tests/diagnostics are candidate artifacts, not independent proof by themselves. They become evidence only after execution/evaluation through the frozen oracle path.

Gold patches, hidden solution metadata, and solution-derived signals remain evaluator-only where applicable and cannot enter routing/execution inputs.

## Failure attribution

Every non-YES result must distinguish at least:
- PRODUCT_FAILURE: valid oracle demonstrates candidate failure;
- HARNESS_FAILURE: evaluation infrastructure prevented valid observation;
- ORACLE_DEFECT: frozen oracle is internally invalid/insufficient;
- ENVIRONMENT_DRIFT: material environment differs from frozen assumptions;
- INCONCLUSIVE_OTHER: evidence cannot support causal attribution.

Only PRODUCT_FAILURE maps directly to verified NO. Other categories map to INCONCLUSIVE until resolved/versioned.

## Anti-p-hacking / anti-post-hoc rule

Oracle commands, mandatory checks, admissible evidence, and conflict rules must be frozen before confirmatory treatment results.

A discovered oracle defect is preserved as evidence, corrected through an explicit oracle/corpus version, and rerun under the declared protocol. It is not silently patched to change a treatment result.

## Block 2 completion

Block 2 is complete when:
- the global ternary success contract is frozen;
- F1-F6 each have family-specific oracle semantics;
- evidence precedence/conflict/failure-attribution rules are frozen.

All are now satisfied.

`BLOCK_2 = COMPLETE`
`BLOCK_3 = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
