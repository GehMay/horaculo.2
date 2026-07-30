## Módulo 1: Identidade e Autenticação (Auth)

Este módulo é o alicerce da plataforma. Ele centraliza o controle de acesso utilizando **JWT (JSON Web Tokens)** e define a separação de papéis (RBAC - *Role-Based Access Control*) para garantir que cada usuário só acesse os recursos permitidos para a sua categoria (FECAP, Aluno, Empresa ou Mentor).

### 1. Estrutura de Banco de Dados (SQLAlchemy)

Para suportar o cadastro unificado inicial e a divisão de papéis, criaremos uma tabela base de usuários. As informações específicas de cada perfil (como RA do aluno ou CNPJ da empresa) ficarão em tabelas separadas que se relacionam com esta tabela base (detalharemos isso no Módulo 2).

**Tabela: `users**`

| Coluna | Tipo (SQLite/SQLAlchemy) | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer / UUID | Chave Primária (Primary Key) |
| `email` | String | Único (Unique), Não Nulo |
| `password_hash` | String | Não Nulo (Senhas criptografadas com `bcrypt`) |
| `role` | String (Enum) | Valores aceitos: `FECAP`, `ALUNO`, `EMPRESA`, `MENTOR` |
| `status` | String (Enum) | Valores: `PENDENTE`, `ATIVO`, `BLOQUEADO` |
| `created_at` | DateTime | Gerado automaticamente |

> **Nota sobre o "status":** Conforme discutimos, a FECAP precisará aprovar empresas e mentores. Portanto, ao se cadastrarem, o status deles será `PENDENTE` e eles não poderão acessar o sistema até a conta Bootstrap da FECAP mudar o status para `ATIVO`. Alunos podem ter status `ATIVO` imediato caso a integração com o banco de dados da faculdade confirme o RA automaticamente.

---

### 2. Especificação dos Endpoints (FastAPI)

Abaixo estão os três endpoints fundamentais que o frontend consumirá para gerenciar a autenticação.

#### 2.1. Criar Conta (Registro Inicial)

* **Rota:** `POST /api/v1/auth/register`
* **Objetivo:** Criar as credenciais de acesso iniciais do usuário, definindo a qual categoria ele pertence.
* **Regra de Negócio:** O sistema deve verificar se o e-mail já existe e aplicar o *hash* na senha antes de salvar no SQLite.

**Payload de Requisição (O que o React envia):**

```json
{
  "email": "joao.silva@aluno.fecap.br",
  "password": "SenhaSegura123!",
  "role": "ALUNO"
}

```

**Payload de Resposta (O que o FastAPI devolve):**

* **Sucesso (201 Created):**

```json
{
  "message": "Usuário criado com sucesso. Complete seu perfil para acessar a plataforma.",
  "user_id": 1,
  "role": "ALUNO",
  "status": "ATIVO"
}

```

* **Erro (400 Bad Request):** Caso o e-mail já esteja em uso.

#### 2.2. Login (Geração de Token)

* **Rota:** `POST /api/v1/auth/login`
* **Objetivo:** Autenticar o usuário e devolver o token JWT que será usado nas próximas requisições.
* *Nota FastAPI:* Para manter o padrão OAuth2 nativo do FastAPI, é comum que este endpoint receba os dados no formato `Form Data` (`application/x-www-form-urlencoded`), usando os campos `username` (onde enviaremos o e-mail) e `password`.

**Payload de Requisição (Form Data):**

* `username`: "joao.silva@aluno.fecap.br"
* `password`: "SenhaSegura123!"

**Payload de Resposta:**

* **Sucesso (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2Fv... (string longa)",
  "token_type": "bearer",
  "role": "ALUNO",
  "status": "ATIVO"
}

```

* **Erro (401 Unauthorized):** Se a senha ou e-mail estiverem incorretos.
* **Erro (403 Forbidden):** Se o usuário estiver com status `PENDENTE` de aprovação da FECAP.

#### 2.3. Validar Sessão e Obter Dados (Me)

* **Rota:** `GET /api/v1/auth/me`
* **Objetivo:** Sempre que o usuário recarregar a página no React, o frontend bate nesta rota enviando o token para pegar os dados básicos do usuário e confirmar que a sessão ainda é válida.
* **Header Obrigatório:** `Authorization: Bearer <seu_token_jwt>`

**Payload de Resposta (200 OK):**

```json
{
  "id": 1,
  "email": "joao.silva@aluno.fecap.br",
  "role": "ALUNO",
  "status": "ATIVO"
}

```

---

### 3. Guia de Implementação para o Frontend (React)

Para que a equipe de Frontend consuma essa API de forma eficiente, aqui estão os procedimentos técnicos recomendados:

1. **Armazenamento do Token:** Quando a rota `/login` retornar o `access_token`, o React deve armazená-lo. Para um MVP, o `localStorage` (ex: `localStorage.setItem('token', response.data.access_token)`) é o caminho mais rápido e comum.
2. **Interceptador de Requisições (Axios Interceptors):** Em vez de colocar o token manualmente em cada requisição que o React fizer, configure um "Interceptor" no Axios. Ele vai ler o token do `localStorage` e injetar automaticamente o cabeçalho `Authorization: Bearer <token>` em todas as chamadas para o backend.
3. **Proteção de Rotas (React Router):** Crie um componente de *Private Route* no React. Se não houver token, ou se a rota `/auth/me` retornar erro (token expirado), o usuário é imediatamente redirecionado para a tela de Login.
4. **Roteamento Baseado em Papéis:** Use o campo `role` devolvido no login para redirecionar o usuário para o painel correto (ex: se `role === 'ALUNO'`, vai para `/dashboard-aluno`; se `role === 'EMPRESA'`, vai para `/dashboard-empresa`).

---

Perfeito. Como você está consolidando a "documentação mãe", vou estruturar esta especificação técnica no formato ideal para compor o seu projeto. Este documento cobre a modelagem de dados, as rotas da API, os *payloads* de comunicação e as instruções de integração para o React.

---

## Módulo 1: Identidade e Autenticação (Auth)

Este módulo é o alicerce da plataforma. Ele centraliza o controle de acesso utilizando **JWT (JSON Web Tokens)** e define a separação de papéis (RBAC - *Role-Based Access Control*) para garantir que cada usuário só acesse os recursos permitidos para a sua categoria (FECAP, Aluno, Empresa ou Mentor).

### 1. Estrutura de Banco de Dados (SQLAlchemy)

Para suportar o cadastro unificado inicial e a divisão de papéis, criaremos uma tabela base de usuários. As informações específicas de cada perfil (como RA do aluno ou CNPJ da empresa) ficarão em tabelas separadas que se relacionam com esta tabela base (detalharemos isso no Módulo 2).

**Tabela: `users**`

| Coluna | Tipo (SQLite/SQLAlchemy) | Restrições / Regras |
| --- | --- | --- |
| `id` | Integer / UUID | Chave Primária (Primary Key) |
| `email` | String | Único (Unique), Não Nulo |
| `password_hash` | String | Não Nulo (Senhas criptografadas com `bcrypt`) |
| `role` | String (Enum) | Valores aceitos: `FECAP`, `ALUNO`, `EMPRESA`, `MENTOR` |
| `status` | String (Enum) | Valores: `PENDENTE`, `ATIVO`, `BLOQUEADO` |
| `created_at` | DateTime | Gerado automaticamente |

> **Nota sobre o "status":** Conforme discutimos, a FECAP precisará aprovar empresas e mentores. Portanto, ao se cadastrarem, o status deles será `PENDENTE` e eles não poderão acessar o sistema até a conta Bootstrap da FECAP mudar o status para `ATIVO`. Alunos podem ter status `ATIVO` imediato caso a integração com o banco de dados da faculdade confirme o RA automaticamente.

---

### 2. Especificação dos Endpoints (FastAPI)

Abaixo estão os três endpoints fundamentais que o frontend consumirá para gerenciar a autenticação.

#### 2.1. Criar Conta (Registro Inicial)

* **Rota:** `POST /api/v1/auth/register`
* **Objetivo:** Criar as credenciais de acesso iniciais do usuário, definindo a qual categoria ele pertence.
* **Regra de Negócio:** O sistema deve verificar se o e-mail já existe e aplicar o *hash* na senha antes de salvar no SQLite.

**Payload de Requisição (O que o React envia):**

```json
{
  "email": "joao.silva@aluno.fecap.br",
  "password": "SenhaSegura123!",
  "role": "ALUNO"
}

```

**Payload de Resposta (O que o FastAPI devolve):**

* **Sucesso (201 Created):**

```json
{
  "message": "Usuário criado com sucesso. Complete seu perfil para acessar a plataforma.",
  "user_id": 1,
  "role": "ALUNO",
  "status": "ATIVO"
}

```

* **Erro (400 Bad Request):** Caso o e-mail já esteja em uso.

#### 2.2. Login (Geração de Token)

* **Rota:** `POST /api/v1/auth/login`
* **Objetivo:** Autenticar o usuário e devolver o token JWT que será usado nas próximas requisições.
* *Nota FastAPI:* Para manter o padrão OAuth2 nativo do FastAPI, é comum que este endpoint receba os dados no formato `Form Data` (`application/x-www-form-urlencoded`), usando os campos `username` (onde enviaremos o e-mail) e `password`.

**Payload de Requisição (Form Data):**

* `username`: "joao.silva@aluno.fecap.br"
* `password`: "SenhaSegura123!"

**Payload de Resposta:**

* **Sucesso (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2Fv... (string longa)",
  "token_type": "bearer",
  "role": "ALUNO",
  "status": "ATIVO"
}

```

* **Erro (401 Unauthorized):** Se a senha ou e-mail estiverem incorretos.
* **Erro (403 Forbidden):** Se o usuário estiver com status `PENDENTE` de aprovação da FECAP.

#### 2.3. Validar Sessão e Obter Dados (Me)

* **Rota:** `GET /api/v1/auth/me`
* **Objetivo:** Sempre que o usuário recarregar a página no React, o frontend bate nesta rota enviando o token para pegar os dados básicos do usuário e confirmar que a sessão ainda é válida.
* **Header Obrigatório:** `Authorization: Bearer <seu_token_jwt>`

**Payload de Resposta (200 OK):**

```json
{
  "id": 1,
  "email": "joao.silva@aluno.fecap.br",
  "role": "ALUNO",
  "status": "ATIVO"
}

```

---

### 3. Guia de Implementação para o Frontend (React)

Para que a equipe de Frontend consuma essa API de forma eficiente, aqui estão os procedimentos técnicos recomendados:

1. **Armazenamento do Token:** Quando a rota `/login` retornar o `access_token`, o React deve armazená-lo. Para um MVP, o `localStorage` (ex: `localStorage.setItem('token', response.data.access_token)`) é o caminho mais rápido e comum.
2. **Interceptador de Requisições (Axios Interceptors):** Em vez de colocar o token manualmente em cada requisição que o React fizer, configure um "Interceptor" no Axios. Ele vai ler o token do `localStorage` e injetar automaticamente o cabeçalho `Authorization: Bearer <token>` em todas as chamadas para o backend.
3. **Proteção de Rotas (React Router):** Crie um componente de *Private Route* no React. Se não houver token, ou se a rota `/auth/me` retornar erro (token expirado), o usuário é imediatamente redirecionado para a tela de Login.
4. **Roteamento Baseado em Papéis:** Use o campo `role` devolvido no login para redirecionar o usuário para o painel correto (ex: se `role === 'ALUNO'`, vai para `/dashboard-aluno`; se `role === 'EMPRESA'`, vai para `/dashboard-empresa`).

---

Perfeito. O Módulo 2 é onde a aplicação deixa de lidar apenas com "usuários genéricos" e passa a entender quem é o Aluno (com seu RA), quem é a Empresa (com seu CNPJ) e quem é o Mentor.

Nesta etapa, usaremos o conceito de **herança ou relacionamento 1-para-1** no banco de dados. O usuário cria a conta básica (Módulo 1) e, no primeiro acesso, preenche os dados específicos da sua categoria (Módulo 2).

---







