## Módulo 2: Gestão de Perfis e Cadastros (Core Entities)

### 1. Estrutura de Banco de Dados (SQLAlchemy)

Cada tipo de usuário terá uma tabela específica conectada à tabela base `users` através de uma Chave Estrangeira (*Foreign Key*).

**Tabela: `profiles_aluno**`

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `user_id` | Integer | Chave Primária e Foreign Key (`users.id`) |
| `ra` | String | Único, Não Nulo (Pode ser usado para validação na FECAP) |
| `nome_completo` | String | Não Nulo |
| `cpf` | String | Único, Não Nulo |
| `telefone` | String | Não Nulo |
| `data_nascimento` | Date | Não Nulo |
| `genero` | String |  |
| `foto_url` | String | URL da imagem salva (opcional no primeiro momento) |

**Tabela: `profiles_empresa**` *(Incorporando os dados padrão Nube)*

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `user_id` | Integer | Chave Primária e Foreign Key (`users.id`) |
| `razao_social` | String | Não Nulo |
| `cnpj` | String | Único, Não Nulo |
| `rep_legal_nome` | String | Não Nulo (Representante Legal) |
| `rep_legal_cpf` | String | Não Nulo |
| `supervisor_nome` | String | Não Nulo (Pessoa que orientará o estagiário) |
| `endereco` | String | Não Nulo |

**Tabela: `profiles_mentor**` *(Pós-Graduandos e Graduados em RH)*

| Coluna | Tipo | Restrições / Regras |
| --- | --- | --- |
| `user_id` | Integer | Chave Primária e Foreign Key (`users.id`) |
| `nome_completo` | String | Não Nulo |
| `cpf` | String | Único, Não Nulo |
| `telefone` | String | Não Nulo |
| `data_nascimento` | Date | Não Nulo |
| `genero` | String |  |
| `foto_url` | String |  |

---

### 2. Especificação dos Endpoints (FastAPI)

Como as necessidades de dados são muito diferentes, o ideal é termos rotas separadas para o preenchimento de cada tipo de perfil. Todas essas rotas exigem o envio do token JWT (Header `Authorization: Bearer <token>`). O Backend saberá qual é o `user_id` extraindo essa informação diretamente do token.

#### 2.1. Completar/Atualizar Perfil de Aluno

* **Rota:** `PUT /api/v1/profiles/aluno`
* **Objetivo:** Inserir ou atualizar os dados pessoais e acadêmicos do aluno. O backend deve validar se o usuário que está chamando a rota realmente tem a *role* `ALUNO`.

**Payload de Requisição:**

```json
{
  "ra": "12345678",
  "nome_completo": "João Vitor da Silva",
  "cpf": "111.222.333-44",
  "telefone": "(11) 99999-9999",
  "data_nascimento": "2002-05-15",
  "genero": "Masculino"
}

```

**Payload de Resposta (200 OK):**

```json
{
  "message": "Perfil atualizado com sucesso.",
  "profile": {
    "ra": "12345678",
    "nome_completo": "João Vitor da Silva"
  }
}

```

#### 2.2. Completar/Atualizar Perfil de Empresa

* **Rota:** `PUT /api/v1/profiles/empresa`
* **Regra de Negócio:** Após a empresa preencher este perfil, o status do usuário (na tabela `users`) deve permanecer como `PENDENTE` até que a FECAP aprove os dados (Módulo 5).

**Payload de Requisição:**

```json
{
  "razao_social": "Tech Inovações LTDA",
  "cnpj": "12.345.678/0001-90",
  "rep_legal_nome": "Carlos Mendes",
  "rep_legal_cpf": "999.888.777-66",
  "supervisor_nome": "Ana Paula (Tech Lead)",
  "endereco": "Av. Paulista, 1000 - São Paulo, SP"
}

```

#### 2.3. Resgatar Perfil Logado

* **Rota:** `GET /api/v1/profiles/me`
* **Objetivo:** Retorna os dados completos do usuário logado, independentemente da categoria. O FastAPI identifica a `role` no token, faz um *JOIN* com a tabela de perfil correspondente e devolve os dados unificados.

---

### 3. Guia de Implementação para o Frontend (React)

Aqui estão as diretrizes de usabilidade e arquitetura para a equipe de Frontend nesta etapa:

1. **O Fluxo de *Onboarding*:**
* Logo após o cadastro (Módulo 1), o usuário faz o login.
* O React bate na rota `/api/v1/profiles/me`. Se a resposta vier vazia (ou com um código 404 para o perfil), o React deve redirecionar o usuário **obrigatoriamente** para a tela "Complete seu Cadastro".
* Ele não deve conseguir acessar o Dashboard (vagas, eventos) sem antes preencher esse perfil.


2. **Validação de Formulários (Zod + React Hook Form):**
* Não confie apenas no backend. O Frontend deve validar CPF e CNPJ antes de enviar o payload. A biblioteca **React Hook Form** junto com o **Zod** formam o padrão atual da indústria para gerenciar e validar formulários complexos no React.


3. **Tratamento de Upload de Fotos:**
* Note que não incluí o arquivo de imagem no JSON. Arquivos binários não viajam bem em JSON.
* A melhor prática é criar uma rota específica no FastAPI apenas para upload (`POST /api/v1/upload`), que recebe o arquivo via `multipart/form-data`, salva no servidor (ou em nuvem como AWS S3/Cloudinary) e devolve uma URL (ex: `https://.../foto123.jpg`).
* O React recebe essa URL e a injeta no payload JSON (campo `foto_url`) durante o `PUT` do perfil.


4. **Máscaras de Input:**
* Utilize bibliotecas como `react-input-mask` para garantir que o usuário digite o CPF (000.000.000-00), CNPJ e Telefone no formato correto. Isso evita erros de validação desnecessários no banco de dados.



---

Este é o módulo que sustenta a grande promessa do projeto: a **credibilidade**. Sem ele, os atributos do aluno seriam apenas autodeclarações, sem peso para as empresas.

Para resolver a dúvida que levantamos anteriormente sobre o vínculo entre mentor e aluno: a forma mais dinâmica e à prova de fraudes é **estabelecer o vínculo no momento do check-in**. O mentor não precisa escolher previamente quem vai avaliar; no dia do evento, ele escaneia o QR Code do aluno, confirmando a presença e atrelando aquele aluno à sua "carteira de avaliação" para aquele evento específico.

---