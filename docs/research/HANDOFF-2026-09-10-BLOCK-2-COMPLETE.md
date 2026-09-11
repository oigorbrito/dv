# HANDOFF — dv research after Block 2 completion

Date: 2026-09-10
Repository: `oigorbrito/dv`
Current research state: Block 1 COMPLETE; Block 2 COMPLETE; Block 3 NOT STARTED
Architecture approval: NONE
Implementation approval: NONE

## Purpose

Allow a new chat/agent to continue the falsification research without reconstructing the full conversation or reopening decisions that are already frozen.

## Canonical project objective

`dv` is not a MetaO+SMAG merge. It is a research effort evaluating whether a minimal capability-composition/economic-policy layer is needed between existing providers, standards, runtimes, verifiers, and heterogeneous capabilities.

The unit of composition is capability/function, not repository, framework, language, or codebase.

MetaO and SMAG are reference capability sources, not mandatory code dependencies.

The project remains research-only. Do not implement a new registry, workflow engine, runtime, memory system, generic router, protocol, or custom IR unless a later empirical block demonstrates a gap that existing standards/components cannot cover.

A valid final result remains: BUILD NOTHING.

## Governing rules

- software-engineering defensibility and empirical validation are required before architecture/component approval;
- `DOCUMENTED != EXECUTED != MEASURED != ACCEPTED`;
- `EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS`;
- `LOWER EXECUTOR TOKENS != LOWER SYSTEM COST`;
- `POPULAR != PROVEN`;
- `INFERRED != EMPIRICALLY_DEMONSTRATED`;
- `INCONCLUSIVE` is a first-class outcome;
- the economic objective is total system cost/tokens per verified solved task;
- work in closed blocks; finish/register one block before opening the next;
- no post-hoc policy/oracle/corpus edits to favor a treatment.

## Research falsification baseline

The strongest current minimal hypothesis remains approximately:

`cheap deterministic certificates + static task-family policy + minimum-sufficient scope + selective verification + compact state-based escalation + existing standards/runtime/adapters`

A smarter/custom `dv` layer is justified only if it reproducibly beats simpler alternatives after including its own decision, context, verification, coordination, maintenance, and handoff costs.

## Block 1 — corpus — COMPLETE

Canonical corpus: 36 tasks.

- 18 development/pilot tasks;
- 18 sealed external holdout tasks;
- six families;
- 3 development + 3 holdout tasks per family.

Families:
- F1 localized defect;
- F2 cross-component/integration defect;
- F3 feature/change;
- F4 test generation/proactive defect discovery;
- F5 refactor/review-driven correction;
- F6 configuration/build/dependency/integration.

Canonical manifest:
`docs/research/2026-09-10-block-1-canonical-corpus-manifest.md`
Commit: `e325fb12f54fe5f9ccc526c83eec027356ba701e`

The 18 external holdout tasks are frozen. F6 was completed with `pytest-dev__pytest-9780` after solution-blind rediscovery. A candidate previously surfaced through `gold.patch` remains excluded from this corpus version.

Important limitation: project-derived development tasks are useful for pilot/ecological validity but have high familiarity/contamination risk and cannot establish external generalization.

## Block 2 — oracle / verification — COMPLETE

### 2A — global success contract

File:
`docs/research/2026-09-10-block-2a-verifiable-success-contract.md`
Commit: `0994a4f4923b721c111aac5b06f370495efb11f4`

Global outcome:
`VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`

Three required dimensions:
- V1 task satisfaction;
- V2 regression/preservation;
- V3 harness validity.

YES requires all mandatory dimensions to pass.
NO requires valid executed evidence of a mandatory candidate failure.
Missing/invalid/ambiguous evidence maps to INCONCLUSIVE, not to failure.

### 2B-F1 — localized defect oracle

File:
`docs/research/2026-09-10-block-2b-f1-localized-defect-oracle.md`
Commit: `468214dbd5c2cdb0211e627605ee06f242b5884d`

Minimum semantics:
`defect-target evidence + local preservation + harness integrity`.

### 2B-F2 — cross-component/integration oracle

File:
`docs/research/2026-09-10-block-2b-f2-cross-component-oracle.md`
Commit: `2f3988034908d3eb9dfbc12c55c36ca355959be5`

Minimum semantics:
`interaction reproduction + boundary/contract preservation + adjacent regression + harness integrity`.

### 2B-F3 — feature/change oracle

File:
`docs/research/2026-09-10-block-2b-f3-feature-change-oracle.md`
Commit: `df2694137d83a7fe90de9e5f740bc88d65500864`

Minimum semantics:
`requested capability + material requirement boundaries + relevant compatibility + harness integrity`.

`DEMO_WORKS != FEATURE_CONTRACT_SATISFIED`.

### 2B-F4 — test-generation oracle

File:
`docs/research/2026-09-10-block-2b-f4-test-generation-oracle.md`
Commit: `ec2aae29543cd050bb3c45686d8b4f5764ccd180`

Minimum semantics:
`test executes + controlled Fail-to-Pass + semantic relevance + stability + harness integrity`.

`FAIL_TO_PASS != UNIVERSAL_TEST_QUALITY`.

### 2B-F5 — refactor/review oracle

File:
`docs/research/2026-09-10-block-2b-f5-refactor-review-oracle.md`
Commit: `f215e2cd6fd8c31e2b0d0693ccb1aa5054061b36`

Minimum semantics:
`functional objective + every mandatory review constraint + relevant preservation + harness integrity`.

`FUNCTIONAL_PASS != REVIEW_CONSTRAINT_SATISFIED`.

### 2B-F6 — config/build/integration oracle

File:
`docs/research/2026-09-10-block-2b-f6-config-build-integration-oracle.md`
Commit: `901c98ee950b5fd5286a4aecc86a8cca76954611`

Minimum semantics:
`operational reproduction + artifact/config outcome + relevant preservation + environment/harness integrity`.

Environment identity is part of the oracle semantics for F6.

### 2C — evidence precedence/conflict semantics

File:
`docs/research/2026-09-10-block-2c-evidence-precedence.md`
Commit: `1a324812beebf216290b2f6665eebc1b38a7a233`

Evidence classes:
- E0 self-report/prose only — never sufficient;
- E1 static/deterministic structural evidence — authoritative only for checked property;
- E2 focused executable task evidence — primary task-satisfaction evidence;
- E3 preservation/regression evidence;
- E4 harness/environment integrity — prerequisite for interpreting executable evidence;
- E5 learned/LLM judgment — optional only where deterministic/executable evidence is insufficient; not approved as mandatory.

Failure attribution:
- PRODUCT_FAILURE -> verified NO;
- HARNESS_FAILURE -> INCONCLUSIVE;
- ORACLE_DEFECT -> INCONCLUSIVE;
- ENVIRONMENT_DRIFT -> INCONCLUSIVE;
- ambiguous/unattributable -> INCONCLUSIVE.

A valid mandatory failure cannot be overridden by executor self-report or non-equivalent positive evidence.

## Exact continuation point

Next block is **Block 3 — Measurement Envelope**.

Do not start implementation and do not reopen corpus/oracle design unless a documented defect is discovered.

Proceed by sub-blocks and finish all of Block 3 before moving to pilot.

Recommended Block 3 decomposition:

### 3A — unit of accounting and run identity
Freeze what constitutes one attempt, one treatment run, one verified solved task, retry/escalation lineage, and how repeated rollouts are identified.

### 3B — token accounting
Measure total system tokens, not executor-only tokens. At minimum separate:
- classification/routing;
- planning/task shaping;
- context construction/reconstruction;
- execution;
- handoff/escalation;
- verification/judging;
- retry/replanning.

Primary token metric remains:
`total system tokens / verified solved task`.

### 3C — monetary and latency accounting
Freeze provider/model cost, infrastructure cost when material, wall-clock latency, model-call latency, coordination/network/runtime overhead, verifier cost, and any cache/reuse accounting.

Primary economic metric should include at least:
`total monetary cost / verified solved task`.

### 3D — treatment-independent resource/accounting integrity
Freeze rules for cache hits, failed/inconclusive attempts, timeouts, retries, parallel calls, reused plans/artifacts, missing provider usage telemetry, and external/runtime overhead.

No treatment may receive favorable accounting by omitting failed attempts or orchestration/verification overhead.

### 3E — Block 3 reconciliation/freeze
Produce one canonical measurement specification suitable for the pilot.

At the end of Block 3, do not claim statistical sufficiency or architecture approval. Pilot remains Block 4.

## Experimental sequence after current point

`Block 3 measurement envelope -> Block 4 pilot -> measure variance/instrumentation -> Block 5 freeze confirmatory protocol/holdout/margins -> Block 6 confirmatory experiment -> NO BUILD | MICRO-POLICY JUSTIFIED | INCONCLUSIVE`

Initial treatment arms remain candidates, not approved policies:
- E0 strongest-direct;
- E1 cheap/free-direct + verify;
- E2 cheap-first -> clean state-based escalation -> strong;
- E3 static policy by task family.

Learned/LLM router remains excluded from the first round unless later evidence changes the frozen experiment design through an explicit protocol version.

## Prior-art constraints that remain in force

Do not reimplement without extraordinary evidence:
- capability registry/discovery;
- agent transport;
- MCP/A2A-like protocols;
- durable runtime/checkpoint/recovery;
- memory store;
- generic workflow engine;
- generic provenance/tracing/experiment tracking;
- plan reuse/cache mechanisms already covered by prior art;
- custom provider-neutral execution IR, currently strongly falsified by Open Workflow + A2A/MCP ecosystem.

MAF remains a strong chassis/falsifier candidate, not approved architecture.

## Current repository head before this handoff

Latest substantive Block 2 commit before the handoff:
`1a324812beebf216290b2f6665eebc1b38a7a233` — `docs: freeze oracle evidence precedence`.

This handoff is documentation only and does not alter any research decision, treatment, oracle, corpus, or architecture.
