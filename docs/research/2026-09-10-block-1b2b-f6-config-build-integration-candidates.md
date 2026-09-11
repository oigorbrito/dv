# Block 1B.2b — F6 configuration/build/integration holdout candidates

Date: 2026-09-10
Status: PARTIAL FREEZE / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F6 (configuration/build/dependency/repository integration). It does not open Block 2.

Selection must be defensible from pre-solution task information. Gold patches, changed-file counts, hidden tests, and post-solution structure are not admissible classification signals.

## F6 admissibility rule

A task qualifies for F6 only when the public problem statement itself is primarily about one or more of:

- installation or packaging behavior;
- dependency declaration/resolution;
- build configuration;
- CI/runtime-environment integration;
- repository/package discovery caused by configuration;
- command/entry-point packaging.

Mentions of setup.py, CI, Docker, or installation that only describe the benchmark harness or reproduction environment do not qualify.

## Frozen candidates

### F6-01 — django__django-12009

- repository: `django/django`
- base commit: `82a88d2f48e13ef5d472741d5ed1c183230cfe4c`
- source: SWE-bench
- split: test
- classification: F6 packaging/installation
- pre-solution rationale: the problem is explicitly about Django installing two command entry points (`django-admin` and `django-admin.py`) through both `scripts` and `entry_points` in `setup.py`, and asks that only one be installed.
- freeze status: FINAL_FROZEN

### F6-02 — pytest-dev__pytest-9681

- repository: `pytest-dev/pytest`
- base commit: `fc72ffa39ed3b34b21fba83d6f80144ab0ae8a36`
- source: SWE-bench
- split: test
- classification: F6 configuration/package-discovery integration
- pre-solution rationale: the problem provides a minimal repository layout and `setup.cfg` where `pythonpath = .` plus `--import-mode importlib` interacts with `conftest.py` and breaks package discovery. The defect is configuration/repository integration rather than an isolated function bug.
- freeze status: FINAL_FROZEN

## Rejected / excluded during this block

### pylint-dev__astroid-1030

The public issue is an excellent F6 dependency-declaration task: Astroid uses setuptools but does not declare it in `setup.cfg`. However, the canonical task metadata marks it as `split: dev`, so it is excluded from this sealed holdout.

### solution-discovered candidates

At least one potential packaging/dependency candidate surfaced first through a `gold.patch` code-search result. It is excluded from this round because discovery via solution material creates avoidable selection leakage. It may not be reused for the sealed holdout unless independently rediscovered under a predeclared solution-blind procedure in a future corpus revision.

## F6 status

- required: 3
- FINAL_FROZEN: 2
- remaining: 1
- blocker: need one additional test-split task whose problem statement independently establishes F6 membership without solution-derived discovery

## Current corpus status

- F1: 3/3
- F2: 3/3
- F3: 3/3
- F4: 3/3
- F5: 3/3
- F6: 2/3
- external sealed holdout: 17/18

Block 1B remains incomplete. Do not open Block 2 until F6 reaches 3/3 and the 18-instance holdout is frozen.
