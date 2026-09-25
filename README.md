<div align="center">

# 🔮 Horáculo — Back-end

<strong>API do projeto Horáculo, criado na 6ª Maratona da Inovação FECAP</strong>

<p>
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white" />
</p>

</div>

---

## 📖 Sobre o projeto

Este repositório é um *fork* de desenvolvimento do back-end do **Horáculo**, plataforma criada durante a **6ª Maratona da Inovação da FECAP** para conectar **FECAP, alunos, empresas e mentores** em um único ecossistema digital.

Aqui está sendo construída a **API em FastAPI** que dá suporte ao front-end da aplicação ([GehMay/horaculo](https://github.com/GehMay/horaculo)), cobrindo autenticação, perfis de usuário e as demais regras de negócio da plataforma.

## 🛠️ Tecnologias utilizadas

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Servidor ASGI:** Uvicorn
- **Banco de dados:** SQLite, via **SQLAlchemy** ORM
- **Migrações:** Alembic
- **Autenticação:** JWT (PyJWT) com senhas protegidas por **bcrypt** (Passlib)
- **Configuração:** Pydantic Settings

## 🔐 Módulos da API

A documentação técnica da API é dividida por módulos em [`doc/`](doc):

| Módulo | Conteúdo |
|---|---|
| [`modulo-1.md`](doc/modulo-1.md) | Identidade e Autenticação (JWT + RBAC com papéis `FECAP`, `ALUNO`, `EMPRESA` e `MENTOR`) |
| [`modulo-2.md`](doc/modulo-2.md) | Perfis específicos de cada tipo de usuário |
| [`modulo-3.md`](doc/modulo-3.md) | Regras de negócio da plataforma |
| [`modulo-4.txt`](doc/modulo-4.txt) | Especificações complementares |
| [`modulo-5.txt`](doc/modulo-5.txt) | Especificações complementares |

O controle de acesso por papéis (RBAC) garante que empresas e mentores fiquem com status `PENDENTE` até serem aprovados pela FECAP, enquanto alunos podem ter acesso liberado automaticamente.

## 📂 Estrutura do projeto

```text
horaculo.2/
├── app/
│   ├── main.py           # Ponto de entrada da aplicação FastAPI
│   ├── config.py         # Configurações da aplicação
│   ├── database.py       # Conexão com o banco de dados
│   ├── core/             # Regras e utilitários centrais
│   ├── models/           # Modelos SQLAlchemy
│   ├── routers/          # Rotas da API
│   └── schemas/          # Schemas Pydantic
├── doc/                  # Documentação técnica por módulo
├── horaculo.db           # Banco de dados SQLite
└── requirements.txt
```

## 💻 Como rodar o projeto localmente

É necessário ter o [Python](https://www.python.org) instalado.

```bash
# Clone o repositório
git clone https://github.com/GehMay/horaculo.2.git
cd horaculo.2

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor de desenvolvimento
uvicorn app.main:app --reload
```

A documentação interativa da API fica disponível em `http://localhost:8000/docs`.

## 👩‍💻 Autoria

Desenvolvido por **Geovanna Tamagusko** ([@GehMay](https://github.com/GehMay)) durante a 6ª Maratona da Inovação FECAP.
