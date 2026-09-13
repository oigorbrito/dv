# Comparative experiment v1 — SMAG vs metaO vs DV

Status: PRE-REGISTERED / NO COMPARATIVE TREATMENT RESULTS OBSERVED
Date: 2026-09-12

## Question

Compare SMAG, metaO, and DV side-by-side on three pre-solution task strata while holding the task, starting revision, evaluator, stop conditions, and (for Experiment A) executor/model constant.

This experiment evaluates the systems as treatments. `empirical-evaluator-ado` is not a treatment and is not required as the measurement authority.

## Frozen treatment revisions

- SMAG: `ec013a1519941da1b7e79264cd61332e3599f8b5`
- metaO: `b4971b51203ae1b65be46e3fc8ddb58b9547b0e6`
- DV: `ba9a319fc3cd79e9de46e285146e028255ed14ae`

The DV revision is intentionally the preserved head that contains the executable adapter/binding/harness work rather than the repository `main` snapshot.

## External evaluator

SWE-bench evaluator repository is pinned to:

`SWE-bench/SWE-bench@02e7a74ffd0b707aab73d203fe87bdc7c76afc8e`

The evaluator is external to all three treatments.

Canonical current CLI shape at the pinned evaluator revision:

```text
swebench eval <dataset> --predictions <predictions.jsonl> --run-id <run-id> --instance <instance-id> --workers 1 --timeout <seconds> --report-dir <dir>
```

Equivalent `python -m swebench.harness.run_evaluation` invocation is admissible only if it resolves to the same pinned evaluator revision and arguments.

## Task materialization

For each task spec:

1. Load the specified dataset and split.
2. Select the row by exact `instance_id`.
3. Assert that dataset `base_commit` equals the SHA frozen in the spec.
4. Expose to the treatment exactly the dataset `problem_statement` plus the repository state at `base_commit`.
5. Do not expose `patch`, `test_patch`, `FAIL_TO_PASS`, `PASS_TO_PASS`, solution head, or any solution-derived structural statistic to the treatment.
6. Preserve a SHA-256 digest of the exact task prompt bytes used in every run.

## Common treatment output contract

Each treatment must ultimately yield either:

- a unified diff against the frozen task base revision, saved as `candidate.diff`; or
- a terminal failure classification with no candidate patch.

A neutral adapter may convert `candidate.diff` into the SWE-bench prediction JSONL schema. That adapter must not modify the patch content.

## Experiment A — controlled executor

Purpose: estimate treatment overhead/effect while reducing executor confounding.

All three treatments receive the same executor/model family and version, provider class, task prompt, base snapshot, timeout, token/cost ceiling, tools, and verifier.

The exact executor/model identifier MUST be frozen before the first Experiment A treatment run. Until then, treatment runs are BLOCKED_PROTOCOL.

## Experiment B — native policy

Purpose: evaluate each system as a complete product, including native executor selection, routing, escalation, failover, or composition.

Experiment B begins only after Experiment A protocol and raw results are sealed. Its results are analyzed separately and must not be pooled with Experiment A as if they estimated the same causal contrast.

## Repetitions

Initial study: 5 repetitions per treatment/task cell.

- 3 treatments
- 3 tasks
- 5 repetitions
- 45 runs per experiment mode

`n=5` is a bounded initial variance/cost study, not a claim of strong statistical power.

Treatment order must be randomized or counterbalanced within task/repetition blocks. The realized order and randomization seed must be preserved.

## Primary outcomes

Per run preserve:

- `verified_solved_task = YES | NO | INCONCLUSIVE`
- wall-clock duration
- total system tokens, with available input/output/reasoning/cache decomposition
- monetary cost
- model/provider calls
- retries
- replans
- executor switches
- handoffs
- verification attempts
- timeout/resource-limit status
- provider failure
- environment/harness failure
- product/treatment failure attribution

Primary economic ratio:

`total_system_tokens / verified_solved_task`

Also report:

- verified success rate
- monetary cost per verified solved task
- latency per verified solved task

Do not collapse these into an unvalidated weighted score. Report dimensions separately and use dominance/Pareto comparisons where appropriate.

## Failure semantics

- A treatment timeout is an observed treatment outcome, not missing data.
- Provider quota/network/auth failure must be preserved and attributed; do not silently retry outside the predeclared retry policy.
- Evaluator/bootstrap failure that prevents valid judgment yields `INCONCLUSIVE`, not treatment `NO`.
- A valid evaluator failure attributable to the candidate yields `NO`.
- Missing mandatory evidence yields `INCONCLUSIVE`.

## Oracle integrity

SWE-bench evaluation material is evaluation-only. Candidate/treatment processes must not have write authority over external oracle metadata, hidden/evaluation tests, evaluator code, or grading output.

A treatment's own acceptance result is diagnostic evidence only; the external evaluator supplies the cross-treatment verified outcome.

## Anti-post-hoc rules

After the first comparative treatment result is observed:

- no task replacement because a treatment performed poorly;
- no task-stratum relabeling using solution structure or observed outcomes;
- no oracle narrowing to make a candidate pass;
- no new mandatory oracle requirement unless the task is formally declared `CORPUS_DEFECT`/`ORACLE_DEFECT` and the protocol is versioned;
- no silent treatment revision changes.

## Run identity

Every run identity must bind at minimum:

`protocol_version + task_id + instance_id + task_base_sha + treatment + treatment_revision + executor_model + repetition + evaluator_revision + environment_id`

Raw stdout/stderr, candidate patch, evaluator report, environment manifest, and accounting telemetry must be preserved under that run identity.
