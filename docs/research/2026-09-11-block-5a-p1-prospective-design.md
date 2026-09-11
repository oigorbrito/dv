# BLOCK 5A — P1 prospective design and multi-executor candidate universe

Date: 2026-09-11
Repository: `C:\Projetos\dv`
Entry HEAD: `d010d41e245e21c7b3e628747b20e1b3a163113c`
Holdout: `SEALED`

## 1. P0 closure as a design lesson

```text
P0_TREATMENT_EVIDENCE = NONE
P0_PROTOCOL_FINDING = historical-task selection without verifier-first admissibility screening produced insufficient executable coverage for comparative evaluation
```

P0 successfully validated corpus-manifest mechanics, run identity, the accounting envelope, Harness v1, telemetry
requirements, treatment-binding mechanics, workspace materialization, oracle-admissibility review, failure attribution,
and the protocol-repair procedure. It did not establish treatment ranking, executor ranking, token savings, cost savings,
quality superiority, dynamic-policy superiority, or generalization. P0 artifacts remain unchanged.

## 2. Research question and measurement boundary

The frozen P1 question is:

> Under a verifier-first prospective task corpus, which executor/policy treatment minimizes complete system resource cost
> per verified solved task while preserving task success and reproducibility?

Primary metric: `TOTAL_SYSTEM_TOKENS / VERIFIED_SOLVED_TASK`.

Secondary metrics are monetary cost per verified solved task, wall-clock latency, verified solve rate, escalation rate,
verification cost, planning/task-shaping cost, retry cost, and failure/inconclusive rate. No composite score is defined.
`EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS`, `LOWER_EXECUTOR_TOKENS != LOWER_SYSTEM_COST`, and `UNMEASURED != ZERO`.
`INCONCLUSIVE` remains first-class.

## 3. Task admissibility and family review

`experiments/p1/task-admissibility-contract-v1.json` freezes the admissibility contract before P1 task discovery. It
requires exact pre-solution identity, a versioned independent verifier, explicit semantics, executable focal and
preservation evidence, reproducible environment, no gold solution, deterministic Harness attribution, one unambiguous
family, and selection independent of treatment results. Exclusion reasons are fixed before search.

The six existing families are retained. P1 should not delete a family because P0 failed:

| Family | Construct | Verifier shape | Environment risk | LLM judgment | Leakage risk |
|---|---|---|---|---|---|
| F1 localized defect | one bounded behavior or validation defect | deterministic focal regression plus preservation suite | package/toolchain | not required for pass/fail | hidden assertion details |
| F2 cross-component defect | state/data/contract interaction | independent integration or lifecycle verifier | multiple services/packages | not required, except task description review | solution wiring |
| F3 feature/change | new externally observable capability | contract/acceptance tests written before treatment | broader build and fixtures | may be needed to freeze scope, never to score | feature design leakage |
| F4 test generation/proactive discovery | verifier construction or boundary discovery | pre-existing independent property/fixture oracle, preferably base fail-to-pass | verifier injection and provenance | judgment may classify findings, not replace oracle | test derived from solution |
| F5 refactor/review correction | preserved semantics under structural change | regression suite plus explicit invariant checks | packaging and integration | not required for deterministic oracle | implementation shape |
| F6 configuration/build/integration | build, distribution, dependency, or integration behavior | locked build/distribution/integration commands | OS, package managers, caches | not required | environment-specific workarounds |

If a family cannot produce these conditions, mark it for redesign and preserve the missing family explicitly.

## 4. Executor categories and current candidate universe

P1 freezes categories rather than vendors: `C1 STRONG_REMOTE`, `C2 ECONOMIC_REMOTE`, `C3 LOCAL_OPEN_WEIGHT`,
`C4 FREE_OR_NEAR_FREE`, and `C5 SPECIALIZED_TOOL_EXECUTOR`. An executor may be described in more than one category,
but a treatment binding must choose exactly one concrete surface and model.

The complete candidate record is `experiments/p1/executor-candidate-universe-v1.json`. It distinguishes
`CURRENTLY_VERIFIED` from `KNOWN_BUT_NOT_CURRENTLY_VERIFIED` and is a shortlist, not a benchmark ranking. Current
documentation confirms OpenAI model/API availability and model identity, Anthropic model pricing documentation, Gemini
pricing/usage/rate-limit behavior, Ollama's OpenAI-compatible local surface, OpenRouter's model metadata/usage surface,
OpenManus, and Microsoft Agent Framework. Exact prices, quotas, licenses, hardware requirements, and telemetry fields
must be snapshotted and qualified again at S0; no current price is copied into the P1 pricing snapshot here.

| Category | Primary | Alternate | Initial decision |
|---|---|---|---|
| C1 | OpenAI Responses API / `gpt-5.6-sol` | Anthropic Claude API / `claude-opus-4.8` | candidates survive documentation gate; runtime qualification required |
| C2 | OpenAI Responses API / `gpt-5.6-luna` | Google Gemini API / `gemini-3.8-flash` | candidates survive documentation gate; quota and usage qualification required |
| C3 | Ollama local / `gpt-oss:20b` | vLLM / model artifact to be pinned | Ollama is documented; vLLM remains unqualified locally |
| C4 | Google AI Studio/Gemini free tier / `gemma-4` | OpenRouter unified API / route to be pinned | no free-cost claim; telemetry and route stability require S0 |
| C5 | OpenManus / pinned configuration required | Microsoft Agent Framework / pinned provider required | frameworks survive prior-art review, not executor qualification |

The universe contains 10 candidate records. No candidate is declared supported for real P1 until the screening contract
passes. The OpenAI, Anthropic, Google, Ollama, OpenRouter, Microsoft, and OpenManus sources are linked in the JSON
artifact and must be treated as time-sensitive.

## 5. Prior-art and chassis falsification

`experiments/p1/prior-art-capability-matrix-v1.json` records `AVAILABLE`, `PARTIAL`, `ABSENT`, and `UNKNOWN` separately;
missing documentation is not silently converted to `ABSENT`.

The local P0 evidence shows MetaO has partial verification/reproducibility and SMAG has capability discovery,
escalation, and verification hooks, but neither is established here as a complete multi-provider experimental runner.
Microsoft Agent Framework documents agents, workflows, tools, human-in-the-loop, checkpointing, and durable hosting;
it is a plausible reusable workflow substrate, not evidence of complete token accounting or independent acceptance.
OpenManus provides a tool-using agent framework, but P1 telemetry and reproducibility remain unknown. IBM `ado` and
Experiment Runner provide experiment-campaign primitives; BenchExec provides strong Linux resource measurement and
result handling but is not an agent/router. SciRep is relevant prior art for reproducible computational experiments,
not a drop-in executor benchmark surface.

The falsification result is `REUSE_FIRST`: no evidence justifies building a new dv runtime, kernel, or router in 5A.

## 6. Standards and protocol reuse

`experiments/p1/standards-reuse-matrix-v1.json` audits MCP, A2A, OpenTelemetry, W3C Trace Context, and provider-specific
OpenAI-compatible HTTP surfaces. MCP is suitable for tool/resource discovery and invocation; A2A is suitable for
agent-to-agent capability and task communication; OpenTelemetry and W3C Trace Context are suitable for trace/metric/log
semantics and propagation. None of these standards alone supplies acceptance authority, complete cost accounting, or
verifier provenance.

Therefore P1 proposes no provider-neutral IR and no new protocol abstraction. Use existing interfaces and a narrow
versioned evidence binding only where a real gap survives S0.

## 7. Conceptual treatments and task shaping

`experiments/p1/treatment-design-v1.json` freezes the simple baselines:

- B0 `STRONG_DIRECT`;
- B1 `CHEAP_DIRECT_VERIFY`;
- B2 `CHEAP_THEN_ESCALATE` with deterministic state-based escalation;
- B3 `STATIC_FAMILY_POLICY`;
- B4 `LOCAL_OR_FREE_FIRST` with deterministic verification/escalation.

B5, an existing mature router policy, remains optional and is not included until prior-art qualification justifies it.
A learned or dynamic custom dv router is not a default treatment.

The shaping comparison is:

- S0 `RAW_TASK`: minimally normalized frozen task;
- S1 `DETERMINISTIC_TASK_SHAPING`: objective, constraints, relevant paths/context boundaries, verifier contract, and
  output requirements organized by deterministic preprocessing, with no LLM planning.

Run S1 first on a small subset paired with S0, measure shaping resources separately, and promote it only if the paired
comparison shows a reproducible system-cost hypothesis worth testing. Do not immediately form the full treatment ×
shaping factorial.

## 8. Accounting for local and free execution

Free API price is not zero system cost, and local execution is not free. For every qualifying executor, retain separate
fields for token usage, hardware identity/time, electricity when measurable, model download/setup amortization policy,
inference wall time, shaping cost, verifier cost, escalation, retry, and maintenance/setup cost. The primary token metric
remains separate from monetary cost. No hardware-time-to-token conversion is allowed.

## 9. Verifier-first corpus acquisition

Acquire P1 tasks in this order: discover a candidate; identify the pre-solution base; freeze the task statement; identify
an independent verifier; prove provenance and hash; run the verifier on the base; run preservation; classify the
environment; admit and freeze the task; then make the solution inaccessible to treatments. A task with no independent
verifier is not repaired by borrowing assertions from its solution.

Start S1 with at least one admitted task per family where possible, but do not claim that six is statistically sufficient.
Select S2 repetitions only after S1 documents variance, failure modes, and resource cost. A defensible minimum is
therefore procedural rather than a fixed n: no family enters S2 without a valid baseline and no result enters a ranking
without complete accounting.

## 10. Staged plan and architectural gate

`experiments/p1/staged-experiment-plan-v1.json` defines:

1. P1-S0 executor/harness qualification on synthetic and verifier fixtures;
2. P1-S1 small development pilot across admitted families;
3. P1-S2 repeated development comparison after variance review;
4. P1-S3 sealed external confirmation with no holdout tuning.

Promotion requires exact provenance, complete telemetry or explicit exclusion, deterministic oracle reconciliation, and
reproducible environment evidence. Claims are limited by stage.

The architectural outcomes are `NO_BUILD`, `MICRO_POLICY_JUSTIFIED`, or `INCONCLUSIVE`. `MICRO_POLICY_JUSTIFIED`
requires improvement over simpler alternatives after including the policy's decision, context, verification,
coordination, escalation, and maintenance costs. If a static policy or existing framework performs equivalently, prefer
reuse or `NO_BUILD`.

## 11. Validation and limitations

All six families were retained; the existing holdout was not inspected or unsealed. The artifacts contain no treatment
output, gold solution, API secret, current frozen price, or architecture approval. Candidate statuses remain screening
statuses. P0 remains closed as a design lesson and its artifacts are untouched.

This block is design evidence only. It establishes neither executor quality nor a P1 result. Current web evidence is
time-sensitive, and local provider/model availability, rate limits, licenses, native usage fields, and hardware support
still require S0 qualification.

```text
BLOCK_5A = COMPLETE
BLOCK_5A_OUTCOME = P1_DESIGN_READY_FOR_TASK_DISCOVERY
P0_TREATMENT_EVIDENCE = NONE
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
ARCHITECTURE_DECISION = NOT_APPROVED
```
