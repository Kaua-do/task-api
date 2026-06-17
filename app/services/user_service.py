from sqlalchemy.orm import Session
from app.models.user_model import (Usuario)
from app.schemas.user_schema import (UserUpdate, ChangePassword)
from fastapi import HTTPException
from app.core.security import (verificar_senha, hash_senha)

def obter_usuario_logado_service(
        usuario: Usuario
):

    return usuario


def atualizar_usuario_service(usuario_atualizado: UserUpdate, usuario: Usuario, db: Session):

    usuario_existente = (db.query(Usuario).filter(Usuario.email == usuario_atualizado.email).first())

    if usuario_existente and usuario_existente.id != usuario.id:

        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    senha_correta = verificar_senha(usuario_atualizado.senha_atual, usuario.senha_hash)

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="Senha atual incorreta"
        )

    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email

    db.commit()

    db.refresh(usuario)

    return usuario


def alterar_senha_service(usuario: Usuario, dados: ChangePassword, db: Session):

    senha_correta = verificar_senha(dados.senha_atual, usuario.senha_hash)

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="Senha atual incorreta"
        )

    usuario.senha_hash = hash_senha(dados.nova_senha)

    db.commit()

    db.refresh(usuario)

    return usuario
