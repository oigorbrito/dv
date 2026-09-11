# P1-W13 C1 surface canonicalization and strong qualification

## Outcome

The wave completed the local C1 surface audit and recorded a minimal Anthropic
identifier erratum. Both approved strong credentials are absent, so no
qualification probe was authorized or executed. No P1 task, treatment,
candidate, model, or holdout was accessed.

```text
STRONG_PATH_READY = NO
P1_S1_RELEASE = NO
HOLDOUT = SEALED
```

## Baseline

The checkout was clean on `main` at
`ba7949f7fb276e7b9c12af0b00679469af567b21`, equal to `origin/main`. The
Harness self-test ran six tests and exited `0`.

## Frozen C1 definitions

The repository contains exactly the frozen candidates `C1-openai-sol` and
`C1-anthropic-opus`, in that order. OpenAI is recorded as GPT-5.6 Sol with
the Responses API model ID `gpt-5.6-sol`. The Anthropic material records the
logical/display name Claude Opus 4.8 but also stores `claude-opus-4.8` in a
Claude API context. Current official Anthropic documentation identifies the
Claude API ID as `claude-opus-4-8`, while the model remains an active legacy
model. The mapping is therefore an erratum to the invocation surface only;
it does not change the candidate, provider, model generation, or order.

Sources checked on September 11, 2026: [OpenAI model documentation](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4)
and [Anthropic API usage primer](https://platform.claude.com/docs/en/claude_api_primer).

## Credential gate and selection

The process checked only boolean presence. `OPENAI_API_KEY PRESENT=False` and
`ANTHROPIC_API_KEY PRESENT=False`. No secret value was read, printed,
persisted, or searched for. The frozen selection rule consequently selected
`NONE`, retaining `P1-W4-BLK-STRONG-CREDENTIAL` as open.

Because no authorized credential was available, the one-probe rule was not
entered. Request ID, response identity, candidate text, usage, raw response,
retry data, and latency are `UNMEASURED`, not zero. There is no provider
qualification result to promote.

## Promotion gate

The carried-forward terms are `S1_CORPUS_READY=PASS`,
`ECONOMIC_PATH_READY=PASS_WITH_TELEMETRY_LIMITATION`,
`ACCOUNTING_PRIMARY_READY=PASS`, `HARNESS_P1_REMOTE_READINESS=PASS`, and
`HOLDOUT_SEALED=true`. `STRONG_PATH_READY=NO`, so
`P1_S1_RELEASE=NO`. Smoke specifications were not materialized, and
`REAL_P0_RUNS` and `P0_RELEASE` remain unchanged.

## Evidence and validation

Evidence is under `pilot-runs/p1-w13-strong-surface/`. The versioned strong
qualification matrix is `experiments/p1/executor-s0-qualification-v5.json`;
previous versions remain preserved. Validation passed for JSON parsing,
identifier/provider mapping, secret scan, holdout leakage, P0 immutability,
Harness `6/6`, and `git diff --check`. Raw provider response hashing is not
applicable because no probe ran.

## Remaining blocker

The next defensible action is an authorized qualification probe for the first
available candidate in the frozen order. It must use one 30-second attempt,
capture the raw response before normalization, and stop before any P1-S1
execution. No comparative or treatment claim is supported by this wave.
