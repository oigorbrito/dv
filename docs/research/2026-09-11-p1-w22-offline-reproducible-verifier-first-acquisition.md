# P1-W22 — Offline-reproducible verifier-first acquisition

## Decision

`P1-W22 = NO_NEW_ADMISSION`. The wave reached its valid stop condition: all
defensible prior leads are closed by recorded decisions, no undecided blocked
lead had its objective unblock condition satisfied, and no new local source
provided enough pre-solution evidence to authorize screening. The corpus remains
`PARTIAL`; `COMPARATIVE_CORPUS_READY = NO`; `P1_S1_RELEASE = NO`.

This is an acquisition result, not treatment evidence. No treatment, model,
candidate, solution diff, paid API, or holdout was executed or inspected.

## Baseline and scope

The wave started on `main` at
`13d2742c7b3ea2de0f5accb02089dd4edf2a2b35`. `origin/main` matched, divergence
was `0/0`, and the worktree was clean. The literal command requested by the
wave, `python -B tools/dv_pilot_harness.py`, is not a self-test command in the
current CLI: it exits `2` because a subcommand is required. The authoritative
self-test, `python -B tools/test_dv_pilot_harness.py`, passed `9/9` with exit
`0`. This CLI mismatch was recorded and did not justify a Harness change.

The raw command evidence is in
`pilot-runs/p1-w22-offline-acquisition/command-evidence.txt`; structured
evidence is in the same directory.

## Frozen gates and exclusions

The acquisition gate was applied before any new source selection:

- exact parent and candidate history;
- independent pre-solution verifier and provenance;
- reproducible environment and preservation;
- no solution-derived oracle or gold-solution requirement;
- valid parent product failure before solution inspection;
- deterministic failure attribution and hashable evidence.

`PARENT_FOCAL = PASS` remains a rejection, not a failure. `BLOCKED` remains
distinct from `REJECTED`, `FAIL`, and `NOT_TESTED`.

The 18-candidate inventory, W15 contaminated leads, `SMAG-N1`, `SMAG-N2`, and
`METAO-GATE-N1` were excluded from fresh acquisition. No definitive rejection
was reopened. `METAO-GATE-N1` remains rejected because its parent focal passed
12/12 with exit `0`; its solution diff was not inspected.

Prior evidence hashes were retained for traceability:

| Evidence | SHA-256 |
| --- | --- |
| W18 lead freeze | `38F8328AD4E8FC8CEAC3F5B75294799BE8F99070E8E301BF1A1CD7D634944232` |
| W18 parent result | `D2A0DAEA72B79B9CF51A78A9332CF6206C06C0E823B3A710721BA1323078732C` |
| W19 acquisition decision | `4F9EC7D655D20D962AFB3EA1BFB9185065BF500047D316C83FCEE8ECEBE97E98` |
| W20 opportunity inventory | `D04E7DF627E2E136BEFAA4C983824179A44E3C8C0E7A4CD9FD29BFABE9968FB7` |
| W21 acquisition closure | `5A2F7CCA26E5C04B093455DC69ADC6D698CEBE7840F914C9135EE0A8B3B5A8C4` |

## Blocker recheck

`P1-W1-BLK-002` remains open: the comparative corpus has not changed.
`P1-W4-BLK-STRONG-CREDENTIAL` remains open: `OPENAI_API_KEY` and
`ANTHROPIC_API_KEY` were both absent. `GEMINI_API_KEY` was present, but no
provider qualification or API call was authorized in this wave, so it does not
qualify a strong path.

`P1-W16-SMAG-PRESERVATION-NETWORK` remains observed but non-gating for the
closed SMAG lead. DNS resolved `github.com`, while TCP/443 failed. This does not
change the definitive `NO_PARENT_FAILURE` decision for `SMAG-N1`.

## Source selection and screening

The local source set considered was the existing, evidence-bounded set:
`metao-gate`, `opencode-direct-proof`, `naia`, `bpt2-abp`, `searchleads`, and
`smag`. No new source was selected. `metao-gate` is closed by the W18 parent
pass; `opencode-direct-proof` has no P1 verifier metadata in DV; `naia` and
`bpt2-abp` remain preserved prior leads without a newly satisfied unblock
condition; `searchleads` is represented in the closed 18-candidate inventory;
and SMAG's open network issue is not a new undecided lead.

Accordingly, there were no metadata-only leads, lead freezes, parent
materializations, parent focal commands, candidate materializations, solution
inspections, candidate executions, or preservation executions in W22. This is
the required outcome when the source-selection rationale cannot be satisfied
without reopening a closed decision or violating the solution-inspection gate.

## Corpus and accounting state

The carried admitted tasks remain `D-F2-05`, `D-F5-01`, and `D-F6-01`, across
families `F2`, `F5`, and `F6`, in two repositories. There was no change in task
count, repository count, runtime diversity, verifier diversity, or admission
state. `TASK_CORPUS = PARTIAL` and `COMPARATIVE_CORPUS_READY = NO` remain
unchanged. No resource accounting record was created because no treatment run
occurred; `UNMEASURED` was not converted to zero.

## Validation and side effects

The structured validation records JSON parsing, closed-inventory exclusion,
failure-attribution consistency, holdout sealing, P0 immutability, secret
handling, the Harness self-test, and `git diff --check` as passing. The literal
Harness invocation is recorded as not applicable because its exit `2` is a CLI
usage error, not a failed run.

No source checkout, DV implementation, P0 artifact, holdout, or historical
workspace was modified. No new workspace was created. No credentials or secret
values were persisted.

## Final state

- `W22 = NO_NEW_ADMISSION`
- `TASK_CORPUS = PARTIAL`
- `COMPARATIVE_CORPUS_READY = NO`
- `P1_S1_RELEASE = NO`
- `REAL_P0_RUNS = 0/24`
- `HOLDOUT = SEALED`
- `STRONG_EXECUTION = NOT_TESTED`
- `solution_diffs_opened = 0`
- `candidate_executions = 0`

The nearest unresolved objective gap is a new or previously undecided task with
an independent parent-side verifier, a valid reproducible parent product
failure, and executable preservation evidence. The parallel external gap is an
authorized strong-executor credential, but it must not be used to relax the
corpus gate.

## Evidence index

- `pilot-runs/p1-w22-offline-acquisition/baseline.json`
- `pilot-runs/p1-w22-offline-acquisition/closed-inventory-exclusion.json`
- `pilot-runs/p1-w22-offline-acquisition/blocker-recheck.json`
- `pilot-runs/p1-w22-offline-acquisition/source-selection.json`
- `pilot-runs/p1-w22-offline-acquisition/acquisition-closure.json`
- `pilot-runs/p1-w22-offline-acquisition/validation.json`
- `pilot-runs/p1-w22-offline-acquisition/command-evidence.txt`
