# Capability coverage matrix — DV / MetaO / SMAG

Data: 2026-09-10

Status: **pesquisa / composição / falsificação. Nenhuma nova arquitetura aprovada.**

Objetivo deste documento: registrar, em uma única matriz, quais capacidades já existem, quais podem ser supridas por MetaO/SMAG/standards externos, quais lacunas permanecem e o que eventualmente precisaria ser adicionado — sempre sob a regra de não reimplementar capacidades já existentes sem evidência de insuficiência.

## 1. Legenda

- `TEMOS` — já existe implementação/prior art suficiente para compor/testar.
- `PARCIAL` — existe parte relevante, mas falta validar integração, neutralidade ou economia ponta a ponta.
- `FALTA PROVAR` — não é uma autorização para implementar; é uma hipótese empírica ainda aberta.
- `NÃO ADICIONAR` — capacidade já suficientemente coberta externamente; nova implementação seria duplicação até prova em contrário.

## 2. Matriz consolidada

| Capacidade / função | Estado no DV | Fonte/candidato atual | Função suprida por MetaO | Função suprida por SMAG | O que falta | Ação defensável agora |
|---|---|---|---|---|---|---|
| Contrato neutro de executor/orquestrador | TEMOS | MetaO `OrchestratorContract`, A2A | contrato framework-neutral; adapters fora do Core | executor é tratado como componente substituível | provar que A2A/contrato comum atende todos os executores-alvo sem tradução excessiva | adaptar/testar; **não criar novo contrato** |
| Capability/tool interoperability | TEMOS | MCP | não precisa ser responsabilidade central do MetaO | pode consumir integrações do executor | validar custo e limites em workflows reais | usar MCP; **não criar protocolo próprio** |
| Agent interoperability | TEMOS | A2A | runtimes/orquestradores podem ficar atrás de boundary substituível | executores/agentes podem ser tratados como alvos externos | validar adapters mínimos e failure semantics | usar A2A/adapters; **não criar transporte próprio** |
| Workflow / Execution IR | PARCIAL FORTE | Open Workflow + workflows existentes | MetaO não precisa possuir IR universal | SMAG possui task/mission path próprio, mas não deve virar standard do DV | testar se Open Workflow representa os casos necessários sem inflar payload/contexto | testar standard existente antes de qualquer schema novo |
| Strategy / selection | TEMOS PARCIAL | MetaO | já possui `Mission -> Strategy / Selection` e runtime selection | possui seleção automática ou explícita de executor | medir se seleção existente é economicamente vantajosa para a política DV | reutilizar como candidato; não duplicar |
| Policy / governance | TEMOS | MetaO + SMAG | policy, budget, approval, quarantine, retry e acceptance permanecem metaO-owned | policy profiles, deny-before-promote, approvals e proteção de boundaries | decidir qual autoridade governa qual boundary para evitar dupla governança | definir precedência/ownership em composição; **não duplicar gates** |
| Budget | TEMOS | MetaO | governance budget implementado | possui policy/budget/risk no pre-execution flow | medir custo total e evitar dois budget layers concorrentes | escolher uma autoridade por execução |
| Approval | TEMOS | MetaO + SMAG | approval é responsabilidade do control plane | `PENDING_APPROVAL`, approval-before-promote e perfis destrutivos | eliminar sobreposição e definir quem é autoridade final | composition rule, não novo módulo |
| Runtime admission / health | TEMOS | MetaO | admission, health, certification e revocation implementados | `agents`/`doctor` detectam readiness local de executores | mapear `READY` do SMAG para health/admission sem promover readiness a availability | adapter + semântica explícita |
| Runtime certification / revocation | TEMOS | MetaO | certificação, freshness e revogação | SMAG não precisa replicar esta função global | provar valor quando executores são locais/efêmeros | reutilizar MetaO onde aplicável |
| Durable mission/task state | TEMOS | MetaO + runtimes duráveis externos | mission store/durable state, recovery/fencing | durable missions e resume path existem | impedir dupla persistência e definir SSOT do estado | escolher store/runtime autoritativo por composição |
| Recovery / fencing / stale worker rejection | TEMOS | MetaO / durable runtimes | fencing, restart, recovery e stale-owner rejection | supervisor possui lifecycle/failure handling no escopo de coding | validar fronteira entre runtime recovery e coding-session supervision | compor; não reimplementar |
| Executor supervision | TEMOS | SMAG | MetaO supervisiona no nível de orquestrador/runtime | supervisor controla startup, readiness, streams, exit e completion evaluation | testar generalização além de Windows + OpenCode | usar SMAG como provider de supervised coding execution |
| Isolated staging | TEMOS | SMAG | não é função central necessária ao MetaO | executa mudanças em staging antes da promoção | validar comportamento com executores adicionais | herdar do SMAG para coding/filesystem mutation |
| Independent audit / acceptance | TEMOS, COM SOBREPOSIÇÃO | MetaO + SMAG | acceptance separada de `ORCHESTRATOR_DONE`, replay determinístico | executor success não é autoridade; audit/acceptance precede promotion | definir níveis: acceptance de missão vs acceptance de patch/workspace | manter duas camadas somente se forem semanticamente distintas e medidamente úteis |
| Promotion / block | TEMOS | SMAG + MetaO | `Accept / Replan / Failover / Block` no nível de missão/orquestrador | Promote/Block no nível do workspace/código | documentar authority chain para não promover algo recusado por camada superior | composição fail-closed |
| Rollback | TEMOS no domínio coding | SMAG | MetaO governa retry/recovery, não precisa replicar rollback de workspace | rollback faz parte da governança operacional de mudanças | validar quais ações são reversíveis fora do domínio coding | manter no provider especializado |
| Evidence/provenance | TEMOS | MetaO + SMAG | evidence binding, acceptance proof, release evidence | classes de evidência, provenance, revision awareness, blocker taxonomy | normalizar envelope mínimo comum sem apagar evidência específica de domínio | adapter/schema mínimo; não criar novo sistema de provenance |
| Evidence classification / fail-closed truth | TEMOS | SMAG e MetaO | separa implemented/executed/accepted | `DOCUMENTED != EXECUTED`, `UNKNOWN_COST != ZERO_COST`, blockers explícitos | harmonizar vocabulário sem forçar equivalência artificial | reutilizar princípios; mapear classes |
| Verification | TEMOS como propriedade, precisa compor | MetaO acceptance + SMAG audit/tests + verificadores de domínio | independent acceptance | independent audit/acceptance e test gates | definir verifier apropriado por tarefa e custo aceitável | plugin/adapter de verifier; não generic verifier universal |
| Plan/task reuse | TEMOS como técnica/prior art | AgentReuse/AgenticCache + possíveis stores externos | MetaO já possui durable mission/replan artifacts, mas reuse semântico não é função central comprovada | SMAG possui task specs/missions, mas não prova semantic plan cache geral | testar reuse seguro e invalidation/revision binding | testar/adaptar; não criar cache proprietário inicialmente |
| Direct/minimum execution | TEMOS como baseline de pesquisa | E3-like `Estimate/Execute/Expand` | MetaO pode deixar execução seguir um runtime selecionado | SMAG consegue executar task diretamente por executor | medir quando caminho mínimo vence planning/orchestration | baseline obrigatória |
| Progressive expansion | TEMOS como técnica/prior art | E3 / adaptive control | MetaO possui replan/failover authority | SMAG possui governance/failure paths | definir sinais verificáveis de insuficiência | política experimental simples antes de ML/router |
| Task compilation/planning | PARCIAL | LLMCompiler/ReWOO/MAF Harness etc. | MetaO possui strategy/replan, mas não deve virar planner universal | SMAG possui pre-execution deliberation, não prova que planejar sempre compensa | testar compile somente em tarefas novas/complexas | manter opcional/escalonado |
| Capability filtering before reasoning | TEMOS como propriedade/prior art | AgentWeave/retrieval/routing/context providers | selection pode limitar runtimes | executor discovery pode limitar agentes disponíveis | implementar somente por ferramenta/standard existente se necessário | medir shortlist size/tokens; não expor capability universe inteiro |
| Lazy context materialization | TEMOS como técnica | context providers/retrieval/external refs | durable/evidence stores podem manter estado fora da janela | supervisor/task path pode consumir escopo delimitado | demonstrar materialização por referência no conjunto real DV | adaptar providers/references |
| Minimal handoff | PARCIAL / FALTA PROVAR | A2A Task/Artifact/Part + external refs | contracts/evidence podem fornecer boundary explícita | task specs dão boundary operacional | falta método comprovado para mínimo suficiente sem context miss excessivo | experimentar payloads/references e medir tokens/success |
| Handoff/bootstrap cost accounting | FALTA PROVAR PONTA A PONTA | instrumentation | MetaO já registra evidence/mission identity | SMAG evidence pode registrar executor/duration/tokens/cost quando disponíveis | unificar medição de tokens/context/bootstrap entre componentes | adicionar **instrumentação de pesquisa**, não novo orchestrator |
| Economic treatment policy (`reuse/direct/compile/...`) | FALTA PROVAR | metareasoning + E3 + reuse prior art | strategy/selection é possível, mas não há prova de ótimo econômico | pre-execution deliberation existe, mas não prova economia total | comparar política mecânica vs selector inteligente | benchmark primeiro; software só se política simples perder |
| Total tokens / verified solved task | FALTA MEDIR | protocolo DV | MetaO pode fornecer acceptance final e parte da telemetria | SMAG pode fornecer execution/evidence do domínio coding | captura uniforme de tokens/custo em todas as camadas | prioridade máxima da instrumentação |
| Monetary cost / verified solved task | FALTA MEDIR | protocolo DV | idem | idem | normalização de preços/provider + custo não-LLM quando relevante | instrumentar sem assumir custo zero |
| Context reconstruction cost | FALTA MEDIR | retrieval/context reconstruction prior art | estado externo pode ser fonte | executor pode reconstruir workspace/contexto | medir quando referência/retrieval economiza ou apenas desloca custo | experimento controlado |
| Coordination overhead | FALTA MEDIR | composição real | meta-control adiciona selection/governance | coding governance adiciona staging/audit/promotion | medir custo incremental MetaO + SMAG + protocols | principal teste de falsificação atual |
| Registry próprio DV | NÃO ADICIONAR | AGNTCY/A2A/MetaO runtime catalog | MetaO já possui catálogo/admission | executor discovery existe | nenhum gap demonstrado | usar existing discovery/registry |
| Memory system próprio DV | NÃO ADICIONAR | external stores/context providers | mission/evidence state já existe | task/mission state existe | nenhum gap demonstrado | não construir |
| Durable runtime próprio DV | NÃO ADICIONAR | MetaO adapters / Temporal / Dapr / MAF etc. | durable execution seam já existe | supervised task lifecycle já existe | nenhum gap demonstrado | não construir |
| Generic router próprio DV | NÃO ADICIONAR | selection/routing prior art | strategy/runtime selection existe | automatic executor selection existe | nenhum ganho demonstrado para outra camada | não construir |
| Protocolos próprios DV | NÃO ADICIONAR | A2A + MCP | adapters podem permanecer no boundary | executors podem ficar atrás de adapters | nenhum gap extraordinário demonstrado | não construir |

## 3. O que o MetaO pode suprir ao DV

O MetaO deve ser tratado como **provider de capacidades**, não como dependência conceitualmente obrigatória. Hoje ele oferece, com diferentes níveis de evidência:

1. contrato framework-neutral para orquestradores/runtimes;
2. strategy/runtime selection;
3. policy, budget e approval;
4. independent acceptance separada de execution success;
5. evidence binding e replay determinístico;
6. mission state durável;
7. recovery, fencing e rejeição de estado stale;
8. runtime health/admission;
9. runtime certification e revocation;
10. adapters para runtimes heterogêneos;
11. failover/replan/block authority;
12. release/evidence gates e rastreabilidade de revisão.

Regra de composição: o DV não deve copiar essas capacidades para um novo Core. Se MetaO for usado, deve entrar atrás de contrato/adaptador e permanecer substituível.

## 4. O que o SMAG pode suprir ao DV

O SMAG deve ser tratado como **provider especializado de execução governada para coding**, também substituível. Hoje oferece:

1. descoberta/readiness de executores locais;
2. seleção automática ou explícita de executor;
3. pre-execution deliberation;
4. policy/risk/budget/approval no domínio de mudança de código/workspace;
5. supervisor de processo e lifecycle;
6. isolated staging;
7. independent audit/acceptance do resultado;
8. evidence e provenance revision-aware;
9. promotion/block;
10. approval-before-promote;
11. rollback/recovery de mudanças governadas;
12. durable mission/task interface;
13. fail-closed failure classification;
14. integração governada com GitHub;
15. executor substitution com evidência real no escopo validado.

Regra de composição: o DV não deve transformar funções específicas de coding do SMAG em responsabilidades universais do kernel. Elas devem permanecer no provider especializado.

## 5. Sobreposição MetaO x SMAG — precisa ser resolvida por ownership, não duplicação

| Área sobreposta | MetaO | SMAG | Regra provisória para DV |
|---|---|---|---|
| seleção | runtime/orchestrator selection | executor selection | cada camada escolhe somente dentro do seu próprio domínio; medir custo de dupla seleção |
| policy | missão/orquestrador/control-plane | workspace/coding execution | policy superior nunca pode ser enfraquecida pela inferior |
| budget | missão/control-plane | task/coding | um budget global pode delegar sub-budget; evitar dois planners de budget independentes |
| approval | control-plane authority | pre-promotion approval | explicitar qual ação exige qual autoridade |
| acceptance | missão/resultado do orquestrador | patch/workspace result | manter ambas apenas quando validam objetos diferentes |
| evidence | missão/runtime/acceptance | executor/workspace/promotion | compor por referências, não duplicar payload completo |
| recovery | missão/runtime/fencing | supervised coding execution | runtime recupera execução; SMAG recupera/contém efeitos de coding |
| blocking | missão/policy/runtime | alteração/promoção | qualquer hard deny aplicável deve permanecer fail-closed |

## 6. O que realmente falta hoje

As lacunas residuais não são, neste momento, grandes subsistemas. São principalmente propriedades a provar:

| Lacuna residual | Natureza | O que precisa ser demonstrado antes de implementar |
|---|---|---|
| coordination overhead | empírica | quanto custa compor MetaO/SMAG/A2A/MCP/workflow vs execução direta |
| minimum-sufficient handoff | empírica/algorítmica | menor payload/referências que preserve sucesso verificável |
| economic treatment selection | política/metareasoning | se escolher `reuse/direct/compile/multi-agent` paga seu próprio custo de decisão |
| total-token accounting | instrumentação | captura completa de classification + planning + routing + context + handoff + execution + replanning + verification |
| provider-neutral composition E2E | integração | trocar MetaO/SMAG/executor por alternativas sem reconstruir o restante |
| workflow standard fit | integração | provar Open Workflow ou equivalente suficiente para casos reais antes de criar IR própria |
| domain verifier selection | integração/política | como selecionar verifier correto sem um generic verifier caro ou superficial |

## 7. O que pode precisar ser adicionado ao DV — somente se os testes justificarem

A lista abaixo é **candidata**, não backlog aprovado:

| Possível adição | Motivo | Condição para existir |
|---|---|---|
| adapters finos | ligar contratos/standards a MetaO, SMAG e outros providers | somente onde protocolo/standard não for consumido diretamente |
| measurement envelope | contabilizar tokens, custo, latência, handoff, retries e success | necessário para a pesquisa; deve ser observacional, não autoridade de execução |
| experiment harness/config | comparar baselines de forma reproduzível | pode ser configuração sobre ferramentas existentes; não criar framework sem necessidade |
| reference resolver | materializar refs externas sob demanda | somente se provider/runtime escolhido não oferecer mecanismo suficiente |
| tiny economic policy | escolher tratamento suficiente mais barato | somente se regra mecânica `reuse -> minimum -> verify -> expand` perder de forma reproduzível e o ganho superar o custo da policy |

## 8. O que não deve ser adicionado agora

- novo runtime;
- nova memória;
- novo registry;
- protocolo de agentes próprio;
- protocolo de tools próprio;
- generic router;
- superorquestrador;
- planner obrigatório;
- IR proprietária antes de falsificar Open Workflow/standards existentes;
- duplicação das autoridades de governance/acceptance já existentes em MetaO e SMAG.

## 9. Baseline de composição a testar

```text
TASK
  |
  +-- verified reuse available? --> REUSE --> VERIFY
  |
  v
minimum viable execution
  |
  v
VERIFY
  | success
  +-------------------------------> STOP
  |
  | insufficient
  v
EXPAND / COMPILE
  |
  v
workflow standard / graph
  |
  +--> MetaO-like capability provider (quando necessário)
  |
  +--> SMAG-like governed coding provider (quando necessário)
  |
  +--> A2A executors / MCP tools
  |
  v
VERIFY
```

A presença de MetaO ou SMAG no capability universe **não significa que ambos devam participar de toda tarefa**.

## 10. Critério de decisão

O DV só deve adquirir uma responsabilidade nova se:

1. a propriedade não estiver suficientemente coberta por standards/providers existentes;
2. uma composição simples tiver sido testada e demonstrada insuficiente;
3. a nova responsabilidade puder ser isolada atrás de contrato substituível;
4. houver evidência de melhora em `total system tokens / verified solved task` ou outra métrica primária predeclarada;
5. o ganho superar o custo de coordenação, manutenção e complexidade adicionados.

Até lá: **eliminar antes de construir**.

## 11. Fontes de verdade dos projetos consultadas

MetaO:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/REQUIREMENTS.md`
- `docs/CAPABILITY-MAP.md`
- `docs/POST-MVP-OPERATIONAL-BASELINE-V1.md`

SMAG:

- `README.md`
- `docs/status/CURRENT-STATE.md`
- `docs/evidence/EVIDENCE.md`

As alegações desta matriz devem continuar revision-aware; mudanças executáveis nos projetos fornecedores exigem reconciliação antes de herdar evidência anterior.