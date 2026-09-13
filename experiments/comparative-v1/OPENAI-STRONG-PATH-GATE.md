# OpenAI strong-path qualification gate

Status: PRE-TREATMENT / HOLDOUT SEALED
Protocol: comparative-v1

## Purpose

Qualify the distinct strong escalation target for `DV-B4` without executing, revealing, or deriving information from T1/T2/T3.

This is infrastructure qualification only. It cannot support claims about task quality, comparative performance, cost savings, or ranking.

## Frozen target

- Provider: OpenAI
- API surface: Responses API
- Endpoint: `https://api.openai.com/v1/responses`
- Model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Service tier: `default`
- Application retry count: `0`
- Probe: `Return exactly: DV_STRONG_PATH_PROBE_OK`
- Max output tokens: `64`

Probe implementation:

`experiments/comparative-v1/tools/qualify-openai-sol.ps1`

Pricing snapshot:

`experiments/comparative-v1/pricing/openai-gpt-5.6-sol-2026-09-12.json`

## Execution

Run from a clean checkout of branch `experiment/smag-metao-dv-cost-performance-v1` in PowerShell 7+ with `OPENAI_API_KEY` present in the process environment:

```powershell
pwsh -NoProfile -File .\experiments\comparative-v1\tools\qualify-openai-sol.ps1 `
  -Model gpt-5.6-sol `
  -ReasoningEffort high `
  -OutputPath .\openai-sol-qualification.json
```

Do not paste, persist, print, or commit the credential value.

## Frozen classification

### PASS / S0_READY

All of the following are required:

1. HTTP 2xx.
2. observed model exactly `gpt-5.6-sol`.
3. response status `completed`.
4. normalized output exactly `DV_STRONG_PATH_PROBE_OK`.
5. input/output/total token usage observed.

This qualifies the provider/model surface for a later synthetic runner smoke. It does not qualify the comparative treatments.

### PASS / S0_READY_TELEMETRY_LIMITED

Identity and exact response contract pass, but one or more required usage subfields are unavailable.

This may be used only if the missing field is explicitly represented as `UNMEASURED` and the comparative accounting protocol does not treat it as zero. If core input/output/total usage is missing, promotion to the cost comparison remains blocked.

### BLOCKED

Examples:

- missing `OPENAI_API_KEY`;
- HTTP 401/403 credential/access failure;
- HTTP 429 quota/credit/rate blocker;
- network/TLS/DNS/transport failure;
- provider-side non-2xx response not attributable to model correctness.

A BLOCKED result is not a product failure and must not be retried silently until success.

### FAIL / S0_FAIL

Examples:

- successful HTTP response but wrong observed model;
- successful response that violates the exact probe contract;
- invalid provider response structure under an otherwise successful request.

## Promotion rule

`DV_B4_STRONG_PATH_READY = YES` only when the probe is `S0_READY`, or when a specifically documented telemetry-limited exception is accepted before any comparative treatment run.

If strong-path qualification passes, the next permitted step is a synthetic `DV-B4` escalation smoke using a non-holdout disposable repository. The smoke must demonstrate:

`cheap/free path -> deterministic verification failure/trigger -> one strong escalation -> candidate artifact -> neutral verification`

The smoke must not use T1/T2/T3 or any solution-derived benchmark information.

## Previous evidence

The prior 2026-09-11 OpenAI qualification reached HTTP 429 `insufficient_quota / credit_balance_exhausted`; therefore the last observed state before this gate was `S0_CREDENTIAL_BLOCKED`. That historical observation is retained and must not be rewritten as a product failure.
