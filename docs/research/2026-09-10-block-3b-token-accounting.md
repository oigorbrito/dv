# Block 3B — Token accounting

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: NONE

## Scope

This sub-block freezes what token usage belongs to a treatment run and how token consumption must be partitioned for later economic comparison.

It does not freeze monetary prices, latency accounting, cache valuation, missing telemetry fallback, statistical aggregation, or treatment ranking.

## Governing principle

The economic objective is not executor-token minimization. It is total system token consumption per verified solved task.

Therefore:

`LOWER EXECUTOR TOKENS != LOWER SYSTEM TOKENS`

`LOWER SYSTEM TOKENS != VERIFIED BETTER TREATMENT`

and the primary token effectiveness metric is:

`TOTAL_SYSTEM_TOKENS / VERIFIED_SOLVED_TASK`

where all treatment-caused token usage from every run is included in the numerator and only terminal `YES` runs count as solved tasks.

## Accounting boundary

Every token-bearing model or model-like call caused by a treatment run must be attributed to exactly one `treatment_run_id` and one functional category.

At minimum, token usage must distinguish:

1. `routing_tokens`
   - classification;
   - task-family selection;
   - policy/routing decisions.

2. `planning_tokens`
   - task shaping;
   - decomposition;
   - plan generation;
   - plan revision attributable to the treatment.

3. `context_tokens`
   - context construction;
   - repository/file summarization;
   - reconstruction after handoff/retry/escalation;
   - state compression/expansion where model tokens are consumed.

4. `execution_tokens`
   - executor reasoning/generation;
   - tool-selection reasoning when token-metered by the executor;
   - code/patch/output generation.

5. `handoff_escalation_tokens`
   - state transfer;
   - handoff summaries;
   - escalation prompts;
   - receiving-model assimilation attributable to a handoff/escalation.

6. `verification_tokens`
   - LLM/verifier/judge calls;
   - semantic review calls;
   - generated verification interpretation where token-metered.

7. `retry_replanning_tokens`
   - retry-specific prompts;
   - repair/retry reasoning;
   - replanning calls not already classified elsewhere.

A protocol may later add finer categories, but it may not collapse away these distinctions if doing so prevents treatment-independent reconciliation.

## Input, output, and other billable token classes

Where provider telemetry exposes them, each token-bearing event should preserve separately:
- input/prompt tokens;
- output/completion tokens;
- cached input tokens or equivalent;
- reasoning tokens or provider-specific hidden/billable token classes where exposed;
- any other provider-reported token class that changes cost or resource interpretation.

Provider-specific fields may be retained in raw evidence while canonical aggregate fields remain provider-neutral.

No unexposed hidden token class may be invented or estimated without an explicitly frozen estimation method. Missing telemetry is handled in Block 3D.

## Total system tokens

For one treatment run:

`total_system_tokens_run = sum(all attributable token-bearing events across all functional categories)`

For a treatment over an evaluation set:

`total_system_tokens_treatment = sum(total_system_tokens_run for every run assigned to treatment)`

The primary effectiveness ratio is:

`token_cost_per_verified_solved_task = total_system_tokens_treatment / verified_solved_count`

where `verified_solved_count` is defined in Block 3A.

If `verified_solved_count = 0`, the ratio is not reported as zero or omitted. It is undefined/infinite for comparative economic purposes and must be explicitly represented as such in the later analysis protocol.

## Failed and inconclusive runs

All token usage from terminal `NO` and `INCONCLUSIVE` runs remains in the treatment numerator.

This includes:
- failed executor attempts;
- invalid intermediate outputs;
- verifier calls;
- retries;
- escalation;
- context reconstruction;
- token-bearing work performed before harness failure becomes known.

Tokens cannot be discarded because they did not produce a verified solution.

## Retry and escalation accounting

Retries and escalations accumulate; they do not replace earlier token usage.

Example semantic identity:

`cheap planning + cheap execution + verification failure + handoff + strong execution + verification = one run total`

Reporting only the strong final call or only the successful attempt is prohibited.

## Shared/precomputed artifacts

This sub-block freezes only the principle that token-bearing work caused specifically by a treatment run belongs to that run.

The exact charging treatment for legitimately shared plans, caches, indexes, static corpus preprocessing, or reusable artifacts is deferred to Block 3D because it requires treatment-independent integrity rules.

However, a treatment may not claim zero token cost for a dynamically created artifact merely by labeling it reusable after observing results.

## Non-token deterministic work

Deterministic computation with no model-token usage is not converted into fictional tokens. Its monetary/latency/infrastructure effects, if material, are handled separately in Blocks 3C–3D.

This preserves dimensional integrity: tokens measure tokens; currency measures money; time measures latency.

## Raw evidence requirement

Each token-bearing event must eventually be bindable to at least:
- `treatment_run_id`;
- event/attempt identity;
- functional category;
- provider/model identity and version where known;
- request/call identity where available;
- provider usage telemetry as returned;
- normalized token fields;
- timestamp/order;
- raw telemetry reference.

The normalized aggregate must be reproducible from raw evidence.

## Anti-gaming rules

- Do not count executor-only tokens as total system tokens.
- Do not omit routing/planning/verification merely because another treatment does not require them.
- Do not exclude failed calls, retries, or escalation.
- Do not estimate favorable token savings from undocumented cache behavior.
- Do not combine tokens from different provider classes into monetary claims; pricing is a separate dimension.
- Do not reinterpret a lower token total as proof of lower total monetary cost or latency.
- Do not use successful-run-only token averages as the primary economic metric.

## Secondary descriptive metrics

Later analysis may report descriptive quantities such as:
- median tokens per run;
- tokens by functional category;
- executor-token share of total tokens;
- verification-token share;
- escalation-token share;
- tokens conditional on `YES`, `NO`, or `INCONCLUSIVE`.

These are diagnostic only unless elevated by a later frozen protocol. They do not replace the primary total-system-tokens-per-verified-solved-task objective.

## Completion criterion

Block 3B is complete when every treatment-caused model-token expenditure has a frozen accounting boundary, mandatory functional partition, and aggregation rule that includes unsuccessful/inconclusive work and preserves the primary metric `total system tokens / verified solved task`.

Status after this document:

`BLOCK_3A = COMPLETE`
`BLOCK_3B = COMPLETE`
`BLOCK_3C = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
