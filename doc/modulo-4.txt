## Módulo 4: Atividades Extracurriculares e Gameficação (Events & Gamification)

### 1. Estrutura de Banco de Dados (SQLAlchemy)

Precisamos de tabelas para gerenciar as atividades (eventos), as inscrições (tanto de alunos quanto de mentores), e o "livro-razão" (ledger) onde os atributos validados são acumulados.

**Tabela: `events` (Atividades/Eventos)**

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer | Chave Primária |
| `titulo` | String | Ex: "Hackathon de Negócios 2026" |
| `descricao` | Text | Detalhamento da atividade |
| `data_hora` | DateTime | Quando ocorrerá |
| `vagas_alunos` | Integer | Limite de inscrições para alunos |
| `vagas_mentores` | Integer | Limite para mentores (ex: 1 para cada 10 alunos) |
| `status` | String (Enum) | `ABERTO`, `EM_ANDAMENTO`, `FINALIZADO` |

**Tabela: `event_attributes` (O que a atividade desenvolve)**
*Mapeia quais competências estão em jogo neste evento.*

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer | Chave Primária |
| `event_id` | Integer | Foreign Key (`events.id`) |
| `atributo_nome` | String | Ex: "Liderança", "Trabalho em Equipe" |
| `pontos_maximos` | Integer | Pontuação máxima que o mentor pode dar (ex: 100) |

**Tabela: `event_enrollments` (Inscrições e Check-in)**

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer | Chave Primária |
| `event_id` | Integer | Foreign Key (`events.id`) |
| `user_id` | Integer | Foreign Key (`users.id` - pode ser Aluno ou Mentor) |
| `check_in` | Boolean | Padrão: `False`. Altera para `True` no momento do evento |
| `avaliador_id` | Integer | Foreign Key (`users.id`). Mentor que bipou o aluno |

**Tabela: `student_attributes` (A Carteira de Habilidades do Aluno)**
*Este é o histórico consolidado que será lido pelo motor de vagas (Módulo 3).*

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer | Chave Primária |
| `aluno_id` | Integer | Foreign Key (`profiles_aluno.user_id`) |
| `mentor_id` | Integer | Foreign Key (`profiles_mentor.user_id`) |
| `event_id` | Integer | Foreign Key (`events.id`) |
| `atributo_nome` | String | Ex: "Liderança" |
| `pontos_obtidos` | Integer | Avaliação real concedida pelo mentor |
| `feedback` | Text | Opcional, justificativa do mentor |

---

### 2. Especificação dos Endpoints (FastAPI)

Estes endpoints cobrem o ciclo de vida completo de uma atividade, desde a inscrição até a atribuição dos pontos.

#### 2.1. Inscrever-se em Atividade

* **Rota:** `POST /api/v1/events/{event_id}/enroll`
* **Objetivo:** Registra o usuário no evento.
* **Regra de Negócio:** O backend lê a *role* no token (Aluno ou Mentor). Se for Aluno, verifica se `vagas_alunos` já foi atingido. Se for Mentor, verifica `vagas_mentores`. Também impede inscrições duplicadas.

#### 2.2. Gerar QR Code Dinâmico (Aluno)

* **Rota:** `GET /api/v1/events/{event_id}/qrcode`
* **Objetivo:** Retorna uma string criptografada única que o frontend do aluno transformará em uma imagem de QR Code.
* **Regra de Seguranca:** O payload do QR Code deve conter o `user_id`, o `event_id` e um *timestamp* de validade (ex: expira em 60 segundos) para evitar que o aluno tire print e mande para o amigo que ficou em casa.

#### 2.3. Processar Check-in (Mentor)

* **Rota:** `POST /api/v1/events/checkin`
* **Objetivo:** O mentor envia os dados lidos do QR Code do aluno.
* **Regra de Negócio:** O sistema valida o token do QR Code. Se for válido, marca `check_in = True` na tabela `event_enrollments` para aquele aluno e atualiza o campo `avaliador_id` com o ID do mentor que fez a leitura.

**Payload de Requisição:**

```json
{
  "qr_data": "eyJhbGciOiJIUzI1Ni... (dados decodificados do QR)"
}

```

#### 2.4. Enviar Avaliação e Feedback (Mentor)

* **Rota:** `POST /api/v1/events/{event_id}/evaluate`
* **Objetivo:** Após o evento, o mentor avalia os alunos que estão atrelados ao seu `avaliador_id`.

**Payload de Requisição:**

```json
{
  "aluno_id": 12,
  "avaliacoes": [
    { "atributo_nome": "Liderança", "pontos_obtidos": 90 },
    { "atributo_nome": "Trabalho em Equipe", "pontos_obtidos": 100 }
  ],
  "feedback": "Aluno demonstrou excelente articulação durante a dinâmica de crise."
}

```

---

### 3. Guia de Implementação para o Frontend (React)

A interface deste módulo ditará o engajamento dos alunos e a produtividade dos mentores.

1. **Leitor e Gerador de QR Code:**
* **Visão do Aluno:** Utilize a biblioteca `qrcode.react` para renderizar a string devolvida pela API (`2.2`) em uma imagem na tela do celular. Implemente um `setInterval` para pedir uma nova string a cada 60 segundos, garantindo a segurança anti-fraude.
* **Visão do Mentor:** Utilize a biblioteca `react-qr-reader` para acessar a câmera do smartphone do mentor pelo navegador (requer HTTPS) e ler o código da tela do aluno.


2. **Interface de Avaliação em Massa (Mentor):**
* Assim que o evento for marcado como `FINALIZADO`, libere no painel do mentor uma tela com a lista de todos os alunos que ele "bipou".
* Use *sliders* (deslizadores) de 0 a 100 para cada atributo. Isso acelera drasticamente o trabalho de avaliação em comparação com a digitação de números.


3. **Visualização Gameficada (Painel do Aluno):**
* A tela de perfil do aluno deve ser visualmente estimulante.
* Utilize a biblioteca **Recharts** ou **Chart.js** para criar "Gráficos de Radar" (Radar Charts). Eles são perfeitos para mostrar o acúmulo de atributos (um polígono que cresce em direções como Liderança, Comunicação, Python, etc.).
* Crie um sistema visual de *Badges* (Selos). Se um aluno atinge 500 pontos em Comunicação, ele ganha um selo "Mestre em Comunicação" que fica visível para as empresas no Módulo 3.

Chegamos ao último módulo da nossa arquitetura de Backend. O Módulo 5 é o painel de controle absoluto da FECAP. É através dele que a instituição garante a governança da plataforma, atende às solicitações dos usuários e monetiza/divulga as iniciativas internas (Horáculo e FECAP TECH).

---