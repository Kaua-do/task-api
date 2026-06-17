from fastapi import (
    APIRouter,
    Depends
)
from app.models.user_model import (
    Usuario
)
from app.schemas.user_schema import (
    UserResponse, UserUpdate, ChangePassword
)
from app.dependencies.auth_dependency import (
    get_current_user
)
from app.services.user_service import (
    obter_usuario_logado_service, atualizar_usuario_service)
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import (alterar_senha_service)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/me", response_model=UserResponse)
def obter_usuario_logado(
        usuario: Usuario = Depends(
            get_current_user
        )
):

    return obter_usuario_logado_service(
        usuario=usuario
    )

@router.put("/me", response_model=UserResponse)
def atualizar_usuario(
        usuario_atualizado: UserUpdate,
        usuario: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)

):
    return atualizar_usuario_service(
        usuario_atualizado=usuario_atualizado,
        usuario=usuario,
        db=db
    )

@router.put("/change-password")
def alterar_senha(
        dados: ChangePassword,
        usuario: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    alterar_senha_service(
        usuario=usuario,
        dados=dados,
        db=db
    )

    return {
        "mensagem":
            "Senha atualizada com sucesso!"
    }




