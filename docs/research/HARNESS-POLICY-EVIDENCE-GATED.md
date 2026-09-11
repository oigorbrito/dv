# Harness policy: evidence-gated methodology and documentation

## Purpose

The harness accepts a methodological or documentary suggestion only when the
suggestion is necessary to obtain, interpret, reproduce, measure, or attribute
experimental evidence. This policy limits changes to the smallest sufficient
scope and prevents documentation or architecture work from being recommended by
preference.

The policy is implemented by `tools/dv_pilot_harness.py policy-check` and the
`validate_suggestion` function. The harness has no recommendation generator;
the guard validates a suggestion supplied by a caller.

## Acceptance gate

A suggestion is `ACCEPTED` only when all conditions hold:

1. `proposed_change` is explicit.
2. `experimental_problem_addressed` identifies a concrete validity,
   reproducibility, measurement, attribution, oracle, or traceability problem.
3. `evidence_class` contains only supported classes.
4. `necessity` is `true`.
5. `existing_artifact_sufficient` is `false`.
6. `smallest_sufficient_change` is explicit.
7. `consequence_if_not_done` explains the impact on evidence.

Supported evidence classes are:

- `EMPIRICAL_RESEARCH_GUIDANCE`;
- `EXPERIMENTAL_DESIGN`;
- `REPRODUCIBILITY`;
- `MEASUREMENT`;
- `ORACLE_VALIDITY`;
- `FAILURE_ATTRIBUTION`;
- `TRACEABILITY`.

Otherwise the result is `REJECTED_UNSUPPORTED`. Rejection does not claim that
the proposed change is technically bad; it means that the supplied evidence
does not justify recommending it for this experiment.

## Documentation rule

Documentation is justified only when it preserves a frozen protocol, exact
inputs or versions, executed commands, raw or hashed evidence, environment
requirements, material validity threats, thresholds actually used, protocol
deviations, or failure attribution needed for reproduction or interpretation.
Existing canonical evidence is reused when it already satisfies the need.

The harness must not recommend documentation merely because it is cleaner,
more complete, more professional, or common in industry. It must not infer
`DOCUMENTED` from `CODE_CONFIRMED`, `EXECUTED`, `MEASURED`, or `ACCEPTED`.

## Operational validation

Run the guard with a JSON suggestion:

```powershell
python -B tools/dv_pilot_harness.py policy-check --suggestion suggestion.json
```

The command returns exit code `0` for `ACCEPTED` and exit code `2` for
`REJECTED_UNSUPPORTED`. It emits only the decision, supported evidence classes,
identified problem, smallest change, and validation errors; it does not emit or
persist secrets.

The policy does not change treatment semantics, run accounting, verifier
semantics, provider bindings, holdout state, or the measurement harness.
