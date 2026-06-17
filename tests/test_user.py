from app.main import app
from tests.conftest import (
criar_usuario_e_token,
categoria_id
)
from tests.conftest import client


def test_atualizar_usuario_mesmo_email(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    usuario_atualizado = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": usuario["email"],
            "senha_atual": usuario["senha_atual"]
        },
        headers=headers
    )

    assert usuario_atualizado.status_code == 200


def test_atualizar_usuario_sem_senha_atual(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    usuario_atualizado = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": usuario["email"],
            "senha_atual": None
        },
        headers=headers
    )

    assert usuario_atualizado.status_code == 422


def test_atualiar_usuario_mudar_senha(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/change-password",
        json={
            "senha_atual": "123456789",
            "nova_senha": "123456"
        },
        headers=headers
    )

    login = client.post(
        "/auth/login",
        data={
            "username": usuario["email"],
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert login.status_code == 200


def test_atualiar_usuario_mudar_senha_com_senha_atual_errada(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/change-password",
        json={
            "senha_atual": "1234567",
            "nova_senha": "123456"
        },
        headers=headers
    )

    assert response.status_code == 401


def test_atualizar_usuario_mudar_senha_com_senha_atual_vazia(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/change-password",
        json={
            "senha_atual": None,
            "nova_senha": "123456"
        },
        headers=headers
    )

    assert response.status_code == 422


def test_atualizar_usuario_mudar_senha_com_nova_senha_vazia(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/change-password",
        json={
            "senha_atual": "123456789",
            "nova_senha": None
        },
        headers=headers
    )

    assert response.status_code == 422


def test_atualizar_usuario_senha_errada(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    usuario_atualizado = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": usuario["email"],
            "senha_atual": "123456"
        },
        headers=headers
    )

    assert usuario_atualizado.status_code == 401


def test_atualizar_usuario_email_duplicado(criar_usuario_e_token):

    usuario_1 = criar_usuario_e_token()

    headers_1 = usuario_1["headers"]

    usuario_2 = criar_usuario_e_token()

    headers_2 = usuario_2["headers"]

    usuario_atualizado = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": usuario_1["email"],
            "senha_atual": "123456789"
        },
        headers=headers_2
    )

    assert usuario_atualizado.status_code == 400


def test_atualizar_usuario_email_invalido(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    login = client.post(
        "/auth/login",
        data={
            "username": usuario["email"],
            "password": "123456789"
        }
    )

    usuario_atualizado = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": "banana",
            "senha_atual": "123456789"
        },
        headers=headers
    )

    assert login.status_code == 200
    assert usuario_atualizado.status_code == 422


def test_atualizar_usuario_nome_curto(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/me",
        json={
            "nome": "Ka",
            "email": usuario["email"],
            "senha_atual": usuario["senha_atual"]
        },
        headers=headers
    )

    assert response.status_code == 422


def test_atualizar_usuario_nome_vazio(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/me",
        json={
            "nome": None,
            "email": usuario["email"],
            "senha_atual": usuario["senha_atual"]
        },
        headers=headers
    )

    assert response.status_code == 422


def test_atualizar_usuario_email_vazio(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.put(
        "/usuarios/me",
        json={
            "nome": "Kauã",
            "email": None,
            "senha_atual": usuario["senha_atual"]
        },
        headers=headers
    )

    assert response.status_code == 422


def test_obter_usuario_logado(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.get(
        "/usuarios/me",
        headers=headers
    )

    dados = response.json()

    assert response.status_code == 200
    assert dados["email"] == usuario["email"]




