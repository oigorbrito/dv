# Master test plan freeze — 2026-09-11

This freeze converts the P0 and P1 findings into one prospective test program.
It creates no treatment evidence and does not change the canonical P0 corpus,
legacy holdout, treatment semantics, pricing, or Harness v1.

The plan is `MASTER_TEST_PLAN_READY`. The current operational state is still
`P1-S0` with no qualified executor path and only one admitted development task.
Therefore `P1_S1_RELEASE = NO`, `REAL_P0_RUNS = 0/24`, and `P0_RELEASE = NO`.

The normative contracts are:

- [master plan](../../experiments/p1/master-test-plan-v1.json)
- [promotion gates](../../experiments/p1/promotion-gates-v1.json)
- [accounting](../../experiments/p1/run-accounting-contract-v1.json)
- [failure attribution](../../experiments/p1/failure-attribution-v1.json)
- [statistical analysis](../../experiments/p1/statistical-analysis-plan-v1.json)
- [holdout policy](../../experiments/p1/p1-holdout-policy-v1.json)
- [architecture gate](../../experiments/p1/architecture-decision-gate-v1.json)
- [run-spec template](../../experiments/p1/run-spec-v1.template.json)
- [run-result schema](../../experiments/p1/run-result-v1.schema.json)

The next defensible action is to expand the verifier-first development corpus and
qualify strong plus economic/local/free executor paths. No smoke run is released
until those gates pass. The legacy holdout remains sealed.
