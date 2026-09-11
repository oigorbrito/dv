# Block 4AB — Authoritative E0 API surface + first real P0 run

Date: 2026-09-10  
Repository: `oigorbrito/dv`  
Status: `COMPLETE / INCONCLUSIVE`

## Frozen packet

`D-F1-01`, family `F1`, repository `oigorbrito/RJ`, base
`c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`, treatment `E0`, model `gpt-5.6-sol`, reasoning `high`, rollout `r1`,
escalation `none`.

The holdout was not opened. Corpus, oracle, treatment, pricing and metric artifacts were not changed.

## API preflight

The process environment was checked without printing the secret. `OPENAI_API_KEY` was absent
(`credential_present=false`). Its value was not printed, stored or committed. Because authentication material was not
available, no authenticated request was attempted; model access, `reasoning.effort=high`, quota and billing could not
be tested.

The exact factual blocker is:

```text
API_CREDENTIAL_UNAVAILABLE
```

No adapter was created because the preflight did not reach an executable API surface. Consequently there is no
returned model, response ID, usage object, authoritative usage reference or pricing calculation. No token estimate was
made.

## Local workspace recovery

The source checkout `C:\Projetos\RJ` was inspected read-only. It has origin
`https://github.com/oigorbrito/RJ.git`, HEAD `4282cd5c836f81c6da95d17cf317c05525b417d7`, branch
`preserve/rjudi-local-2026-09-08-192438`, and 42 pre-existing dirty status lines. It was not modified.

A new isolated workspace was recovered from that local source using `--local --no-hardlinks --no-checkout`, then
checked out detached at the exact frozen SHA:

```text
path: C:\Projetos\dv\pilot-runs\block-4ab-d-f1-01-e0-r1\workspace
HEAD: c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d
detached: true
clean: true
origin: C:\Projetos\RJ
```

Toolchain: Python `3.13.14`, .NET `10.0.401`, Git `2.55.0.windows.5`. Raw evidence is preserved in
`pilot-runs/block-4ab-d-f1-01-e0-r1/evidence/block-4ab-preflight.txt`.

## Execution boundary and decision

E0 was not executed. No candidate was manually produced. The two frozen dotnet oracle commands were not run because
there is no candidate state. Harness v1 and its reconciliation were not run for the same reason. This preserves the
protocol distinction between a recovered workspace and an executed, measured treatment run.

```text
BLOCK_4AB = COMPLETE
BLOCK_4AB_OUTCOME = INCONCLUSIVE / API_CREDENTIAL_UNAVAILABLE
API_CONNECTIVITY = NOT_TESTED (credential absent)
CREDENTIAL_PRESENT = false
MODEL_ACCESS = NOT_TESTED
RESPONSE_MODEL_IDENTITY = MISSING
PROVIDER_NATIVE_TELEMETRY = UNAVAILABLE
WORKSPACE_RECOVERY = PASS
E0_EXECUTION = NOT_EXECUTED
ORACLE_STATUS = NOT_EXECUTED
HARNESS_RECONCILIATION = NOT_EXECUTED
BLOCK_2_RESULT = INCONCLUSIVE
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
```

Next blocker: provide `OPENAI_API_KEY` through the authorized execution environment, then rerun the frozen preflight
and only proceed if the exact model, reasoning effort, workspace tooling and provider-native usage telemetry are
available. No GitHub push was performed.
