# Block 4AA — Local historical workspace recovery + first real run

Date: 2026-09-10  
Repository: `oigorbrito/dv`  
Status: `COMPLETE / INCONCLUSIVE`

## Frozen packet

- task: `D-F1-01`
- family: `F1`
- repository: `oigorbrito/RJ`
- base: `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`
- treatment: `E0`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- rollout: `r1`
- escalation: `none`

The holdout was not opened. Corpus, treatment, oracle, harness and pricing artifacts were not changed.

## Historical source inspection

`C:\Projetos\RJ` exists and has the expected origin `https://github.com/oigorbrito/RJ.git`. Its observed HEAD is
`4282cd5c836f81c6da95d17cf317c05525b417d7`, on branch `preserve/rjudi-local-2026-09-08-192438`, with pre-existing
WIP (`42` status lines). The source checkout was probed only and was not modified.

The exact historical commit is locally available. `cat-file -e` succeeded and `show -s --format=fuller` identified:

```text
c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d
Author: Codex <codex@openai.com>
Subject: Preserve RAG evaluation WIP
```

## Isolated recovery

The first `--local` clone attempt failed while creating a hardlink because of filesystem permissions. The permitted
local fallback `--local --no-hardlinks --no-checkout` succeeded without network access. The workspace was checked out
detached at the exact frozen SHA and is clean:

```text
workspace: C:\Projetos\dv\pilot-runs\block-4aa-d-f1-01-e0-r1\workspace
HEAD: c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d
detached HEAD: true
worktree: clean
origin: C:\Projetos\RJ
```

Toolchain recorded: Python `3.13.14`, .NET `10.0.401`, Git `2.55.0.windows.5`. Raw recovery and preflight evidence
is retained in `pilot-runs/block-4aa-d-f1-01-e0-r1/evidence/recovery-and-preflight.txt`.

## E0 admissibility and stop boundary

This Codex session does not expose an authorized E0 execution surface that simultaneously provides the frozen model
identity, `DV_RUN_ID` association, and provider-native authoritative token and monetary telemetry. Transcript text is
not provider-native telemetry; tokens were not estimated and no candidate was manually produced.

Under the frozen treatment-binding rules, an unavailable execution surface is `INCONCLUSIVE` and cannot be silently
substituted. Therefore E0 was not executed. The exact frozen oracle commands, `tools/dv_pilot_harness.py`, and
`tools/dv_oracle_adapter.py` were not invoked because no candidate state exists and doing so would not be a valid run.

## Decision

```text
BLOCK_4AA = COMPLETE
BLOCK_4AA_OUTCOME = INCONCLUSIVE / EXECUTOR_TELEMETRY_SURFACE_UNAVAILABLE
HISTORICAL_OBJECT = AVAILABLE
ISOLATED_WORKSPACE = PASS
E0 = NOT_EXECUTED
TELEMETRY = UNAVAILABLE
ORACLES = NOT_EXECUTED
HARNESS_RECONCILIATION = NOT_EXECUTED
REAL_P0_RUNS = 0/24
P0_MEASUREMENT_READINESS = NOT_ESTABLISHED
P0_RELEASE = NO
HOLDOUT = SEALED
```

Next blocker: provide an authorized E0 executor surface for `gpt-5.6-sol` / `high` / `r1` with provider-native usage
telemetry bound to the existing Harness v1 run, then repeat the frozen run without changing the recovered workspace
base or any evaluation artifact.
