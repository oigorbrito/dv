# AGENTS.md — Regras Permanentes do dv

Status: NORMATIVO PARA QUALQUER AGENTE/CONTRIBUIDOR

## 1. Objetivo do projeto

O `dv` pesquisa e, somente se empiricamente justificado, poderá materializar uma camada mínima de integração/composição entre capacidades fornecidas por projetos independentes.

MetaO, SMAG, OpenManus e qualquer outro projeto são referências ou providers potenciais de capacidades. Nenhum deles é dependência arquitetural obrigatória por identidade.

A unidade de análise e composição é a **capacidade/função**, não o código, linguagem, framework ou repositório de origem.

## 2. Gate permanente de admissibilidade

Nenhuma proposta de arquitetura, componente, adapter, provider, protocolo, política, workflow, algoritmo ou mudança de direção pode ser tratada como aprovada apenas porque:

- parece tecnicamente elegante;
- funciona em um exemplo isolado;
- é popular ou madura;
- vem de um projeto conhecido;
- reduz custo/tokens em apenas uma parte do sistema;
- foi sugerida por um agente/LLM;
- já existe em MetaO, SMAG ou outro projeto.

Para ser promovida a decisão do projeto, deve satisfazer **dois eixos obrigatórios**:

### A. Engenharia de software defensável

A solução deve ser justificável por princípios de engenharia de software adequados ao caso, incluindo quando aplicável:

- baixo acoplamento e alta coesão;
- contratos/interfaces explícitos;
- substituibilidade de providers;
- separação clara de responsabilidades e autoridade;
- adapters estreitos e bounded contexts;
- isolamento de falhas;
- estado durável fora do contexto cognitivo quando apropriado;
- idempotência, recovery e observabilidade quando necessários;
- segurança e fail-closed para limites críticos;
- versionamento e rastreabilidade;
- manutenibilidade por equipe pequena/um mantenedor;
- complexidade proporcional ao benefício demonstrado;
- preferência por standards e componentes existentes antes de implementação própria.

Uma decisão arquitetural que não possa ser defendida sob esse eixo permanece `PROPOSED` ou `INCONCLUSIVE`.

### B. Validação empírica adequada à alegação

A alegação deve ser testada com evidência proporcional ao que se quer afirmar. Quando aplicável, exigir:

- baseline explícita;
- hipótese e critérios definidos antes do resultado;
- tarefas/casos representativos;
- ambiente e revisão/versão identificados;
- execução real quando a alegação for operacional;
- repetições quando variância puder afetar a conclusão;
- oracle/verificador independente quando possível;
- métricas relevantes capturadas;
- resultados brutos e falhas preservados;
- blockers classificados sem promoção indevida;
- comparação controlada;
- limitações registradas;
- possibilidade explícita de `INCONCLUSIVE`.

Para economia, a métrica primária permanece:

`total system tokens / verified solved task`

Também considerar custo monetário total, sucesso verificado, latência, retries, replans/expansions, handoff/context, model calls, executor tier e custo de coordenação/verificação.

Economia local não constitui ganho se o custo total do sistema absorver a diferença.

## 3. Regra de evidência

Manter separadas as categorias:

`DOCUMENTED != CODE_CONFIRMED != EXECUTED != MEASURED != ACCEPTED`

E ainda:

`POPULAR != PROVEN`

`WORKING DEMO != GENERAL EVIDENCE`

`EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS`

`LOWER EXECUTOR TOKENS != LOWER SYSTEM COST`

`HISTORICAL PASS != CURRENT EXECUTION`

`INFERRED != EMPIRICALLY DEMONSTRATED`

Nenhum agente pode elevar silenciosamente uma alegação a uma classe mais forte de evidência.

## 4. Falsificação antes de construção

Antes de propor código novo:

1. identificar a capacidade necessária;
2. procurar standards/projetos/providers que já a satisfaçam;
3. testar composição simples primeiro;
4. medir o custo total;
5. tentar falsificar a necessidade do componente novo;
6. só materializar software próprio se uma lacuna sobreviver e o benefício for demonstrável.

`Não construir nada` é um resultado válido e preferível quando composição existente satisfaz os requisitos.

## 5. Proatividade sem apego tecnológico

Agentes trabalhando no `dv` devem ser proativos na descoberta e avaliação de novos projetos, standards e abordagens relevantes.

Quando surgir alternativa potencialmente melhor:

- reabrir a comparação;
- avaliar a capacidade oferecida;
- comparar maturidade, manutenção, custo, tokens, desempenho, verificabilidade e interoperabilidade;
- não preservar MetaO, SMAG, OpenManus ou qualquer outro provider por inércia;
- preferir substituição/composição quando a evidência justificar.

O ecossistema é mutável. A arquitetura deve absorver evolução principalmente por contratos/standards/adapters, não por acoplamento às implementações internas dos providers.

## 6. Baseline econômica atual

Enquanto não houver evidência superior, usar como baseline de comparação — não como arquitetura congelada:

`REUSE -> minimum plausible execution -> VERIFY -> EXPAND only when necessary`

Planejamento pesado, mais contexto, executor mais forte, workflow complexo ou multi-agent são escalonamentos, não defaults automáticos.

## 7. Regra de decisão final

Uma decisão do `dv` só pode ser tratada como **aprovada** quando:

1. a propriedade/necessidade está claramente definida;
2. a solução é defensável em engenharia de software;
3. existe evidência empírica suficiente para a alegação feita;
4. alternativas mais simples relevantes foram comparadas;
5. o custo total e os trade-offs foram considerados;
6. limitações e escopo da evidência estão explícitos.

Se qualquer condição crítica permanecer sem demonstração, o resultado deve permanecer `PROPOSED`, `BLOCKED` ou `INCONCLUSIVE`, nunca `PASS` por inferência.
