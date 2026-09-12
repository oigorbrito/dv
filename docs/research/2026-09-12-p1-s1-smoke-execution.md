# P1-S1 — Execução dos quatro smoke runs

## Escopo

Esta onda executou, uma única vez e na ordem congelada, os quatro specs de
`D-F2-06`: B0/S0, B0/S1, B4/S0 e B4/S1. Não houve P0, P1-S2, holdout ou
comparação de tratamentos. A chave Gemini foi lida somente do ambiente e não
foi registrada.

## Resultado observado

| Run | Executor | Verifier | Reconciliation | Classificação |
|---|---:|---:|---:|---|
| B0/S0 | HTTPError, exit 75 | exit 1 | FAIL | INCONCLUSIVE / PROVIDER_FAILURE + HARNESS_FAILURE |
| B0/S1 | HTTP 200, 1279 tokens | exit 1 | FAIL | INCONCLUSIVE / HARNESS_FAILURE |
| B4/S0 | HTTP 200, 1237 tokens | exit 1 | FAIL | INCONCLUSIVE / HARNESS_FAILURE |
| B4/S1 | HTTPError, exit 75 | exit 1 | FAIL | INCONCLUSIVE / PROVIDER_FAILURE + HARNESS_FAILURE |

Nos dois runs HTTP 200, o modelo observado foi `gemini-3.8-flash`; foram
preservados input/output/total/reasoning tokens e os hashes dos artefatos
brutos. Request-id e custo monetário não foram expostos pelo binding e ficaram
não medidos. Runs com HTTPError não tiveram corpo de resposta persistido.

## Falhas de pipeline

O verifier falhou no ambiente Windows por diferença `DIRTY\\r\\n` versus
`DIRTY\\n`. A reconciliação também detectou que a materialização por blobs não
contém um repositório Git independente: o `git rev-parse` resolveu o checkout
DV pai, não o SHA histórico declarado. Por isso não há resultado de produto e
nenhum candidato foi aplicado ou reparado manualmente.

## Gates

`P1_S1_SMOKE_EXECUTION=BLOCKED`, `P1_S1_COMPLETE=NO`,
`STRONG_PATH_READY=PASS`, `TASK_CORPUS=PARTIAL`,
`COMPARATIVE_CORPUS_READY=NO`, `P1_S2_RELEASE=NO`.

`REAL_P0_RUNS` permanece `0/24`, `P0_RELEASE=NO` e `HOLDOUT=SEALED`.
O próximo passo é uma onda separada de remediação do Harness/materialização,
com captura de status HTTP/request-id, aplicação de candidato e workspace Git
isolado, antes de qualquer repetição autorizada.

## Evidência

Raw evidence permanece em `pilot-runs/p1-s1-smoke/`, incluindo os quatro
`run.json`, logs, reconciliações, eventos e manifests de materialização.
