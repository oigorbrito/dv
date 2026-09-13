# Executor freeze — Comparative experiment v1

Status: `NO_NATIVE_INTERSECTION / EXPERIMENT_A_BLOCKED_PROTOCOL`
Date: 2026-09-12
Treatment results observed: NO

## Decision

At the frozen treatment revisions, there is not sufficient evidence to certify one exact native executor surface that can be selected identically by SMAG, metaO, and DV while also fixing the same exact model/provider binding.

Therefore Experiment A MUST NOT begin using heterogeneous executor frontends and MUST NOT be described as a controlled same-executor comparison.

This is a fail-closed protocol decision. It does not claim that a future revision of one or more systems cannot support a common executor.

## Frozen evidence

### SMAG

Revision: `ec013a1519941da1b7e79264cd61332e3599f8b5`

The documented product boundary is a governance/control plane around supported coding executor CLIs. The frozen README demonstrates executor discovery through `smag agents` and explicit selection such as `smag --agent codex ...`. Current reconciled operational evidence at this revision is specifically scoped to Windows + OpenCode supervised execution, not to an OpenAI Responses API binding.

Conclusion for this protocol: no certified native OpenAI Responses API executor surface has been established at the frozen SMAG revision.

### metaO

Revision: `b4971b51203ae1b65be46e3fc8ddb58b9547b0e6`

The frozen source contains several executor/orchestrator adapters, including Codex App Server, Gemini, DeepSeek, OpenAI Agents, CrewAI and LangGraph. `CodexAppServerOrchestratorAdapter` supports an explicit `model` parameter and delegates execution over the Codex App Server JSON-RPC boundary.

Conclusion for this protocol: metaO can pin a Codex App Server model, but that surface is not the same executor frontend as a direct OpenAI Responses API call or a generic coding CLI.

### DV

Revision: `ba9a319fc3cd79e9de46e285146e028255ed14ae`

The frozen P1 executor universe defines the strong remote primary candidate as:

- provider: OpenAI
- executor: Responses API
- model: `gpt-5.6-sol`
- surface: remote API

It separately defines Gemini API and other candidates. The operational preserved branch includes a concrete Gemini API binding. No exact Codex CLI surface is established as the frozen P1 primary executor binding.

Conclusion for this protocol: substituting DV's Responses API/Gemini API surface for SMAG's Codex/OpenCode CLI would change both treatment and executor frontend.

## Why apparent model equivalence is insufficient

The following are NOT interchangeable for Experiment A merely because they may ultimately reach related model families:

- Codex CLI
- Codex App Server
- OpenAI Responses API
- Gemini API
- OpenCode CLI

They differ in context construction, tool mediation, sandbox/workspace behavior, retries, hidden system instructions, token accounting, streaming, patch production, and failure surfaces. Using different frontends would confound the treatment contrast.

`SAME_PROVIDER_OR_MODEL_FAMILY != SAME_EXECUTOR`

## Experiment A disposition

`EXPERIMENT_A = BLOCKED_PROTOCOL`

The block may be removed only by one of these versioned conditions:

1. a future frozen treatment revision proves the same native executor+model binding across all three treatments; or
2. a neutral external executor shim is qualified and each treatment can delegate to it without adding treatment-specific intelligent routing/planning/execution logic.

Do not silently relax the same-executor requirement after observing any treatment result.

## Neutral shim admissibility contract

A neutral shim is admissible only if all of the following hold:

1. One implementation is used byte-for-byte for SMAG, metaO, and DV.
2. It invokes one exact provider endpoint/executor and one exact model/version.
3. It receives the exact frozen task prompt and working directory.
4. It performs no model selection, routing, planning, re-planning, decomposition, governance, verification, acceptance, or failover.
5. It uses one predeclared retry policy; default is zero application retries.
6. It emits a unified `candidate.diff` or a typed terminal failure.
7. It records raw provider response/error, request/response identity where available, usage accounting, timestamps, exit/failure state, and hashes of material artifacts.
8. Each treatment must call the shim through a generic delegation boundary; no treatment receives a privileged alternate path.
9. Treatment-specific governance/supervision may wrap the shim because that is the treatment being measured, but must not replace or augment the shim's executor call with a second executor.
10. Shim qualification must use development/pilot tasks only. Sealed T1/T2/T3 holdout tasks remain untouched until qualification is complete and the shim revision is frozen.

## Preferred shim candidate

For minimal differential adaptation, the first candidate to qualify is a direct OpenAI Responses API binding with model `gpt-5.6-sol`, because DV already freezes that executor/model pair in its candidate universe and metaO already contains OpenAI-family adapter infrastructure.

This preference is provisional, not approval. SMAG must first demonstrate a non-intelligent generic command/delegation boundary capable of invoking the same shim without bypassing the governance path being evaluated.

If SMAG cannot wrap a generic external command without introducing a special executor implementation, the shim route is not yet qualified and Experiment A remains blocked.

## Next qualification step

Inspect and test only the generic delegation boundaries of the three frozen treatments against a harmless development/pilot task. Do not execute any sealed T1/T2/T3 task during plumbing qualification.

Required result:

`SHIM_DELEGATION = PASS | FAIL | INCONCLUSIVE`

Only `PASS` permits creation of an Experiment A executor freeze with an exact shim SHA, endpoint, model, timeout and accounting contract.
