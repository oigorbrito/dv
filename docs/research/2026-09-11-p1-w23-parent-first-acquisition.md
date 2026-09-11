# P1-W23 — Acquisition search with parent-failure prequalification

## Closure decision

`W23 = NO_NEW_ADMISSION`. The wave reached stop condition C/D: every
defensible parent-first opportunity available in the existing inventory is
closed, blocked, or lacks sufficient pre-solution evidence. No lead reached the
parent-failure qualification gate, so no solution diff was authorized or
inspected.

This wave produced no treatment evidence. No model, treatment, paid API,
candidate execution, or holdout access occurred.

## Baseline

The local baseline was:

- branch: `main`;
- `HEAD`: `149471703eab0476b506fa755abe74ebceb67f5f`;
- `origin/main`: `13d2742c7b3ea2de0f5accb02089dd4edf2a2b35`;
- divergence: `LOCAL_ONLY=1`, `REMOTE_ONLY=0`;
- worktree: clean;
- holdout: sealed.

The literal bare Harness invocation exited `2` because the current CLI requires
a subcommand. Per the W23 contract, this is `NOT_APPLICABLE`, not a Harness
failure. The supported self-test passed `9/9` with exit `0`; `git diff --check`
passed.

## Remote publication

W22 remained one local commit ahead. The remote-publication recheck was not
repeated: no new authorization was available in this session. The state remains
`BLOCKED_USER_AUTHORIZATION`. No force push, rebase, reset, or pull was used.

## Closed inventory and blockers

The 18-candidate historical inventory and definitive W15-W21 decisions were
excluded from fresh acquisition. `METAO-GATE-N1` was not reopened because its
parent focal already passed `12/12` with exit `0`, yielding `NO_PARENT_FAILURE`.
SMAG-N1/N2 and all other definitive rejections remain closed.

The blocker register is unchanged:

- `P1-W1-BLK-002`: comparative corpus insufficient;
- `P1-W4-BLK-STRONG-CREDENTIAL`: authorized C1 credential absent;
- `P1-W16-SMAG-PRESERVATION-NETWORK`: external preservation dependency,
  non-gating for the definitively rejected SMAG lead;
- W22 remote publication: local commit not published because authorization was
  unavailable.

No previously blocked undecided candidate had a newly satisfied unblock
condition. The objective source-search gap remains an independent parent-side
verifier, a reproducible parent product failure, and executable preservation.

## Parent-first source prequalification

The bounded source review considered `metao-gate`,
`opencode-direct-proof`, `naia`, `bpt2-abp`, `searchleads`, and `smag`. No
source was promoted to deeper screening. The decisions were:

| Source | Decision | Evidence-bound reason |
| --- | --- | --- |
| `metao-gate` | `REJECT_SOURCE` | Existing lead has parent PASS, not a product failure |
| `opencode-direct-proof` | `REJECT_SOURCE` | No P1 verifier metadata in DV |
| `naia` | `REJECT_SOURCE` | Preserved closed lead; no undecided lead available |
| `bpt2-abp` | `BLOCKED_SOURCE` | Prior restore and network dependency remain unresolved |
| `searchleads` | `REJECT_SOURCE` | Already represented in the closed inventory |
| `smag` | `BLOCKED_SOURCE` | No undecided lead; closed preservation depends on network |

This is a parent-first decision, not a repository-quality judgment. No source
was selected merely for diversity or because it contained an interesting fix.

## Lead and parent results

There were no new metadata-only opportunities, lead freezes, parent
materializations, parent focal executions, repeatability checks, or immutable
pre-solution freezes. The only carried lead reviewed for the gate was
`METAO-GATE-N1`:

- parent: `2572ddcc1ca4c0aa78abc095fdc35bccc6e15a05`;
- prospective candidate: `2f730773d073a5c4c5bd05b7ae4c0a4f2481a533`;
- parent focal: `PASS`, `12/12`, exit `0`;
- classification: `NO_PARENT_FAILURE`;
- disposition: `REJECTED`;
- solution diff: `NOT_INSPECTED`;
- candidate execution: `NOT_TESTED`.

Because the parent passed, the lead could not satisfy the W23 objective. No
candidate was rejected due to a solution-derived interpretation, and no lead
was incorrectly classified as `PRODUCT_FAILURE`.

## Corpus state and reproducibility

Admitted tasks remain `D-F2-05`, `D-F5-01`, and `D-F6-01`, across families
`F2`, `F5`, and `F6`, in two repositories. Counts are unchanged: `3` tasks
and `2` repositories before and after W23. Runtime and verifier diversity are
unchanged. `TASK_CORPUS = PARTIAL` and `COMPARATIVE_CORPUS_READY = NO` remain
in force.

The structured evidence in
`pilot-runs/p1-w23-parent-first-acquisition/` records the baseline, source
prequalification, lead gate, closure, and validation. Since no actual parent or
candidate execution occurred in W23, no new task hash, verifier hash, lockfile
hash, duration, or resource accounting record was generated.

## Validation and side effects

JSON parsing, parent-failure gate consistency, closed-inventory exclusion,
solution-leakage scan, evidence-path validation, holdout scan, P0 immutability,
secret scan, Harness self-test, and `git diff --check` passed. No source
checkout was modified. No workspace, candidate, solution, treatment, model, or
holdout artifact was created or changed.

## Final state

- `W23 = NO_NEW_ADMISSION`;
- `candidates admitted = 0`;
- `parent-failure-qualified leads = 0`;
- `solution diffs inspected = 0`;
- `candidate executions = 0`;
- `TASK_CORPUS = PARTIAL`;
- `COMPARATIVE_CORPUS_READY = NO`;
- `P1_S1_RELEASE = NO`;
- `REAL_P0_RUNS = 0/24`;
- `HOLDOUT = SEALED`.

The next defensible objective is a new or genuinely undecided lead whose parent
contains a pre-existing independent verifier and can demonstrate a reproducible
task-relevant failure with local or bounded reproducible preservation. The
strong-executor credential remains a separate external blocker.

## Evidence index

- `pilot-runs/p1-w23-parent-first-acquisition/baseline.json`;
- `pilot-runs/p1-w23-parent-first-acquisition/source-prequalification.json`;
- `pilot-runs/p1-w23-parent-first-acquisition/lead-prequalification.json`;
- `pilot-runs/p1-w23-parent-first-acquisition/acquisition-closure.json`;
- `pilot-runs/p1-w23-parent-first-acquisition/validation.json`.
