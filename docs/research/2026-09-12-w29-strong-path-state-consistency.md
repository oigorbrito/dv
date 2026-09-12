# W29 — Strong-path state consistency

## Decision

The canonical state is `C1_GOOGLE_GEMINI_QUALIFIED=YES` and
`STRONG_PATH_READY=PASS`. The later qualification artifact `v9` supersedes the
prospective amendment's pre-probe state. No later canonical artifact revokes
that qualification.

The conflicting `NO` is stale pre-qualification state or a credential-presence
confusion. It is not supported as a current canonical qualification decision.
The qualification gate requires credential/quota state for the qualification
probe; `promotion-gates-v1` does not define absence of a credential at a later
read as an automatic demotion. Qualification therefore persists as historical
evidence, while runtime credential availability remains a separate operational
condition.

## Evidence and precedence

The amendment in commit `aa975df4e3d7fc3615d11883bbfe54b057fa88f2` records
Gemini as eligible but not yet qualified. The qualification in commit
`e218cb675eb760dc4a83ea475eec331d331ed71e` records the exact candidate,
provider, requested and observed model, exact probe response, zero application
retries, and `S0_READY_TELEMETRY_LIMITED`. Its gate state explicitly records
`C1_GOOGLE_GEMINI_QUALIFIED=YES` and `STRONG_PATH_READY=PASS`.

The qualification JSON and promotion gate independently agree. Later smoke
and remediation evidence also preserves `STRONG_PATH_READY=PASS`; their `NO`
states concern smoke completion or operational rerun conditions, not C1
qualification. Full hashes and the machine-readable decision are preserved in
`pilot-runs/p1-w29-state-consistency/decision.json`.

## Disqualification search

No post-qualification evidence was found for a model identity mismatch,
provider contract violation, corrupted qualification artifact, revoked
amendment, failed mandatory qualification criterion, or explicit gate demotion.
The four prior smoke attempts remain immutable blocked/inconclusive evidence.

## Reconciled gates

The neutral newline remediation established parent verifier reproduction,
candidate capture, candidate application, HTTP-error telemetry, and a local
fixture-only pipeline. Therefore `SMOKE_RERUN_READY` is operationally ready
for a separately authorized future wave with new run IDs. This wave does not
rerun the four previous attempts.

`P1_S1_COMPLETE` remains `NO`, `P1_S2_RELEASE` remains `NO`, and no treatment
or smoke execution occurred. `REAL_P0_RUNS` remains `0/24`, `P0_RELEASE` remains
`NO`, and `HOLDOUT` remains `SEALED`.

## Scope and limitations

This is a state-consistency and traceability decision, not new scientific
evidence. It makes no claim about treatment quality, comparative performance,
cost, or task success. No API call, treatment, candidate, or holdout access
occurred.
