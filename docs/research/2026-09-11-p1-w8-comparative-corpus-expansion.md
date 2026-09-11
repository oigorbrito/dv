# P1-W8 comparative corpus expansion

## Outcome

W8 closes the local verifier-first corpus search without executing treatments,
smoke runs, models, or the sealed holdout.

```text
TASK_CORPUS = PARTIAL
S1_CORPUS_READY = PASS
COMPARATIVE_CORPUS_READY = NO
ADMITTED_TASKS = 2
ADMITTED_FAMILIES = 2
REPOSITORIES = 1
NEW_CANDIDATES = 0
P1_S1_RELEASE = NO
HOLDOUT = SEALED
```

The new corpus version is
`experiments/p1/p1-development-corpus-v3.json`. It retains exactly D-F5-01 and
D-F6-01 from v2. No task was removed, relabeled, or replaced.

## Baseline and search boundary

The wave started at `83f8108684992a02dab89d9fe4501edb91b5c730` with a clean
worktree and equal local `origin/main`. The Harness self-test passed 6/6 with
exit code 0. The previous 18-candidate registry was reviewed before any new
screening.

The local development universe under `C:\Projetos` was enumerated. Existing
P1 source repositories were RJ and SMAG; additional local evidence repositories
included MetaO gate, BPT2, Rag-git, empirical-evaluator-ado, and
opencode-direct-proof. No additional source exposed a pre-frozen P1 task record
with an independently hashable verifier and reproducible baseline contract in
the DV corpus registry.

The search stopped under the W8 repeated-provenance-barrier rule. Continuing
would require either constructing a retrospective verifier, using solution
knowledge, or acquiring external task metadata. None is permitted in this
wave.

## Admitted development tasks

| Task | Family | Repository | Baseline evidence |
|---|---|---|---|
| D-F5-01 | F5 | oigorbrito/metaO | focal 10/10 and preservation 469/469 passed |
| D-F6-01 | F6 | oigorbrito/metaO | focal and preservation passed |

Both tasks have exact historical bases, versioned verifier references and
prior baseline evidence. Their evidence remains tied to the original SHA and
environment; W8 did not rerun them unnecessarily.

## Non-admitted candidates

The existing 18 candidates remain governed by
`pilot-runs/block-5b/task-discovery-screening.json`. D-F1-01 remains excluded
because its frozen MTP/VSTest runner configuration is incompatible. F2/F3/F4
and additional F1/F5/F6 candidates remain rejected or not admitted because
independent verifier provenance, oracle validity, base usability, or solution
independence was not established. D-F4-03 specifically retains its
solution-leakage rejection.

No new candidate was fabricated from a similar test, a solution patch, or a
post-hoc assertion. No candidate was selected based on expected treatment
behavior.

## Diversity and claims

The admitted corpus covers two families, one repository, Python and Rust, and
Python-unittest plus Cargo-workspace verifier types. This is useful pipeline
diversity but remains concentrated and has only one task per family. It does
not support comparative treatment evidence, executor ranking, family
superiority, generalization, or statistical superiority.

The two tasks satisfy the frozen S1 pipeline/smoke preference, but S1 release
remains `NO` because the strong executor credential blocker is unchanged.
The S2 corpus blocker remains open only for comparative work.

## Blockers and limitations

```text
P1-W1-BLK-002 = OPEN_FOR_S2
P1-W4-BLK-STRONG-CREDENTIAL = OPEN
P1-W1-BLK-003 = OPEN_FOR_S1
P1-W1-BLK-004 = CLOSED
P1-W5-D-F1-01 = CLOSED
```

`HOLDOUT_ACCESS=NONE`. P0 artifacts remain unchanged. No model API, treatment,
candidate, smoke spec, or holdout content was accessed.

## Validation and next objective

The W8 evidence set records JSON parsing, duplicate-ID, admitted base and
verifier hash, evidence-path, secret, holdout, and P0 immutability checks. The
Harness self-test passed 6/6, and `git diff --check` passed. The next objective
is a new verifier-first acquisition source with independently versioned
artifacts; otherwise the project may proceed only to smoke mechanics after the
strong executor gate is resolved, without comparative claims.
