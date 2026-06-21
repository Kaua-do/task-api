# TaskAPI

API REST para gerenciamento de tarefas, usuários e categorias, desenvolvida com **FastAPI**, utilizando **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT Authentication** e **Docker**.

---

## Tecnologias utilizadas

* Python 3.14
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT Authentication
* Docker
* Pytest
* Pydantic

---

## Funcionalidades

### Autenticação

* Cadastro de usuários
* Login com JWT
* Alteração de senha
* Atualização de perfil

### Categorias

* Criar categoria
* Listar categorias
* Atualizar categoria
* Excluir categoria

### Tarefas

* Criar tarefa
* Listar tarefas
* Buscar tarefa por ID
* Filtrar por categoria, prioridade, titulo, descrição
* Atualizar tarefa
* Excluir tarefa

---

## Estrutura do projeto

```
TaskAPI
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── core/
│   ├── dependencies/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
└── README.md
```

---

## Instalação local

Clone o projeto:

```bash
git clone <https://github.com/Kaua-do/task-api.git>
cd TaskAPI
```

Crie um ambiente virtual:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Configuração

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:123456@localhost:5432/taskapi
SECRET_KEY=sua_chave_super_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Executando as migrations

```bash
alembic upgrade head
```

---

## Executando a API

```bash
uvicorn app.main:app --reload
```

Documentação:

Swagger:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Executando com Docker

Subir os containers:

```bash
docker compose up --build
```

Executar as migrations:

```bash
docker compose exec api alembic upgrade head
```

Acessar a documentação:

```
http://localhost:8000/docs
```

---

## Executando os testes

```bash
pytest
```

Ou:

```bash
pytest --cov=app
```

---

## Endpoints principais

### Autenticação

```
POST /auth/register
POST /auth/login
```

### Usuários

```
GET  /usuarios/me
PUT  /usuarios/me
PUT  /usuarios/change-password
```

### Categorias

```
POST   /categorias
GET    /categorias
PUT    /categorias/{id}
DELETE /categorias/{id}
```

### Tarefas

```
POST   /tarefas
GET    /tarefas
GET    /tarefas/{id}
PUT    /tarefas/{id}
DELETE /tarefas/{id}
```

---

## Arquitetura

A aplicação segue uma arquitetura em camadas:

```
Routers
   ↓
Services
   ↓
Models
   ↓
Database
```

As regras de negócio foram separadas em serviços para facilitar manutenção, organização e testes.

---

## Status do projeto

✅ FastAPI
✅ SQLAlchemy
✅ PostgreSQL
✅ Alembic
✅ JWT Authentication
✅ Docker
✅ Testes automatizados
✅ CRUD de Usuários
✅ CRUD de Categorias
✅ CRUD de Tarefas

**Versão atual: v1.0**


## Aprendizados

Durante o desenvolvimento desta API, foram praticados conceitos importantes de desenvolvimento backend, como:

* Estruturação de projetos com FastAPI
* Criação de APIs REST
* Modelagem de banco de dados relacional
* Uso do SQLAlchemy ORM
* Gerenciamento de migrations com Alembic
* Autenticação e autorização com JWT
* Validação de dados com Pydantic
* Arquitetura em camadas (Routers, Services e Models)
* Containerização de aplicações com Docker
* Escrita de testes automatizados com Pytest
* Organização de dependências e ambientes de desenvolvimento
* Versionamento de código utilizando Git e GitHub

Este projeto representa uma aplicação completa de estudos em backend utilizando Python e serve como base para projetos mais avançados.

---

## Licença

Este projeto foi desenvolvido para fins de estudo e aprendizado.

Sinta-se livre para utilizá-lo como referência, modificar o código e adaptá-lo às suas necessidades.


API em produção:

https://sua-api.onrender.com

Documentação Swagger:

https://sua-api.onrender.com/docs
