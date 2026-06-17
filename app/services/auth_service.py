from app.schemas.user_schema import (UserCreate)
from sqlalchemy.orm import Session
from app.models.user_model import (Usuario)
from uuid import uuid4
from fastapi import HTTPException
from app.core.security import (hash_senha, verificar_senha, criar_access_token)
from fastapi.security import(OAuth2PasswordRequestForm)

def registrar_usuario_service(
        usuario: UserCreate,
        db: Session,
):
    usuario_existente = (
            db.query(Usuario).filter(
                Usuario.email == usuario.email
            )
            .first()
        )

    if usuario_existente:

        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo_usuario = Usuario(
        id=str(uuid4()),
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha)
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    return novo_usuario



def login_service(
        dados: OAuth2PasswordRequestForm,
        db: Session
):

    usuario = (
        db.query(Usuario).filter(
            Usuario.email == dados.username).first()
        )


    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    senha_correta = verificar_senha(
        dados.password,
        usuario.senha_hash
    )

    if not senha_correta:

        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    access_token = criar_access_token(
        {
            "sub": usuario.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }