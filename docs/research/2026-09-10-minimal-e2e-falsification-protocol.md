# dv — Protocolo mínimo E2E de falsificação

Status: RESEARCH PROTOCOL — NÃO IMPLEMENTAR ARQUITETURA AINDA
Data: 2026-09-10

## 1. Pergunta de pesquisa

O `dv` precisa de uma camada própria de decisão/composição para reduzir custo total por tarefa verificadamente resolvida, ou uma combinação de baselines simples e componentes existentes já é suficiente?

Hipótese nula operacional:

> H0: nenhuma nova camada `dv` é necessária; baselines simples e composição existente atingem desempenho equivalente ou melhor com menor custo/complexidade.

Uma nova responsabilidade só pode ser aceita se H0 for rejeitada por evidência reproduzível.

## 2. Métrica primária

`total system tokens / verified solved task`

O numerador deve incluir, quando aplicável: classificação, seleção/routing, planning/task shaping, retrieval/context, schemas/tools expostos, handoff/bootstrap, execução, retries, replanning/expansion, verificação e coordenação.

Economia local no executor não conta se o custo total aumentar.

## 3. Métricas secundárias obrigatórias

- verified task success;
- monetary cost / verified solved task;
- latency / verified solved task;
- number of model calls;
- retries e escalations;
- verifier calls;
- handoff/context bytes e tokens;
- tool/schema tokens expostos;
- selected tier/provider;
- failure class;
- coordination overhead;
- maintenance/update cost quando mensurável.

## 4. Baselines/policies

### B0 — Strong direct
Executor forte desde o início, sem router inteligente.

### B1 — Cheap/free direct + verify
Executor barato/free desde o início; sucesso só conta após verificação.

### B2 — Cheap-first cascade
Executor barato primeiro; em falha, escalar para forte.

Variantes:
- B2a: full-trajectory handoff;
- B2b: clean handoff com estado externo + TaskSpec mínimo + falhas observáveis + artifact refs.

### B3 — Static family policy
Tabela estática por família de tarefa, aprendida apenas em treino.

### B4 — Family × risk/difficulty policy
Tabela simples por família e pequeno conjunto de sinais observáveis previamente definidos.

### B5 — Minimal exploration policy
Pequena exploração barata para colher sinais; depois continuar ou escalar.

### B6 — Learned/LLM router
Somente como braço posterior. Deve pagar integralmente o custo de classificação/routing.

## 5. Controles obrigatórios

### Holdout real
Separar treino/tuning de teste antes de avaliar B3–B6. Resultado in-sample não promove arquitetura.

### Fixed-tier baselines
Sempre incluir políticas de tier fixo para verificar se o ganho do router não é apenas consequência da proporção de modelos fortes escolhidos.

### Mesmo harness e mesmo verifier
Dentro de cada comparação, manter constantes versão do harness, ferramentas, ambiente, orçamento, timeout, verifier/oracle e dataset quando possível.

### Revision binding
Cada resultado deve ser ligado a task/dataset revision, provider/model revision, harness revision, verifier revision, environment/runtime revision e policy revision.

## 6. Corpus mínimo

O primeiro experimento deve conter mais de uma família de tarefa. Candidatas:

1. alteração de código pequena/local;
2. correção de bug com testes existentes;
3. mudança multi-arquivo;
4. documentação/transformação textual verificável;
5. tarefa de ferramenta/automação com saída estruturada;
6. tarefa com efeito externo simulável/sandboxed;
7. tarefa sem verifier determinístico completo.

Cada família precisa de instâncias suficientes para comparação útil e holdout independente.

## 7. Verificação

Preferir o certificado suficiente mais barato por família:

`schema/type/hash -> lint/build -> tests -> sandbox execution -> specialized verifier -> cheap LLM verifier -> strong LLM verifier -> human`

Não pagar por verifier mais caro quando um oracle determinístico já basta.

Resultado só conta como `verified solved` quando o oracle previamente declarado aceita.

## 8. Handoff como variável experimental

Não assumir que trajetória completa ajuda o próximo executor.

Medir separadamente:
- full trajectory;
- compacted trajectory;
- trajectory removal preservando workspace/state;
- minimal TaskSpec + refs + observed failures.

Objetivo conceitual:

`min |handoff| subject to verified-success >= threshold`

## 9. Critério de promoção

Nenhum B3–B6 pode justificar nova responsabilidade apenas por apresentar menor custo médio.

Para promoção deve demonstrar, em holdout:

1. verified success não inferior ao baseline de referência dentro de margem pré-declarada, ou superioridade explícita;
2. redução de `total system tokens / verified solved task` ou outra métrica primária pré-declarada;
3. ganho maior que seu próprio custo de decisão/coordenação;
4. resultado reproduzível em mais de uma família;
5. ausência de degradação inaceitável em falhas críticas;
6. complexidade de software proporcional ao ganho;
7. substituibilidade/remoção sem reconstrução global.

Se os dados forem insuficientes: `INCONCLUSIVE`.

## 10. Critérios de eliminação

Eliminar ou não promover quando:
- fixed-tier simples empata ou vence;
- ganho desaparece no holdout;
- routing/planning consome a economia;
- handoff aumenta custo sem recuperar qualidade;
- melhora existe apenas em uma família estreita e não justifica generalização;
- verificação torna a política mais cara que strong-direct;
- manutenção/drift exige rebenchmarking frequente demais;
- a propriedade já é coberta por composição simples de standards/providers existentes.

## 11. Resultados possíveis

### A — Brain eliminado
Standards/providers + regras simples já entregam melhor fronteira custo/qualidade.

### B — Micro-policy justificada
B3/B4/B5 superam baselines com ganho reproduzível e baixo overhead.

### C — Router inteligente justificado
B6 supera policies simples no holdout depois de pagar custo de decisão/manutenção.

### D — INCONCLUSIVE
Diferenças pequenas, instáveis ou corpus insuficiente. Não promover arquitetura.

## 12. Regra normativa

Nenhuma conclusão deste protocolo substitui a regra permanente do projeto:

> toda decisão arquitetural deve ser defensável sob princípios de engenharia de software e sustentada por validação empírica adequada à alegação.

`DOCUMENTED != EXECUTED != MEASURED != ACCEPTED`.

O resultado preferível continua sendo eliminar responsabilidades antes de construir software novo.
