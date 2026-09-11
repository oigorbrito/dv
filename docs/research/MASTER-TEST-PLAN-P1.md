# DV / P1 Master Test Plan

Date: 2026-09-11
Repository: `C:\Projetos\dv`
Entry HEAD: `d270b45845acc066feedf1d051a03d3d4e87e207`
Status: prospective methodology freeze; no treatment evidence

## 1. Scope and research question

The primary question is:

> Under a verifier-first prospective task corpus, which executor/policy treatment minimizes complete system resource cost per verified solved task while preserving task success and reproducibility?

Secondary questions address deterministic task shaping, economic/local/free executors, deterministic escalation, static
family policy versus dynamic policy, and whether existing frameworks and standards eliminate the need for a new DV
runtime/router.

The primary metric is `TOTAL_SYSTEM_TOKENS / VERIFIED_SOLVED_TASK`. Secondary metrics are monetary cost per verified
solved task, wall-clock latency, verified solve rate, escalation rate, verification cost, shaping cost, retry cost, and
failure/inconclusive rate. No composite score is defined.

The following evidence boundaries are normative:

```text
DOCUMENTED != CODE_CONFIRMED != EXECUTED != MEASURED != ACCEPTED
EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS
LOWER_EXECUTOR_TOKENS != LOWER_SYSTEM_COST
POPULAR != PROVEN
INFERRED != EMPIRICALLY_DEMONSTRATED
UNMEASURED != ZERO
UNMEASURED RUN != PILOT EVIDENCE
INCONCLUSIVE is first-class
```

The P0 remains `CLOSED_AS_DESIGN_LESSON` with `P0_TREATMENT_EVIDENCE = NONE`, `REAL_P0_RUNS = 0/24`, and release `NO`.
The legacy holdout remains sealed.

## 2. Falsifiable hypotheses

- H0-A: B2 has no reproducible system-cost advantage over simpler baselines.
- H1-A: B2 lowers complete system cost per verified solved task versus B0/B1 while preserving acceptable solve rate.
- H0-B: S1 provides no reproducible complete-system improvement over S0.
- H1-B: S1 reduces total resources or improves verified solve rate enough to offset its own cost.
- H0-C: B3 is not materially worse than a more dynamic policy. Survival of H0-C is evidence against a smart router.
- H0-D: B4 provides no useful cost/performance frontier.
- H1-D: B4 achieves useful verified success at a lower monetary/system-resource frontier.

No hypothesis is accepted from intuition, popularity, executor token count alone, or a single successful example.

## 3. Corpus and verifier-first admissibility

The task acquisition order is immutable: discover candidate; identify exact pre-solution base; freeze task statement;
identify independent verifier; prove provenance; hash/version verifier; materialize clean base; execute baseline focal
and preservation evidence; verify reproducible environment; classify admissibility; admit task; isolate solution.

The P1 admission contract requires exact base, frozen statement, independent verifier and provenance, reproducible base
and candidate execution, preservation evidence, reproducible environment, no gold solution exposure, hashable artifacts,
separable failure attribution, and one unambiguous family. Historical popularity or expected model behavior is never an
admission criterion.

Family coverage is staged. F1–F6 remain defined, but only families with deterministic/executable verification enter
comparative claims. P1-S1 prefers 2–4 admitted tasks across at least 2 operationalizable families; one task is permitted
only as `SMOKE_TEST_ONLY`. P1-S2 prefers at least 3 independent tasks per included family. If fewer are available, claims
are explicitly task/family limited. No fixed sample size is asserted before variance and resource review.

Current state from 5B is one admitted F6 task, D-F6-01, and no release to S1. F1/F5 require environment recovery; F2/F3/F4
require independent verifier recovery or new prospective acquisition. The defective legacy P0 holdout is not reused
automatically.

## 4. Executors and treatments

Executor categories are C1 strong remote, C2 economic remote, C3 local open-weight, C4 free/near-free, and C5 specialized
tool executor. Each concrete binding must expose identity, reproducible parameters, candidate capture, timeout/cancel,
retry/escalation events, cost provenance, credential/quota state, and usage telemetry or an explicit limitation.

For remote executors, retain provider/API/model, request parameters, usage fields, cache/reasoning fields where exposed,
price source/date, and API usage identifiers. For local executors, retain artifact/tag/digest, quantization, inference
runtime, OS/hardware, warm/cold state, load time, wall time, token telemetry, and energy evidence when reliable.

The conceptual treatments remain:

- B0 `STRONG_DIRECT`;
- B1 `CHEAP_DIRECT_VERIFY`;
- B2 `CHEAP_THEN_ESCALATE`;
- B3 `STATIC_FAMILY_POLICY`;
- B4 `LOCAL_OR_FREE_FIRST`.

No learned/custom DV router is introduced in early P1. OpenManus or Microsoft Agent Framework can only be compared as a
complete treatment after pairing framework, underlying executor/model, tools, policy, and verification.

## 5. Shaping and escalation

S0 is the minimally normalized raw task. S1 deterministically derives objective, constraints, allowed scope, repository
boundaries, verifier reference, environment constraints, and required artifact from frozen metadata. No LLM planning is
allowed. S0/S1 first runs are paired on the same task, executor, treatment, and environment; only shaping differs. Shaping
cost is accounted separately, and S1 becomes default only if its net benefit is reproduced.

B2/B4 escalation triggers are frozen before observation: missing candidate before timeout, explicit executor blocker,
focal/preservation failure, structurally invalid artifact, or deterministic resource ceiling. Subjective difficulty,
manual intuition, hidden reasoning classification, and post-hoc model selection are forbidden. Handoffs contain only
task identity, frozen task, artifact/diff when relevant, failed verifier, exit code, compact failure certificate, and
remaining budget.

## 6. Run, environment and accounting contracts

The unit is a treatment run: frozen task × treatment × executor binding × shaping × rollout/repetition. Retries,
escalations, replans and handoffs remain inside the run unless a later contract explicitly defines otherwise. Every run
has a globally unique ID and records OS, toolchain, repository SHA, clean state, dependency lock, non-secret environment,
hardware where applicable, executor version, provider/model identity, network/cache state, warm/cold state, and timestamps.

Accounting partitions routing, shaping, planning, context/input, execution, escalation/handoff, verification, and
retry/replanning. Failed and inconclusive runs retain all consumed resources. The primary token metric is kept separate
from monetary cost and latency.

Free and local execution is not cost-free: record inference time, utilization when measurable, electricity when reliable,
startup/load, download/setup, storage, maintenance, verification, escalation, and retries. Do not convert hardware time
to token equivalents. Remote runs retain original pricing source/date and usage identifiers; future price normalization is
a separate analysis.

Cache state is explicit: provider cache, local warm model, creation, amortization, and matched comparison state are
recorded. Timeout and budget limits are frozen by stage; consumed resources remain counted when a limit is reached.

## 7. Verification and failure attribution

`VERIFIED_SOLVED_TASK = YES` requires task satisfaction, regression/preservation, and Harness validity. `NO` requires valid
executable candidate failure evidence. Harness failure, oracle defect, environment drift, missing evidence, ambiguous
attribution, or required missing telemetry produces `INCONCLUSIVE`.

Failure classes are `PRODUCT_FAILURE`, `HARNESS_FAILURE`, `ORACLE_DEFECT`, `ENVIRONMENT_DRIFT`, `RESOURCE_LIMIT`,
`PROVIDER_FAILURE`, and `INCONCLUSIVE_OTHER`. Only valid product failure supports treatment `NO`; all classes consume
resources. Evidence priority favors focused execution, regression/preservation, and harness/environment integrity over
prose or LLM judgment.

## 8. Statistical analysis and repetitions

Use paired comparisons whenever feasible. Report raw per-task and per-family outcomes, solve proportions, tokens and
money per verified solution, latency distributions, escalation frequencies, and failure/inconclusive counts. Prefer
median plus distributions and robust summaries; bootstrap intervals may be used where appropriate. No arbitrary p-value
threshold is frozen. When sample size is small, report descriptive evidence and `INCONCLUSIVE`, never universal
superiority.

P1-S1 normally uses one rollout for pipeline validation. S2 begins comparative development runs after S1 validity. S3
selects repetitions only after observing variance and resource cost, then applies the same repetition policy to all
treatments. Increase equally until uncertainty is stable enough for the intended limited claim or a predeclared resource
ceiling is reached; do not stop because a preferred treatment leads.

## 9. Staged program and promotion

| Phase | Purpose | Promotion gate | Claims allowed |
|---|---|---|---|
| P1-S0 | executor/Harness qualification | strong plus economic/local/free path, identity, capture, timeout, accounting | surface qualification only |
| P1-S1 | smoke/pilot validation | valid baselines, compatible Harness, telemetry, no leakage; one task is smoke-only | pipeline validity |
| P1-S2 | development comparison | stable materialization, verifier, accounting, timeout and deterministic escalation | limited development observations |
| P1-S3 | repeated variance-aware comparison | diverse tasks, pinned versions, variance estimate, resolved deviations | scoped development comparison |
| P1-S4 | sealed external confirmation | frozen treatments/executors/shaping/repetitions/accounting and sealed holdout | protocol-scoped confirmation |
| P1-S5 | architectural decision | complete overhead accounting, simpler alternatives and prior art assessed | NO_BUILD, MICRO_POLICY_JUSTIFIED or INCONCLUSIVE |

No phase advances merely because a prior phase “ran successfully.”

## 10. Holdout and version drift

Create a new P1 holdout only after development acquisition and verification are stable. Before sealing, verify base,
verifier, environment, and frozen statement. After sealing, do not tune treatment, escalation, shaping, executor selection,
or repetition. Release is one final confirmation campaign after all definitions are frozen. The legacy P0 holdout stays
sealed.

If an executor changes or disappears, classify `MODEL_VERSION_DRIFT` and either continue with the exact pinned model,
restart the stage prospectively, or preserve separate cohorts. Never substitute silently.

## 11. Architectural falsification and stop rules

Before building, compare static configuration, MCP, A2A, provider APIs, OpenTelemetry, existing frameworks, and experiment
runners. Existing standards are reused for tools, agent communication, telemetry and propagation; acceptance authority,
verifier provenance and complete cost accounting remain explicit DV evidence contracts.

Stop with `NO_BUILD` if strong-direct is economically acceptable, cheap-direct+verify matches escalation, static policy
matches dynamic policy, an existing framework is equivalent, or savings do not exceed coordination/maintenance burden.
`MICRO_POLICY_JUSTIFIED` requires reproducible improvement that survives holdout, includes its own overhead, defeats
simpler baselines, and cannot be supplied by reuse. Otherwise the result is `INCONCLUSIVE`.

## 12. Current next-action queue

1. `A-001` — expand verifier-first development corpus. Dependency: current partial corpus. Artifact: admitted task records.
   Gate: at least two operationalizable families where possible. Blocked by: F1/F2/F3/F4/F5 verifier/environment gaps.
2. `A-002` — qualify one strong executor. Dependency: callable credentialed surface. Artifact: S0 qualification record.
   Gate: identity, capture, timeout, usage and cost evidence. Blocked by: credential/quota authorization.
3. `A-003` — qualify one economic or local/free executor. Dependency: A-002 and local/provider setup. Artifact: S0 record.
   Gate: compatible accounting and telemetry. Blocked by: credentials, runtime/model download and hardware evidence.
4. `A-004` — validate native telemetry and remote/local accounting. Dependency: A-002/A-003. Artifact: qualification evidence.
   Gate: no unexplained mandatory fields. Blocked by: provider/runtime capabilities.
5. `A-005` — materialize S1 run specs. Dependency: admitted corpus and qualified paths. Artifact: versioned run specs.
   Gate: unique IDs, exact bases, no solution/holdout leakage. Blocked by: A-001 through A-004.
6. `A-006` — execute smoke runs. Dependency: A-005 and explicit release. Artifact: raw run results.
   Gate: verifier/Harness/accounting integrity. Blocked by: `P1_S1_RELEASE = NO`.

## 13. Consistency audit of P1 artifacts

| Artifact | Audit |
|---|---|
| task-admissibility-contract-v1 | CONSISTENT |
| executor-screening-contract-v1 | CONSISTENT |
| treatment-design-v1 | CONSISTENT |
| staged-experiment-plan-v1 | NEEDS_PROSPECTIVE_AMENDMENT — master plan expands explicit S4/S5 naming; original is preserved |
| executor-candidate-universe-v1 | CONSISTENT as candidate universe, not final binding |
| executor-s0-qualification-v1 | CONSISTENT with current partial S0 state |
| task-shaping-schema-v1 | CONSISTENT |
| p1-development-corpus-v1 | CONSISTENT with one-task partial corpus |

No frozen artifact was silently rewritten. The master contracts are additive and their references are explicit.

## 14. Block closure

```text
MASTER_TEST_PLAN = COMPLETE
MASTER_TEST_PLAN_OUTCOME = MASTER_TEST_PLAN_READY
CURRENT_PHASE = P1-S0_EXECUTOR_AND_HARNESS_QUALIFICATION
P1_S1_RELEASE = NO
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
TREATMENT_EXECUTION = false
ARCHITECTURE_DECISION = NOT_APPROVED
```
