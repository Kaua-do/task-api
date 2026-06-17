import uuid
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def criar_usuario_e_token():

    def _criar_usuario():

        email = f"{uuid.uuid4()}@email.com"
        senha = "123456789"

        client.post(
            "/auth/register",
            json={
                "nome": "Usuario Teste",
                "email": email,
                "senha": senha
            }
        )

        login = client.post(
            "/auth/login",
            data={
                "username": email,
                "password": senha
            }
        )

        token = login.json()["access_token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }

        return {
            "email": email,
            "senha_atual": senha,
            "token": token,
            "headers": headers
        }

    return _criar_usuario


@pytest.fixture
def categoria_id(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    response = client.get(
        "/categorias/",
        headers=usuario["headers"]
    )

    categorias = response.json()

    return categorias[0]["id"]

