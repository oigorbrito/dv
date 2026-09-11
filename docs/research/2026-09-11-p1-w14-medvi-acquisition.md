# P1-W14 medvi verifier-first acquisition

## Outcome

The medvi source was screened without executing a model, treatment, P1-S1
smoke, or holdout. No new task was admitted. The existing P1 corpus remains
partial with three admitted tasks across F2, F5, and F6.

```text
MEDVI_ACQUISITION = CLOSED_NO_ADMISSION
TASK_CORPUS = PARTIAL
COMPARATIVE_CORPUS_READY = NO
P1_S1_RELEASE = NO
HOLDOUT = SEALED
```

## Baseline and source

The DV checkout was clean on `main` at
`718b7b62eff40f03a80ce2688b831f9f12d71dcc`, equal to `origin/main` at the
wave baseline. The Harness self-test ran six tests and exited `0`. The public source
`oigorbrito/medvi` was verified at `531ba28602714359bafeeb8d806e4e06cc7ac34b`.
Its temporary clone was kept outside the tracked DV artifacts.

## Freeze and screening procedure

The metadata for M1, M2, M3, M4, M5, and L1-L5 was recorded before any
solution diff was inspected. Each high-priority parent was materialized as a
clean detached checkout. The candidate freeze records task statement,
parent, verifier, commands, and environment contract. Solution diffs were
inspected only afterward for historical confirmation and duplication.

M1's pre-existing observability tests were a valid independent focal
surface and passed `7/7`, but the stated solution commit has the same tree as
its parent. It therefore supplies no historical product delta for a task.
Its broader preservation suite was blocked by the missing generated Prisma
client. This same Prisma preservation blocker applies to M1, M2, and M3.

M2's parent build/typecheck and test commands were available, but typecheck
was blocked by the absent generated Prisma client. Preservation also exposed
the same Prisma setup failure and unrelated logger failures, so attribution
to the auth change is not defensible.

M3's build failed deterministically on the parent because
`submitCheckout` is undefined, while its preservation suite was blocked by
the absent generated Prisma client. The focal failure is useful historical
evidence, but incomplete preservation prevents admission.

M4/M1 are a duplicate logger/observability line for corpus purposes. M5 is a
broad checkout/deployability changeset. L1-L5 were cheap-screened by parent
metadata and solution file status: each relevant focal test was added or
modified in the solution changeset, or the changeset was broad/interleaved.
Those leads were rejected as lacking a clean independent verifier or
focal attribution. No test from a solution was backported.

## Candidate and baseline evidence

The raw records are under `pilot-runs/p1-w14-medvi-acquisition/`. The three
materialized parents were:

| Candidate | Parent | Focal result | Preservation | Decision |
|---|---|---|---|---|
| MEDVI-M1 | `f5feac3...` | 7/7 pass | Prisma client setup blocked | rejected: no tree delta |
| MEDVI-M2 | `10b5d8e...` | typecheck blocked by Prisma client | failed/blocked with unrelated failures | rejected |
| MEDVI-M3 | `0243741...` | expected product build failure | Prisma client setup blocked | rejected |

The exact full SHAs, commands, exit codes, and evidence paths are in
`candidate-freezes.json` and `candidate-executions.json`. The environment
used only the parent lockfile through `npm ci --ignore-scripts`. No lockfile,
source file, solution, or external production service was changed.

## Corpus impact

The corpus remains unchanged:

```text
before: 3 tasks, 3 families, 2 repositories
after:  3 tasks, 3 families, 2 repositories
```

The admitted tasks remain `D-F2-05`, `D-F5-01`, and `D-F6-01`. No new family,
runtime, or verifier type was added. The comparative corpus is still not
ready because no additional independent task survived the verifier,
preservation, and environment gates.

## Blockers and limitations

`P1-W1-BLK-002` remains open for comparative corpus expansion, and
`P1-W4-BLK-STRONG-CREDENTIAL` remains open for strong executor qualification.
`P1-W14-MEDVI-ENV` now explicitly covers preservation for M1, M2, and M3;
M2 additionally has a focal environment block, while M3 has a valid
expected product build failure. The medvi source did not provide an
admissible task in the screened leads. The environment limitation is
recorded as observed evidence, not as a claim that no reproducible setup
could ever exist.

The W14 commit was not remotely preserved. The push attempt failed because
`github.com:443` was unreachable. `P1-W14-BLK-GITHUB-PUSH` records the
local/remote SHAs, ahead/behind state, impact, and exact unblock condition.

The legacy holdout remained sealed and no holdout path was inspected. No
treatment result, candidate output, or model/API call influenced selection.
The wave therefore supports only a corpus-acquisition decision, not a
treatment or executor conclusion.

## Next step

Continue verifier-first discovery from another source or a newly identified
medvi history only when an independent verifier and reproducible preservation
environment can be established before solution inspection. Separately,
qualify an authorized strong executor before considering P1-S1.
