# Block 4AD — Authenticated API preflight + first real P0 run

Date: 2026-09-10 (local project date)  
Repository: `oigorbrito/dv`  
Status: `COMPLETE / INCONCLUSIVE`  
Holdout: `SEALED / NOT OPENED`

## Entry state

- Block 4AC: `COMPLETE`
- previous outcome: `INCONCLUSIVE / API_CREDENTIAL_UNAVAILABLE`
- previous commit: `1a8d9c1b9aa75b927a85ff72376dc41da53d37ff`
- real P0 runs: `0/24`
- P0 release: `NO`

## Credential and API preflight

The only credential check recorded the boolean `credential_present=true`. The secret value was never printed, persisted, or committed.

| Check | Result | Evidence |
|---|---|---|
| credential presence | `true` | sanitized evidence file |
| connectivity to `api.openai.com` | `PASS` | `GET /v1/models` completed |
| authentication | `PASS` | authenticated models request completed |
| account/project authorization | `NOT_EXECUTED` | Responses request was rejected before an authorized run |
| frozen model access | `ADVERTISED` | `gpt-5.6-sol` appeared in model listing |
| reasoning effort `high` | `NOT_EXECUTED` | no Responses execution accepted |
| quota/billing | `FAIL` | Responses preflight returned HTTP 429 |

The literal observed blocker is `API_QUOTA_OR_BILLING_BLOCKED`. No response was accepted, so there is no `response.id`, returned model identity, or provider-native usage telemetry.

Raw sanitized evidence:

`pilot-runs/block-4ad-d-f1-01-e0-r1/evidence/api-preflight-2026-09-10.json`

## Frozen first-run packet

The first run was not started because the authenticated API preflight did not pass. The packet remains unchanged:

- task: `D-F1-01`
- family: `F1`
- repository: `oigorbrito/RJ`
- base: `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`
- treatment: `E0`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- rollout: `r1`
- escalation: `none`
- holdout: sealed

No workspace was materialized, no candidate was produced, and the mandated .NET tests, oracle, Harness v1 run, and reconciliation were not executed. No candidate/manual substitute was created.

## Decision

```text
BLOCK_4AD = COMPLETE
BLOCK_4AD_OUTCOME = INCONCLUSIVE / API_QUOTA_OR_BILLING_BLOCKED
CREDENTIAL_PRESENT = true
API_CONNECTIVITY = PASS
AUTH_STATUS = PASS
MODEL_ACCESS = ADVERTISED; EXECUTION NOT_ACCEPTED
API_AUTHORIZATION = NOT_EXECUTED
QUOTA_BILLING = BLOCKED (HTTP 429)
RESPONSE_MODEL_IDENTITY = MISSING
PROVIDER_NATIVE_TELEMETRY = NOT_AVAILABLE
WORKSPACE_EXECUTION = NOT_EXECUTED
ORACLE_STATUS = NOT_EXECUTED
HARNESS_RECONCILIATION = NOT_EXECUTED
BLOCK_2_RESULT = INCONCLUSIVE
REAL_P0_RUNS = 0/24
P0_MEASUREMENT_READINESS = NOT_ESTABLISHED
P0_RELEASE = NO
HOLDOUT = SEALED
```

Next blocker: restore usable API quota/billing for the authorized project, then rerun the same frozen preflight and first-run packet. This result does not evaluate E0 and does not support treatment ranking.
