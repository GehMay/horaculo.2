## Módulo 3: Workspace da Empresa (Recruiting & Pipeline)

### 1. O Motor do Kanban (Drag and Drop)

O coração do painel da empresa é o funil de candidatos. Uma visualização em lista tradicional é ineficiente para RH; a interface precisa ser um quadro visual.

* **Biblioteca Recomendada:** Para implementar o recurso de "Arrastar e Soltar" (Drag and Drop) no React, recomendo fortemente o **`dnd-kit`** ou o **`@hello-pangea/dnd`** (um fork moderno e mantido do antigo `react-beautiful-dnd`). Elas lidam perfeitamente com acessibilidade e física de movimento.
* **A Estrutura Visual:** A interface deve renderizar colunas baseadas nos status definidos no backend (`NOVO`, `EM_ANALISE`, `ENTREVISTA`, `APROVADO`, `REPROVADO`). Os alunos (candidaturas) são os *cards* dentro dessas colunas.
* **Atualização Otimista (Optimistic UI):** Esta é a regra de ouro para a trabalhabilidade do Kanban.
1. O usuário de RH arrasta o *card* do aluno de "Novo" para "Entrevista".
2. O React atualiza o estado local **imediatamente**, movendo o card na tela, sem esperar a resposta do servidor. Isso dá a sensação de um sistema ultrarrápido (zero *lag*).
3. Em *background*, o frontend dispara a requisição `PATCH /api/v1/applications/{id}/status`.
4. Se a API retornar um erro (ex: falha de rede), o React exibe um alerta vermelho (*toast*) e reverte o *card* automaticamente para a coluna anterior.



### 2. A Visão da Empresa sobre o Aluno (Credibilidade)

Quando o recrutador clica no *card* do aluno no Kanban, abre-se um modal (ou painel lateral/Drawer) com o perfil detalhado. É aqui que o trabalho do Módulo 4 do backend entra em cena.

* **Renderização do Match:** O modal não deve apenas listar habilidades, mas exibir graficamente o porquê daquele aluno ter um *match score* alto. O componente de Gráfico de Radar (que o aluno vê no seu painel) também deve ser renderizado aqui, na visão da empresa, de forma "Somente Leitura" (Read-Only).
* **Selo de Mentoria:** Junto aos atributos (ex: Liderança, Comunicação), a interface deve destacar visualmente que aqueles pontos foram **auditados e validados**. Exiba um ícone de verificação (um *check* verde) acompanhado do texto: *"Validado por X mentores especialistas em RH"*. Isso resolve o problema central do seu projeto, que é tangibilizar a credibilidade da performance extracurricular.

### 3. Criação de Vagas (Formulário Dinâmico)

A interface de abertura de vagas não pode ser um formulário estático. Ela precisa permitir que a empresa adicione múltiplos requisitos de forma dinâmica.

* **Integração e Gestão de Estado:** A tela consome o `POST /api/v1/jobs`. Para o frontend, o desafio é gerenciar o array de requisitos (`requisitos: [{ atributo, peso_desejado }]`).
* **Field Arrays no React:** Utilizando o **React Hook Form**, a equipe deve implementar a funcionalidade `useFieldArray`. Isso permite que o usuário clique em um botão "+ Adicionar Habilidade", renderizando novos campos de *input* e *sliders* (para o peso desejado de 1 a 5) dinamicamente na tela, mantendo a performance do formulário intacta.

### 4. Vitrine FECAP TECH (B2B)

Além de recrutar, a empresa também interage com a instituição.

* **Integração:** Uma aba separada no menu consome o `GET /api/v1/showcase` (filtrado para projetos corporativos).
* **Interface:** Exiba os projetos de consultoria e tecnologia da FECAP como *Cards* elegantes. O botão de ação (CTA) de cada projeto deve engatilhar automaticamente a criação de um ticket de interesse (`POST /api/v1/tickets`), abrindo um canal de comunicação direta entre a empresa e o setor comercial da faculdade.