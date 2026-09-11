# dv — Desenho do primeiro experimento empírico

Status: EXPERIMENT DESIGN — NÃO É IMPLEMENTAÇÃO DE ARQUITETURA
Data: 2026-09-10

## 1. Objetivo

Executar a primeira comparação capaz de falsificar a necessidade de uma camada própria de decisão/composição no `dv`.

O experimento não tenta provar que uma arquitetura é universalmente melhor. Ele testa se políticas simples conseguem atingir a mesma ou melhor fronteira entre sucesso verificado e custo total em um escopo declarado.

## 2. Pergunta principal

Entre políticas de execução forte, execução barata, cascata e routing simples, qual minimiza:

`total system tokens / verified solved task`

sem degradação inaceitável de `verified task success`?

## 3. Fases

### Fase P — Pilot

Finalidades:
- validar instrumentação;
- descobrir variância;
- estimar taxas de sucesso;
- detectar tarefas impossíveis ou oracles defeituosos;
- estimar custo/tokens por braço;
- calibrar o tamanho da execução confirmatória.

Resultados do pilot NÃO promovem arquitetura.

### Fase C — Confirmatory

Antes de executar:
- congelar corpus/holdout;
- congelar arms/policies;
- congelar métricas primárias;
- congelar margem de não-inferioridade ou hipótese de superioridade;
- congelar regra de exclusão de runs;
- congelar verifier/oracle;
- registrar revisions de providers/harness/environment/policy.

Depois do congelamento, não ajustar policy no holdout.

## 4. Braços mínimos da primeira rodada

Para manter o experimento barato, começar com quatro braços:

- E0: strong-direct;
- E1: cheap/free-direct + verify;
- E2: cheap-first -> clean escalation -> strong;
- E3: static task-family policy.

Não incluir ainda learned/LLM router. Ele só entra se E3 não explicar suficientemente a fronteira observada e houver razão empírica para acreditar que inteligência adicional paga seu custo.

## 5. Corpus inicial

Usar tarefas que permitam oracle forte e execução repetível.

Prioridade inicial:

1. small/local code edits com testes determinísticos;
2. bug fixes com testes existentes;
3. multi-file code changes com acceptance pré-definida;
4. transformações/documentação com oracle estrutural ou golden output quando defensável;
5. tool/automation tasks com schema/end-state verificável.

Evitar na primeira rodada tarefas cuja avaliação dependa principalmente de LLM-as-a-Judge, para não misturar custo/instabilidade do executor com custo/instabilidade do verifier.

## 6. Train vs holdout

E3 pode usar somente dados de treino/pilot para decidir qual tier/provider usar por família.

O conjunto confirmatório deve permanecer oculto à policy até a execução.

A mesma tarefa não pode aparecer em treino e holdout por reformulação trivial.

Quando possível, separar por origem/repositório/problema, não apenas por prompt, para reduzir leakage.

## 7. Repetições e estocasticidade

Não assumir que uma única execução representa confiabilidade.

Para braços não determinísticos:
- executar rollouts independentes;
- preservar seed/configuração quando houver suporte;
- calcular sucesso por tarefa e consistência entre rollouts;
- não confundir número de testes unitários com número de tentativas independentes.

O número final de repetições não deve ser inventado antecipadamente. O pilot deve informar variância e permitir definir a execução confirmatória por precisão/intervalo de confiança/poder estatístico compatível com o efeito mínimo de interesse.

## 8. Oracle e evidência

Cada tarefa deve possuir acceptance criteria declarados antes da execução.

Preferência:

`deterministic oracle > specialized executable verifier > LLM judge`

Para código, quando aplicável:
- build/typecheck;
- testes relevantes;
- testes ocultos/independentes quando disponíveis;
- invariantes de workspace;
- análise de efeitos colaterais;
- security checks somente quando fazem parte da alegação.

Não aceitar a mensagem final do agente como prova de sucesso.

## 9. Handoff de E2

Na primeira rodada usar clean escalation como baseline principal:

- preservar workspace/state válido;
- entregar TaskSpec curto;
- entregar falhas observáveis relevantes;
- entregar refs para artifacts;
- não retransmitir raciocínio completo do executor barato.

Full-trajectory handoff pode existir como ablação separada, não como default.

## 10. Medição por run

Registrar ao menos:

- experiment_id;
- task_id e task_family;
- arm/policy revision;
- provider/model/executor revision;
- harness revision;
- verifier revision;
- environment revision;
- input tokens;
- output tokens;
- cached tokens quando reportados;
- classification/routing tokens;
- context/schema/tool tokens quando mensuráveis;
- handoff tokens;
- verifier tokens;
- total tokens;
- monetary cost;
- latency;
- model/tool calls;
- retries;
- escalation flag;
- final verifier result;
- failure class;
- raw artifact/evidence refs.

## 11. Métricas derivadas

Primárias:
- verified success rate;
- total tokens / verified solved task.

Secundárias:
- monetary cost / verified solved task;
- latency / verified solved task;
- reliability/consistency across independent rollouts;
- escalation rate;
- failed-cheap waste before escalation;
- routing overhead;
- verifier overhead;
- coordination overhead;
- provider utilization distribution.

## 12. Comparações críticas

### E0 vs E1
Responde se o executor barato sozinho já é economicamente competitivo.

### E0 vs E2
Responde se cheap-first + escalation economiza ou apenas paga duas vezes.

### E0 vs E3
Responde se uma tabela simples consegue evitar tanto overkill quanto failed-cheap waste.

### E2 vs E3
Responde se routing prévio simples é melhor que descobrir dificuldade por falha.

## 13. Controles contra conclusões falsas

- comparar sempre contra strong-direct;
- reportar distribuição de tiers escolhidos;
- manter custos do router/policy no numerador;
- não remover failures da análise salvo regra congelada de infrastructure failure;
- preservar timeouts/rate limits/provider errors como classes distintas;
- reportar tarefas sem solução e oracle defects separadamente;
- não promover ganho observado apenas em treino;
- não escolher somente tarefas favoráveis ao cheap tier;
- não confundir pass parcial com verified solved;
- não usar média de custo sem considerar failures.

## 14. Critério estatístico

O confirmatory run deve declarar antes da execução se a afirmação é:

- superioridade;
- não-inferioridade de sucesso com superioridade de custo;
- ou análise exploratória sem claim de promoção.

Para a hipótese economicamente mais interessante, preferir:

> sucesso verificado não inferior dentro de margem defensável + custo/tokens significativamente menor.

A margem deve ser justificada pelo domínio/risco e não escolhida depois de ver os resultados.

Reportar intervalos de confiança e efeito absoluto, não apenas p-value.

## 15. Safety/irreversibility

A primeira rodada deve usar ambientes isolados, reversíveis ou simulados.

Não usar minimum-first/cheap-first em efeitos externos irreversíveis sem sandbox, dry-run, transaction/compensation ou approval gate adequado.

## 16. Critério de decisão após a primeira rodada

### Se E0 vencer ou empatar economicamente
A hipótese de policy adicional enfraquece. Não construir.

### Se E1 vencer
Talvez nem routing seja necessário para aquele escopo. Não generalizar além das famílias testadas.

### Se E2 vencer
Cheap-first + verify/escalation pode bastar; testar robustez e handoff antes de qualquer router.

### Se E3 vencer
Justifica investigar uma micro-policy/configuração tabular, ainda sem Brain ou learned router.

### Se diferenças forem instáveis
`INCONCLUSIVE`; aumentar evidência, não complexidade.

## 17. Próximo passo permitido

Após este desenho, o próximo artefato permitido é somente a especificação do corpus, measurement envelope e harness de experimento.

Nenhuma implementação de Brain, router ou nova Execution IR está autorizada por este documento.

## 18. Regra fixa

Toda conclusão continua sujeita a:

> engenharia de software defensável + validação empírica adequada à alegação.

O experimento deve poder concluir legitimamente que o melhor resultado é não construir nada novo.
