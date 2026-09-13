# DV treatment identity for comparative-v1

Status: PRE-REGISTERED / BLOCKED UNTIL DISTINCT ESCALATION TARGET QUALIFIES
Date: 2026-09-12

## Why a DV identity rule is required

DV is an integration/composition research project with multiple prospective policy treatments rather than one already-canonical monolithic runner. The comparison `SMAG vs metaO vs DV` therefore requires a prospective operationalization of the DV candidate before sealed comparative tasks are released.

The choice in this file is made without observing T1/T2/T3 treatment outcomes.

## Selected operationalization

For this comparative experiment, the DV candidate is operationalized as:

`DV-B4 = LOCAL_OR_FREE_FIRST + deterministic external verification + at most one deterministic escalation to a distinct stronger qualified executor`.

This is selected prospectively because:

1. the canonical DV objective emphasizes reuse, minimum sufficient execution, verification, and expansion only when necessary;
2. B4 is already a named prospective treatment in `experiments/p1/treatment-design-v1.json`;
3. B4 already has a pre-existing non-holdout S1 smoke binding and qualification evidence;
4. the architecture decision gate explicitly identifies competitive local/free-first composition as a decision-relevant outcome;
5. this avoids inventing a new learned/dynamic router.

This selection is an experiment operationalization, not a claim that B4 is empirically superior or the final DV architecture.

## Initial path

Frozen initial path class:

- policy: `B4_LOCAL_OR_FREE_FIRST`
- first executor: `C4-google-gemini-3-8-flash`
- provider: Google
- model: `gemini-3.8-flash`
- surface: Gemini API `generateContent`
- qualification evidence: `experiments/p1/executor-s0-qualification-v8.json`
- qualification state: `S0_READY_TELEMETRY_LIMITED`
- free-tier state in cited qualification: `CONFIRMED`

Telemetry marked `UNMEASURED` in the source qualification remains `UNMEASURED`; it must never be converted to zero.

## Verification and escalation

After the initial candidate attempt, the neutral task oracle is executed outside treatment authority.

Escalation is permitted exactly once when and only when one of these frozen conditions is observed:

- no candidate artifact before timeout;
- explicit executor/provider blocker;
- focal verifier failure attributable to the candidate;
- preservation/non-regression failure attributable to the candidate;
- structurally invalid candidate artifact.

Harness/oracle/environment failure does NOT trigger treatment escalation; it yields `INCONCLUSIVE` under the external failure-attribution rules.

The initial attempt, verification attempt, escalation handoff, escalated attempt, and final verification are all counted in total-system cost.

## Escalation target gate

The escalation target MUST be:

- a distinct executor/model path from the initial `gemini-3.8-flash` path;
- qualified prospectively on a synthetic/non-holdout probe;
- capable of producing a candidate patch in the same clean-worktree contract;
- able to expose model/provider identity and usage or explicit telemetry missingness;
- pinned by provider, surface, model identifier/version where observable, and adapter revision.

Current state:

`DISTINCT_STRONG_ESCALATION_TARGET = NOT_YET_QUALIFIED`

Therefore:

`DV_B4_COMPARATIVE_RELEASE = BLOCKED`

Do not silently substitute the same Gemini path as both cheap/free and strong escalation target.

## Preferred qualification order for the distinct strong target

Use the pre-existing DV executor candidate universe and qualify in this order, stopping at the first admissible distinct strong path:

1. OpenAI Responses API strong path (`gpt-5.6-sol`) if credentials/network/telemetry permit;
2. another already-listed C1 strong provider path if prospectively qualified;
3. otherwise declare `DV_B4_STRONG_PATH = BLOCKED` rather than inventing a new provider after seeing comparative outcomes.

No T1/T2/T3 task may be used to qualify or choose the escalation target.

## Retry ceiling

- initial application attempt: 1
- application retry within same path: 0
- verification after initial attempt: 1
- escalation transitions: at most 1
- escalated application attempt: 1
- final verification after escalation: 1
- further executor switching: prohibited

Provider-internal retries, if not controllable or observable, must be recorded as `UNMEASURED` rather than assumed zero.

## Shaping

For comparative-v1, use `S0_RAW_TASK` for DV. Do not activate deterministic S1 task shaping in the primary comparison because SMAG/metaO would not receive the same extra transformation authority and it would introduce another treatment factor.

A later factorial study may compare S0 vs S1 separately.

## Accounting boundary

Count all DV-owned resources for:

- routing/policy decision;
- task/context preparation;
- initial executor call;
- candidate normalization/extraction;
- treatment-owned verification requests, if any;
- escalation decision;
- handoff/context transfer;
- escalated executor call;
- retries/replanning;
- treatment-owned post-processing.

The final neutral benchmark verifier is recorded separately as evaluation cost and is not attributed to one treatment unless the same verifier cost is intentionally included for all treatments.

## Current release state

```text
DV_POLICY_IDENTITY             = FROZEN_B4
DV_INITIAL_PATH                = QUALIFIED_TELEMETRY_LIMITED
DV_DISTINCT_STRONG_TARGET      = NOT_YET_QUALIFIED
DV_NATIVE_SMOKE                = BLOCKED
DV_COMPARATIVE_RELEASE         = NO
T1_T2_T3_RELEASE               = NO
TREATMENT_OUTCOMES_OBSERVED    = NO
```
