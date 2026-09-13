# Native runner qualification — SMAG vs metaO vs DV

Status: PRE-TREATMENT QUALIFICATION
Date: 2026-09-12

No sealed comparative task T1/T2/T3 is used by this qualification.

## Purpose

Before any comparative treatment run, prove that each candidate has an operationally defined treatment boundary that can:

1. receive a model-visible task without hidden oracle material;
2. operate on a clean disposable worktree pinned to a declared base revision;
3. produce or leave an observable candidate workspace change;
4. expose a terminal treatment decision/status;
5. preserve stdout/stderr and sufficient execution evidence;
6. allow a neutral collector to compute a final `candidate.diff` without modifying treatment output;
7. keep the external verifier outside treatment authority.

This gate tests runner/harness validity only. It must not be interpreted as task quality, performance, ranking, savings, or comparative evidence.

## Frozen treatment revisions

- SMAG: `ec013a1519941da1b7e79264cd61332e3599f8b5`
- metaO: `b4971b51203ae1b65be46e3fc8ddb58b9547b0e6`
- DV: `ba9a319fc3cd79e9de46e285146e028255ed14ae`

## Neutral smoke task

Use a fresh disposable Git repository containing only:

- `README.md` with any fixed baseline content; and
- no `NATIVE-RUNNER-SMOKE.txt` file.

Model-visible instruction:

```text
Create exactly NATIVE-RUNNER-SMOKE.txt containing exactly NATIVE_RUNNER_SMOKE_OK followed by one LF newline. Do not modify any other tracked file. Do not create any other file.
```

Neutral verifier requirements after treatment termination:

- `NATIVE-RUNNER-SMOKE.txt` exists;
- its bytes equal `NATIVE_RUNNER_SMOKE_OK\n`;
- no other tracked or untracked workspace change is present apart from the sentinel file and treatment-owned evidence kept outside the target repository;
- a unified diff against the frozen smoke base can be produced by the neutral collector;
- treatment exit/decision and raw stdout/stderr are preserved.

A model/provider failure is a treatment/provider observation. Failure of the neutral collector/verifier itself is `INCONCLUSIVE`, not product `FAIL`.

## SMAG qualification

### Native surface

Canonical user CLI at the frozen revision is the published `smag-ia@0.1.4` executable. The documented governed-task form is:

```text
npx --yes --package=smag-ia@0.1.4 smag --agent <executor-id> "<task>"
```

The architecture executes the selected runtime inside isolated staging, independently audits/accepts staged changes, and promotes or blocks them. Executor success is not the final authority.

### Qualification state

`RUNNER_BOUNDARY = PASS_CODE_AND_DOCUMENTATION`

Reason: the frozen governance core accepts runtime command/arguments and the frozen public CLI exposes governed executor invocation. Final smoke remains `NOT_EXECUTED` until run in the target Windows environment with a READY executor/provider.

Required observed smoke evidence:

- CLI version/package identity;
- `smag agents` status;
- treatment exit code/final decision;
- stdout/stderr;
- target pre/post Git status;
- neutral `candidate.diff`;
- provider/model identity and usage if exposed by the selected executor.

## metaO qualification

### Native surface

The frozen architecture is:

`Mission -> Strategy/Selection -> Policy/Budget -> OrchestratorContract -> Runtime Adapter -> Orchestrator -> Evidence -> Independent Acceptance -> Accept/Replan/Failover/Block`.

The canonical operator entry point is `metao run <mission.json>` with runtimes supplied through the declarative runtime catalog/factory path. The committed quickstart runtime is only an onboarding example and MUST NOT be used as a coding-treatment substitute.

The frozen source includes real adapter surfaces such as Codex App Server, OpenAI Agents, CrewAI, LangGraph, Gemini, DeepSeek, and Jules. A comparative coding smoke must use an actual admitted coding-capable runtime, not `quickstart-local`.

### Qualification state

`RUNNER_BOUNDARY = PASS_CODE_AND_DOCUMENTATION`

Reason: the mission/runtime/independent-acceptance boundary is implemented and operationally documented at the frozen revision. Exact coding-runtime catalog/mission materialization for this comparative experiment remains `NOT_EXECUTED` and must be qualified before T1/T2/T3.

Required observed smoke evidence:

- metaO package/revision identity;
- exact runtime catalog digest;
- runtime certificate/admission state where required;
- mission JSON digest;
- selected runtime/orchestrator identity;
- treatment terminal state and independent acceptance decision;
- stdout/stderr and persisted inspect evidence;
- neutral `candidate.diff`;
- provider/model identity and usage when exposed by the runtime.

## DV qualification

### Important treatment-identity boundary

DV is an integration/composition research project, not a measurement system and not a single frozen executor.

At the frozen revision its prospective treatment design contains multiple policies:

- B0 strong direct;
- B1 economic direct + verification;
- B2 economic first + deterministic escalation;
- B3 static task-family policy;
- B4 local/free-first + deterministic verification/escalation.

A custom learned/dynamic DV router is explicitly not the default treatment.

The frozen DV master plan requires staged qualification before comparative claims. Current qualification evidence includes provider paths, but the policy campaign has not yet produced a single canonical `DV_NATIVE` treatment identity for comparison against SMAG and metaO.

### Qualification state

`RUNNER_BOUNDARY = INCONCLUSIVE_TREATMENT_IDENTITY`

This is not a product failure. It means the benchmark cannot scientifically call an arbitrary B0-B4 configuration "DV" without prospectively freezing which configuration operationalizes the DV candidate.

The existing `dv_pilot_harness.py` is measurement/experiment infrastructure. It MUST NOT by itself be counted as the DV treatment in this comparison.

Before DV can enter comparative T1/T2/T3 runs, all of the following must be frozen without observing holdout treatment outcomes:

1. chosen DV policy id (`B0`..`B4` or an already-justified existing framework policy);
2. exact initial executor/provider/model binding;
3. exact deterministic verification rule;
4. exact escalation condition and escalation target if applicable;
5. maximum calls/retries/escalations;
6. treatment-owned vs neutral-measurement telemetry boundary;
7. one successful non-holdout native runner smoke with raw evidence.

## Current gate

```text
SMAG_RUNNER_BOUNDARY  = PASS_CODE_AND_DOCUMENTATION
SMAG_NATIVE_SMOKE     = NOT_EXECUTED

METAO_RUNNER_BOUNDARY = PASS_CODE_AND_DOCUMENTATION
METAO_NATIVE_SMOKE    = NOT_EXECUTED

DV_RUNNER_BOUNDARY    = INCONCLUSIVE_TREATMENT_IDENTITY
DV_NATIVE_SMOKE       = BLOCKED_BY_TREATMENT_IDENTITY

T1_T2_T3_RELEASE      = NO
COMPARATIVE_RESULTS   = NONE
```

## Promotion rule

T1/T2/T3 may be released only when:

- all three treatment identities are immutable;
- all three native smoke runs have valid observable evidence;
- the neutral collector/verifier contract passes on the smoke repository;
- telemetry missingness is explicitly represented as `UNMEASURED`, never zero;
- provider/model drift policy is frozen;
- no sealed oracle or gold solution has been exposed to any treatment.
