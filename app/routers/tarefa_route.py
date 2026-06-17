from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TarefaCreate, TarefaUpdate, TarefaResponse
from app.dependencies.auth_dependency import (get_current_user)
from app.models.user_model import(Usuario)
from app.schemas.task_schema import (AlterarStatusTarefa)
from app.services.task_service import (alterar_status_service)
from app.services.task_service import (
    criar_tarefa_service,
    listar_tarefas_service,
    buscar_tarefa_service,
    editar_tarefa_service,
    deletar_tarefa_service
)
from typing import Literal

router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"],
)

@router.post("/")
def criar_tarefa(
        dados: TarefaCreate,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):

    tarefa = criar_tarefa_service(
        dados=dados,
        usuario=usuario,
        db=db
    )

    return tarefa

@router.get("/", response_model = list[TarefaResponse])
def listar_tarefas(
        status: Literal[
            "pendente",
            "concluida"
        ] | None = None,
        busca: str | None = None,
        ordenar_por: Literal[
            "prioridade",
            "titulo",
            "status"
        ] | None = None,
        ordem: Literal[
            "asc",
            "desc"
        ] | None = "asc",
        categoria: Literal[
        "Academia",
        "Estudo",
        "Trabalho",
        "Casa",
        "Igreja",
        "Projeto",
        "Saúde",
        "Outros"
        ] | None = None,
        limit: int = Query(
            default=10,
            ge=1,
            le=100
        ),
        offset: int = Query(
            default = 0,
            ge=0
        ),
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(
            get_current_user
        )
):

    tarefas = listar_tarefas_service(
        usuario=usuario,
        db=db,
        status=status,
        busca=busca,
        ordenar_por=ordenar_por,
        ordem=ordem,
        categoria=categoria,
        limit=limit,
        offset=offset
    )

    return tarefas


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def buscar_tarefa(tarefa_id: str, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):

    tarefa = buscar_tarefa_service(
        tarefa_id=tarefa_id,
        usuario=usuario,
        db=db
    )

    return tarefa

@router.put("/{tarefa_id}", response_model=TarefaResponse)
def editar_tarefa(tarefa_id:str, tarefa_atualizada: TarefaUpdate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):

    tarefa = editar_tarefa_service(
        tarefa_id=tarefa_id,
        tarefa_atualizada=tarefa_atualizada,
        usuario=usuario,
        db=db
    )

    return tarefa



@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id:str, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):

    deletar_tarefa_service(
        tarefa_id=tarefa_id,
        usuario=usuario,
        db=db

    )

    return {
        "mensagem": "Tarefa deletada"
    }

@router.patch("/{tarefa_id}/status")
def alterar_status(
        tarefa_id: str,
        dados: AlterarStatusTarefa,
        db:Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user),
):

    alterar_status_service(
        tarefa_id=tarefa_id,
        dados=dados,
        db=db,
        usuario=usuario
    )

    return {
        "mensagem":
            f"Tarefa marcada como {dados.status}"
    }

