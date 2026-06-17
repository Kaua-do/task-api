from tests.conftest import (
criar_usuario_e_token,
categoria_id
)
from app.main import app
from tests.conftest import client

def test_criar_tarefa(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.post(
        "/tarefas/",
        json={
            "titulo": "Estudar FastAPI",
            "descricao": "Aprender testes automatizados",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa = response.json()

    assert response.status_code == 200
    assert tarefa["titulo"] == "Estudar FastAPI"
    assert tarefa["prioridade"] == "alta"


def test_criar_tarefa_titulo_vazio(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.post(
        "/tarefas/",
        json={
            "titulo": None,
            "descricao": "Aprender testes automatizados",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    assert response.status_code == 422


def test_listar_tarefas(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar Python",
            "descricao": "FAzer testes automatizados",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response_listar = client.get(
        "/tarefas/",
        headers=headers
    )

    tarefas = response_listar.json()

    titulos = [tarefa["titulo"] for tarefa in tarefas]

    assert response_criar.status_code == 200
    assert len(tarefas) > 0
    assert "Treinar Python" in titulos


def test_editar_tarefa(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar Python",
            "descricao": "Aprender FastAPI",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa_criada = response_criar.json()

    tarefa_id = tarefa_criada["id"]

    response_editar = client.put(
        f"/tarefas/{tarefa_id}",
        json={
            "titulo": "Treinar Python Avançado",
            "prioridade": "alta"
        },
        headers=headers
    )

    tarefa_editada = response_editar.json()

    assert response_editar.status_code == 200
    assert tarefa_editada["titulo"] == "Treinar Python Avançado"
    assert tarefa_editada["prioridade"] == "alta"


def test_excluir_tarefa(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa para deletar",
            "descricao": "Será removida",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa_criada = response_criar.json()

    tarefa_id = tarefa_criada["id"]

    response_excluir = client.delete(
        f"/tarefas/{tarefa_id}",
        headers=headers
    )

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}",
        headers=headers
    )

    assert response_excluir.status_code == 200
    assert response_buscar.status_code == 404


def test_buscar_tarefa(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar Python",
            "descricao": "Buscar tarefa teste",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa_criada = response_criar.json()

    tarefa_id = tarefa_criada["id"]

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}/",
        headers=headers
    )

    tarefa = response_buscar.json()

    assert response_buscar.status_code == 200
    assert tarefa["id"] == tarefa_id
    assert tarefa["titulo"] == "Treinar Python"


def test_alterar_status(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar Python",
            "descricao": "Alterar status teste",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa_criada = response_criar.json()

    tarefa_id = tarefa_criada["id"]

    response_alterar = client.patch(
        f"/tarefas/{tarefa_id}/status",
        json={
            "status": "concluida"
        },
        headers=headers
    )

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}/",
        headers=headers
    )

    tarefa = response_buscar.json()

    assert response_alterar.status_code == 200
    assert tarefa["status"] == "concluida"


def test_usuario_nao_acessa_tarefa_de_outro_usuario(criar_usuario_e_token, categoria_id):

    usuario_1 = criar_usuario_e_token()

    headers_1 = usuario_1["headers"]

    usuario_2 = criar_usuario_e_token()

    headers_2 = usuario_2["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa secreta",
            "descricao": "Não pode acessar",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers_1
    )

    tarefa = response_criar.json()

    tarefa_id = tarefa["id"]

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}/",
        headers=headers_2
    )

    assert response_buscar.status_code == 404

def test_filtrar_tarefas_por_status(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_tarefa_1 = client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa pendente",
            "descricao": "Ainda não concluída",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa_1 = response_tarefa_1.json()

    tarefa_id = tarefa_1["id"]

    client.patch(
        f"/tarefas/{tarefa_id}/status",
        json={
            "status": "concluida"
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa pendente real",
            "descricao": "Não concluída",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response_filtrar = client.get(
        f"/tarefas/?status=pendente",
        headers=headers
    )

    tarefas = response_filtrar.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert "Tarefa pendente real" in titulos
    assert "Tarefa pendente" not in titulos


def test_busca_textual(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa um papo",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa apenas dois",
            "descricao": "2",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response_filtrar = client.get(
        f"/tarefas/?busca=papo",
        headers=headers
    )

    tarefas = response_filtrar.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert "Tarefa um papo" in titulos
    assert "Tarefa apenas dois" not in titulos

def test_busca_textual_descricao(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar Python",
            "descricao": "Estudar FastAPI urgente",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response_filtrar = client.get(
        "/tarefas/?busca=FastAPI",
        headers=headers
    )

    tarefas = response_filtrar.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert "Treinar Python" in titulos


def test_filtrar_por_categoria(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.get(
        "/categorias/",
        headers=headers
    )

    categorias = response.json()

    categoria_estudo = next(
        categoria["id"]
        for categoria in categorias
        if categoria["nome"] == "Estudo"
    )

    categoria_casa = next(
        categoria["id"]
    for categoria in categorias
    if categoria["nome"] == "Casa"
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Estudar Python",
            "descricao": "Backend",
            "prioridade": "alta",
            "categoria_id": categoria_estudo
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Varrer a casa",
            "descricao": "Limpeza",
            "prioridade": "media",
            "categoria_id": categoria_casa
        },
        headers=headers
    )

    response_filtrar = client.get(
        f"/tarefas/?categoria=Estudo",
        headers=headers
    )

    tarefas = response_filtrar.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert "Estudar Python" in titulos
    assert "Varrer a casa" not in titulos

def test_ordenar_tarefa_por_prioridade_asc(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa alta",
            "descricao": "1",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa baixa",
            "descricao": "2",
            "prioridade": "baixa",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa media",
            "descricao": "3",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response = client.get(
        "/tarefas/?ordenar_por=prioridade&ordem=asc",
        headers=headers
    )

    tarefas = response.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert titulos == [
        "Tarefa baixa",
        "Tarefa media",
        "Tarefa alta"
    ]

def test_ordenar_tarefa_por_prioridade_desc(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa alta",
            "descricao": "1",
            "prioridade": "alta",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa baixa",
            "descricao": "2",
            "prioridade": "baixa",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa media",
            "descricao": "3",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response = client.get(
        "/tarefas/?ordenar_por=prioridade&ordem=desc",
        headers=headers
    )

    tarefas = response.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert titulos == [
        "Tarefa alta",
        "Tarefa media",
        "Tarefa baixa"
    ]

def test_ordenar_tarefa_por_titulo_asc(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Abacaxi",
            "descricao": "2",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Caderno",
            "descricao": "3",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response = client.get(
        "/tarefas/?ordenar_por=titulo&ordem=asc",
        headers=headers
    )

    tarefas = response.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert titulos == [
        "Abacaxi",
        "Banana",
        "Caderno"
    ]


def test_ordenar_tarefa_por_titulo_desc(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Abacaxi",
            "descricao": "2",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Caderno",
            "descricao": "3",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    response = client.get(
        "/tarefas/?ordenar_por=titulo&ordem=desc",
        headers=headers
    )

    tarefas = response.json()

    titulos = [
        tarefa["titulo"]
        for tarefa in tarefas
    ]

    assert titulos == [
        "Caderno",
        "Banana",
        "Abacaxi"
    ]


def test_buscar_tarefa_inexistente(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    tarefa_id = "4g3y4343i4g357"

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}",
        headers=headers
    )

    assert response_buscar.status_code == 404

def test_editar_tarefa_inexistente(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    tarefa_id = "4g3y4343i4g357"

    response_buscar = client.put(
        f"/tarefas/{tarefa_id}/",
        json={
            "titulo": "Banana 2",
        },
        headers=headers
    )

    assert response_buscar.status_code == 404


def test_editar_tarefa_descricao_vazia(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa = response_criar.json()

    tarefa_id = tarefa["id"]

    response_editar = client.put(
        f"/tarefas/{tarefa_id}/",
        json={
            "titulo": "Caderno",
            "descricao": None,
            "prioridade": "media",
            "categoria_id": 1
        },
        headers=headers
    )

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}/",
        headers=headers
    )

    tarefa = response_buscar.json()

    assert response_criar.status_code == 200
    assert response_editar.status_code == 200
    assert tarefa["descricao"] == "1"


def test_editar_tarefa_categoria_zero(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa = response_criar.json()

    tarefa_id = tarefa["id"]

    response_editar = client.put(
        f"/tarefas/{tarefa_id}/",
        json={
            "titulo": "Caderno",
            "descricao": "",
            "prioridade": "media",
            "categoria_id": 0
        },
        headers=headers
    )

    response_buscar = client.get(
        f"/tarefas/{tarefa_id}/",
        headers=headers
    )

    tarefa = response_buscar.json()

    assert response_criar.status_code == 200
    assert response_editar.status_code == 200
    assert tarefa["categoria"] is None


def test_editar_tarefa_categoria_invalida(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa = response_criar.json()

    tarefa_id = tarefa["id"]

    response_editar = client.put(
        f"/tarefas/{tarefa_id}/",
        json={
            "titulo": "Caderno",
            "descricao": "",
            "prioridade": "media",
            "categoria_id": 9999
        },
        headers=headers
    )

    assert response_criar.status_code == 200
    assert response_editar.status_code == 400



def test_deletar_tarefa_inexistente(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    tarefa_id = "4g3y4343i4g357"

    response_buscar = client.delete(
        f"/tarefas/{tarefa_id}/",
        headers=headers
    )

    assert response_buscar.status_code == 404


def test_alterar_status_inexistente(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    tarefa_id = "33u434735835h85385"

    response_patch = client.patch(
        f"/tarefas/{tarefa_id}/status",
        json={
            "status": "concluida"
        },
        headers=headers
    )

    assert response_patch.status_code == 404


def test_status_invalido(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Treinar",
            "descricao": "Teste",
            "prioridade": "media",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    tarefa = response_criar.json()

    tarefa_id = tarefa["id"]

    response_patch = client.patch(
        f"/tarefas/{tarefa_id}/status",
        json={
            "status": "banana"
        },
        headers=headers
    )

    assert response_patch.status_code == 422


def test_categoria_invalida(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Banana",
            "descricao": "1",
            "prioridade": "baixa",
            "categoria_id": 99999
        },
        headers=headers
    )

    assert response_criar.status_code == 400


def test_prioridade_invalida(criar_usuario_e_token, categoria_id):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response_criar = client.post(
        "/tarefas/",
        json={
            "titulo": "Teste prioridade",
            "descricao": "Teste",
            "prioridade": "banana",
            "categoria_id": categoria_id
        },
        headers=headers
    )

    assert response_criar.status_code == 422







