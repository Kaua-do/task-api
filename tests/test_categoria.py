from app.main import app
from tests.conftest import (
criar_usuario_e_token,
categoria_id
)
from tests.conftest import client

def test_listar_categorias(criar_usuario_e_token):

    usuario = criar_usuario_e_token()

    headers = usuario["headers"]

    response = client.get("/categorias/", headers=headers)

    assert response.status_code == 200

    categorias = response.json()

    assert len(categorias) > 0

    nomes = [categoria["nome"] for categoria in categorias]

    assert "Academia" in nomes

