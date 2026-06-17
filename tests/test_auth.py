from app.main import app
import uuid
from tests.conftest import client

from TaskAPI.app.core.security import criar_access_token
from TaskAPI.tests.conftest import criar_usuario_e_token


def test_registrar_usuario():

    email_unico = f"{uuid.uuid4()}@email.com"

    response = client.post(
        "/auth/register",
        json={
            "nome": "Kaua Teste",
            "email": email_unico,
            "senha": "123456"
        }
    )

    assert response.status_code == 200

def test_registrar_email_invalido():

    response = client.post(
        "/auth/register",
        json={
            "nome": "Kaua",
            "email": "banana",
            "senha": "123456"
        }
    )

    assert response.status_code == 422


def test_registrar_nome_vazio():

    email = f"{uuid.uuid4()}@email.com"

    response = client.post(
        "/auth/register",
        json={
            "nome": None,
            "email": email,
            "senha": "123456"
        }
    )

    assert response.status_code == 422


def test_registrar_senha_vazia():

    email = f"{uuid.uuid4()}@email.com"

    response = client.post(
        "/auth/register",
        json={
            "nome": "Kauã",
            "email": email,
            "senha": None
        }
    )

    assert response.status_code == 422



def test_registrar_email_vazio():

    response = client.post(
        "/auth/register",
        json={
            "nome": "Kaua",
            "email": None,
            "senha": "123456"
        }
    )

    assert response.status_code == 422


def test_login_usuario():

    response = client.post(
        "/auth/login",
        data={
            "username": "kaua@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_senha_errada():

    response = client.post(
        "/auth/login",
        data={
            "username": "kaua@email.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401

def test_email_duplicado():

    response = client.post(
        "/auth/register",
        json={
            "nome": "Outro Usuario",
            "email": "kaua@email.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 400


def test_email_inexistente():

    response = client.post(
        "/auth/login",
        data={
            "username": "naoexiste@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401


def test_token_invalido():

    headers = {"Authorization": "Bearer token_invalido"}

    response = client.get(
        "/tarefas/",
        headers=headers
    )

    assert response.status_code == 401


def test_sem_token():

    response = client.get("/usuarios/me")

    assert response.status_code == 401


def test_token_sem_user_id():

    email = f"{uuid.uuid4()}@email.com"

    usuario = client.post(
        "/auth/register",
        json={
            "nome": "Kaua",
            "email": email,
            "senha": "123456"
        }
    )

    token = criar_access_token(
        {
            "sub": None
        }
    )

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        "/tarefas/",
        headers=headers
    )

    assert response.status_code == 401


