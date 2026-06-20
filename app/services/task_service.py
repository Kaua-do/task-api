from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy import case

from app.models.tarefa_model import (
    Tarefa
)

from app.models.user_model import (
    Usuario
)

from app.schemas.task_schema import (
    TarefaUpdate, TarefaCreate
)
from fastapi import HTTPException

from uuid import uuid4
from app.schemas.task_schema import AlterarStatusTarefa
from app.models.categoria_model import Categoria

def buscar_tarefa_usuario(tarefa_id: str, db: Session, usuario: Usuario):

    tarefa = (
        db.query(Tarefa)
        .filter(
            Tarefa.id == tarefa_id,
            Tarefa.usuario_id == usuario.id
        )
        .first()
    )

    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    return tarefa


def criar_tarefa_service(
        dados: TarefaCreate,
        db: Session,
        usuario: Usuario
):

    if dados.categoria_id != 0:
        if dados.categoria_id:
            categoria_existe = db.query(Categoria).filter(Categoria.id == dados.categoria_id).first()

            if categoria_existe is None:
                raise HTTPException(
                    status_code=400,
                    detail="Categoria inválida"
                )

    if dados.categoria_id == 0:
        dados.categoria_id = None

    nova_tarefa = Tarefa(
        id=str(uuid4()),
        titulo=dados.titulo,
        descricao=dados.descricao,
        prioridade=dados.prioridade,
        status="pendente",
        usuario_id=usuario.id,
        categoria_id=dados.categoria_id,
    )

    db.add(nova_tarefa)

    db.commit()

    db.refresh(nova_tarefa)

    return nova_tarefa


def listar_tarefas_service(
        usuario: Usuario,
        db: Session,
        status: str | None = None,
        busca: str | None = None,
        ordenar_por: str | None = None,
        ordem: str | None = "asc",
        categoria: str | None = None,
        limit: int = 10,
        offset: int = 0
):
    query = db.query(Tarefa).filter(
        Tarefa.usuario_id == usuario.id
    )

    if status:
        query = query.filter(
            Tarefa.status == status
        )

    if busca:
        query = query.filter(
            or_(
                Tarefa.titulo.ilike(
                    f"%{busca}%"
                ),
                Tarefa.descricao.ilike(
                    f"%{busca}%"
                )
            )
        )

    if categoria:
        query = query.join(Categoria).filter(Categoria.nome == categoria)

    if ordenar_por:
        if ordenar_por == "prioridade":

            campo = case(
                (Tarefa.prioridade == "baixa", 1),
                (Tarefa.prioridade == "media", 2),
                (Tarefa.prioridade == "alta", 3),
                else_=0
            )

        else:
            campo = getattr(Tarefa, ordenar_por)

        if ordem == "asc":
            query = query.order_by(
                campo.asc()
            )
        else:
            query = query.order_by(
                campo.desc()
            )

    query = query.offset(offset)
    query = query.limit(limit)

    return query.all()



def buscar_tarefa_service(tarefa_id: str, db: Session, usuario: Usuario):

    return buscar_tarefa_usuario(tarefa_id=tarefa_id,usuario=usuario,db=db)



def editar_tarefa_service(tarefa_id:str, tarefa_atualizada: TarefaUpdate, db: Session, usuario: Usuario):

    tarefa = buscar_tarefa_usuario(tarefa_id=tarefa_id,usuario=usuario,db=db)

    if tarefa_atualizada.titulo is not None:
        tarefa.titulo = tarefa_atualizada.titulo

    if tarefa_atualizada.descricao is not None:
        tarefa.descricao = tarefa_atualizada.descricao

    if tarefa_atualizada.prioridade is not None:
        tarefa.prioridade = tarefa_atualizada.prioridade

    if tarefa_atualizada.categoria_id == 0:
        tarefa.categoria_id = None

    elif tarefa_atualizada.categoria_id is not None:
        categoria_existente = db.query(Categoria).filter(Categoria.id == tarefa_atualizada.categoria_id).first()

        if categoria_existente is None:
            raise HTTPException(
                status_code=400,
                detail="Categoria inválida"
            )

        tarefa.categoria_id = tarefa_atualizada.categoria_id

    db.commit()

    db.refresh(tarefa)

    return tarefa


def deletar_tarefa_service(tarefa_id:str, db: Session, usuario: Usuario):

    tarefa = buscar_tarefa_usuario(tarefa_id=tarefa_id,usuario=usuario,db=db)

    db.delete(tarefa)
    db.commit()



def alterar_status_service(tarefa_id: str, dados: AlterarStatusTarefa, db:Session, usuario: Usuario):

    tarefa = buscar_tarefa_service(tarefa_id=tarefa_id, db=db, usuario=usuario)

    tarefa.status = dados.status

    db.commit()

    db.refresh(tarefa)






