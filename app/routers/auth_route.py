from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import (UserCreate)
from fastapi.security import(OAuth2PasswordRequestForm)
from app.services.auth_service import (registrar_usuario_service, login_service)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def registrar_usuario(
        usuario: UserCreate,
        db: Session = Depends(get_db),
):

    registrar_usuario_service(
        usuario=usuario,
        db=db
    )

    return {
        "mensagem":
            "Usuário criado com sucesso"
    }

@router.post("/login")
def login(
        dados: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    token = login_service(
        dados=dados,
        db=db
    )

    return token


