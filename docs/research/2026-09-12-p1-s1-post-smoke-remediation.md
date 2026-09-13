# P1-S1 — Remediação pós-smoke

Esta onda não repetiu os quatro smoke runs e não fez chamada Gemini. Ela tratou
somente os blockers concretamente observados no primeiro smoke.

## Mudanças estreitas

- O executor aceita apenas o contrato já declarado de `candidate.diff`: diff
  unificado bruto ou em fence `diff`/`patch`; saída livre é rejeitada.
- O Harness aplica deterministicamente esse diff com `git apply`; não há
  reparo manual nem transformação por outro modelo.
- A materialização cria `.git` isolado, aponta seu object database para um
  alternate somente leitura do checkout-fonte e inicializa HEAD/index com Git.
- Erros HTTP preservam status, razão, corpo de erro, headers não sensíveis,
  request-id quando exposto e hash do artefato, sem retries.

## Readiness

Captura e aplicação de candidato passaram em fixtures. O dry run local
end-to-end passou. O controle do parent no cwd correto continua falhando por
newline Windows (`DIRTY\\r\\n` contra `DIRTY\\n`), portanto a reprodução do
oracle histórico ainda não está pronta e `SMOKE_RERUN_READY=NO`.

O custo monetário continua `UNMEASURED`, mas não é blocker do smoke enquanto o
accounting canônico representar essa ausência explicitamente. Não houve
alteração de tratamento, shaping, oracle, holdout ou dos quatro resultados
anteriores.
