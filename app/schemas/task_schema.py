from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from app.schemas.categoria_schema import CategoriaResponse


class TarefaCreate(BaseModel):
    titulo: str = Field(
        min_length=1,
    )
    descricao: str
    prioridade: Literal[
        "alta",
        "media",
        "baixa"
    ] | None = None
    categoria_id: int | None = None


class TarefaResponse(BaseModel):

    id: str
    titulo: str
    descricao: str
    prioridade: str | None = None
    status: str
    categoria: CategoriaResponse | None = None

    model_config = ConfigDict(
        from_attributes=True
    )



class TarefaUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    prioridade: Literal[
        "alta",
        "media",
        "baixa"
    ] | None = None
    categoria_id: int | None = None


class AlterarStatusTarefa(BaseModel):
    status: Literal[
        "pendente",
        "concluida"
    ]

