# TaskAPI

API REST para gerenciamento de tarefas desenvolvida com FastAPI.

## Objetivo

Projeto criado para praticar conceitos fundamentais de desenvolvimento backend utilizando Python, incluindo autenticação JWT, arquitetura em camadas, validação de dados e testes automatizados.

## Tecnologias

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* Pydantic
* Pytest

## Funcionalidades

### Usuários

* Cadastro de usuário
* Login com JWT
* Atualização de perfil
* Alteração de senha

### Tarefas

* Criar tarefa
* Listar tarefas
* Buscar tarefa por ID
* Atualizar tarefa
* Alterar status
* Excluir tarefa

### Recursos adicionais

* Busca textual
* Filtros por status
* Filtros por categoria
* Filtros por prioridade
* Ordenação
* Paginação

## Estrutura do projeto

app/

* core/
* dependencies/
* models/
* routers/
* schemas/
* services/

tests/

## Como executar

Instale as dependências:

pip install -r requirements.txt

Execute a aplicação:

uvicorn app.main:app --reload

Acesse a documentação:

http://127.0.0.1:8000/docs

## Testes

Executar todos os testes:

pytest

Executar com cobertura:

pytest --cov=app --cov-report=html

## Cobertura

Cobertura atual aproximada: 98%

## Aprendizados

* FastAPI
* SQLAlchemy
* JWT
* Arquitetura em camadas
* Testes automatizados
* Validação com Pydantic
* Organização de projetos backend
